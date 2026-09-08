from flask import Blueprint, render_template
from flask_login import login_required, current_user

workouts_bp = Blueprint('workouts', __name__, url_prefix='/workouts')

REPS_BY_GOAL = {
    'cutting': {'sets': 3, 'reps': '12-15'},
    'maintaining': {'sets': 3, 'reps': '8-12'},
    'bulking': {'sets': 4, 'reps': '6-10'},
}

GOAL_NOTES = {
    'cutting': 'Keep rest periods short (45-60s) and finish each session with 15 minutes of incline walking or cycling.',
    'maintaining': 'Standard rest periods (60-90s). Focus on clean form and consistent effort session to session.',
    'bulking': 'Rest 90-120s between sets. Once you hit the top of the rep range for all sets, add 2.5-5kg next session.',
}

PLANS = {
    'beginner': [
        {'title': 'Day 1 - Full Body A', 'exercises': ['Squat', 'Bench Press', 'Bent-over Row', 'Plank']},
        {'title': 'Day 2 - Full Body B', 'exercises': ['Deadlift', 'Overhead Press', 'Lat Pulldown', 'Bicycle Crunches']},
        {'title': 'Day 3 - Full Body C', 'exercises': ['Leg Press', 'Incline Dumbbell Press', 'Seated Cable Row', 'Side Plank']},
    ],
    'intermediate': [
        {'title': 'Day 1 - Upper', 'exercises': ['Bench Press', 'Barbell Row', 'Overhead Press', 'Lat Pulldown', 'Bicep Curl', 'Tricep Pushdown']},
        {'title': 'Day 2 - Lower', 'exercises': ['Squat', 'Romanian Deadlift', 'Leg Press', 'Leg Curl', 'Calf Raise']},
        {'title': 'Day 3 - Upper', 'exercises': ['Incline Bench Press', 'Pull-up', 'Dumbbell Shoulder Press', 'Seated Cable Row', 'Hammer Curl', 'Skull Crusher']},
        {'title': 'Day 4 - Lower', 'exercises': ['Deadlift', 'Front Squat', 'Walking Lunge', 'Leg Extension', 'Standing Calf Raise']},
    ],
    'advanced': [
        {'title': 'Day 1 - Push', 'exercises': ['Bench Press', 'Overhead Press', 'Incline Dumbbell Press', 'Lateral Raise', 'Tricep Dips']},
        {'title': 'Day 2 - Pull', 'exercises': ['Deadlift', 'Pull-up', 'Barbell Row', 'Face Pull', 'Bicep Curl']},
        {'title': 'Day 3 - Legs', 'exercises': ['Squat', 'Leg Press', 'Romanian Deadlift', 'Leg Curl', 'Calf Raise']},
        {'title': 'Day 4 - Push', 'exercises': ['Incline Bench Press', 'Arnold Press', 'Cable Fly', 'Overhead Tricep Extension']},
        {'title': 'Day 5 - Pull', 'exercises': ['Rack Pull', 'T-Bar Row', 'Lat Pulldown', 'Hammer Curl']},
    ],
}


@workouts_bp.route('/')
@login_required
def plan():
    level = current_user.fitness_level if current_user.fitness_level in PLANS else 'beginner'
    goal = current_user.goal if current_user.goal in REPS_BY_GOAL else 'maintaining'

    scheme = REPS_BY_GOAL[goal]
    days = PLANS[level]

    return render_template(
        'workouts.html',
        level=level,
        goal=goal,
        days=days,
        sets=scheme['sets'],
        reps=scheme['reps'],
        note=GOAL_NOTES[goal],
    )
