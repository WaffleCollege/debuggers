from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
import openai

debate_bp = Blueprint('debate', __name__)

openai.api_key = "your_openai_api_key"

debate_data = {
    "id": 1,
    "topic": "環境問題について",
    "time": "03:00",
    "moderator_message": "これからディベートを開始します。",
    "ai_message": "私は反対の立場です。",
    "user_message": ""
}


def generate_ai_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=300,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

@debate_bp.route('/debate', methods=['GET', 'POST'])
def debate():
    if request.method == 'POST':
        user_message = request.form.get('debate.user_message')
        if user_message:
            debate_data["user_message"] = user_message
            prompt = f"テーマ: {debate_data['topic']}\nユーザーの意見: {user_message}\nAIの反論:"
            debate_data["ai_message"] = generate_ai_response(prompt)

    return render_template('debate.html', debate=debate_data)

@debate_bp.route('/interrupt_debate/<int:debate_id>', methods=['POST'])
def interrupt_debate(debate_id):
    """ディベートを中断"""
    if debate_id == debate_data["id"]:
        debate_data["moderator_message"] = "ディベートが中断されました。"
    return redirect(url_for('debate.debate'))

