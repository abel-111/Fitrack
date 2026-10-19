from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, jsonify
from flask_login import login_required, current_user
from datetime import datetime, date, timedelta
from app.models import db, LiftLog, WorkoutLog
from app.services.ai_coach import ROLE_DETAILS
from app.services.workout_database import COMMON_EXERCISES, WORKOUT_CATEGORIES, search_exercises

workouts_bp = Blueprint('workouts', __name__, url_prefix='/workouts')

REPS_BY_GOAL = {
    'cutting': {'sets': 3, 'reps': '12-15', 'rest': '45-60s'},
    'maintaining': {'sets': 3, 'reps': '8-12', 'rest': '60-90s'},
    'bulking': {'sets': 4, 'reps': '6-10', 'rest': '90-120s'},
}

GOAL_NOTES = {
    'cutting': 'Keep rest periods short (45-60s) to keep heart rate elevated. Finish with 10-15 mins of incline treadmill walk.',
    'maintaining': 'Standard rest periods (60-90s). Focus on crisp movement quality and maintaining weight loads session to session.',
    'bulking': 'Rest 90-120s between sets. Prioritize progressive overload—when you hit the top rep target on all sets, increase load by 2.5-5kg next week.',
}

ROLE_WARMUPS = {
    'desk_worker': {
        'title': '💼 Desk Posture & Spine Reset (5 Mins)',
        'note': 'Combat 8 hours of sitting by activating dormant glutes and opening tight hip flexors & pecs before touching weights.',
        'exercises': [
            'Thoracic Spine Foam Roll / Extension — 10 reps',
            'Kneeling Hip Flexor / Couch Stretch — 45s per side',
            'Band Pull-Aparts / Face Pulls — 15 reps',
            'Glute Bridges with 2s hold at top — 12 reps'
        ]
    },
    'student': {
        'title': '🎓 Express Focus Warm-Up (4 Mins)',
        'note': 'Quick neural primer to clear study brain fog and prep your central nervous system for lifting.',
        'exercises': [
            'Jumping Jacks or Light Skipping — 60 seconds',
            'Bodyweight Squats with reach — 12 reps',
            'Arm Circles & Shoulder Dislocates — 15 reps',
            'World\'s Greatest Stretch — 5 per side'
        ]
    },
    'athlete': {
        'title': '🏃 Dynamic Power & Elasticity Primer (7 Mins)',
        'note': 'High-velocity movement preparation for maximum tendon recoil and joint stabilization.',
        'exercises': [
            'Leg Swings (Front/Back & Side) — 10 per leg',
            'Pogo Hops / Ankle Bounces — 2 x 20 reps',
            'Walking Lunges with Torso Twist — 10 per leg',
            'Inchworms with Push-up — 6 reps'
        ]
    },
    'bodybuilder': {
        'title': '🏋️ Hypertrophy Activation & Joint Lubrication (5 Mins)',
        'note': 'Warm up synovial fluid in elbows, knees, and shoulders before heavy loading.',
        'exercises': [
            'Rotator Cuff Cable/Band Rotations — 2 x 15 reps',
            'Light Cable Crossover / Pec Fly — 15 slow reps',
            'Bodyweight Hanging Decompression — 45 seconds',
            'Empty Barbell Warm-Up Sets — 2 x 10 reps'
        ]
    },
    'busy_parent': {
        'title': '👨‍👩‍👧 3-Minute Quick Flow',
        'note': 'Fast full-body sequence so you can get straight to work with zero wasted minutes.',
        'exercises': [
            'Deep Squat Hold into Hamstring Stretch — 60 seconds',
            'Cat-Cow Spine Mobilization — 10 slow cycles',
            'Walkouts to High Plank — 8 reps'
        ]
    },
    'general': {
        'title': '🧘 Essential Functional Warm-Up (5 Mins)',
        'note': 'General cardiovascular elevation and multi-planar mobility routine.',
        'exercises': [
            'Brisk Treadmill or Rower — 3 minutes',
            'Arm Circles & Torso Twists — 15 reps each',
            'Bodyweight Squats to Stand — 10 reps',
            'Hip 90/90 Rotations — 6 per side'
        ]
    }
}

