import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.models import db

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@profile_bp.route('/', methods=['GET'])
@login_required
def view():
    return render_template('profile.html')


@profile_bp.route('/picture', methods=['POST'])
@login_required
def upload_picture():
    file = request.files.get('picture')

    if not file or file.filename == '':
        flash('Choose an image first.', 'danger')
        return redirect(url_for('profile.view'))

    if not allowed_file(file.filename):
        flash('Only PNG, JPG, JPEG, or WEBP images are allowed.', 'danger')
        return redirect(url_for('profile.view'))

    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)

    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = secure_filename(f'user_{current_user.id}.{ext}')
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)

    current_user.profile_picture = filename
    db.session.commit()

    flash('Profile picture updated!', 'success')
    return redirect(url_for('profile.view'))
