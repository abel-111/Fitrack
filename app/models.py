from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    height_cm = db.Column(db.Float)
    weight_kg = db.Column(db.Float)
    target_weight_kg = db.Column(db.Float)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))

    fitness_level = db.Column(db.String(20), default='beginner')   # beginner / intermediate / advanced
    goal = db.Column(db.String(20), default='maintaining')          # cutting / bulking / maintaining
    role = db.Column(db.String(50), default='general')              # desk_worker / student / athlete / bodybuilder / busy_parent / general
    dietary_preference = db.Column(db.String(30), default='standard') # standard / vegetarian / vegan / keto / high_protein
    activity_level = db.Column(db.String(30), default='moderate')  # sedentary / light / moderate / very_active
    state = db.Column(db.String(50), default='Tamil Nadu')
    cuisine_preference = db.Column(db.String(50), default='home_state')  # home_state / other_states / continental / fusion

    profile_picture = db.Column(db.String(200), default='default.png')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    is_coach = db.Column(db.Boolean, default=False)
    coach_approved = db.Column(db.Boolean, default=False)  # Admin must approve coaches
    coach_bio = db.Column(db.String(300), default='Certified Fitness & Nutrition Specialist')
    coach_specialty = db.Column(db.String(100), default='General Fitness, Strength & Nutrition')

    is_admin = db.Column(db.Boolean, default=False)

    attendances = db.relationship('Attendance', backref='user', lazy=True)
    weight_logs = db.relationship('WeightLog', backref='user', lazy=True)
    lift_logs = db.relationship('LiftLog', backref='user', lazy=True, order_by='desc(LiftLog.logged_at)')
    preferred_days = db.relationship('PreferredDay', backref='user', lazy=True)
    diet_plans = db.relationship('UserDietPlan', backref='user', lazy=True, order_by='desc(UserDietPlan.created_at)')
    food_logs = db.relationship('FoodLog', backref='user', lazy=True, order_by='desc(FoodLog.logged_at)')
    workout_logs = db.relationship('WorkoutLog', backref='user', lazy=True, order_by='desc(WorkoutLog.logged_at)')
    client_messages = db.relationship('CoachMessage', foreign_keys='CoachMessage.client_id', backref='client_user', lazy=True)
    coach_messages = db.relationship('CoachMessage', foreign_keys='CoachMessage.coach_id', backref='coach_user', lazy=True)

    ROLE_LABELS = {
        'desk_worker': '💼 Desk Worker',
        'student': '🎓 Student',
        'athlete': '🏃 Athlete',
        'bodybuilder': '🏋️ Bodybuilder',
        'busy_parent': '👨‍👩‍👧 Busy Parent / Pro',
        'general': '🧘 General Fitness',
    }

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_role_display(self):
        return self.ROLE_LABELS.get(self.role, '🧘 General Fitness')

    def calculate_bmi(self):
        """Calculate BMI if height and weight exist."""
        weight = self.weight_kg
        if not weight and self.weight_logs:
            weight = self.weight_logs[-1].weight_kg
        if not weight or not self.height_cm or self.height_cm <= 0:
            return None, 'Unknown'
        h_m = self.height_cm / 100.0
        bmi = round(weight / (h_m * h_m), 1)
        if bmi < 18.5:
            cat = 'Underweight'
        elif bmi < 25.0:
            cat = 'Healthy weight'
        elif bmi < 30.0:
            cat = 'Overweight'
        else:
            cat = 'Obese'
        return bmi, cat

    def calculate_bmr(self):
        """Mifflin-St Jeor formula for BMR."""
        weight = self.weight_kg or 70.0
        height = self.height_cm or 175.0
        age = self.age or 25
        gender = (self.gender or 'male').lower()
        if gender == 'female':
            bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
        else:
            bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
        return round(bmr)

    def calculate_tdee(self):
        """Total Daily Energy Expenditure based on activity level & role."""
        bmr = self.calculate_bmr()
        multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'very_active': 1.725
        }
        # adjust activity factor if role implies sedentary desk or intense athlete
        activity = self.activity_level or 'moderate'
        if self.role == 'desk_worker' and activity == 'moderate':
            factor = 1.35
        elif self.role == 'athlete' and activity in ('moderate', 'light'):
            factor = 1.7
        else:
            factor = multipliers.get(activity, 1.45)
        return round(bmr * factor)

    def get_calorie_target(self):
        tdee = self.calculate_tdee()
        goal = self.goal or 'maintaining'
        if goal == 'cutting':
            return max(1300, round(tdee - 450))
        elif goal == 'bulking':
            return round(tdee + 350)
        return tdee

    def get_target_macros(self):
        """Return dict of calories, protein (g), carbs (g), fat (g)."""
        calories = self.get_calorie_target()
        weight = self.weight_kg or 70.0
        goal = self.goal or 'maintaining'

        if goal == 'cutting':
            protein_g = round(weight * 2.2)
            fat_cals = calories * 0.25
            fat_g = round(fat_cals / 9)
            carb_cals = max(0, calories - (protein_g * 4) - (fat_g * 9))
            carb_g = round(carb_cals / 4)
        elif goal == 'bulking':
            protein_g = round(weight * 2.0)
            fat_cals = calories * 0.25
            fat_g = round(fat_cals / 9)
            carb_cals = max(0, calories - (protein_g * 4) - (fat_g * 9))
            carb_g = round(carb_cals / 4)
        else:
            protein_g = round(weight * 1.8)
            fat_cals = calories * 0.28
            fat_g = round(fat_cals / 9)
            carb_cals = max(0, calories - (protein_g * 4) - (fat_g * 9))
            carb_g = round(carb_cals / 4)

        return {
            'calories': calories,
            'protein': protein_g,
            'carbs': carb_g,
            'fat': fat_g
        }

    def _checkin_dates(self):
        """All distinct check-in dates, newest first."""
        return sorted({a.date for a in self.attendances}, reverse=True)

    def has_checked_in_today(self):
        return date.today() in {a.date for a in self.attendances}

    def get_current_streak(self):
        dates = self._checkin_dates()
        if not dates:
            return 0

        today = date.today()
        # streak is "alive" only if last check-in was today or yesterday
        if dates[0] not in (today, today - timedelta(days=1)):
            return 0

        streak = 1
        expected = dates[0] - timedelta(days=1)
        for d in dates[1:]:
            if d == expected:
                streak += 1
                expected -= timedelta(days=1)
            elif d < expected:
                break
        return streak

    def get_longest_streak(self):
        dates = sorted({a.date for a in self.attendances})
        if not dates:
            return 0

        longest = current = 1
        for prev, curr in zip(dates, dates[1:]):
            if curr == prev + timedelta(days=1):
                current += 1
            else:
                current = 1
            longest = max(longest, current)
        return longest

    def get_month_checkin_count(self):
        today = date.today()
        return sum(
            1 for a in self.attendances
            if a.date.year == today.year and a.date.month == today.month
        )
    DAY_ORDER = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    def get_preferred_days_sorted(self):
        days = {pd.day_of_week for pd in self.preferred_days}
        return [d for d in self.DAY_ORDER if d in days]

    def get_daily_food_summary(self, target_date=None):
        """
        Calculates total calories, protein, carbs, fat consumed on target_date (default today),
        and compares with user's targets. Returns grouped logs by meal type.
        """
        if target_date is None:
            target_date = date.today()
        elif isinstance(target_date, str):
            try:
                target_date = datetime.strptime(target_date, '%Y-%m-%d').date()
            except ValueError:
                target_date = date.today()

        logs = FoodLog.query.filter_by(user_id=self.id, date=target_date).order_by(FoodLog.logged_at.asc()).all()

        total_cals = sum(l.calories for l in logs)
        total_protein = sum(l.protein for l in logs)
        total_carbs = sum(l.carbs for l in logs)
        total_fat = sum(l.fat for l in logs)

        targets = self.get_target_macros()
        cals_target = targets.get('calories', 2000)
        protein_target = targets.get('protein', 130)

        cals_pct = min(100, round((total_cals / cals_target * 100))) if cals_target > 0 else 0
        protein_pct = min(100, round((total_protein / protein_target * 100))) if protein_target > 0 else 0

        rem_cals = max(0, round(cals_target - total_cals))
        rem_protein = max(0.0, round(protein_target - total_protein, 1))

        meals = {
            'breakfast': {'key': 'breakfast', 'label': 'Breakfast', 'icon': '🌅', 'food_items': [], 'calories': 0.0, 'protein': 0.0},
            'lunch': {'key': 'lunch', 'label': 'Lunch', 'icon': '☀️', 'food_items': [], 'calories': 0.0, 'protein': 0.0},
            'snack': {'key': 'snack', 'label': 'Evening Tiffin / Snack', 'icon': '☕', 'food_items': [], 'calories': 0.0, 'protein': 0.0},
            'dinner': {'key': 'dinner', 'label': 'Dinner', 'icon': '🌙', 'food_items': [], 'calories': 0.0, 'protein': 0.0},
        }

        for l in logs:
            m_type = (l.meal_type or 'snack').lower()
            if m_type not in meals:
                m_type = 'snack'
            meals[m_type]['food_items'].append(l)
            meals[m_type]['calories'] += l.calories
            meals[m_type]['protein'] += l.protein

        for m in meals.values():
            m['calories'] = round(m['calories'])
            m['protein'] = round(m['protein'], 1)

        return {
            'date': target_date,
            'date_str': target_date.strftime('%Y-%m-%d'),
            'date_display': target_date.strftime('%A, %b %d'),
            'is_today': target_date == date.today(),
            'total_calories': round(total_cals),
            'total_protein': round(total_protein, 1),
            'total_carbs': round(total_carbs, 1),
            'total_fat': round(total_fat, 1),
            'calorie_target': cals_target,
            'protein_target': protein_target,
            'calorie_pct': cals_pct,
            'protein_pct': protein_pct,
            'remaining_calories': rem_cals,
            'remaining_protein': rem_protein,
            'over_calorie_budget': total_cals > cals_target,
            'logs': logs,
            'meals': meals,
            'count': len(logs)
        }

    def get_daily_workout_summary(self, target_date=None):
        """
        Calculates total exercises, sets, volume lifted, duration on target_date (default today),
        and returns grouped workout logs by muscle / workout category.
        """
        if target_date is None:
            target_date = date.today()
        elif isinstance(target_date, str):
            try:
                target_date = datetime.strptime(target_date, '%Y-%m-%d').date()
            except ValueError:
                target_date = date.today()

        logs = WorkoutLog.query.filter_by(user_id=self.id, date=target_date).order_by(WorkoutLog.logged_at.asc()).all()

        total_exercises = len(logs)
        total_sets = sum(l.sets for l in logs)
        total_volume = sum(l.get_total_volume() for l in logs)
        total_duration = sum((l.duration_mins or 0) for l in logs)

        categories = {
            'chest': {'key': 'chest', 'label': 'Chest & Triceps', 'icon': '🏋️', 'exercises': [], 'total_sets': 0, 'total_volume': 0.0},
            'back': {'key': 'back', 'label': 'Back & Biceps', 'icon': '🚣', 'exercises': [], 'total_sets': 0, 'total_volume': 0.0},
            'legs': {'key': 'legs', 'label': 'Legs & Glutes', 'icon': '🦵', 'exercises': [], 'total_sets': 0, 'total_volume': 0.0},
            'shoulders': {'key': 'shoulders', 'label': 'Shoulders & Traps', 'icon': '🥥', 'exercises': [], 'total_sets': 0, 'total_volume': 0.0},
            'arms': {'key': 'arms', 'label': 'Arms & Forearms', 'icon': '💪', 'exercises': [], 'total_sets': 0, 'total_volume': 0.0},
            'core': {'key': 'core', 'label': 'Core & Abs', 'icon': '🧘', 'exercises': [], 'total_sets': 0, 'total_volume': 0.0},
            'cardio': {'key': 'cardio', 'label': 'Cardio & Conditioning', 'icon': '🏃', 'exercises': [], 'total_sets': 0, 'total_volume': 0.0},
            'custom': {'key': 'custom', 'label': 'Custom & Functional', 'icon': '⚡', 'exercises': [], 'total_sets': 0, 'total_volume': 0.0},
        }

        for l in logs:
            cat_key = (l.category or 'custom').lower()
            if cat_key not in categories:
                cat_key = 'custom'
            categories[cat_key]['exercises'].append(l)
            categories[cat_key]['total_sets'] += (l.sets or 0)
            categories[cat_key]['total_volume'] += l.get_total_volume()

        for c in categories.values():
            c['total_volume'] = round(c['total_volume'], 1)

        return {
            'date': target_date,
            'date_str': target_date.strftime('%Y-%m-%d'),
            'date_display': target_date.strftime('%A, %b %d'),
            'is_today': target_date == date.today(),
            'total_exercises': total_exercises,
            'total_sets': total_sets,
            'total_volume': round(total_volume, 1),
            'total_duration': total_duration,
            'categories': categories,
            'logs': logs,
            'has_workouts': total_exercises > 0
        }




