import openai

# OpenAI APIキーとモデル名を設定
openai.organization = '' # ここに組織IDを設定
openai.project =''
openai.api_key = ''

# OpenAI APIを使用してテーマを生成する関数
def generate_theme(category):
    prompt = f"あなたはディベートテーマを生成するAIです。カテゴリーが「{category}」の場合、賛成と反対が対立する30文字以内のテーマを1つ作成してください。"
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=50,
        temperature=0.7,
    )
    return response['choices'][0]['message']['content'].strip()

# 主張を生成する関数
def generate_claim(topic, position):
    prompt = f"ディベートテーマは「{topic}」です。あなたは{position}側として、3分程度の主張を生成してください。"
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=300,
        temperature=0.7,
    )
    return response['choices'][0]['message']['content'].strip()

# 反論を生成する関数
def generate_counter(topic, user_claim, position):
    prompt = f"ディベートテーマは「{topic}」です。あなたは{position}側として、以下の主張に対する反論を3分程度で生成してください。\n\nユーザーの主張:\n{user_claim}"
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=300,
        temperature=0.7,
    )
    return response['choices'][0]['message']['content'].strip()

# 最終立論を生成する関数
def generate_final(topic, user_claim, user_counter, position):
    prompt = f"ディベートテーマは「{topic}」です。あなたは{position}側として、以下の情報を踏まえた最終立論を3分程度で生成してください。\n\nユーザーの主張:\n{user_claim}\n\nユーザーの反論:\n{user_counter}"
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=300,
        temperature=0.7,
    )
    return response['choices'][0]['message']['content'].strip()
