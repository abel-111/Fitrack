"""
Workout & Exercise Database for Fitrack.
Provides comprehensive preset resistance and cardio exercises categorized by muscle groups,
with recommended starting sets, reps, weight guides, and muscle targets.
"""

COMMON_EXERCISES = [
    # --- CHEST & TRICEPS ---
    {
        'id': 'barbell_bench_press',
        'name': 'Barbell Bench Press',
        'category': 'chest',
        'category_label': 'Chest & Triceps',
        'muscle': 'Pectoralis Major, Anterior Deltoid, Triceps',
        'default_sets': 3,
        'default_reps': 10,
        'default_weight': 50.0,
        'unit': 'kg',
        'is_compound': True,
        'icon': '🏋️',
        'tip': 'Retract scapulae, touch lower sternum with control, and press up firmly.',
        'tags': ['chest', 'bench', 'push', 'compound', 'barbell', 'upper body']
    },
    {
        'id': 'incline_dumbbell_press',
        'name': 'Incline Dumbbell Press',
        'category': 'chest',
        'category_label': 'Chest & Triceps',
        'muscle': 'Clavicular Pecs (Upper Chest), Triceps',
        'default_sets': 3,
        'default_reps': 12,
        'default_weight': 20.0,
        'unit': 'kg',
        'is_compound': True,
        'icon': '📐',
        'tip': 'Set bench to 30 degrees for optimum clavicular upper-chest engagement.',
        'tags': ['chest', 'incline', 'dumbbell', 'upper chest', 'push']
    },
    {
        'id': 'chest_dips',
        'name': 'Chest Dips (Parallel Bars)',
        'category': 'chest',
        'category_label': 'Chest & Triceps',
        'muscle': 'Lower Pecs, Triceps, Anterior Delts',
        'default_sets': 3,
        'default_reps': 10,
        'default_weight': 0.0,
        'unit': 'kg',
        'is_compound': True,
        'icon': '🤸',
        'tip': 'Lean forward 30 degrees and flare elbows slightly to hit the chest.',
        'tags': ['chest', 'dips', 'calisthenics', 'bodyweight', 'lower chest']
    },
    {
        'id': 'cable_chest_fly',
        'name': 'Cable Chest Fly',
        'category': 'chest',
        'category_label': 'Chest & Triceps',
        'muscle': 'Pectoralis Major (Squeeze & Stretch)',
        'default_sets': 3,
        'default_reps': 15,
        'default_weight': 15.0,
        'unit': 'kg',
        'is_compound': False,
        'icon': '🦅',
        'tip': 'Keep a slight bend in elbows and focus on bringing biceps together.',
        'tags': ['chest', 'cable', 'fly', 'isolation', 'pump']
    },
    {
        'id': 'push_ups',
        'name': 'Standard Push-Ups',
        'category': 'chest',
        'category_label': 'Chest & Triceps',
        'muscle': 'Chest, Core, Triceps',
        'default_sets': 3,
        'default_reps': 20,
        'default_weight': 0.0,
        'unit': 'kg',
        'is_compound': True,
        'icon': '🔥',
        'tip': 'Maintain a rigid high plank with glutes squeezed throughout the descent.',
        'tags': ['chest', 'pushups', 'bodyweight', 'calisthenics']
    },

    # --- BACK & BICEPS ---
    {
        'id': 'conventional_deadlift',
        'name': 'Conventional Deadlift',
        'category': 'back',
        'category_label': 'Back & Biceps',
        'muscle': 'Erector Spinae, Lats, Glutes, Hamstrings',
        'default_sets': 4,
        'default_reps': 6,
        'default_weight': 70.0,
        'unit': 'kg',
        'is_compound': True,
        'icon': '⚡',
        'tip': 'Pull slack out of bar, brace abdomen, and push floor away with midfoot.',
        'tags': ['back', 'deadlift', 'posterior chain', 'heavy', 'compound']
    },
    {
        'id': 'barbell_bent_row',
        'name': 'Bent-over Barbell Row',
        'category': 'back',
        'category_label': 'Back & Biceps',
        'muscle': 'Rhomboids, Middle Traps, Lats',
        'default_sets': 3,
        'default_reps': 10,
        'default_weight': 40.0,
        'unit': 'kg',
        'is_compound': True,
        'icon': '🚣',
        'tip': 'Hinge at hips, keep flat spine, and pull bar toward navel.',
        'tags': ['back', 'row', 'barbell', 'thickness', 'compound']
    },
    {
        'id': 'lat_pulldown',
        'name': 'Lat Pulldown',
        'category': 'back',
        'category_label': 'Back & Biceps',
        'muscle': 'Latissimus Dorsi, Biceps, Teres Major',
        'default_sets': 3,
        'default_reps': 12,
        'default_weight': 45.0,
        'unit': 'kg',
        'is_compound': True,
        'icon': '🧗',
        'tip': 'Pull bar down to upper sternum while depressing shoulder blades.',
        'tags': ['back', 'lats', 'width', 'pulldown', 'cable']
    },
    {
        'id': 'pull_ups',
        'name': 'Bodyweight Pull-ups',
        'category': 'back',
        'category_label': 'Back & Biceps',
        'muscle': 'Lats, Upper Back, Brachialis',
        'default_sets': 3,
        'default_reps': 8,
        'default_weight': 0.0,
        'unit': 'kg',
        'is_compound': True,
        'icon': '💪',
        'tip': 'Full hang at bottom; drive elbows into back pockets on the way up.',
        'tags': ['back', 'pullup', 'bodyweight', 'calisthenics', 'lats']
    },
    {
        'id': 'seated_cable_row',
        'name': 'Seated Cable Row (Close-Grip)',
        'category': 'back',
        'category_label': 'Back & Biceps',
        'muscle': 'Mid Traps, Rhomboids, Lats',
        'default_sets': 3,
        'default_reps': 12,
        'default_weight': 40.0,
        'unit': 'kg',
        'is_compound': True,
        'icon': '🎯',
        'tip': 'Avoid excessive torso swinging; squeeze shoulder blades together for 1 sec.',
        'tags': ['back', 'cable', 'row', 'mid back', 'posture']
    },

    # --- LEGS & GLUTES ---
    {
        'id': 'barbell_back_squat',
        'name': 'Barbell Back Squat',
        'category': 'legs',
        'category_label': 'Legs & Glutes',
        'muscle': 'Quadriceps, Gluteus Maximus, Adductors',
        'default_sets': 4,
        'default_reps': 8,
        'default_weight': 60.0,
        'unit': 'kg',
        'is_compound': True,
        'icon': '🦵',
        'tip': 'Drive knees in line with toes, maintain neutral spine, reach parallel.',
        'tags': ['legs', 'squat', 'quads', 'glutes', 'compound', 'barbell']
    },
    {
        'id': 'romanian_deadlift',
        'name': 'Romanian Deadlift (RDL)',
        'category': 'legs',
        'category_label': 'Legs & Glutes',
        'muscle': 'Hamstrings, Glutes, Lower Back',
        'default_sets': 3,
        'default_reps': 10,
        'default_weight': 50.0,
        'unit': 'kg',
        'is_compound': True,
        'icon': '🍑',
        'tip': 'Send hips straight back with soft knees until deep hamstring stretch.',
        'tags': ['legs', 'rdl', 'hamstrings', 'glutes', 'hinge']
    },
    {
        'id': 'leg_press',
        'name': '45-Degree Leg Press',
        'category': 'legs',
        'category_label': 'Legs & Glutes',
        'muscle': 'Quadriceps & Glute Drive',
        'default_sets': 3,
        'default_reps': 12,
        'default_weight': 100.0,
        'unit': 'kg',
        'is_compound': True,
        'icon': '⚙️',
        'tip': 'Do not lock out knees at top; keep lower back firmly pressed into seat pad.',
        'tags': ['legs', 'press', 'quads', 'machine', 'heavy']
    },
    {
        'id': 'bulgarian_split_squat',
        'name': 'Bulgarian Split Squat',
        'category': 'legs',
        'category_label': 'Legs & Glutes',
        'muscle': 'Single-Leg Quads & Glute Medius',
        'default_sets': 3,
        'default_reps': 10,
        'default_weight': 14.0,
        'unit': 'kg',
        'is_compound': True,
        'icon': '🔥',
        'tip': 'Rear foot elevated on bench; descend straight down with upright or 10° torso.',
        'tags': ['legs', 'unilateral', 'glutes', 'quads', 'dumbbell']
    },
    {
        'id': 'lying_leg_curl',
        'name': 'Lying Hamstring Leg Curl',
        'category': 'legs',
        'category_label': 'Legs & Glutes',
        'muscle': 'Hamstrings Bicep Femoris',
        'default_sets': 3,
        'default_reps': 12,
        'default_weight': 35.0,
        'unit': 'kg',
        'is_compound': False,
        'icon': '🌀',
        'tip': 'Point toes slightly downward to keep tension exclusively on hamstrings.',
        'tags': ['legs', 'hamstrings', 'isolation', 'machine']
    },
    {
        'id': 'standing_calf_raise',
        'name': 'Standing Calf Raise',
        'category': 'legs',
        'category_label': 'Legs & Glutes',
        'muscle': 'Gastrocnemius & Soleus',
        'default_sets': 4,
        'default_reps': 15,
        'default_weight': 40.0,
        'unit': 'kg',
        'is_compound': False,
        'icon': '🦶',
        'tip': 'Hold full bottom stretch for 2 seconds to eliminate Achilles tendon bounce.',
        'tags': ['legs', 'calves', 'isolation']
    },

    # --- SHOULDERS & TRAPS ---
    {
        'id': 'overhead_military_press',
        'name': 'Overhead Shoulder Press (OHP)',
        'category': 'shoulders',
        'category_label': 'Shoulders & Traps',
        'muscle': 'Anterior Delts, Lateral Delts, Triceps, Upper Traps',
        'default_sets': 3,
        'default_reps': 8,
        'default_weight': 35.0,
        'unit': 'kg',
        'is_compound': True,
        'icon': '🥥',
        'tip': 'Squeeze glutes and abs tightly to avoid hyper-extending the lumbar spine.',
        'tags': ['shoulders', 'ohp', 'military press', 'compound', 'delts']
    },
    {
        'id': 'dumbbell_lateral_raise',
        'name': 'Dumbbell Lateral Raise',
        'category': 'shoulders',
        'category_label': 'Shoulders & Traps',
        'muscle': 'Lateral Deltoids (Shoulder Width)',
        'default_sets': 4,
        'default_reps': 15,
        'default_weight': 8.0,
        'unit': 'kg',
        'is_compound': False,
        'icon': '🕊️',
        'tip': 'Pour the pitcher: lead with elbows and raise to parallel without shrugging.',
        'tags': ['shoulders', 'side delts', 'lateral', 'width', 'dumbbell']
    },
    {
        'id': 'cable_face_pull',
        'name': 'Cable Face Pull with External Rotation',
        'category': 'shoulders',
        'category_label': 'Shoulders & Traps',
        'muscle': 'Rear Delts, Infraspinatus, Traps',
        'default_sets': 3,
        'default_reps': 15,
        'default_weight': 20.0,
        'unit': 'kg',
        'is_compound': False,
        'icon': '🛡️',
        'tip': 'Pull rope toward temples while externally rotating fists backward.',
        'tags': ['shoulders', 'rear delts', 'rotator cuff', 'posture', 'cable']
    },
    {
        'id': 'dumbbell_shrugs',
        'name': 'Dumbbell Shrugs',
        'category': 'shoulders',
        'category_label': 'Shoulders & Traps',
        'muscle': 'Upper Trapezius',
        'default_sets': 3,
        'default_reps': 12,
        'default_weight': 24.0,
        'unit': 'kg',
        'is_compound': False,
        'icon': '⛰️',
        'tip': 'Elevate straight up toward ears; pause 2 seconds at the top contraction.',
        'tags': ['shoulders', 'traps', 'shrugs', 'neck']
    },

    # --- ARMS & FOREARMS ---
    {
        'id': 'barbell_bicep_curl',
        'name': 'Barbell / EZ-Bar Bicep Curl',
        'category': 'arms',
        'category_label': 'Arms & Forearms',
        'muscle': 'Biceps Brachii (Long & Short Heads)',
        'default_sets': 3,
        'default_reps': 10,
        'default_weight': 25.0,
        'unit': 'kg',
        'is_compound': False,
        'icon': '💪',
        'tip': 'Keep elbows pinned to your ribs and avoid swinging with lower back.',
        'tags': ['arms', 'biceps', 'curl', 'barbell', 'ez bar']
    },
    {
        'id': 'dumbbell_hammer_curl',
        'name': 'Dumbbell Hammer Curl',
        'category': 'arms',
        'category_label': 'Arms & Forearms',
        'muscle': 'Brachialis & Brachioradialis (Arm Thickness)',
        'default_sets': 3,
        'default_reps': 12,
        'default_weight': 12.0,
        'unit': 'kg',
        'is_compound': False,
        'icon': '🔨',
        'tip': 'Neutral palms-in grip thickens upper arm and strengthens grip/forearms.',
        'tags': ['arms', 'hammer curl', 'biceps', 'forearms', 'dumbbell']
    },
    {
        'id': 'tricep_rope_pushdown',
        'name': 'Tricep Cable Rope Pushdown',
        'category': 'arms',
        'category_label': 'Arms & Forearms',
        'muscle': 'Triceps Lateral & Medial Heads',
        'default_sets': 3,
        'default_reps': 12,
        'default_weight': 25.0,
        'unit': 'kg',
        'is_compound': False,
        'icon': '⚡',
        'tip': 'Spread the rope outwards at the bottom and lock out triceps hard.',
        'tags': ['arms', 'triceps', 'pushdown', 'cable', 'horseshoe']
    },
    {
        'id': 'skull_crushers',
        'name': 'Skull Crushers / EZ-Bar Lying Extension',
        'category': 'arms',
        'category_label': 'Arms & Forearms',
        'muscle': 'Triceps Long Head',
        'default_sets': 3,
        'default_reps': 10,
        'default_weight': 20.0,
        'unit': 'kg',
        'is_compound': False,
        'icon': '💀',
        'tip': 'Angle upper arms back slightly (10-15°) to keep constant tension on long head.',
        'tags': ['arms', 'triceps', 'skull crusher', 'extension']
    },

    # --- CORE & ABS ---
    {
        'id': 'hanging_leg_raise',
        'name': 'Hanging Leg / Knee Raises',
        'category': 'core',
        'category_label': 'Core & Abs',
        'muscle': 'Lower Rectus Abdominis, Hip Flexors',
        'default_sets': 3,
        'default_reps': 12,
        'default_weight': 0.0,
        'unit': 'kg',
        'is_compound': True,
        'icon': '🧘',
        'tip': 'Tilt the pelvis up toward your chest instead of just swinging your thighs.',
        'tags': ['core', 'abs', 'hanging', 'bodyweight', 'lower abs']
    },
    {
        'id': 'plank_hold',
        'name': 'Isometric Core Plank Hold',
        'category': 'core',
        'category_label': 'Core & Abs',
        'muscle': 'Transverse Abdominis, Core Stabilizers',
        'default_sets': 3,
        'default_reps': 60,
        'default_weight': 0.0,
        'unit': 's',
        'is_compound': False,
        'icon': '🧱',
        'tip': 'Brace core as if taking a punch; pull elbows towards toes isometrically.',
        'tags': ['core', 'plank', 'stability', 'bodyweight']
    },
    {
        'id': 'ab_wheel_rollout',
        'name': 'Ab Wheel Rollout',
        'category': 'core',
        'category_label': 'Core & Abs',
        'muscle': 'Full Abdominal Wall & Lats',
        'default_sets': 3,
        'default_reps': 10,
        'default_weight': 0.0,
        'unit': 'kg',
        'is_compound': True,
        'icon': '🎡',
        'tip': 'Keep posterior pelvic tilt; never let lower back sag into extension.',
        'tags': ['core', 'ab wheel', 'advanced abs']
    },

    # --- CARDIO & CONDITIONING ---
    {
        'id': 'treadmill_incline_walk',
        'name': 'Treadmill Incline Fat-Burn Walk',
        'category': 'cardio',
        'category_label': 'Cardio & Conditioning',
        'muscle': 'Calves, Glutes, Cardiovascular Health',
        'default_sets': 1,
        'default_reps': 20,
        'default_weight': 0.0,
        'unit': 'mins',
        'is_compound': False,
        'icon': '🏃',
        'tip': '12-15% incline at 4.5-5.5 km/h without holding onto side handles.',
        'tags': ['cardio', 'treadmill', 'walking', 'fat burn', 'zone 2']
    },
    {
        'id': 'hiit_sprints',
        'name': 'HIIT Interval Sprints / Bike',
        'category': 'cardio',
        'category_label': 'Cardio & Conditioning',
        'muscle': 'Anaerobic Capacity & Leg Power',
        'default_sets': 8,
        'default_reps': 30,
        'default_weight': 0.0,
        'unit': 's',
        'is_compound': True,
        'icon': '⚡',
        'tip': '20s maximum all-out effort sprint followed by 40s active recovery.',
        'tags': ['cardio', 'hiit', 'sprints', 'conditioning']
    },
    {
        'id': 'rowing_machine',
        'name': 'Indoor Rowing Ergometer',
        'category': 'cardio',
        'category_label': 'Cardio & Conditioning',
        'muscle': 'Full Body (Legs, Back, Core, Cardio)',
        'default_sets': 1,
        'default_reps': 15,
        'default_weight': 0.0,
        'unit': 'mins',
        'is_compound': True,
        'icon': '🚣',
        'tip': 'Drive through legs (60%), swing with hips (20%), pull with arms (20%).',
        'tags': ['cardio', 'rowing', 'full body', 'conditioning']
    },
    {
        'id': 'jump_rope',
        'name': 'Jump Rope / Skipping',
        'category': 'cardio',
        'category_label': 'Cardio & Conditioning',
        'muscle': 'Calves, Foot Arches, Agility, Shoulders',
        'default_sets': 4,
        'default_reps': 2,
        'default_weight': 0.0,
        'unit': 'mins',
        'is_compound': False,
        'icon': '🪢',
        'tip': 'Stay light on the balls of your feet with wrists rotating smoothly.',
        'tags': ['cardio', 'skipping', 'agility', 'boxing']
    }
]