PLANS = {
    'beginner': [
        {
            'title': 'Day 1 - Push Foundation',
            'focus': 'Chest, Shoulders (Front/Lateral Delts), Triceps',
            'exercises': [
                {'name': 'Barbell or Dumbbell Bench Press', 'muscle': 'Chest & Triceps', 'tip': 'Tuck shoulder blades down and back, controlled descent.'},
                {'name': 'Incline Dumbbell Press', 'muscle': 'Upper Chest', 'tip': 'Set bench to 30 degrees for clavicular head stimulation.'},
                {'name': 'Seated Overhead Dumbbell Press', 'muscle': 'Anterior Deltoids', 'tip': 'Press overhead smoothly without arching lower back.'},
                {'name': 'Dumbbell Lateral Raise', 'muscle': 'Side Delts', 'tip': 'Slight forward lean, lead with elbows up to shoulder level.'},
                {'name': 'Tricep Rope Pushdown', 'muscle': 'Triceps Lateral Head', 'tip': 'Keep elbows pinned to ribs; spread the rope at bottom.'}
            ]
        },
        {
            'title': 'Day 2 - Pull Foundation',
            'focus': 'Back, Lats, Rear Delts, Biceps',
            'exercises': [
                {'name': 'Lat Pulldown', 'muscle': 'Lats & Back Width', 'tip': 'Pull smoothly down to upper chest, pausing 1 second.'},
                {'name': 'Seated Cable Row', 'muscle': 'Mid Back & Rhomboids', 'tip': 'Squeeze shoulder blades together firmly at the torso.'},
                {'name': 'Chest-Supported Dumbbell Row', 'muscle': 'Upper Back', 'tip': 'Eliminate momentum; pull elbows back toward hips.'},
                {'name': 'Face Pulls / Rear Delt Fly', 'muscle': 'Rear Delts & Posture', 'tip': 'Pull towards forehead with external rotation.'},
                {'name': 'Standing Dumbbell Bicep Curl', 'muscle': 'Biceps Brachii', 'tip': 'Strict posture, zero hip swing, supinate wrists.'}
            ]
        },
        {
            'title': 'Day 3 - Legs & Core Foundation',
            'focus': 'Quads, Hamstrings, Glutes, Calves, Abs',
            'exercises': [
                {'name': 'Goblet Squat or Leg Press', 'muscle': 'Quads & Glutes', 'tip': 'Drive knees out, maintain upright chest, full depth.'},
                {'name': 'Romanian Deadlift (Dumbbell or Barbell)', 'muscle': 'Hamstrings & Glutes', 'tip': 'Hinge backwards at hips until deep hamstring stretch.'},
                {'name': 'Seated Leg Extension', 'muscle': 'Quads Isolation', 'tip': 'Control the eccentric phase and squeeze at peak.'},
                {'name': 'Lying or Seated Leg Curl', 'muscle': 'Hamstrings Flexion', 'tip': 'Keep hips glued to pad, avoid lower back arch.'},
                {'name': 'Standing Calf Raise', 'muscle': 'Calves', 'tip': 'Pause at the bottom stretch for 2 full seconds.'},
                {'name': 'Plank or Bicycle Crunches', 'muscle': 'Core Stability', 'tip': 'Brace core as if expecting a punch; hold steady.'}
            ]
        },
    ],
    'intermediate': [
        {
            'title': 'Day 1 - Push Hypertrophy',
            'focus': 'Chest, Anterior Delts, Lateral Delts, Triceps',
            'exercises': [
                {'name': 'Flat Barbell Bench Press', 'muscle': 'Pectoralis Major', 'tip': '3-second eccentric descent on heavy working sets.'},
                {'name': 'Incline Dumbbell Bench Press', 'muscle': 'Upper Pecs', 'tip': 'Deep stretch at bottom, converge dumbbells smoothly at top.'},
                {'name': 'Standing Overhead Military Press', 'muscle': 'Front Deltoids', 'tip': 'Brace glutes and abs tight; full lockout overhead.'},
                {'name': 'Cable Lateral Raise', 'muscle': 'Lateral Deltoids', 'tip': 'Constant tension on the side delts; slight elbow bend.'},
                {'name': 'Cable Chest Fly', 'muscle': 'Inner Pec Squeeze', 'tip': 'Focus on peak contraction and controlled stretch.'},
                {'name': 'Tricep Rope Pushdown', 'muscle': 'Triceps Lateral Head', 'tip': 'Spread the rope at the bottom and lock out.'}
            ]
        },
        {
            'title': 'Day 2 - Pull Hypertrophy',
            'focus': 'Lats, Upper Back, Rear Delts, Biceps',
            'exercises': [
                {'name': 'Conventional Deadlift or Rack Pull', 'muscle': 'Total Posterior Chain', 'tip': 'Reset after each repetition with tight lats.'},
                {'name': 'Wide-Grip Lat Pulldown or Pull-up', 'muscle': 'Lats Width', 'tip': 'Drive elbows down towards hips; don\'t swing.'},
                {'name': 'Bent-over Barbell Row', 'muscle': 'Mid Back & Rhomboids', 'tip': 'Torso at 45 degrees, explosive pull to lower ribcage.'},
                {'name': 'Cable Face Pull with External Rotation', 'muscle': 'Rear Delts & Rotator Cuff', 'tip': 'Pull towards temples, thumbs pointing back.'},
                {'name': 'Incline Dumbbell Bicep Curl', 'muscle': 'Biceps Long Head', 'tip': 'Full stretch at bottom, supinate wrists at top.'},
                {'name': 'Dumbbell Hammer Curl', 'muscle': 'Brachialis & Forearms', 'tip': 'Thickens upper arm and strengthens grip.'}
            ]
        },
        {
            'title': 'Day 3 - Legs & Core Power',
            'focus': 'Quads, Hamstrings, Glutes, Calves, Abs',
            'exercises': [
                {'name': 'Barbell Back Squat', 'muscle': 'Quads & Glutes', 'tip': 'Hit parallel or below with upright torso and knee control.'},
                {'name': 'Romanian Deadlift', 'muscle': 'Hamstrings & Glutes', 'tip': 'Shins remain vertical during hip hinge.'},
                {'name': 'Leg Press or Hack Squat', 'muscle': 'Quads Hypertrophy', 'tip': 'Feet shoulder-width, deep controlled descent.'},
                {'name': 'Lying Leg Curl', 'muscle': 'Hamstrings Isolation', 'tip': 'Keep hips glued to pad; avoid swinging weights.'},
                {'name': 'Standing Calf Raise', 'muscle': 'Gastrocnemius', 'tip': 'Hold bottom stretch for 2 full seconds.'},
                {'name': 'Hanging Knee/Leg Raises', 'muscle': 'Lower Abs', 'tip': 'Curl pelvis upward; avoid swinging momentum.'}
            ]
        },
        {
            'title': 'Day 4 - Legs & Shoulders Focus',
            'focus': 'Quads, Hamstrings, Deltoids (All 3 Heads), Traps',
            'exercises': [
                {'name': 'Bulgarian Split Squat or Walking Lunges', 'muscle': 'Unilateral Quads & Glutes', 'tip': 'Lean forward slightly for glute & quad stretch.'},
                {'name': 'Seated Leg Extension', 'muscle': 'Quads Peak Contraction', 'tip': 'Pause 1 second at top lockout.'},
                {'name': 'Seated Dumbbell Arnold Press', 'muscle': 'Total Shoulder Complex', 'tip': 'Smooth rotation from chest to overhead lockout.'},
                {'name': 'Dumbbell Lateral Raise (Heavy/Drop-set)', 'muscle': 'Lateral Deltoids', 'tip': 'Controlled 3-second negative.'},
                {'name': 'Bent-over Rear Delt Fly', 'muscle': 'Posterior Deltoids', 'tip': 'Squeeze back of shoulder blades at top.'},
                {'name': 'Dumbbell Shrugs', 'muscle': 'Upper Trapezius', 'tip': 'Straight up and down with 2-second peak hold; no rolling.'}
            ]
        },
    ],
    'advanced': [
        {
            'title': 'Day 1 - Push Hypertrophy & Strength',
            'focus': 'Chest, Anterior & Lateral Delts, Triceps',
            'exercises': [
                {'name': 'Flat Barbell Bench Press', 'muscle': 'Pectoralis Major', 'tip': 'Heavy working sets with 2 RIR.'},
                {'name': 'Incline Dumbbell Press', 'muscle': 'Clavicular Pecs', 'tip': 'Elbows at 45-degree angle, deep stretch.'},
                {'name': 'Standing Overhead Military Press', 'muscle': 'Anterior Deltoids', 'tip': 'Strict lockouts without knee bounce.'},
                {'name': 'Cable Lateral Raise', 'muscle': 'Lateral Deltoids', 'tip': 'Constant tension on the side delts across full ROM.'},
                {'name': 'Weighted Tricep Dips', 'muscle': 'Lower Pecs & Triceps', 'tip': 'Slow descent, drive hard through palms.'},
                {'name': 'Overhead EZ-Bar Tricep Extension', 'muscle': 'Tricep Long Head', 'tip': 'Keep elbows pointing forward and tucked.'}
            ]
        },
        {
            'title': 'Day 2 - Pull Hypertrophy & Back Density',
            'focus': 'Back Thickness, Lats, Rear Delts, Biceps',
            'exercises': [
                {'name': 'Conventional Deadlift', 'muscle': 'Total Posterior Chain', 'tip': 'Reset after each repetition; pull slack out of bar.'},
                {'name': 'Weighted Pull-ups', 'muscle': 'Lats & Biceps', 'tip': 'Full dead-hang at bottom, chest to bar at top.'},
                {'name': 'Meadows Row or T-Bar Row', 'muscle': 'Lats & Rhomboids', 'tip': 'Drive elbow back towards hip with strict form.'},
                {'name': 'Cable Face Pull with External Rotation', 'muscle': 'Rear Delts & Rotator Cuff', 'tip': 'Pull towards temples, hold squeeze 1s.'},
                {'name': 'Barbell Bicep Curl', 'muscle': 'Biceps Brachii', 'tip': 'Strict posture, zero hip swing.'},
                {'name': 'Incline Dumbbell Hammer Curl', 'muscle': 'Brachialis & Forearms', 'tip': 'Slow, controlled eccentric tempo.'}
            ]
        },
        {
            'title': 'Day 3 - Legs & Abs Heavy',
            'focus': 'Quads, Hamstrings, Glutes, Calves, Core',
            'exercises': [
                {'name': 'Barbell Back Squat', 'muscle': 'Quads & Glutes', 'tip': 'Deep controlled depth, drive through midfoot.'},
                {'name': 'Romanian Deadlift', 'muscle': 'Hamstrings', 'tip': 'Keep bar glued to thighs, deep posterior stretch.'},
                {'name': 'Hack Squat or Heavy Leg Press', 'muscle': 'Quad Tear-drop', 'tip': 'Foot placement low-to-mid on platform.'},
                {'name': 'Lying Leg Curl', 'muscle': 'Hamstring Flexion', 'tip': 'Toes pointed down to reduce calf contribution.'},
                {'name': 'Seated Calf Raise', 'muscle': 'Soleus', 'tip': 'Slow, rhythmic 15-20 reps with bottom pause.'},
                {'name': 'Hanging Leg Raises', 'muscle': 'Lower Abs & Hip Flexors', 'tip': 'Curl pelvis upward; don\'t just swing legs.'}
            ]
        },
        {
            'title': 'Day 4 - Push Weak Points & Hypertrophy',
            'focus': 'Incline Chest, Side Delts, Tricep Horseshoe',
            'exercises': [
                {'name': 'Incline Barbell Bench Press', 'muscle': 'Upper Chest', 'tip': 'Touch collarbone area gently, pause 1s at bottom.'},
                {'name': 'Seated Dumbbell Shoulder Press', 'muscle': 'Shoulder Delts', 'tip': 'Controlled 3s lowering phase.'},
                {'name': 'Cable Chest Fly (High-to-Low)', 'muscle': 'Lower & Inner Pec Squeeze', 'tip': 'Focus on intense peak contraction.'},
                {'name': 'Dumbbell Lateral Raise (Heavy Partial + Full)', 'muscle': 'Lateral Deltoids', 'tip': 'High volume, maximum side delt burn.'},
                {'name': 'Tricep Rope Pushdown Drop-Set', 'muscle': 'Triceps Lateral Head', 'tip': 'Squeeze hard at lockout.'}
            ]
        },
        {
            'title': 'Day 5 - Pull & Posterior Detail',
            'focus': 'Lats Width, Upper Back, Traps, Forearms',
            'exercises': [
                {'name': 'Rack Pulls below Knee', 'muscle': 'Erectors & Upper Traps', 'tip': 'Heavy explosive lockouts.'},
                {'name': 'Seated Cable Row with V-Grip', 'muscle': 'Mid Back', 'tip': 'Squeeze back hard at torso.'},
                {'name': 'Chest-Supported Row', 'muscle': 'Rhomboids & Mid Traps', 'tip': 'Isolate upper back without spinal fatigue.'},
                {'name': 'Cable Reverse Pec Deck Fly', 'muscle': 'Rear Deltoids', 'tip': 'Keep arms almost straight, squeeze rear delts.'},
                {'name': 'Dumbbell Shrugs with 2s hold', 'muscle': 'Upper Trapezius', 'tip': 'Straight up and down, no shoulder rolling.'},
                {'name': 'Preacher Curl / Spider Curl', 'muscle': 'Biceps Short Head', 'tip': 'Strict isolation without shoulder assist.'}
            ]
        },
        {
            'title': 'Day 6 - Legs & Shoulders Complete',
            'focus': 'Quad Sweep, Hamstrings, 3D Delts & Traps',
            'exercises': [
                {'name': 'Front Squat or Bulgarian Split Squat', 'muscle': 'Quad Dominance & Core', 'tip': 'Upright torso, deep stretch at bottom.'},
                {'name': 'Seated Leg Extension & Curl Superset', 'muscle': 'Quads & Hamstrings Isolation', 'tip': 'Continuous tension through entire set.'},
                {'name': 'Standing Overhead Barbell Push Press', 'muscle': 'Total Shoulder Power', 'tip': 'Explosive drive from legs, strict lockout.'},
                {'name': 'Cable Face Pull to Overhead Press', 'muscle': 'Rear Delts & Lower Traps', 'tip': 'Great for rotator cuff and 3D shoulder shape.'},
                {'name': 'Heavy Dumbbell Lateral Raise', 'muscle': 'Side Delts', 'tip': 'Controlled movement, lead with elbows.'},
                {'name': 'Farmer\'s Walk or Heavy Trap Shrugs', 'muscle': 'Trapezius & Grip Strength', 'tip': 'Chest proud, shoulders back, smooth stride.'}
            ]
        }
    ],
}


