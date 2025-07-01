import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Value Matching App", layout="wide")
st.title("🧭 価値観マッチング：あなたに合う企業は？")

# 質問とスライダー
st.subheader("🔍 あなたの志向性を教えてください")

q1 = st.slider('① 自由な裁量  ←→  明確なルール', -2, 2, 0, format='%d')
q2 = st.slider('② 静かな環境  ←→  活気ある環境', -2, 2, 0, format='%d')
q3 = st.slider('③ 本質重視  ←→  スピード重視', -2, 2, 0, format='%d')

# 質問の回答をベクトル化
user_vector = np.array([q1, q2, q3])

# ダミー企業データ（企業ごとにベクトルを持たせる）
company_data = [
    {'Company': 'A社', 'Value': '本質と静けさを重視', 'Vector': np.array([-1, -2, -2]), 'URL': 'https://example.com/a'},
    {'Company': 'B社', 'Value': 'スピードと活気', 'Vector': np.array([1, 2, 2]), 'URL': 'https://example.com/b'},
    {'Company': 'C社', 'Value': 'バランス重視', 'Vector': np.array([0, 0, 0]), 'URL': 'https://example.com/c'},
]

# コサイン類似度 or ユークリッド距離などでスコア計算（ここでは単純な逆距離）
def calc_score(user, company):
    return 1 / (1 + np.linalg.norm(user - company))

# スコア算出
for item in company_data:
    item['Score'] = round(calc_score(user_vector, item['Vector']), 3)

# 表示
df = pd.DataFrame(company_data)
df_sorted = df.sort_values(by='Score', ascending=False)

st.subheader("🧩 あなたに合いそうな企業ランキング")
st.dataframe(df_sorted[['Company', 'Value', 'Score', 'URL']], use_container_width=True)

# Stripeの支払いリンク
payment_url = 'https://buy.stripe.com/28E4gzevx5YV2Lv1VeeZ201'

# 購入ボタン
if st.button('📄 このレポートを500円で購入する'):
    st.markdown(f'[こちらをクリックして決済ページへ移動]({payment_url})', unsafe_allow_html=True)
