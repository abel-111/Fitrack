import json
from datetime import datetime, date, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models import db, UserDietPlan, FoodLog
from app.services.ai_coach import (
    generate_ai_diet_plan,
    calculate_user_targets,
    ROLE_DETAILS,
    MEAL_RECIPES,
    get_regional_food_recommendations_today
)
from app.services.food_database import (
    COMMON_FOODS,
    FOOD_CATEGORIES,
    search_foods,
    get_food_by_id
)

diet_bp = Blueprint('diet', __name__, url_prefix='/diet')

DIETARY_PREFERENCES = [
    ('standard', '🍗 Standard Non-Veg (Chicken, Fish, Eggs & Dal)'),
    ('vegetarian', '🧀 Vegetarian (Paneer, Soya, Dal & Sprouts)'),
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
    ('other_states', '🗺️ Explore Other Regional States'),
    ('continental', '🌍 Continental & Healthy Fusion'),
]

@diet_bp.route('/', methods=['GET'])
@login_required
def view_plan():
    # Parse requested date for food tracking (defaults to today)
    date_str = request.args.get('date')
    selected_date = date.today()
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = date.today()

    prev_date = selected_date - timedelta(days=1)
    next_date = selected_date + timedelta(days=1)
    is_today = (selected_date == date.today())

    # Get user's logged food summary for this date
    food_summary = current_user.get_daily_food_summary(selected_date)

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
    regional_recommendations = get_regional_food_recommendations_today(current_user, active_plan.dietary_preference)

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
        cuisine_preferences=CUISINE_PREFERENCES,
        regional_recommendations=regional_recommendations,
        food_summary=food_summary,
        selected_date=selected_date,
        selected_date_str=selected_date.strftime('%Y-%m-%d'),
        prev_date_str=prev_date.strftime('%Y-%m-%d'),
        next_date_str=next_date.strftime('%Y-%m-%d'),
        is_today=is_today,
        food_categories=FOOD_CATEGORIES,
        common_foods=COMMON_FOODS
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


@diet_bp.route('/food-log/add', methods=['POST'])
@login_required
def add_food_log():
    # Support both JSON request and Form submit
    is_json = request.is_json
    data = request.get_json(silent=True) if is_json else request.form

    food_name = (data.get('food_name') or '').strip()
    if not food_name:
        if is_json:
            return jsonify({'error': 'Food name is required'}), 400
        flash('Please provide a food name', 'warning')
        return redirect(url_for('diet.view_plan'))

    meal_type = (data.get('meal_type') or 'snack').lower()
    if meal_type not in ['breakfast', 'lunch', 'snack', 'dinner']:
        meal_type = 'snack'

    serving_size = (data.get('serving_size') or '1 serving').strip()

    try:
        quantity = max(0.1, float(data.get('quantity') or 1.0))
    except (ValueError, TypeError):
        quantity = 1.0

    try:
        raw_cals = max(0.0, float(data.get('calories') or 0.0))
    except (ValueError, TypeError):
        raw_cals = 0.0

    try:
        raw_prot = max(0.0, float(data.get('protein') or 0.0))
    except (ValueError, TypeError):
        raw_prot = 0.0

    try:
        raw_carbs = max(0.0, float(data.get('carbs') or 0.0))
    except (ValueError, TypeError):
        raw_carbs = 0.0

    try:
        raw_fat = max(0.0, float(data.get('fat') or 0.0))
    except (ValueError, TypeError):
        raw_fat = 0.0

    # If is_per_serving is passed or default, multiply by quantity
    is_per_serving = data.get('is_per_unit', 'true') in ['true', True, '1']
    if is_per_serving:
        calories = raw_cals * quantity
        protein = raw_prot * quantity
        carbs = raw_carbs * quantity
        fat = raw_fat * quantity
    else:
        calories = raw_cals
        protein = raw_prot
        carbs = raw_carbs
        fat = raw_fat

    date_str = data.get('date')
    target_date = date.today()
    if date_str:
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            target_date = date.today()

    new_log = FoodLog(
        user_id=current_user.id,
        date=target_date,
        meal_type=meal_type,
        food_name=food_name,
        serving_size=serving_size,
        quantity=quantity,
        calories=round(calories, 1),
        protein=round(protein, 1),
        carbs=round(carbs, 1),
        fat=round(fat, 1)
    )
    db.session.add(new_log)
    db.session.commit()

    if is_json:
        summary = current_user.get_daily_food_summary(target_date)
        return jsonify({
            'success': True,
            'message': f'Logged {food_name} ({round(calories)} kcal, {round(protein, 1)}g protein)',
            'log_id': new_log.id,
            'summary': {
                'total_calories': summary['total_calories'],
                'total_protein': summary['total_protein'],
                'calorie_pct': summary['calorie_pct'],
                'protein_pct': summary['protein_pct'],
                'remaining_calories': summary['remaining_calories'],
                'remaining_protein': summary['remaining_protein']
            }
        })

    flash(f'Logged {food_name}: +{round(calories)} kcal, +{round(protein, 1)}g protein to {meal_type.capitalize()}!', 'success')
    return redirect(url_for('diet.view_plan', date=target_date.strftime('%Y-%m-%d')))


