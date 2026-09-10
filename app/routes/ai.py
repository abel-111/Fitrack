from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.services.ai_coach import get_user_ai_recommendations, ask_ai_coach, ROLE_DETAILS

ai_bp = Blueprint('ai', __name__, url_prefix='/ai')

@ai_bp.route('/recommendations', methods=['GET'])
@login_required
def recommendations():
    insights = get_user_ai_recommendations(current_user)
    role_key = current_user.role if current_user.role in ROLE_DETAILS else 'general'
    role_info = ROLE_DETAILS[role_key]

    return render_template(
        'recommendations.html',
        insights=insights,
        role_info=role_info
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