@workouts_bp.route('/')
@login_required
def plan():
    level = current_user.fitness_level if current_user.fitness_level in PLANS else 'beginner'
    goal = current_user.goal if current_user.goal in REPS_BY_GOAL else 'maintaining'
    role = current_user.role if current_user.role in ROLE_WARMUPS else 'general'

    scheme = REPS_BY_GOAL[goal]
    days = PLANS[level]
    warmup = ROLE_WARMUPS[role]
    role_info = ROLE_DETAILS.get(role, ROLE_DETAILS['general'])

    # Parse requested date for workout tracking (defaults to today)
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

    # Get user's logged workout summary for this date (mirrors diet.html food_summary)
    workout_summary = current_user.get_daily_workout_summary(selected_date)

    # Query recent lift logs for legacy/chart view
    lifts = LiftLog.query.filter_by(user_id=current_user.id).order_by(LiftLog.logged_at.desc()).limit(20).all()
    latest_bench = LiftLog.query.filter_by(user_id=current_user.id).filter(LiftLog.exercise_name.ilike('%bench%')).order_by(LiftLog.logged_at.desc()).first()

    # Build a dict of { exercise_name_lower: last_WorkoutLog } for all scheduled exercises
    # so the template can show last weight and recommend next target
    all_exercise_names = []
    for day in days:
        for ex in day['exercises']:
            all_exercise_names.append(ex['name'])

    last_logged_weights = {}
    if all_exercise_names:
        for ex_name in all_exercise_names:
            last_log = (
                WorkoutLog.query
                .filter_by(user_id=current_user.id)
                .filter(WorkoutLog.exercise_name.ilike(f'%{ex_name[:15]}%'))
                .order_by(WorkoutLog.date.desc(), WorkoutLog.logged_at.desc())
                .first()
            )
            if last_log:
                last_logged_weights[ex_name] = {
                    'weight': last_log.weight,
                    'unit': last_log.unit,
                    'date': last_log.date.strftime('%d %b'),
                    'next_target': last_log.target_next_weight or WorkoutLog.calculate_next_target(last_log.weight, last_log.unit, ex_name)
                }

    return render_template(
        'workouts.html',
        level=level,
        goal=goal,
        role=role,
        role_info=role_info,
        days=days,
        sets=scheme['sets'],
        reps=scheme['reps'],
        rest=scheme['rest'],
        note=GOAL_NOTES[goal],
        warmup=warmup,
        lifts=lifts,
        latest_bench=latest_bench,
        workout_summary=workout_summary,
        workout_categories=WORKOUT_CATEGORIES,
        common_exercises=COMMON_EXERCISES,
        last_logged_weights=last_logged_weights,
        selected_date_str=selected_date.strftime('%Y-%m-%d'),
        prev_date_str=prev_date.strftime('%Y-%m-%d'),
        next_date_str=next_date.strftime('%Y-%m-%d'),
        is_today=is_today
    )


