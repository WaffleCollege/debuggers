from flask import Blueprint, request, render_template,jsonify, render_template
from ai import openai
from extensions import db
from models import AllDebate
import logging


feedback_bp = Blueprint('feedback', __name__)

# OpenAI APIキーとモデル名を設定
openai.organization = '' # ここに組織IDを設定
openai.api_key = ''




@feedback_bp.route('/api/evaluateDebate', methods=['POST'])
def evaluate_debate():
   # データベースから最新のディベートを取得
   debate = AllDebate.query.order_by(AllDebate.id.desc()).first()


   if not debate:
       return jsonify({"error": "ディベートデータが見つかりません"}), 404


   # ディベート内容を構築
   debate_content = f"""
   テーマ: {debate.topic}


   ユーザー (先攻): {debate.user_1}
   AI (後攻): {debate.user_2}


   ユーザーの主張:
   {debate.user_1_claim}


   AIの主張:
   {debate.user_2_claim}


   ユーザーの反論:
   {debate.user_1_counter}


   AIの反論:
   {debate.user_2_counter}


   ユーザーの最終立論:
   {debate.user_1_final}


   AIの最終立論:
   {debate.user_2_final}
   """


   # OpenAI API プロンプトの作成
   prompt = f"""
   あなたはディベートの審査員です。以下のディベート内容を評価し、ガイドラインに沿って、以下の形式で、結果を出力してください:
   ガイドライン: 
   フィードバックには「甘口」と「辛口」の2種類がある。ジャッジは新聞を読んでいればわかる一般的な知識を持つ人と想定とする。個人的な考え、専門知識、偏見をできるだけ排除して、客観的に判定する。
以下は、「甘口」の基準である。
1.内容
-主張に理由があったか
-反論があったか
-例を用いて、十分に説明しているか
制約条件:
    - ジャッジは以下の基準を守ること
	1.内容
    - 相手の主張に理由があったか
    - 相手の主張に反論があったか
    -例を用いて十分に説明しているか
2.表現
    - はっきりとわかりやすい言葉で話しているか
	- 構成はわかりやすいか（主張、理由、主張の順番で話せているか。ナンバリング）
    - スピーカーの役割を果たしているか。

フィードバックは、やる気を出させるような言葉で伝えてください。
よかった点と、よくなかった点、改善点を述べてください。よかった点がよくなかった点より多くなるように出力してください。
それぞれの項目について評価を行った後、具体的な言動について教えてください。さらに、どうすればもっと良くなるのか、具体例を出してください。

続いて、以下は、「辛口」の基準である。
＜ガイドライン＞
ジャッジは新聞を読んでいればわかる一般的な知識を持つ人と想定とする。個人的な考え、専門知識、偏見をできるだけ排除して、客観的に判定する。
基準は、
1.内容
-主張に理由があったか
-反論があったか
-例を用いて、十分に説明しているか

2.表現
-はっきりとわかりやすい言葉で話しているか。
-構成はわかりやすいか（主張、理由、主張の順番で話せているか。ナンバリング。)
-スピーカーの役割を果たしているか。

フィードバックは、厳しくはっきりと伝えてください。
よかった点と、よくなかった点、改善点を全て述べてください。
それぞれの項目について評価を行った後、具体的な言動について教えてください。さらに、どうすればもっと良くなるのか、具体例を出してください。



出力の形式は以下の通りにしてください。
勝者: (ユーザー または AI)
甘口のフィードバック: (ここに「ユーザー」に対する甘口のフィードバックを記載。)
辛口のフィードバック: (ここに「ユーザー」に対する辛口のフィードバックを記載。)

引き分けは許可されていません。必ず「ユーザー」または「AI」を勝者として選んでください。

   ディベート内容:
   {debate_content}

   
   """



   try:
       # OpenAIのChatCompletion APIを呼び出し
       response = openai.ChatCompletion.create(
           model="gpt-4o-mini-2024-07-18",
           messages=[
               {"role": "system", "content": "あなたはディベートの審査員です。"},
               {"role": "user", "content": prompt}
           ]
       )


       # AIのレスポンスを解析
       result_text = response['choices'][0]['message']['content']
       result_lines = [line.strip() for line in result_text.split('\n') if line.strip()] 
       # デバッグ出力
       print("Result Lines:", result_lines)




       # 結果を抽出
       winner = result_lines[0].replace("勝者: ", "").strip()
       mild_feedback = result_lines[1].replace("甘口のフィードバック: ", "").strip()
       harsh_feedback = result_lines[2].replace("辛口のフィードバック: ", "").strip()


       # 必須条件: 勝者が「ユーザー」または「AI」かを確認
       if winner not in ["ユーザー", "AI"]:
           raise ValueError("無効な勝者がAIから返されました。")


       # データベースに勝者を保存
       debate.winner = winner
       db.session.commit()


       # レスポンスを返す
       return jsonify({
           "winner": winner,
           "mildFeedback": mild_feedback,
           "harshFeedback": harsh_feedback
       })


   except Exception as e:
       return jsonify({"error": f"AI判定中に予期しないエラーが発生しました: {str(e)}"}), 500



       

@feedback_bp.route('/feedback', methods=['POST'])
def feedback_page():
   feedback_type = request.form.get('feedback_type', 'sweet')
   mild_evaluation = request.form.get('mildEvaluation', "")
   harsh_evaluation = request.form.get('harshEvaluation', "")


   # フィードバック内容を適切に取得
   if feedback_type == 'sweet':
       feedback_message = mild_evaluation or "甘口のフィードバックが見つかりません"
   elif feedback_type == 'spicy':
       feedback_message = harsh_evaluation or "辛口のフィードバックが見つかりません"
   else:
       feedback_message = "フィードバックタイプが無効です。"


   return render_template('feedback_detail.html', feedback_message=feedback_message)


