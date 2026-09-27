from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.ai_coach import get_user_ai_recommendations, ask_ai_coach, ROLE_DETAILS
from app.models import db, User, CoachMessage

ai_bp = Blueprint('ai', __name__, url_prefix='/ai')

@ai_bp.route('/recommendations', methods=['GET'])
@login_required
def recommendations():
    insights = get_user_ai_recommendations(current_user)
    role_key = current_user.role if current_user.role in ROLE_DETAILS else 'general'
    role_info = ROLE_DETAILS[role_key]

    # Only show admin-approved coaches to clients
    coaches = User.query.filter_by(is_coach=True, coach_approved=True).all()
    # Recent doubts sent by this client
    my_doubts = CoachMessage.query.filter_by(client_id=current_user.id).order_by(CoachMessage.created_at.desc()).all()

    return render_template(
        'recommendations.html',
        insights=insights,
        role_info=role_info,
        coaches=coaches,
        my_doubts=my_doubts
    )

@ai_bp.route('/chat', methods=['POST'])
@login_required
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get('message', '').strip()

    if not message:
        return jsonify({'error': 'Message cannot be empty'}), 400

    reply = ask_ai_coach(current_user, message)
    return jsonify({
        'success': True,
        'response': reply,
        'role': current_user.get_role_display()
    })

# ==================== HUMAN COACH DOUBT & PORTAL ROUTES ====================

@ai_bp.route('/ask-coach', methods=['POST'])
@login_required
def ask_human_coach():
    coach_id = request.form.get('coach_id')
    subject = request.form.get('subject', 'Fitness & Nutrition Doubt').strip()
    doubt_text = request.form.get('message', '').strip()

    if not doubt_text:
        flash('Please type your question or doubt before submitting.', 'danger')
        return redirect(url_for('ai.recommendations'))

    coach = User.query.filter_by(id=coach_id, is_coach=True).first()
    if not coach:
        # Fallback to the first available coach
        coach = User.query.filter_by(is_coach=True).first()

    if not coach:
        flash('No dedicated coaches are currently available.', 'danger')
        return redirect(url_for('ai.recommendations'))

    msg = CoachMessage(
        client_id=current_user.id,
        coach_id=coach.id,
        sender_role='client',
        subject=subject or 'General Question',
        message=doubt_text,
        is_read=False
    )
    db.session.add(msg)
    db.session.commit()

    flash(f"Your question has been sent to Coach {coach.username}! They will answer in your Coach hub.", "success")
    return redirect(url_for('ai.recommendations'))


@ai_bp.route('/coach-portal', methods=['GET'])
@login_required
def coach_portal():
    if not getattr(current_user, 'is_coach', False):
        flash('Access restricted to verified Fitness Coaches.', 'danger')
        return redirect(url_for('auth.dashboard'))

    # Check if the coach has been approved by admin
    if not getattr(current_user, 'coach_approved', False):
        flash(
            '⏳ Your coach account is pending admin approval. You will be notified once approved.',
            'info'
        )
        return redirect(url_for('auth.dashboard'))
    # All doubts sent to this coach
    all_messages = CoachMessage.query.filter_by(coach_id=current_user.id).order_by(CoachMessage.created_at.desc()).all()
    
    # Group by client for an easy inbox feel
    clients_dict = {}
    for m in all_messages:
        cid = m.client_id
        if cid not in clients_dict:
            clients_dict[cid] = {
                'client': m.client_user,
                'messages': []
            }
        clients_dict[cid]['messages'].append(m)

    return render_template(
        'coach_portal.html',
        all_messages=all_messages,
        clients_dict=clients_dict
    )


@ai_bp.route('/coach-reply', methods=['POST'])
@login_required
def coach_reply():
    if not getattr(current_user, 'is_coach', False):
        return jsonify({'error': 'Unauthorized'}), 403

    client_id = request.form.get('client_id')
    reply_text = request.form.get('reply_text', '').strip()
    subject = request.form.get('subject', 'Coach Advice & Feedback')

    if not client_id or not reply_text:
        flash('Reply content cannot be empty.', 'danger')
        return redirect(url_for('ai.coach_portal'))

    reply_msg = CoachMessage(
        client_id=int(client_id),
        coach_id=current_user.id,
        sender_role='coach',
        subject=subject,
        message=reply_text,
        is_read=False
    )
    db.session.add(reply_msg)
    db.session.commit()

    flash('Reply sent to your client successfully!', 'success')
    return redirect(url_for('ai.coach_portal'))
