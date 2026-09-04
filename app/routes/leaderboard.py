from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import date
from sqlalchemy import func
from app.models import db, User, Attendance

leaderboard_bp = Blueprint('leaderboard', __name__)


@leaderboard_bp.route('/leaderboard')
@login_required
def leaderboard():
    today = date.today()
    start_of_month = today.replace(day=1)

    rows = (
        db.session.query(
            User.id,
            User.username,
            func.count(Attendance.id).label('checkin_count')
        )
        .join(Attendance, Attendance.user_id == User.id)
        .filter(Attendance.date >= start_of_month, Attendance.date <= today)
        .group_by(User.id)
        .order_by(func.count(Attendance.id).desc())
        .limit(20)
        .all()
    )

    return render_template(
        'leaderboard.html',
        rows=rows,
        current_user_id=current_user.id
    )
