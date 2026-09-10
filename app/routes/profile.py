import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.models import db, PreferredDay

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

from app.services.ai_coach import ROLE_DETAILS

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
FITNESS_LEVELS = ['beginner', 'intermediate', 'advanced']
GOALS = ['cutting', 'maintaining', 'bulking']
DIETARY_PREFERENCES = [
    ('standard', '🍗 Standard / Balanced'),
    ('vegetarian', '🧀 Vegetarian'),
    ('vegan', '🌱 100% Vegan'),
    ('keto', '🥑 Keto / Low-Carb')
]
ACTIVITY_LEVELS = [
    ('sedentary', 'Sedentary (Desk job, little exercise)'),
    ('light', 'Lightly Active (1-2 workouts/week)'),
    ('moderate', 'Moderately Active (3-5 workouts/week)'),
    ('very_active', 'Very Active (6-7 intense workouts/week)')
]


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@profile_bp.route('/', methods=['GET'])
@login_required
def view():
    selected_days = {pd.day_of_week for pd in current_user.preferred_days}
    bmi, bmi_cat = current_user.calculate_bmi()
    bmr = current_user.calculate_bmr()
    tdee = current_user.calculate_tdee()
    calorie_target = current_user.get_calorie_target()
    macros = current_user.get_target_macros()

    return render_template(
        'profile.html',
        days=DAYS,
        selected_days=selected_days,
        fitness_levels=FITNESS_LEVELS,
        goals=GOALS,
        roles=ROLE_DETAILS,
        dietary_preferences=DIETARY_PREFERENCES,
        activity_levels=ACTIVITY_LEVELS,
        bmi=bmi,
        bmi_category=bmi_cat,
        bmr=bmr,
        tdee=tdee,
        calorie_target=calorie_target,
        macros=macros
    )


@profile_bp.route('/picture', methods=['POST'])
@login_required
def upload_picture():
    file = request.files.get('picture')

    if not file or file.filename == '':
        flash('Choose an image first.', 'danger')
        return redirect(url_for('profile.view'))

    if not allowed_file(file.filename):
        flash('Only PNG, JPG, JPEG, or WEBP images are allowed.', 'danger')
        return redirect(url_for('profile.view'))

    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)

    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = secure_filename(f'user_{current_user.id}.{ext}')
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)

    current_user.profile_picture = filename
    db.session.commit()

    flash('Profile picture updated!', 'success')
    return redirect(url_for('profile.view'))


@profile_bp.route('/days', methods=['POST'])
@login_required
def update_days():
    selected = [d for d in request.form.getlist('days') if d in DAYS]

    PreferredDay.query.filter_by(user_id=current_user.id).delete()
    for day in selected:
        db.session.add(PreferredDay(user_id=current_user.id, day_of_week=day))
    db.session.commit()

    flash('Workout days updated!', 'success')
    return redirect(url_for('profile.view'))


@profile_bp.route('/settings', methods=['POST'])
@login_required
def update_settings():
    fitness_level = request.form.get('fitness_level')
    goal = request.form.get('goal')
    role = request.form.get('role')
    dietary_pref = request.form.get('dietary_preference')
    activity_level = request.form.get('activity_level')

    height_cm = request.form.get('height_cm', type=float)
    weight_kg = request.form.get('weight_kg', type=float)
    target_weight_kg = request.form.get('target_weight_kg', type=float)
    age = request.form.get('age', type=int)
    gender = request.form.get('gender')

    if fitness_level in FITNESS_LEVELS:
        current_user.fitness_level = fitness_level
    if goal in GOALS:
        current_user.goal = goal
    if role in ROLE_DETAILS:
        current_user.role = role
    if dietary_pref in [p[0] for p in DIETARY_PREFERENCES]:
        current_user.dietary_preference = dietary_pref
    if activity_level in [a[0] for a in ACTIVITY_LEVELS]:
        current_user.activity_level = activity_level

    if height_cm and height_cm > 0:
        current_user.height_cm = height_cm
    if weight_kg and weight_kg > 0:
        current_user.weight_kg = weight_kg
    if target_weight_kg and target_weight_kg > 0:
        current_user.target_weight_kg = target_weight_kg
    if age and age > 0:
        current_user.age = age
    if gender in ['male', 'female', 'other']:
        current_user.gender = gender

    db.session.commit()
    flash('Fitness profile & biometric settings updated!', 'success')
    return redirect(url_for('profile.view'))

