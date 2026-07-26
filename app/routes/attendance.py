from flask import Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import date
from app.models import db, Attendance

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/checkin', methods=['POST'])
@login_required
def checkin():
    today = date.today()
    already = Attendance.query.filter_by(user_id=current_user.id, date=today).first()

    if already:
        flash("You've already checked in today.", 'info')
    else:
        db.session.add(Attendance(user_id=current_user.id, date=today))
        db.session.commit()
        flash('Checked in! Keep the streak going.', 'success')

    return redirect(url_for('auth.dashboard'))