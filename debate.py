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

def generate_mock_ai_response(prompt):
    """仮のAI応答を生成"""
    return f"これは仮の応答です。「{prompt}」について賛成/反対の立場を示す理由を述べます。"

@debate_bp.route('/debate', methods=['GET', 'POST'])
def debate():
    debate = AllDebate.query.first()
    if not debate:
        return "ディベートデータが存在しません", 404

    # ユーザーの発言回数をトラッキング
    if not hasattr(debate, 'user_input_count'):
        debate.user_input_count = 0

    if request.method == 'POST':
        user_message = request.form.get('user_message')
        if user_message:
            try:
                feedback_list = json.loads(debate.feedback) if debate.feedback else []
            except json.JSONDecodeError:
                feedback_list = []

            # ユーザーの発言を記録
            feedback_list.append({"speaker": "ユーザー", "message": user_message})
            debate.user_input_count += 1

            # 司会の発言とAIの応答を追加
            if debate.user_input_count == 1:
                feedback_list.append({"speaker": "司会", "message": "反対側の「AI」さん、主張を始めてください。時間制限は3分です。"})
            elif debate.user_input_count == 2:
                feedback_list.append({"speaker": "司会", "message": "それでは、賛成側の「ユーザー」さん、反論を始めてください。時間制限は3分です。"})
            elif debate.user_input_count == 3:
                feedback_list.append({"speaker": "司会", "message": "それでは、賛成側の「ユーザー」さん、最終立論を始めてください。時間制限は3分です。"})

            ai_response = generate_ai_response(user_message)
            feedback_list.append({"speaker": "AI", "message": ai_response})
            ai_response = generate_ai_response(user_message)
            if ai_response == "AI応答を生成できませんでした。":
                ai_response = generate_mock_ai_response(user_message)


            if debate.user_input_count == 3:
                feedback_list.append({"speaker": "司会", "message": "反対側の「AI」さん、最終立論を始めてください。時間制限は3分です。"})

            # フィードバックをJSONとして保存
            debate.feedback = json.dumps(feedback_list)
            db.session.commit()

    # フィードバックをリスト形式に変換してテンプレートに渡す
    try:
        feedback_list = json.loads(debate.feedback) if debate.feedback else []
    except json.JSONDecodeError:
        feedback_list = []

    # ディベート開始時に司会の最初の発言を記録
    if len(feedback_list) == 0:
        feedback_list.append({"speaker": "司会", "message": f"これから、テーマ「{debate.category}」についてディベートを開始します。"
                                                       f"賛成側の「ユーザー」さん、主張を始めてください。時間制限は3分です。"})
        debate.feedback = json.dumps(feedback_list)
        db.session.commit()

    # 結果発表ボタンの表示条件
    show_results_button = debate.user_input_count >= 3
    return render_template('debate.html', debate=debate, feedback=feedback_list, show_results_button=show_results_button)
@debate_bp.route('/interrupt/<int:debate_id>', methods=['POST'])
def interrupt_debate(debate_id):
    debate = AllDebate.query.get(debate_id)
    if debate:
        db.session.commit()

    return redirect(url_for('mode.mode_selection'))


@debate_bp.route('/stop', methods=['POST'])
def stop_debate():
    """ディベートを中止してデータベースをリセット"""
    # データベースのすべてのデータを削除
    db.session.query(AllDebate).delete()
    db.session.commit()

    # 初期データを再追加
    initial_data = AllDebate(
        user_1="ユーザー",
        user_2="AI",
        mode="やさしい",
        category="テクノロジー",
        topic="テクノロジーについて",
        feedback="[]",  # 初期化
    )
    db.session.add(initial_data)
    db.session.commit()

    return redirect(url_for('mode.mode_selection'))