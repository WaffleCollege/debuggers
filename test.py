
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# OpenAIのAPIキーを設定
openai.api_key = ""

@app.route('/api/getDebateResult', methods=['POST'])
def get_debate_result():
    data = request.json
    debate_content = data.get("debateContent", "")

    # OpenAIのChatGPT APIで勝敗と評価を生成
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "あなたはディベートの審査員です。"},
            {"role": "user", "content": f"""以下のディベートを評価し、勝者と甘口・辛口の評価を提供してください:
             ユーザーの主張：\n{debate_content}}
                制約条件:
                    - ジャッジは以下の基準を守ること
                    1.内容
                    - 相手の主張に理由があったか
                    - 相手の主張に反論があったか
                    -例を用いて十分に説明しているか
                    2.表現
                    - はっきりとわかりやすい言葉で話しているか
                    - 構成はわかりやすいか（主張、理由、主張の順番で話せているか。ナンバリング）
                    - スピーカーの役割を果たしているか。"""

        ]
    )

    result_text = response['choices'][0]['message']['content']

    # 勝者と評価を抽出する（例に応じて処理を調整）
    result_lines = result_text.split('\n')
    winner = result_lines[0].replace("勝者: ", "")
    mild_evaluation = result_lines[1].replace("甘口の評価: ", "")
    harsh_evaluation = result_lines[2].replace("辛口の評価: ", "")

    return jsonify({
        "winner": winner,
        "mildEvaluation": mild_evaluation,
        "harshEvaluation": harsh_evaluation
    })

if __name__ == '__main__':
    app.run(debug=True)