class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class WeightLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    weight_kg = db.Column(db.Float, nullable=False)
    logged_at = db.Column(db.DateTime, default=datetime.utcnow)


class PreferredDay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    day_of_week = db.Column(db.String(10), nullable=False)  # 'Mon', 'Tue', etc.


class UserDietPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    goal = db.Column(db.String(30), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    dietary_preference = db.Column(db.String(30), nullable=False)
    state = db.Column(db.String(50), default='Tamil Nadu')
    cuisine_preference = db.Column(db.String(50), default='home_state')
    target_calories = db.Column(db.Integer, nullable=False)
    target_protein = db.Column(db.Integer, nullable=False)
    target_carbs = db.Column(db.Integer, nullable=False)
    target_fat = db.Column(db.Integer, nullable=False)
    meals_json = db.Column(db.Text, nullable=False)  # JSON-encoded array of meals
    role_tips = db.Column(db.Text, nullable=True)     # JSON-encoded or newline-separated tips
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class LiftLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise_name = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(10), default='kg')  # 'kg' or 'lbs'
    reps = db.Column(db.Integer, default=10)
    target_next_weight = db.Column(db.Float, nullable=False)
    notes = db.Column(db.String(200), nullable=True)
    logged_at = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def calculate_next_target(weight, unit='kg', exercise_name=''):
        """
        Calculates progressive overload next session goal.
        Rule: If he bench presses 50kg -> next section bench 55kg (or in lbs: 100 lbs -> 110 lbs / +10 lbs).
        For compound lifts (bench, squat, deadlift, overhead press, rows), increment is 5kg / 10 lbs.
        For smaller isolation movements, increment is 2.5kg / 5 lbs.
        """
        name_lower = (exercise_name or '').lower()
        is_lbs = (unit or 'kg').lower() == 'lbs'

        is_compound = any(c in name_lower for c in ['bench', 'squat', 'deadlift', 'press', 'row'])

        if is_lbs:
            increment = 10.0 if is_compound else 5.0
        else:
            increment = 5.0 if is_compound else 2.5

        return round(weight + increment, 1)


class FoodLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today, index=True)
    meal_type = db.Column(db.String(30), nullable=False, default='snack')  # breakfast, lunch, snack, dinner
    food_name = db.Column(db.String(150), nullable=False)
    serving_size = db.Column(db.String(100), default='1 serving')
    quantity = db.Column(db.Float, default=1.0)
    calories = db.Column(db.Float, nullable=False, default=0.0)
    protein = db.Column(db.Float, nullable=False, default=0.0)
    carbs = db.Column(db.Float, default=0.0)
    fat = db.Column(db.Float, default=0.0)
    logged_at = db.Column(db.DateTime, default=datetime.utcnow)

    MEAL_LABELS = {
        'breakfast': ('Breakfast', '🌅'),
        'lunch': ('Lunch', '☀️'),
        'snack': ('Evening Tiffin / Snack', '☕'),
        'dinner': ('Dinner', '🌙')
    }

    def get_meal_label(self):
        info = self.MEAL_LABELS.get(self.meal_type, ('Snack', '☕'))
        return f"{info[1]} {info[0]}"


class WorkoutLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today, index=True)
    category = db.Column(db.String(40), nullable=False, default='custom')  # chest, back, legs, shoulders, arms, core, cardio, custom
    exercise_name = db.Column(db.String(150), nullable=False)
    sets = db.Column(db.Integer, default=3)
    reps = db.Column(db.Integer, default=10)
    weight = db.Column(db.Float, default=0.0)
    unit = db.Column(db.String(10), default='kg')  # 'kg' or 'lbs'
    duration_mins = db.Column(db.Integer, default=0)
    calories_burned = db.Column(db.Float, default=0.0)
    target_next_weight = db.Column(db.Float, nullable=True)
    notes = db.Column(db.String(250), nullable=True)
    is_custom = db.Column(db.Boolean, default=False)
    logged_at = db.Column(db.DateTime, default=datetime.utcnow)

    CATEGORY_META = {
        'chest': ('Chest & Triceps', '🏋️'),
        'back': ('Back & Biceps', '🚣'),
        'legs': ('Legs & Glutes', '🦵'),
        'shoulders': ('Shoulders & Traps', '🥥'),
        'arms': ('Arms & Forearms', '💪'),
        'core': ('Core & Abs', '🧘'),
        'cardio': ('Cardio & Conditioning', '🏃'),
        'custom': ('Custom & Functional', '⚡'),
    }

    def get_category_label(self):
        info = self.CATEGORY_META.get(self.category, ('Custom & Functional', '⚡'))
        return f"{info[1]} {info[0]}"

    def get_total_volume(self):
        w = self.weight or 0.0
        s = self.sets or 1
        r = self.reps or 1
        return round(w * s * r, 1)

    @staticmethod
    def calculate_next_target(weight, unit='kg', exercise_name=''):
        """
        Progressive overload rule:
        For compound lifts (bench, squat, deadlift, overhead press, rows), increment is 5kg / 10 lbs.
        For smaller isolation movements, increment is 2.5kg / 5 lbs.
        """
        if weight is None or weight <= 0:
            return 0.0
        name_lower = (exercise_name or '').lower()
        is_lbs = (unit or 'kg').lower() == 'lbs'
        is_compound = any(c in name_lower for c in ['bench', 'squat', 'deadlift', 'press', 'row', 'pull-up', 'dips', 'lunge'])
        if is_lbs:
            increment = 10.0 if is_compound else 5.0
        else:
            increment = 5.0 if is_compound else 2.5
        return round(weight + increment, 1)


class CoachMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    coach_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sender_role = db.Column(db.String(20), default='client')  # 'client' or 'coach'
    subject = db.Column(db.String(150), default='General Fitness Doubt')
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def time_display(self):
        return self.created_at.strftime('%b %d, %I:%M %p')

