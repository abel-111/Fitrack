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

    attendances = db.relationship('Attendance', backref='user', lazy=True)
    weight_logs = db.relationship('WeightLog', backref='user', lazy=True)
    preferred_days = db.relationship('PreferredDay', backref='user', lazy=True)
    diet_plans = db.relationship('UserDietPlan', backref='user', lazy=True, order_by='desc(UserDietPlan.created_at)')

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