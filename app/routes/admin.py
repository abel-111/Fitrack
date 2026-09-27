from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import db, User

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(fn):
    """Decorator: restricts route to admins only."""
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not getattr(current_user, 'is_admin', False):
            flash('Access restricted to Fitrack Administrators.', 'danger')
            return redirect(url_for('auth.dashboard'))
        return fn(*args, **kwargs)
    return wrapper


@admin_bp.route('/')
@login_required
@admin_required
def portal():
    pending_coaches  = User.query.filter_by(is_coach=True, coach_approved=False).order_by(User.created_at.desc()).all()
    approved_coaches = User.query.filter_by(is_coach=True, coach_approved=True).order_by(User.created_at.desc()).all()
    total_clients    = User.query.filter_by(is_coach=False, is_admin=False).count()
    total_coaches    = User.query.filter_by(is_coach=True).count()
    approved_count   = User.query.filter_by(is_coach=True, coach_approved=True).count()
    pending_count    = User.query.filter_by(is_coach=True, coach_approved=False).count()
    total_users      = User.query.count()

    return render_template(
        'admin_portal.html',
        pending_coaches=pending_coaches,
        approved_coaches=approved_coaches,
        total_clients=total_clients,
        total_coaches=total_coaches,
        approved_count=approved_count,
        pending_count=pending_count,
        total_users=total_users,
    )


@admin_bp.route('/approve-coach/<int:coach_id>', methods=['POST'])
@login_required
@admin_required
def approve_coach(coach_id):
    coach = User.query.filter_by(id=coach_id, is_coach=True).first_or_404()
    coach.coach_approved = True
    db.session.commit()
    flash(f'✅ Coach {coach.username} has been approved and can now access their portal.', 'success')
    return redirect(url_for('admin.portal'))


@admin_bp.route('/reject-coach/<int:coach_id>', methods=['POST'])
@login_required
@admin_required
def reject_coach(coach_id):
    coach = User.query.filter_by(id=coach_id, is_coach=True).first_or_404()
    coach.coach_approved = False
    db.session.commit()
    flash(f'⛔ Coach {coach.username} has been revoked / rejected.', 'warning')
    return redirect(url_for('admin.portal'))


@admin_bp.route('/remove-coach/<int:coach_id>', methods=['POST'])
@login_required
@admin_required
def remove_coach(coach_id):
    """Demote a coach account back to regular client."""
    coach = User.query.filter_by(id=coach_id, is_coach=True).first_or_404()
    coach.is_coach = False
    coach.coach_approved = False
    db.session.commit()
    flash(f'🔄 {coach.username} has been demoted to a regular client account.', 'info')
    return redirect(url_for('admin.portal'))
