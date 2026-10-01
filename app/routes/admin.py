from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import db, User, CoachMessage, Attendance, WeightLog, FoodLog, UserDietPlan

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
    search_q = request.args.get('q', '').strip()
    role_filter = request.args.get('role', 'all')

    client_query = User.query.filter_by(is_coach=False, is_admin=False)
    if search_q:
        client_query = client_query.filter(
            (User.username.ilike(f'%{search_q}%')) | (User.email.ilike(f'%{search_q}%'))
        )
    if role_filter != 'all':
        client_query = client_query.filter_by(role=role_filter)

    clients = client_query.order_by(User.created_at.desc()).all()

    pending_coaches  = User.query.filter_by(is_coach=True, coach_approved=False).order_by(User.created_at.desc()).all()
    approved_coaches = User.query.filter_by(is_coach=True, coach_approved=True).order_by(User.created_at.desc()).all()
    total_clients    = User.query.filter_by(is_coach=False, is_admin=False).count()
    total_coaches    = User.query.filter_by(is_coach=True).count()
    approved_count   = User.query.filter_by(is_coach=True, coach_approved=True).count()
    pending_count    = User.query.filter_by(is_coach=True, coach_approved=False).count()
    total_users      = User.query.count()

    return render_template(
        'admin_portal.html',
        clients=clients,
        pending_coaches=pending_coaches,
        approved_coaches=approved_coaches,
        total_clients=total_clients,
        total_coaches=total_coaches,
        approved_count=approved_count,
        pending_count=pending_count,
        total_users=total_users,
        search_q=search_q,
        role_filter=role_filter,
    )


@admin_bp.route('/user/<int:user_id>')
@login_required
@admin_required
def user_details(user_id):
    """View full dossier on any client or coach."""
    target_user = User.query.get_or_404(user_id)
    bmi, bmi_cat = target_user.calculate_bmi()
    macros = target_user.get_target_macros()
    calorie_target = target_user.get_calorie_target()
    recent_weights = WeightLog.query.filter_by(user_id=target_user.id).order_by(WeightLog.logged_at.desc()).limit(10).all()
    recent_food = FoodLog.query.filter_by(user_id=target_user.id).order_by(FoodLog.logged_at.desc()).limit(15).all()
    plans = UserDietPlan.query.filter_by(user_id=target_user.id).order_by(UserDietPlan.created_at.desc()).all()

    return render_template(
        'admin_user_detail.html',
        target_user=target_user,
        bmi=bmi,
        bmi_cat=bmi_cat,
        macros=macros,
        calorie_target=calorie_target,
        recent_weights=recent_weights,
        recent_food=recent_food,
        plans=plans
    )


@admin_bp.route('/user/<int:user_id>/update', methods=['POST'])
@login_required
@admin_required
def update_user(user_id):
    """Admin full editing access to user/coach biometrics & credentials."""
    target_user = User.query.get_or_404(user_id)
    
    target_user.username = request.form.get('username', target_user.username).strip()
    target_user.email = request.form.get('email', target_user.email).strip()
    
    new_password = request.form.get('new_password', '').strip()
    if new_password:
        target_user.set_password(new_password)
        
    if not target_user.is_coach and not target_user.is_admin:
        target_user.goal = request.form.get('goal', target_user.goal)
        target_user.role = request.form.get('role', target_user.role)
        target_user.dietary_preference = request.form.get('dietary_preference', target_user.dietary_preference)
        target_user.fitness_level = request.form.get('fitness_level', target_user.fitness_level)
        
        try:
            target_user.weight_kg = float(request.form.get('weight_kg')) if request.form.get('weight_kg') else None
        except ValueError:
            pass
        try:
            target_user.height_cm = float(request.form.get('height_cm')) if request.form.get('height_cm') else None
        except ValueError:
            pass
        try:
            target_user.target_weight_kg = float(request.form.get('target_weight_kg')) if request.form.get('target_weight_kg') else None
        except ValueError:
            pass
    elif target_user.is_coach:
        target_user.coach_specialty = request.form.get('coach_specialty', target_user.coach_specialty)
        target_user.coach_bio = request.form.get('coach_bio', target_user.coach_bio)
        target_user.coach_approved = True if request.form.get('coach_approved') == '1' else False

    db.session.commit()
    flash(f"✅ User profile for {target_user.username} successfully updated by Admin.", "success")
    return redirect(url_for('admin.user_details', user_id=target_user.id))


@admin_bp.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """Delete a user account."""
    if user_id == current_user.id:
        flash("You cannot delete your own admin account.", "danger")
        return redirect(url_for('admin.portal'))
        
    target_user = User.query.get_or_404(user_id)
    username = target_user.username
    
    # Delete related dependencies
    Attendance.query.filter_by(user_id=target_user.id).delete()
    WeightLog.query.filter_by(user_id=target_user.id).delete()
    FoodLog.query.filter_by(user_id=target_user.id).delete()
    UserDietPlan.query.filter_by(user_id=target_user.id).delete()
    CoachMessage.query.filter((CoachMessage.client_id == target_user.id) | (CoachMessage.coach_id == target_user.id)).delete()
    
    db.session.delete(target_user)
    db.session.commit()
    flash(f"🗑️ Account for '{username}' and all associated records have been removed.", "warning")
    return redirect(url_for('admin.portal'))



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
