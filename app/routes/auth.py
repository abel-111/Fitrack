from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'general')
        account_type = request.form.get('account_type', 'client')
        coach_specialty = request.form.get('coach_specialty', 'General Fitness & Nutrition')
        coach_bio = request.form.get('coach_bio', 'Certified Fitness Specialist')

        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('auth.signup'))

        if User.query.filter_by(username=username).first():
            flash('Username already taken.', 'danger')
            return redirect(url_for('auth.signup'))

        is_coach_val = (account_type == 'coach')
        user = User(
            username=username,
            email=email,
            role=role if role in User.ROLE_LABELS else 'general',
            is_coach=is_coach_val,
            coach_specialty=coach_specialty if is_coach_val else None,
            coach_bio=coach_bio if is_coach_val else None
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    from app.services.ai_coach import ROLE_DETAILS
    return render_template('signup.html', roles=ROLE_DETAILS)



@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if getattr(current_user, 'is_coach', False):
            return redirect(url_for('ai.coach_portal'))
        return redirect(url_for('auth.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            if user.is_coach:
                flash(f"Welcome back, Coach {user.username}!", "success")
                return redirect(url_for('ai.coach_portal'))
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth_bp.route('/dashboard')
@login_required
def dashboard():
    from app.services.ai_coach import ROLE_DETAILS, get_user_ai_recommendations
    from app.models import UserDietPlan, LiftLog

    role_key = current_user.role if current_user.role in ROLE_DETAILS else 'general'
    role_info = ROLE_DETAILS[role_key]
    ai_insights = get_user_ai_recommendations(current_user)
    active_plan = UserDietPlan.query.filter_by(user_id=current_user.id, is_active=True).first()
    latest_lift = LiftLog.query.filter_by(user_id=current_user.id).order_by(LiftLog.logged_at.desc()).first()

    bmi, bmi_cat = current_user.calculate_bmi()
    calorie_target = current_user.get_calorie_target()
    macros = current_user.get_target_macros()
    today_food = current_user.get_daily_food_summary()
    today_workout = current_user.get_daily_workout_summary()

    return render_template(
        'dashboard.html',
        current_streak=current_user.get_current_streak(),
        longest_streak=current_user.get_longest_streak(),
        month_count=current_user.get_month_checkin_count(),
        checked_in_today=current_user.has_checked_in_today(),
        preferred_days=current_user.get_preferred_days_sorted(),
        role_info=role_info,
        ai_insights=ai_insights,
        active_plan=active_plan,
        bmi=bmi,
        bmi_category=bmi_cat,
        calorie_target=calorie_target,
        macros=macros,
        latest_lift=latest_lift,
        today_food=today_food,
        today_workout=today_workout
    )



@auth_bp.route('/')
def index():
    return redirect(url_for('auth.login'))