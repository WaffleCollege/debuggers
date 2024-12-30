from flask import Blueprint, request, render_template, redirect, url_for
from extensions import db
from models import AllDebate

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

debate_bp = Blueprint('debate', __name__, url_prefix='/debate')

if OPENAI_AVAILABLE:
    openai.api_key = None

def generate_ai_response(prompt):
    if not OPENAI_AVAILABLE or not openai.api_key:
        return "AI応答を生成できませんでした。"
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=300,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except Exception:
        return "AI応答を生成できませんでした。"

import json

@debate_bp.route('/debate', methods=['GET', 'POST'])
def debate():
    debate = AllDebate.query.first()
    if not debate:
        return "ディベートデータが存在しません", 404

    if request.method == 'POST':
        user_message = request.form.get('user_message')
        if user_message:
            try:
                feedback_list = json.loads(debate.feedback) if debate.feedback else []
            except json.JSONDecodeError:
                feedback_list = []

            feedback_list.append({"speaker": "ユーザー", "message": user_message})

            feedback_list.append({"speaker": "司会", "message": "次はAIの応答です。"})

            ai_response = generate_ai_response(user_message)
            feedback_list.append({"speaker": "AI", "message": ai_response})

            debate.feedback = json.dumps(feedback_list)
            db.session.commit()

    try:
        feedback_list = json.loads(debate.feedback) if debate.feedback else []
    except json.JSONDecodeError:
        feedback_list = []

    if len(feedback_list) == 0:
        feedback_list.append({"speaker": "司会", "message": f"これから、テーマ「{debate.category}」についてディベートを開始します。" 
                                                       f"賛成側の「AI」さん、主張を始めてください。時間制限は3分です。"})

    return render_template('debate.html', debate=debate, feedback=feedback_list)


@debate_bp.route('/interrupt/<int:debate_id>', methods=['POST'])
def interrupt_debate(debate_id):
    debate = AllDebate.query.get(debate_id)
    if debate:
        db.session.commit()

    return redirect(url_for('mode.mode_selection'))
