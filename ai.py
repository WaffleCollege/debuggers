import openai

# OpenAI APIキーとモデル名を設定
openai.organization = '' # ここに組織IDを設定
openai.project =''
openai.api_key = ''


# OpenAI APIを使用してテーマを生成する関数
def generate_theme(category):
    prompt = f"あなたはディベートテーマを生成するAIです。{category}に関連する、賛成と反対が対立する30文字以内の議題を1つ作成し、議題のみを答えてください。"
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=50,
        temperature=0.7,
    )
    return response['choices'][0]['message']['content'].strip()

# 主張
def generate_claim(topic, position):
    prompt = f"ディベートテーマは{topic}です。あなたは{position}側として、300字以内で主張を生成してください。"
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=400,
        temperature=0.7,
    )
    return response['choices'][0]['message']['content'].strip()

# 反論
def generate_counter(topic, user_claim, position):
    prompt = f"ディベートテーマは「{topic}」です。あなたは{position}側として、以下の主張に対する反論を300字以内で生成してください。\n\nユーザーの主張:\n{user_claim}"
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=400,
        temperature=0.7,
    )
    return response['choices'][0]['message']['content'].strip()

# 最終立論
def generate_final(topic, user_claim, user_counter, position):
    prompt = f"ディベートテーマは「{topic}」です。あなたは{position}側として、以下の情報を踏まえた最終立論を300字以内で生成してください。\n\nユーザーの主張:\n{user_claim}\n\nユーザーの反論:\n{user_counter}"
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=400,
        temperature=0.7,
    )
    return response['choices'][0]['message']['content'].strip()


#司会AI
def generate_moderator_comment(stage, debate):
    if stage == "start":
        return f"これから「{debate.topic}」のディベートを開始します。それでは、賛成側の{debate.user_1}さん主張を始めてください。時間制限は3分です。"
    elif stage == "claim_user_2":
        return f"続いて、反対側の{debate.user_2}さん、主張を始めてください。時間制限は3分です。"
    elif stage == "counter_user_1":
        return f"続いて、賛成側の{debate.user_1}さん、{debate.user_2}さんに対して反論をお願いします。時間制限は3分です。"
    elif stage == "counter_user_2":
        return f"続いて、反対側の{debate.user_2}さん、{debate.user_1}さんに対して反論をお願いします。時間制限は3分です。"
    elif stage == "final_user_1":
        return f"それでは、賛成側の{debate.user_1}さん、これまでの議論を踏まえて、最終立論を始めてください。時間制限は3分です。"
    elif stage == "final_user_2":
        return f"それでは、反対側の{debate.user_2}さん、これまでの議論を踏まえて、最終立論を始めてください。時間制限は3分です。"
    elif stage == "end":
        return f"これで「{debate.topic}」のディベートは終了です。"
