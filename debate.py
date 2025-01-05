from flask import Blueprint, render_template, jsonify, request,redirect,url_for
from models import AllDebate
from ai import generate_theme, generate_claim, generate_counter, generate_final
import json
from extensions import db
debate_bp = Blueprint('debate', __name__, url_prefix='/debate')


@debate_bp.route('/debate', methods=['GET'])
def debate():
    # Debate画面を表示する処理
    return render_template('debate.html')

@debate_bp.route('/start', methods=['GET'])
def start_debate():
    debate = AllDebate.query.order_by(AllDebate.id.desc()).first()
    if not debate.topic:
        debate.topic = generate_theme(debate.category)
        db.session.commit()
    return render_template('debate.html', debate=debate)

def handle_stage(debate, stage):
    if stage == "claim_user_1":
        debate.user_1_claim = generate_claim(debate.topic, "賛成")
        return {"speaker": debate.user_1, "message": debate.user_1_claim}
    elif stage == "claim_user_2":
        debate.user_2_claim = generate_claim(debate.topic, "反対")
        return {"speaker": debate.user_2, "message": debate.user_2_claim}
    elif stage == "counter_user_1":
        debate.user_1_counter = generate_counter(debate.topic, debate.user_2_claim, "賛成")
        return {"speaker": debate.user_1, "message": debate.user_1_counter}
    elif stage == "counter_user_2":
        debate.user_2_counter = generate_counter(debate.topic, debate.user_1_claim, "反対")
        return {"speaker": debate.user_2, "message": debate.user_2_counter}
    elif stage == "final_user_1":
        debate.user_1_final = generate_final(debate.topic, debate.user_2_claim, debate.user_2_counter, "賛成")
        return {"speaker": debate.user_1, "message": debate.user_1_final}
    elif stage == "final_user_2":
        debate.user_2_final = generate_final(debate.topic, debate.user_1_claim, debate.user_1_counter, "反対")
        return {"speaker": debate.user_2, "message": debate.user_2_final}
    else:
        raise ValueError("無効なステージ")

@debate_bp.route('/progress', methods=['POST'])
def progress_debate():
    try:
        stage = request.json.get("stage")
        debate = AllDebate.query.order_by(AllDebate.id.desc()).first()
        if not stage or not debate:
            return jsonify({"error": "ステージまたはディベート情報がありません"}), 400

        feedback_entry = handle_stage(debate, stage)

        # フィードバックに追加
        feedback = json.loads(debate.feedback)
        feedback.append(feedback_entry)
        debate.feedback = json.dumps(feedback)

        db.session.commit()
        return jsonify({"message": f"{stage}が完了しました。", "feedback": feedback})
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"サーバーエラーが発生しました: {str(e)}"}), 500


@debate_bp.route('/stop', methods=['POST'])
def stop_debate():
    # ディベート停止処理（必要なら追加）
    print("Debate stopped")
    return redirect(url_for('home')) 