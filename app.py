import streamlit as st
import pandas as pd

st.set_page_config(page_title="Value Matching", layout="wide")

st.title("🔍 あなたの価値観に合う企業を探す")

# --- ユーザーの選択を保持するセッション変数 ---
if 'selections' not in st.session_state:
    st.session_state.selections = {
        'q1': None,
        'q2': None,
        'q3': None
    }

# --- 質問リスト ---
questions = {
    'q1': {
        'text': '働く上で最も大切にしたいことは？',
        'choices': ['自由と裁量', '安定と明確なルール', '社会的意義と貢献']
    },
    'q2': {
        'text': 'チーム内でのあなたの役割は？',
        'choices': ['静かに観察する', '分析して判断する', '空気を変える']
    },
    'q3': {
        'text': '理想の職場環境は？',
        'choices': ['一人で集中できる', '仲間と話せる', '刺激が多い']
    }
}

# --- 選択肢の表示と記録 ---
st.subheader("📌 あなたの価値観を選んでください（最大3つ）")
for q_key, q_data in questions.items():
    st.session_state.selections[q_key] = st.radio(
        label=q_data['text'],
        options=q_data['choices'],
        index=None,
        key=q_key
    )

# --- 仮のスコア算出ロジック（選択内容でスコアを変える） ---
def compute_scores(selections):
    base_data = [
        {"Company": "A社", "Value": "誠実さと創造性", "Base": 0.6},
        {"Company": "B社", "Value": "スピードと結果", "Base": 0.5},
        {"Company": "C社", "Value": "協働と尊重", "Base": 0.4},
    ]

    # 仮の重み付け（選択によりBaseスコアを加算）
    weights = {
        '自由と裁量': ('A社', 0.2),
        '安定と明確なルール': ('B社', 0.2),
        '社会的意義と貢献': ('C社', 0.2),
        '静かに観察する': ('C社', 0.1),
        '分析して判断する': ('B社', 0.1),
        '空気を変える': ('A社', 0.1),
        '一人で集中できる': ('A社', 0.1),
        '仲間と話せる': ('C社', 0.1),
        '刺激が多い': ('B社', 0.1),
    }

    scores = {}
    for entry in base_data:
        scores[entry['Company']] = entry['Base']

    for val in selections.values():
        if val and val in weights:
            target, bonus = weights[val]
            scores[target] += bonus

    df = pd.DataFrame([
        {
            "Company": c['Company'],
            "Value": c['Value'],
            "Score": round(scores[c['Company']], 2),
            "URL": f"https://example.com/{c['Company']}"
        }
        for c in base_data
    ])
    return df

# --- スコア表示 ---
if any(st.session_state.selections.values()):
    df = compute_scores(st.session_state.selections)
    st.subheader("🏆 マッチングスコア")
    st.dataframe(df.sort_values("Score", ascending=False), use_container_width=True)

    # Stripeリンク（例）
    payment_url = 'https://buy.stripe.com/28E4gzevx5YV2Lv1VeeZ201'
    if st.button('📄 500円でレポートを購入する'):
        st.markdown(f'[決済ページへ移動]({payment_url})', unsafe_allow_html=True)
else:
    st.info("🔄 質問に1つ以上答えると、マッチング結果が表示されます")
