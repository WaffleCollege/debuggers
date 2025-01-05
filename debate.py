from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from models import AllDebate
from ai import generate_theme, generate_claim, generate_counter, generate_final, generate_moderator_comment
import json
from extensions import db

debate_bp = Blueprint('debate', __name__, url_prefix='/debate')

# ディベート画面の初期化
@debate_bp.route('/debate', methods=['GET'])
def debate():
    debate = AllDebate.query.order_by(AllDebate.id.desc()).first()
    if not debate:
        return "ディベートデータが存在しません。", 404

    feedback = json.loads(debate.feedback) if debate.feedback else []
    return render_template('debate.html', debate=debate, feedback=feedback)

# ディベート開始時の設定
@debate_bp.route('/start', methods=['GET'])
def start_debate():
    debate = AllDebate.query.order_by(AllDebate.id.desc()).first()
    if not debate:
        return jsonify({"error": "ディベートが見つかりません"}), 404

    if not debate.topic:
        debate.topic = generate_theme(debate.category)
        db.session.commit()

    # 司会の開始コメントを追加
    feedback = json.loads(debate.feedback) if debate.feedback else []
    moderator_message = generate_moderator_comment("start", debate)
    feedback.append({"speaker": "司会", "message": moderator_message})

    debate.feedback = json.dumps(feedback)
    db.session.commit()

    return render_template('debate.html', debate=debate, feedback=feedback)

# ステージ進行を処理
@debate_bp.route('/progress', methods=['POST'])
def progress_debate():
    try:
        data = request.json
        stage = data.get("stage")
        user_message = data.get("message", "")
        debate = AllDebate.query.order_by(AllDebate.id.desc()).first()

        if not debate:
            return jsonify({"error": "ディベートが存在しません"}), 404

        feedback = json.loads(debate.feedback) if debate.feedback else []

        # ステージごとの処理
        if stage == "claim_user_1":
            if debate.user_1 == "AI":
                response = generate_claim(debate.topic, "賛成")
                feedback.append({"speaker": debate.user_1, "message": response})
                debate.user_1_claim = response
            else:
                feedback.append({"speaker": debate.user_1, "message": user_message})
                debate.user_1_claim = user_message

            feedback.append({"speaker": "司会", "message": generate_moderator_comment("claim_user_2", debate)})

        elif stage == "claim_user_2":
            if debate.user_2 == "AI":
                response = generate_claim(debate.topic, "反対")
                feedback.append({"speaker": debate.user_2, "message": response})
                debate.user_2_claim = response
            else:
                feedback.append({"speaker": debate.user_2, "message": user_message})
                debate.user_2_claim = user_message

            feedback.append({"speaker": "司会", "message": generate_moderator_comment("counter_user_1", debate)})

        elif stage == "counter_user_1":
            if debate.user_1 == "AI":
                response = generate_counter(debate.topic, debate.user_2_claim, "賛成")
                feedback.append({"speaker": debate.user_1, "message": response})
                debate.user_1_counter = response
            else:
                feedback.append({"speaker": debate.user_1, "message": user_message})
                debate.user_1_counter = user_message

            feedback.append({"speaker": "司会", "message": generate_moderator_comment("counter_user_2", debate)})

        elif stage == "counter_user_2":
            if debate.user_2 == "AI":
                response = generate_counter(debate.topic, debate.user_1_claim, "反対")
                feedback.append({"speaker": debate.user_2, "message": response})
                debate.user_2_counter = response
            else:
                feedback.append({"speaker": debate.user_2, "message": user_message})
                debate.user_2_counter = user_message

            feedback.append({"speaker": "司会", "message": generate_moderator_comment("final_user_1", debate)})

        elif stage == "final_user_1":
            if debate.user_1 == "AI":
                response = generate_final(debate.topic, debate.user_2_claim, debate.user_2_counter, "賛成")
                feedback.append({"speaker": debate.user_1, "message": response})
                debate.user_1_final = response
            else:
                feedback.append({"speaker": debate.user_1, "message": user_message})
                debate.user_1_final = user_message

            feedback.append({"speaker": "司会", "message": generate_moderator_comment("final_user_2", debate)})

        elif stage == "final_user_2":
            if debate.user_2 == "AI":
                response = generate_final(debate.topic, debate.user_1_claim, debate.user_1_counter, "反対")
                feedback.append({"speaker": debate.user_2, "message": response})
                debate.user_2_final = response
            else:
                feedback.append({"speaker": debate.user_2, "message": user_message})
                debate.user_2_final = user_message

            feedback.append({"speaker": "司会", "message": generate_moderator_comment("end", debate)})

        # フィードバックを更新
        debate.feedback = json.dumps(feedback)
        db.session.commit()

        return jsonify({"feedback": feedback})
    except Exception as e:
        return jsonify({"error": f"サーバーエラー: {str(e)}"}), 500

# ディベートを終了
@debate_bp.route('/stop', methods=['POST'])
def stop_debate():
    print("Debate stopped")
    return redirect(url_for('home'))