WORKOUT_CATEGORIES = [
    ('all', '🌟 All Exercises'),
    ('chest', '🏋️ Chest & Triceps'),
    ('back', '🚣 Back & Biceps'),
    ('legs', '🦵 Legs & Glutes'),
    ('shoulders', '🥥 Shoulders & Traps'),
    ('arms', '💪 Arms & Forearms'),
    ('core', '🧘 Core & Abs'),
    ('cardio', '🏃 Cardio & Conditioning'),
    ('custom', '⚡ Custom & Functional'),
]


def search_exercises(query='', category=None, limit=35):
    """
    Search exercises by keyword in name, category, muscle, or tags.
    Optionally filter by category.
    """
    q = (query or '').strip().lower()
    results = []

    for ex in COMMON_EXERCISES:
        if category and category != 'all' and ex.get('category') != category:
            continue

        if not q:
            results.append(ex)
        else:
            name_match = q in ex['name'].lower()
            muscle_match = q in ex.get('muscle', '').lower()
            tag_match = any(q in tag for tag in ex.get('tags', []))
            cat_match = q in ex.get('category', '').lower()

            if name_match or muscle_match or tag_match or cat_match:
                results.append(ex)

        if len(results) >= limit:
            break

    return results


def get_exercise_by_id(exercise_id):
    """Retrieve exercise dictionary by id."""
    for ex in COMMON_EXERCISES:
        if ex['id'] == exercise_id:
            return ex
    return None
