from flask import Blueprint, render_template, jsonify, request, redirect, url_for, jsonify
from models import AllDebate
from ai import generate_theme, generate_claim, generate_counter, generate_final, generate_moderator_comment
import json
from extensions import db





# OpenAI APIの設定（実際のキーに置き換えてください）
openai.api_key = 'your-api-key-here'

# ディスカッションのテーマリスト AIにプロンプト通りに作ってもらいたい
def generate_themes():
    prompt = """
    以下の分類から形式（例えば自由討論型）を選び、それに沿ったテーマを生成してください。例えば自由討論型を選んだら、「形式は自由討論型で〇〇というテーマで話し合います」というふうに言ってください。
    ・課題解決型
        ・時事に関連するテーマ（例：投票率を上げる方法）
        ・馴染みのないテーマ（例：ルーミートを話題にする方法）
    ・自由討論型（抽象的なテーマについて話し合う。例：「４番目のメダルがあるとしたら何色か」「インクの切れたボールペンの有効活用方法」など)
    ・選択型（例：人生で仕事、恋愛、家族の優先順位をつけるとしたら）
    """

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.7,
    )

    themes = response.choices[0].text.strip().split('\n')
    return [theme.strip() for theme in themes if theme.strip()]


# アプリケーション起動時にテーマを生成
themes = generate_themes()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_discussion', methods=['POST'])
def start_discussion():
    user_role = request.json['role']
    time_setting = request.json['time']
    theme = random.choice(themes)
    
    # AIの役割を決定（ユーザーが選んだ以外の2つ）
    ai_roles = [role for role in ['進行役', 'タイムキーパー', '書記', '発表者'] if role != user_role][:2]
    
    return jsonify({
        'theme': theme,
        'user_role': user_role,
        'ai_roles': ai_roles,
        'time': time_setting
    })