@workouts_bp.route('/log/add', methods=['POST'])
@login_required
def add_workout_log():
    """
    Log a workout / exercise entry (preset or custom), with sets, reps, weight,
    intensity, duration, and progressive overload calculations.
    """
    is_json = request.is_json
    data = request.get_json(silent=True) if is_json else request.form

    exercise_name = (data.get('exercise_name') or '').strip()
    custom_exercise = (data.get('custom_exercise') or '').strip()
    is_custom_flag = str(data.get('is_custom', '')).lower() in ('true', '1', 'yes')

    if (exercise_name.lower() == 'custom' or not exercise_name) and custom_exercise:
        exercise_name = custom_exercise
        is_custom_flag = True
    elif custom_exercise and not exercise_name:
        exercise_name = custom_exercise
        is_custom_flag = True

    category = (data.get('category') or 'custom').strip().lower()
    valid_categories = {'chest', 'back', 'legs', 'shoulders', 'arms', 'core', 'cardio', 'custom'}
    if category not in valid_categories:
        category = 'custom'

    # Date parsing
    date_str = data.get('date')
    target_date = date.today()
    if date_str:
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            target_date = date.today()

    try:
        sets = max(1, int(data.get('sets') or 3))
    except (ValueError, TypeError):
        sets = 3

    try:
        reps = max(1, int(data.get('reps') or 10))
    except (ValueError, TypeError):
        reps = 10

    try:
        weight = float(data.get('weight') or 0.0)
    except (ValueError, TypeError):
        weight = 0.0

    try:
        duration_mins = max(0, int(data.get('duration_mins') or 0))
    except (ValueError, TypeError):
        duration_mins = 0

    unit = (data.get('unit') or 'kg').strip().lower()
    if unit not in ('kg', 'lbs'):
        unit = 'kg'

    notes = (data.get('notes') or '').strip()

    if not exercise_name:
        if is_json:
            return jsonify({'error': 'Please provide an exercise or workout name.'}), 400
        flash('Please provide an exercise or workout name.', 'warning')
        return redirect(url_for('workouts.plan', date=target_date.strftime('%Y-%m-%d')))

    # Calculate progressive overload target
    target_next_weight = WorkoutLog.calculate_next_target(weight, unit, exercise_name) if weight > 0 else None

    # Estimate calories burned (~5 kcal per minute or ~7 kcal per heavy set)
    estimated_cals = round((duration_mins * 7.0) if duration_mins > 0 else (sets * 8.5), 1)

    new_log = WorkoutLog(
        user_id=current_user.id,
        date=target_date,
        category=category,
        exercise_name=exercise_name,
        sets=sets,
        reps=reps,
        weight=weight,
        unit=unit,
        duration_mins=duration_mins,
        calories_burned=estimated_cals,
        target_next_weight=target_next_weight,
        notes=notes,
        is_custom=is_custom_flag
    )
    db.session.add(new_log)

    # Sync with LiftLog if a positive weight was lifted so overall lift records update
    if weight > 0:
        lift_entry = LiftLog(
            user_id=current_user.id,
            exercise_name=exercise_name,
            weight=weight,
            unit=unit,
            reps=reps,
            target_next_weight=target_next_weight,
            notes=notes
        )
        db.session.add(lift_entry)

    db.session.commit()

    if is_json:
        summary = current_user.get_daily_workout_summary(target_date)
        return jsonify({
            'success': True,
            'message': f'Logged {exercise_name} ({sets} sets × {reps} reps @ {weight}{unit})!',
            'log_id': new_log.id,
            'summary': {
                'total_exercises': summary['total_exercises'],
                'total_sets': summary['total_sets'],
                'total_volume': summary['total_volume']
            }
        })

    flash(
        f"✓ Logged '{exercise_name}' ({sets} sets × {reps} reps" +
        (f" @ {weight}{unit}" if weight > 0 else "") +
        (f" • Next target: {target_next_weight}{unit} 🎯" if target_next_weight else "") + ")!",
        'success'
    )
    return redirect(url_for('workouts.plan', date=target_date.strftime('%Y-%m-%d')))


