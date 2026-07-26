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

    profile_picture = db.Column(db.String(200), default='default.png')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    attendances = db.relationship('Attendance', backref='user', lazy=True)
    weight_logs = db.relationship('WeightLog', backref='user', lazy=True)
    preferred_days = db.relationship('PreferredDay', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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