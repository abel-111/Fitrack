import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models import db, UserDietPlan
from app.services.ai_coach import generate_ai_diet_plan, calculate_user_targets, ROLE_DETAILS, MEAL_RECIPES

diet_bp = Blueprint('diet', __name__, url_prefix='/diet')

DIETARY_PREFERENCES = [
    ('standard', '🍗 South Indian Non-Veg (Chicken, Fish, Eggs & Dal)'),
    ('vegetarian', '🧀 South Indian Vegetarian (Paneer, Soya, Dal & Sprouts)'),
    ('vegan', '🌱 Pure Plant-Based (Millets, Chana, Soya & Dal)'),
    ('keto', '🥑 Low-Carb / Keto (Egg Podimas, Fish, Coconut & Greens)')
]

SOUTH_INDIAN_STATES = [
    'Tamil Nadu',
    'Kerala',
    'Karnataka',
    'Andhra Pradesh',
    'Telangana',
]

CUISINE_PREFERENCES = [
    ('home_state', '🏠 My Home State Dishes'),
    ('other_states', '🗺️ Explore Other South Indian States'),
    ('continental', '🌍 Continental & Healthy Fusion'),
]

@diet_bp.route('/', methods=['GET'])
@login_required
def view_plan():
    # Fetch user's active diet plan
    active_plan = UserDietPlan.query.filter_by(user_id=current_user.id, is_active=True).first()

    # If user doesn't have one yet, auto-generate their initial AI plan!
    if not active_plan:
        plan_data = generate_ai_diet_plan(current_user)
        active_plan = UserDietPlan(
            user_id=current_user.id,
            title=plan_data['title'],
            goal=plan_data['goal'],
            role=plan_data['role'],
            dietary_preference=plan_data['dietary_preference'],
            target_calories=plan_data['target_calories'],
            target_protein=plan_data['target_protein'],
            target_carbs=plan_data['target_carbs'],
            target_fat=plan_data['target_fat'],
            meals_json=json.dumps(plan_data['meals']),
            role_tips=json.dumps(plan_data['role_tips']),
            is_active=True
        )
        db.session.add(active_plan)
        db.session.commit()

    meals = json.loads(active_plan.meals_json) if active_plan.meals_json else []
    role_tips = json.loads(active_plan.role_tips) if active_plan.role_tips else []

    completed_meals = sum(1 for m in meals if m.get('completed'))
    total_meals = len(meals)
    adherence_pct = round((completed_meals / total_meals * 100)) if total_meals > 0 else 0

    role_info = ROLE_DETAILS.get(current_user.role, ROLE_DETAILS['general'])
    targets = calculate_user_targets(current_user)

    return render_template(
        'diet.html',
        plan=active_plan,
        meals=meals,
        role_tips=role_tips,
        completed_meals=completed_meals,
        total_meals=total_meals,
        adherence_pct=adherence_pct,
        role_info=role_info,
        targets=targets,
        dietary_preferences=DIETARY_PREFERENCES,
        roles=ROLE_DETAILS,
        south_indian_states=SOUTH_INDIAN_STATES,
        cuisine_preferences=CUISINE_PREFERENCES
    )


@diet_bp.route('/generate', methods=['POST'])
@login_required
def generate_new():
    dietary_pref = request.form.get('dietary_preference', current_user.dietary_preference or 'standard')
    role_override = request.form.get('role', current_user.role)
    custom_cals = request.form.get('custom_calories', type=int)
    state_override = request.form.get('state', current_user.state or 'Tamil Nadu')
    cuisine_pref = request.form.get('cuisine_preference', current_user.cuisine_preference or 'home_state')

    if role_override in ROLE_DETAILS:
        current_user.role = role_override
    if dietary_pref in ['standard', 'vegetarian', 'vegan', 'keto']:
        current_user.dietary_preference = dietary_pref
    if state_override in SOUTH_INDIAN_STATES:
        current_user.state = state_override
    if cuisine_pref in [c[0] for c in CUISINE_PREFERENCES]:
        current_user.cuisine_preference = cuisine_pref

    db.session.commit()

    plan_data = generate_ai_diet_plan(
        current_user,
        dietary_preference=dietary_pref,
        custom_calories=custom_cals,
        state=state_override,
        cuisine_preference=cuisine_pref
    )

    # Deactivate older plans
    UserDietPlan.query.filter_by(user_id=current_user.id).update({'is_active': False})

    new_plan = UserDietPlan(
        user_id=current_user.id,
        title=plan_data['title'],
        goal=plan_data['goal'],
        role=plan_data['role'],
        dietary_preference=plan_data['dietary_preference'],
        state=state_override,
        cuisine_preference=cuisine_pref,
        target_calories=plan_data['target_calories'],
        target_protein=plan_data['target_protein'],
        target_carbs=plan_data['target_carbs'],
        target_fat=plan_data['target_fat'],
        meals_json=json.dumps(plan_data['meals']),
        role_tips=json.dumps(plan_data['role_tips']),
        is_active=True
    )
    db.session.add(new_plan)
    db.session.commit()

    flash(f'Your {state_override} meal plan has been updated!', 'success')
    return redirect(url_for('diet.view_plan'))


@diet_bp.route('/toggle-meal', methods=['POST'])
@login_required
def toggle_meal():
    data = request.get_json(silent=True) or {}
    meal_id = data.get('meal_id')

    plan = UserDietPlan.query.filter_by(user_id=current_user.id, is_active=True).first()
    if not plan or not plan.meals_json:
        return jsonify({'error': 'No active diet plan found'}), 404

    meals = json.loads(plan.meals_json)
    matched = False
    new_state = False

    for m in meals:
        if m.get('id') == meal_id:
            m['completed'] = not m.get('completed', False)
            new_state = m['completed']
            matched = True
            break

    if not matched:
        return jsonify({'error': 'Meal not found in plan'}), 404

    plan.meals_json = json.dumps(meals)
    db.session.commit()

    completed_count = sum(1 for m in meals if m.get('completed'))
    adherence_pct = round((completed_count / len(meals)) * 100) if meals else 0

    return jsonify({
        'success': True,
        'meal_id': meal_id,
        'completed': new_state,
        'completed_count': completed_count,
        'total_meals': len(meals),
        'adherence_pct': adherence_pct
    })


@diet_bp.route('/reset-daily', methods=['POST'])
@login_required
def reset_daily():
    plan = UserDietPlan.query.filter_by(user_id=current_user.id, is_active=True).first()
    if plan and plan.meals_json:
        meals = json.loads(plan.meals_json)
        for m in meals:
            m['completed'] = False
        plan.meals_json = json.dumps(meals)
        db.session.commit()
        flash('Daily meal checklist reset for today!', 'info')
    return redirect(url_for('diet.view_plan'))
