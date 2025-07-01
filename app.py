import streamlit as st
import pandas as pd

st.set_page_config(page_title="価値観マッチング", layout="wide")
st.title("🎯 価値観マッチング診断")

# 質問と選択肢
questions = {
    "Q1. 働く上でどちらを重視しますか？": ["安定", "変化"],
    "Q2. 人と働くときに重視するのは？": ["協調性", "成果主義"],
    "Q3. 理想の働き方は？": ["専門特化", "多様な経験"],
}

answers = {}

# スライダーで回答
for q, (left, right) in questions.items():
    st.markdown(f"**{q}**")
    choice = st.select_slider(
        label='',
        options=[left, f"{left}寄り", "中間", f"{right}寄り", right],
        value="中間",
        key=q
    )
    answers[q] = choice
    st.write("あなたの選択:", choice)
    st.divider()

# ダミー企業データ（回答によってスコア変化させる）
dummy_data = pd.DataFrame([
    {"Company": "A社", "Value": "変化×成果", "Score": 0.75},
    {"Company": "B社", "Value": "安定×協調", "Score": 0.80},
    {"Company": "C社", "Value": "専門×成果", "Score": 0.65},
])

# スコアに仮ロジック（例：選択肢ごとにスコア加算）
score_adjust = {
    "安定": {"B社": 0.05},
    "変化": {"A社": 0.05},
    "成果主義": {"A社": 0.05, "C社": 0.03},
    "協調性": {"B社": 0.05},
    "専門特化": {"C社": 0.05},
    "多様な経験": {"A社": 0.03},
}

for q, choice in answers.items():
    base = choice.replace("寄り", "").replace("中間", "")
    for company, delta in score_adjust.get(base, {}).items():
        dummy_data.loc[dummy_data["Company"] == company, "Score"] += delta

st.subheader("🔍 あなたに合う企業ランキング")
st.dataframe(dummy_data.sort_values("Score", ascending=False), use_container_width=True)

# Stripe購入リンク
payment_url = 'https://buy.stripe.com/28E4gzevx5YV2Lv1VeeZ201'
if st.button('📄 500円でレポートを購入する'):
    st.markdown(f'[👉 購入ページに進む]({payment_url})', unsafe_allow_html=True)