@workouts_bp.route('/log/delete/<int:log_id>', methods=['POST'])
@login_required
def delete_workout_log(log_id):
    """Delete a workout log entry."""
    entry = WorkoutLog.query.filter_by(id=log_id, user_id=current_user.id).first()
    if not entry:
        if request.is_json:
            return jsonify({'error': 'Workout log not found'}), 404
        flash('Workout entry not found.', 'warning')
        return redirect(url_for('workouts.plan'))

    log_date_str = entry.date.strftime('%Y-%m-%d')
    ex_name = entry.exercise_name
    db.session.delete(entry)
    db.session.commit()

    if request.is_json:
        summary = current_user.get_daily_workout_summary(log_date_str)
        return jsonify({
            'success': True,
            'message': f'Removed {ex_name}',
            'summary': {
                'total_exercises': summary['total_exercises'],
                'total_sets': summary['total_sets'],
                'total_volume': summary['total_volume']
            }
        })

    flash(f"Removed '{ex_name}' from your workout log.", 'info')
    return redirect(url_for('workouts.plan', date=log_date_str))


@workouts_bp.route('/log/quick-add', methods=['POST'])
@login_required
def quick_add_plan_exercise():
    """Quick-log an exercise directly from the scheduled split routine into the daily tracker."""
    exercise_name = (request.form.get('exercise_name') or '').strip()
    category = (request.form.get('category') or 'custom').strip().lower()
    date_str = request.form.get('date')

    target_date = date.today()
    if date_str:
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            target_date = date.today()

    if not exercise_name:
        flash('Exercise name missing.', 'warning')
        return redirect(url_for('workouts.plan', date=target_date.strftime('%Y-%m-%d')))

    try:
        sets = max(1, int(request.form.get('sets') or 3))
    except (ValueError, TypeError):
        sets = 3

    try:
        reps = max(1, int(request.form.get('reps') or 10))
    except (ValueError, TypeError):
        reps = 10

    try:
        weight = float(request.form.get('weight') or 0.0)
    except (ValueError, TypeError):
        weight = 0.0

    unit = (request.form.get('unit') or 'kg').strip().lower()
    target_next = WorkoutLog.calculate_next_target(weight, unit, exercise_name) if weight > 0 else None

    new_log = WorkoutLog(
        user_id=current_user.id,
        date=target_date,
        category=category,
        exercise_name=exercise_name,
        sets=sets,
        reps=reps,
        weight=weight,
        unit=unit,
        target_next_weight=target_next,
        notes='Quick logged from scheduled routine',
        is_custom=False
    )
    db.session.add(new_log)
    if weight > 0:
        db.session.add(LiftLog(
            user_id=current_user.id,
            exercise_name=exercise_name,
            weight=weight,
            unit=unit,
            reps=reps,
            target_next_weight=target_next,
            notes='Logged from workout tracker'
        ))
    db.session.commit()

    flash(f"Logged '{exercise_name}' to today's workout tracker!", 'success')
    return redirect(url_for('workouts.plan', date=target_date.strftime('%Y-%m-%d')))


