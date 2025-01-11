from flask import Blueprint, request, render_template,jsonify, render_template
from ai import openai
from models import AllDebate



feedback_bp = Blueprint('feedback', __name__)

# OpenAI APIキーとモデル名を設定
openai.organization = '' # ここに組織IDを設定
openai.api_key = ''


# 勝敗とフィードバックを生成
@feedback_bp.route('/api/getDebateResult', methods=['POST'])
def get_debate_result():
    data = request.json
    debate_content = data.get("debateContent", "")

    try:
        # OpenAIのChatGPT APIで勝敗と評価を生成
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "あなたはディベートの審査員です。"},
                {"role": "user", "content": f"""以下のディベートを評価し、勝者と甘口・辛口の評価を提供してください:
ディベート内容：{debate_content}
制約条件:
- ジャッジは以下の基準を守ること:
  1. 内容:
     - 相手の主張に理由があったか。
     - 相手の主張に反論があったか。
     - 例を用いて十分に説明しているか。
  2. 表現:
     - はっきりとわかりやすい言葉で話しているか。
     - 構成がわかりやすいか（主張、理由、結論の順番）。
     - スピーカーの役割を果たしているか。"""
                }
            ]
        )

        # ChatGPTのレスポンスから勝者と評価を抽出
        result_text = response['choices'][0]['message']['content']
        result_lines = result_text.split('\n')
        winner = result_lines[0].replace("勝者: ", "").strip()
        mild_evaluation = result_lines[1].replace("甘口の評価: ", "").strip()
        harsh_evaluation = result_lines[2].replace("辛口の評価: ", "").strip()

        return jsonify({
            "winner": winner,
            "mildEvaluation": mild_evaluation,
            "harshEvaluation": harsh_evaluation
        })

    except Exception as e:
        return jsonify({"error": f"AI判定中にエラーが発生しました: {str(e)}"}), 500


# フィードバックの表示
@feedback_bp.route('/feedback', methods=['POST'])
def feedback_page():
    feedback_type = request.form.get('feedback_type', 'sweet')

    # フィードバック内容を適切に取得
    if feedback_type == 'sweet':
        feedback_message = request.form.get('mildEvaluation', "甘口のフィードバックが見つかりません")
    elif feedback_type == 'spicy':
        feedback_message = request.form.get('harshEvaluation', "辛口のフィードバックが見つかりません")
    else:
        feedback_message = "フィードバックタイプが無効です。"

    # フィードバック詳細画面を表示
    return render_template('feedback_detail.html', feedback_message=feedback_message)


