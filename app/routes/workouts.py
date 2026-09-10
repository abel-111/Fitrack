from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.services.ai_coach import ROLE_DETAILS

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
            'title': 'Day 1 - Full Body A',
            'focus': 'Chest, Quads, Lats, Core',
            'exercises': [
                {'name': 'Barbell or Goblet Squat', 'muscle': 'Quads & Glutes', 'tip': 'Drive knees out and keep chest proud.'},
                {'name': 'Barbell or Dumbbell Bench Press', 'muscle': 'Chest & Triceps', 'tip': 'Tuck shoulder blades down and back.'},
                {'name': 'Bent-over Barbell Row', 'muscle': 'Upper Back & Lats', 'tip': 'Pull towards lower ribs with a flat spine.'},
                {'name': 'Plank', 'muscle': 'Core Stability', 'tip': 'Brace core as if expecting a punch; hold 45-60s.'}
            ]
        },
        {
            'title': 'Day 2 - Full Body B',
            'focus': 'Hamstrings, Shoulders, Back, Abs',
            'exercises': [
                {'name': 'Romanian Deadlift', 'muscle': 'Hamstrings & Glutes', 'tip': 'Hinge backwards at hips until hamstring stretch.'},
                {'name': 'Overhead Shoulder Press', 'muscle': 'Deltoids & Triceps', 'tip': 'Lock out elbows overhead without arching lower back.'},
                {'name': 'Lat Pulldown', 'muscle': 'Lats & Biceps', 'tip': 'Pull down to upper chest, pausing 1 second.'},
                {'name': 'Bicycle Crunches', 'muscle': 'Obliques & Rectus Abdominis', 'tip': 'Controlled tempo, opposite elbow to knee.'}
            ]
        },
        {
            'title': 'Day 3 - Full Body C',
            'focus': 'Legs, Upper Chest, Mid Back, Core',
            'exercises': [
                {'name': 'Leg Press or Lunges', 'muscle': 'Quads & Glutes', 'tip': 'Full range of motion without locking knees at top.'},
                {'name': 'Incline Dumbbell Press', 'muscle': 'Upper Chest', 'tip': 'Set bench to 30 degrees for clavicular head stimulation.'},
                {'name': 'Seated Cable Row', 'muscle': 'Mid Back & Rhomboids', 'tip': 'Squeeze shoulder blades together for a full second.'},
                {'name': 'Side Plank', 'muscle': 'Lateral Core', 'tip': 'Keep straight line from head to ankles; 30s per side.'}
            ]
        },
    ],
    'intermediate': [
        {
            'title': 'Day 1 - Upper Power',
            'focus': 'Chest, Lats, Shoulders, Arms',
            'exercises': [
                {'name': 'Barbell Bench Press', 'muscle': 'Chest & Triceps', 'tip': '3-second eccentric descent on heavy sets.'},
                {'name': 'Barbell Row', 'muscle': 'Lats & Upper Back', 'tip': 'Torso at 45 degrees, explosive pull.'},
                {'name': 'Standing Overhead Press', 'muscle': 'Anterior Delts', 'tip': 'Brace glutes and abs tight.'},
                {'name': 'Wide-Grip Lat Pulldown', 'muscle': 'Lats Width', 'tip': 'Lean back slightly and flare lats.'},
                {'name': 'Incline Dumbbell Bicep Curl', 'muscle': 'Biceps Long Head', 'tip': 'Full stretch at bottom, supinate wrists.'},
                {'name': 'Tricep Rope Pushdown', 'muscle': 'Triceps Lateral Head', 'tip': 'Spread the rope at the bottom.'}
            ]
        },
        {
            'title': 'Day 2 - Lower Strength',
            'focus': 'Quads, Hamstrings, Calves',
            'exercises': [
                {'name': 'Barbell Back Squat', 'muscle': 'Quads & Glutes', 'tip': 'Hit parallel or below with upright torso.'},
                {'name': 'Romanian Deadlift', 'muscle': 'Hamstrings & Glutes', 'tip': 'Shins remain vertical during hip hinge.'},
                {'name': 'Leg Press', 'muscle': 'Quads Hypertrophy', 'tip': 'Feet middle-width, deep controlled descent.'},
                {'name': 'Lying Leg Curl', 'muscle': 'Hamstrings Isolation', 'tip': 'Keep hips glued to pad.'},
                {'name': 'Standing Calf Raise', 'muscle': 'Gastrocnemius', 'tip': 'Hold bottom stretch for 2 full seconds.'}
            ]
        },
        {
            'title': 'Day 3 - Upper Hypertrophy',
            'focus': 'Pecs, Upper Back, Shoulders',
            'exercises': [
                {'name': 'Incline Dumbbell Bench Press', 'muscle': 'Upper Pecs', 'tip': 'Deep stretch at bottom, converge dumbbells at top.'},
                {'name': 'Bodyweight or Assisted Pull-up', 'muscle': 'Lats & Core', 'tip': 'Pull chest to bar with no swinging.'},
                {'name': 'Seated Dumbbell Arnold Press', 'muscle': 'Total Shoulder', 'tip': 'Smooth rotation throughout movement.'},
                {'name': 'Chest-Supported Row', 'muscle': 'Mid Traps & Rhomboids', 'tip': 'Eliminate lower back momentum.'},
                {'name': 'Hammer Curls', 'muscle': 'Brachialis & Forearms', 'tip': 'Thickens the upper arm and grip strength.'},
                {'name': 'Skull Crushers / EZ Bar Extension', 'muscle': 'Triceps Long Head', 'tip': 'Keep elbows tucked inward.'}
            ]
        },
        {
            'title': 'Day 4 - Lower Hypertrophy',
            'focus': 'Deadlifts, Quads, Hamstrings, Calves',
            'exercises': [
                {'name': 'Conventional or Trap Bar Deadlift', 'muscle': 'Posterior Chain', 'tip': 'Push the floor away through midfoot.'},
                {'name': 'Bulgarian Split Squat or Walking Lunges', 'muscle': 'Unilateral Quads/Glutes', 'tip': 'Lean forward slightly for glute bias.'},
                {'name': 'Seated Leg Extension', 'muscle': 'Quads Peak Contraction', 'tip': 'Pause 1 second at top lockout.'},
                {'name': 'Seated Leg Curl', 'muscle': 'Hamstrings', 'tip': 'High tension throughout range.'},
                {'name': 'Seated Calf Raise', 'muscle': 'Soleus', 'tip': 'Slow and rhythmic 15-20 reps.'}
            ]
        },
    ],
    'advanced': [
        {
            'title': 'Day 1 - Push Hypertrophy',
            'focus': 'Chest, Front Delts, Triceps',
            'exercises': [
                {'name': 'Flat Barbell Bench Press', 'muscle': 'Pectoralis Major', 'tip': 'Heavy working sets with 2 RIR.'},
                {'name': 'Incline Dumbbell Press', 'muscle': 'Clavicular Pecs', 'tip': 'Elbows at 45-degree angle.'},
                {'name': 'Standing Overhead Military Press', 'muscle': 'Anterior Deltoids', 'tip': 'Strict lockouts without knee bounce.'},
                {'name': 'Cable Lateral Raise', 'muscle': 'Lateral Deltoids', 'tip': 'Constant tension on the side delts.'},
                {'name': 'Weighted Tricep Dips', 'muscle': 'Lower Pecs & Triceps', 'tip': 'Slow descent, drive through palms.'}
            ]
        },
        {
            'title': 'Day 2 - Pull Hypertrophy',
            'focus': 'Back Thickness, Lats, Biceps',
            'exercises': [
                {'name': 'Conventional Deadlift', 'muscle': 'Total Posterior Chain', 'tip': 'Reset after each repetition.'},
                {'name': 'Weighted Pull-ups', 'muscle': 'Lats & Biceps', 'tip': 'Full dead-hang at bottom.'},
                {'name': 'Meadows Row or T-Bar Row', 'muscle': 'Lats & Rhomboids', 'tip': 'Drive elbow back towards hip.'},
                {'name': 'Cable Face Pull with External Rotation', 'muscle': 'Rear Delts & Rotator Cuff', 'tip': 'Pull towards temples.'},
                {'name': 'Barbell Bicep Curl', 'muscle': 'Biceps Brachii', 'tip': 'Strict posture, zero hip swing.'}
            ]
        },
        {
            'title': 'Day 3 - Legs & Abs',
            'focus': 'Quads, Hamstrings, Glutes, Calves',
            'exercises': [
                {'name': 'Barbell Back Squat', 'muscle': 'Quads & Glutes', 'tip': 'Deep controlled depth.'},
                {'name': 'Romanian Deadlift', 'muscle': 'Hamstrings', 'tip': 'Keep bar glued to thighs.'},
                {'name': 'Hack Squat or Leg Press', 'muscle': 'Quad Tear-drop', 'tip': 'Foot placement low on platform.'},
                {'name': 'Lying Leg Curl', 'muscle': 'Hamstring Flexion', 'tip': 'Toes pointed down to reduce calf contribution.'},
                {'name': 'Hanging Leg Raises', 'muscle': 'Lower Abs & Hip Flexors', 'tip': 'Curl pelvis upward, don\'t just swing legs.'}
            ]
        },
        {
            'title': 'Day 4 - Push Strength & Weak Points',
            'focus': 'Incline Chest, Shoulders, Arms',
            'exercises': [
                {'name': 'Incline Barbell Bench Press', 'muscle': 'Upper Chest', 'tip': 'Touch collarbone area gently.'},
                {'name': 'Dumbbell Arnold Press', 'muscle': 'Shoulders', 'tip': 'Controlled 3s lowering phase.'},
                {'name': 'Cable Chest Fly', 'muscle': 'Inner Pec Squeeze', 'tip': 'Focus on peak contraction.'},
                {'name': 'Overhead EZ-Bar Tricep Extension', 'muscle': 'Tricep Long Head', 'tip': 'Elbows pointed forward.'}
            ]
        },
        {
            'title': 'Day 5 - Pull & Upper Back',
            'focus': 'Upper Back, Traps, Forearms',
            'exercises': [
                {'name': 'Rack Pulls below Knee', 'muscle': 'Erectors & Upper Traps', 'tip': 'Heavy lockouts.'},
                {'name': 'Seated Cable Row with V-Grip', 'muscle': 'Mid Back', 'tip': 'Squeeze back hard at torso.'},
                {'name': 'Incline Dumbbell Hammer Curl', 'muscle': 'Brachialis', 'tip': 'Controlled negative.'},
                {'name': 'Dumbbell Shrugs with 2s hold', 'muscle': 'Upper Trapezius', 'tip': 'Straight up and down, no rolling.'}
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
        warmup=warmup
    )

