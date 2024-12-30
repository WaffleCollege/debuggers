from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

#データベースは、後で

#選んだカテゴリーと自分で書いたお題をデータベースに保存する。
@app.post('/debate_page')#debate_pageにpostでアクセスした
def submit_topic():
    category = request.form["category"]#name=categoryのボタンを選択したら、categoryとして保存される。
    text = request.form["free_text"]

    if category:
        # カテゴリーの保存処理
        categories = ['環境問題', '教育', '社会問題', "就活"]
        new_category = Category(category=category)
        db.session.add(new_category)
    if text:
        # 話題の保存処理
        new_topic = Topic(text=text)
        db.session.add(new_topic)
    db.session.commit()
    return render_template("debate.html")##画面遷移


#categoryを選択したら、その場でAIが議題を生成する画面にいくか、議論画面で司会者が言うか