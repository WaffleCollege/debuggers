import openai

# OpenAI APIキーとモデル名を設定
openai.organization = '' # ここに組織IDを設定
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
    prompt = f"""ディベートテーマは{topic}です。あなたは{position}側として、約500字程度で主張を生成してください。
    ディベートの立論（3分）の流れは以下の通りです:

    **出力形式:** 自然な会話

    **構造:**

    * 結論
    * 定義 (必要であれば)
    * ポイント1
    * 説明
    * ポイント2
    * 説明
    * まとめ

    **各セクションは必ず改行で区切ってください。**

    **例:**

    AIの導入は、企業の生産性向上に大きく貢献します。 \n

    AIとは、人間の知能を模倣したコンピューターシステムを指します。(必要であれば)\n

    AIは、単純作業の自動化によって人件費を削減し、企業の収益性を向上させます。\n
    * 例えば、製造業においては、ロボットの導入により生産性が大幅に向上し、人件費が削減されています。\n

    ポイント2: AIは、新たな製品やサービスの開発を加速させ、イノベーションを促進します。\n
    * 例えば、AIを活用した医療診断システムは、より正確な診断を可能にし、医療の発展に貢献しています。\n

    まとめ: 以上のように、AIの導入は、企業の生産性向上とイノベーションの促進という二つの側面から、社会全体に大きな貢献をもたらします。\n

    **制約条件:**

    * 各セクションは必ず改行で区切ってください。
    * 箇条書きは使用せず、文章で記述してください。
    * 論理的な流れで、説得力のある文章を作成してください。"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=400,
        temperature=0.7,
    )
    return response['choices'][0]['message']['content'].strip()

# 反論
def generate_counter(topic, user_claim, position):
    prompt = f"""ディベートテーマは「{topic}」です。あなたは{position}側として、以下の主張に対する反論を300字以内で生成してください。
    \n\nユーザーの主張:\n{user_claim}
    -ディベート（反論）の流れは以下の通りです
        1. **結論**: あなたの主張を簡潔に述べてください。 
        2. **ユーザーの一つ目のポイントへの反論**: - ユーザーの主張:{user_claim}に具体的に反論してください。あなたは{position}側です。
        3. **ユーザー一つ目のポイントへの再反論**: - 否定側からの反論を再反論してください。
        4. **二つ目のポイントの説明**: - 現在の状況とその問題点、そしてその解決がもたらす利益を説明してください。 
        5. **結論**: あなたの主張を再度述べてください。
    -制約条件
        ・暴力的、性的、政治的な発言をしてはいけません
        ・偏見や偏った見解に陥らないようにしてください。
        ・礼儀正しく、敬意をもって議論をしてください。
        ・あなたは、主張や意見を根拠とデータに基づいて行います。証拠のない主張や根拠のない意見は行いません。
        ・反論では、相手の論理的に弱いところについて主に主張を行います。

"""


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
        return f"これで「{debate.topic}」のディベートは終了です。評価画面へ移動してください。"