@workouts_bp.route('/api/exercises', methods=['GET'])
@login_required
def api_exercises():
    """Live search and filter API for exercises."""
    q = request.args.get('q', '').strip()
    cat = request.args.get('category', 'all').strip()
    results = search_exercises(query=q, category=cat, limit=35)
    return jsonify({'exercises': results})


@workouts_bp.route('/lift/log', methods=['POST'])
@login_required
def log_lift():
    """Legacy lift logging endpoint, redirecting into new workflow."""
    exercise_name = request.form.get('exercise_name', '').strip()
    custom_exercise = request.form.get('custom_exercise', '').strip()
    if exercise_name == 'Custom' and custom_exercise:
        exercise_name = custom_exercise

    weight = request.form.get('weight', type=float)
    unit = request.form.get('unit', 'kg').strip().lower()
    if unit not in ('kg', 'lbs'):
        unit = 'kg'
    reps = request.form.get('reps', type=int) or 10
    notes = request.form.get('notes', '').strip()

    if not exercise_name:
        flash('Please select or specify an exercise name.', 'warning')
        return redirect(url_for('workouts.plan'))

    if weight is None or weight <= 0:
        flash('Please enter a valid weight lifted.', 'danger')
        return redirect(url_for('workouts.plan'))

    target_next = LiftLog.calculate_next_target(weight, unit, exercise_name)

    lift_entry = LiftLog(
        user_id=current_user.id,
        exercise_name=exercise_name,
        weight=weight,
        unit=unit,
        reps=reps,
        target_next_weight=target_next,
        notes=notes
    )
    db.session.add(lift_entry)

    # Also record in WorkoutLog
    name_lower = exercise_name.lower()
    cat = 'chest' if 'bench' in name_lower or 'press' in name_lower else (
        'back' if 'deadlift' in name_lower or 'row' in name_lower or 'lat' in name_lower else (
            'legs' if 'squat' in name_lower or 'leg' in name_lower else 'custom'
        )
    )
    workout_entry = WorkoutLog(
        user_id=current_user.id,
        date=date.today(),
        category=cat,
        exercise_name=exercise_name,
        sets=3,
        reps=reps,
        weight=weight,
        unit=unit,
        target_next_weight=target_next,
        notes=notes,
        is_custom=True
    )
    db.session.add(workout_entry)
    db.session.commit()

    flash(f"Logged {exercise_name} ({weight}{unit} × {reps})! Your next target is {target_next}{unit} 🎯", 'success')
    return redirect(url_for('workouts.plan'))


@workouts_bp.route('/lift/<int:lift_id>/delete', methods=['POST'])
@login_required
def delete_lift(lift_id):
    entry = LiftLog.query.get_or_404(lift_id)
    if entry.user_id != current_user.id:
        abort(403)
    db.session.delete(entry)
    db.session.commit()
    flash('Lift entry removed.', 'info')
    return redirect(url_for('workouts.plan'))


