from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from models import AllDebate
from ai import generate_theme, generate_claim, generate_counter, generate_final, generate_moderator_comment
import json
from extensions import db

debate_bp = Blueprint('debate', __name__, url_prefix='/debate')

@debate_bp.route('/debate', methods=['GET'])
def debate():
    # 最新のデータを取得
    debate = AllDebate.query.order_by(AllDebate.id.desc()).first()

    if not debate:
        # データが存在しない場合のみ新規作成
        debate = AllDebate(
            user_1="ユーザー",
            user_2="AI",
            category="未設定",
            role="先攻",
            topic="未設定",
            feedback="[]"
        )
        db.session.add(debate)
        db.session.commit()

    feedback = json.loads(debate.feedback) if debate.feedback else []
    return render_template('debate.html', debate=debate, feedback=feedback)


@debate_bp.route('/start', methods=['GET'])
def start_debate():
    debate = AllDebate.query.order_by(AllDebate.id.desc()).first()
    if not debate:
        return jsonify({"error": "ディベートが見つかりません"}), 404

    # テーマが未設定の場合にテーマを生成
    if not debate.topic or debate.topic == "未設定":
        try:
            category = debate.category if debate.category and debate.category != "未設定" else "テクノロジー"
            debate.topic = generate_theme(category)
            db.session.commit()
        except Exception as e:
            print(f"テーマ生成中にエラー: {str(e)}")
            return jsonify({"error": "テーマ生成に失敗しました"}), 500

    # フィードバックリセット
    debate.feedback = "[]"
    db.session.commit()

    # 開始メッセージを追加
    feedback = json.loads(debate.feedback)
    moderator_message = generate_moderator_comment("start", debate)
    feedback.append({"speaker": "司会", "message": moderator_message})
    debate.feedback = json.dumps(feedback)
    db.session.commit()

    return render_template('debate.html', debate=debate, feedback=feedback)


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
#ホーム画面に戻る
@debate_bp.route('/home', methods=['POST'])
def home_debate():
    print("Back to home")
    return redirect(url_for('home'))
#前に戻る
@debate_bp.route('/back', methods=['POST'])
def back_debate():
    print("Back to previous screen")
    return redirect(url_for('setting.setting'))

@debate_bp.route('/evaluation', methods=['GET'])
def show_evaluation():
    debate = AllDebate.query.order_by(AllDebate.id.desc()).first()
    if not debate:
        return "ディベートが存在しません", 404

    # 評価用のデータを渡す
    return render_template('feedback_main.html', debate=debate)



