#flaskをimport ここは同じだと思うから後で統合すると思う
from flask import Flask, render_template, request, redirect, url_for


#簡単、普通などの、モード選択ボタンを押したらデータベースに保存
@app.post('/category_page')
def next_category_page():
    mode = request.form["mode"]#name=modeのボタンを選択したら、categoryとして保存される。
    # カテゴリーの保存処理
    modes = ['やさしい', 'ふつう', 'むずかしい']
    new_mode = Mode(mode=mode)
    db.session.add(new_mode)
    db.session.commit()
    return render_template('category.html')#次のページへ