@diet_bp.route('/food-log/delete/<int:log_id>', methods=['POST'])
@login_required
def delete_food_log(log_id):
    log = FoodLog.query.filter_by(id=log_id, user_id=current_user.id).first()
    if not log:
        if request.is_json:
            return jsonify({'error': 'Food log not found'}), 404
        flash('Food entry not found', 'warning')
        return redirect(url_for('diet.view_plan'))

    log_date_str = log.date.strftime('%Y-%m-%d')
    food_name = log.food_name
    db.session.delete(log)
    db.session.commit()

    if request.is_json:
        summary = current_user.get_daily_food_summary(log_date_str)
        return jsonify({
            'success': True,
            'message': f'Removed {food_name}',
            'summary': {
                'total_calories': summary['total_calories'],
                'total_protein': summary['total_protein'],
                'calorie_pct': summary['calorie_pct'],
                'protein_pct': summary['protein_pct'],
                'remaining_calories': summary['remaining_calories'],
                'remaining_protein': summary['remaining_protein']
            }
        })

    flash(f'Removed {food_name} from your food log.', 'info')
    return redirect(url_for('diet.view_plan', date=log_date_str))


@diet_bp.route('/food-log/log-plan-meal', methods=['POST'])
@login_required
def log_plan_meal():
    """
    Log a meal directly from the user's active AI plan into their daily food tracker.
    """
    is_json = request.is_json
    data = request.get_json(silent=True) if is_json else request.form

    meal_id = data.get('meal_id')
    date_str = data.get('date')
    target_date = date.today()
    if date_str:
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            target_date = date.today()

    plan = UserDietPlan.query.filter_by(user_id=current_user.id, is_active=True).first()
    if not plan or not plan.meals_json:
        if is_json:
            return jsonify({'error': 'No active diet plan found'}), 404
        flash('No active diet plan found', 'warning')
        return redirect(url_for('diet.view_plan'))

    meals = json.loads(plan.meals_json)
    target_meal = None
    for m in meals:
        if m.get('id') == meal_id:
            target_meal = m
            m['completed'] = True  # mark completed
            break

    if not target_meal:
        if is_json:
            return jsonify({'error': 'Meal not found in plan'}), 404
        flash('Meal not found in plan', 'warning')
        return redirect(url_for('diet.view_plan'))

    plan.meals_json = json.dumps(meals)

    # Map meal slot to meal_type
    slot_lower = (target_meal.get('slot_name') or 'Snack').lower()
    if 'breakfast' in slot_lower:
        m_type = 'breakfast'
    elif 'lunch' in slot_lower:
        m_type = 'lunch'
    elif 'dinner' in slot_lower:
        m_type = 'dinner'
    else:
        m_type = 'snack'

    new_log = FoodLog(
        user_id=current_user.id,
        date=target_date,
        meal_type=m_type,
        food_name=target_meal.get('name', 'Plan Meal'),
        serving_size='1 standard portion',
        quantity=1.0,
        calories=float(target_meal.get('calories', 0)),
        protein=float(target_meal.get('protein', 0)),
        carbs=float(target_meal.get('carbs', 0)),
        fat=float(target_meal.get('fat', 0))
    )
    db.session.add(new_log)
    db.session.commit()

    if is_json:
        summary = current_user.get_daily_food_summary(target_date)
        return jsonify({
            'success': True,
            'message': f"Logged {target_meal['name']} to today's food tracker!",
            'summary': {
                'total_calories': summary['total_calories'],
                'total_protein': summary['total_protein'],
                'calorie_pct': summary['calorie_pct'],
                'protein_pct': summary['protein_pct']
            }
        })

    flash(f"Logged '{target_meal['name']}' to today's food tracker (+{target_meal.get('calories')} kcal, +{target_meal.get('protein')}g protein)!", 'success')
    return redirect(url_for('diet.view_plan', date=target_date.strftime('%Y-%m-%d')))


@diet_bp.route('/api/foods', methods=['GET'])
@login_required
def api_foods():
    q = request.args.get('q', '').strip()
    cat = request.args.get('category', 'all').strip()
    foods = search_foods(query=q, category=cat, limit=30)
    return jsonify({'foods': foods})

