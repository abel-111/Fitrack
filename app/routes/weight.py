from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.models import db, WeightLog

weight_bp = Blueprint('weight', __name__, url_prefix='/weight')

@weight_bp.route('/', methods=['GET'])
@login_required
def history():
    logs = (WeightLog.query
            .filter_by(user_id=current_user.id)
            .order_by(WeightLog.logged_at.asc())
            .all())

    chart_points = build_chart_points(logs)

    return render_template(
        'weight.html',
        logs=list(reversed(logs)),  # newest first for the table
        chart_points=chart_points,
        has_logs=len(logs) >= 2
    )


@weight_bp.route('/log', methods=['POST'])
@login_required
def log_weight():
    weight = request.form.get('weight_kg', type=float)

    if not weight or weight <= 0:
        flash('Enter a valid weight.', 'danger')
        return redirect(url_for('weight.history'))

    entry = WeightLog(user_id=current_user.id, weight_kg=weight)
    db.session.add(entry)

    # keep the profile's "current weight" in sync
    current_user.weight_kg = weight

    db.session.commit()
    flash('Weight logged!', 'success')
    return redirect(url_for('weight.history'))


@weight_bp.route('/<int:log_id>/edit', methods=['POST'])
@login_required
def edit_weight(log_id):
    entry = WeightLog.query.get_or_404(log_id)

    if entry.user_id != current_user.id:
        abort(403)

    weight = request.form.get('weight_kg', type=float)
    if not weight or weight <= 0:
        flash('Enter a valid weight.', 'danger')
        return redirect(url_for('weight.history'))

    entry.weight_kg = weight
    db.session.commit()

    # if this was the most recent entry, keep profile weight in sync
    latest = (WeightLog.query
              .filter_by(user_id=current_user.id)
              .order_by(WeightLog.logged_at.desc())
              .first())
    if latest and latest.id == entry.id:
        current_user.weight_kg = weight
        db.session.commit()

    flash('Entry updated!', 'success')
    return redirect(url_for('weight.history'))


@weight_bp.route('/<int:log_id>/delete', methods=['POST'])
@login_required
def delete_weight(log_id):
    entry = WeightLog.query.get_or_404(log_id)

    if entry.user_id != current_user.id:
        abort(403)

    db.session.delete(entry)
    db.session.commit()
    flash('Entry deleted.', 'success')
    return redirect(url_for('weight.history'))


def build_chart_points(logs, width=600, height=200, padding=30):
    """Turn WeightLog rows into an SVG polyline 'x,y x,y ...' string."""
    if len(logs) < 2:
        return ''

    weights = [l.weight_kg for l in logs]
    min_w, max_w = min(weights), max(weights)
    w_range = (max_w - min_w) or 1  # avoid divide-by-zero if all equal

    n = len(logs)
    step_x = (width - 2 * padding) / (n - 1)

    points = []
    for i, log in enumerate(logs):
        x = padding + i * step_x
        # invert y: higher weight = higher on chart (lower y value)
        y = height - padding - ((log.weight_kg - min_w) / w_range) * (height - 2 * padding)
        points.append(f"{x:.1f},{y:.1f}")

    return ' '.join(points)
