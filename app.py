import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Value Matching App", layout="wide")
st.title("🎯 あなたの志向性に合う企業は？")

st.subheader("🔍 以下の質問に直感でお答えください")

# ラベルと内部スコアの対応
options = {
    'かなり自由裁量': -2,
    'やや自由裁量': -1,
    '中立': 0,
    'やや明確ルール': 1,
    'かなり明確ルール': 2
}
# 共通のラベルリスト
labels = list(options.keys())

# 各質問ごとのスライダー
q1_label = st.select_slider('① 自由な裁量 ←→ 明確なルール', options=labels, value='中立')
q2_label = st.select_slider('② 静かな環境 ←→ 活気ある環境', options=labels, value='中立')
q3_label = st.select_slider('③ 本質重視 ←→ スピード重視', options=labels, value='中立')

# 数値に変換
user_vector = np.array([
    options[q1_label],
    options[q2_label],
    options[q3_label],
])

# ダミー企業データ（ベクトル）
company_data = [
    {'Company': 'A社', 'Value': '本質と静けさを重視', 'Vector': np.array([-1, -2, -2]), 'URL': 'https://example.com/a'},
    {'Company': 'B社', 'Value': 'スピードと活気', 'Vector': np.array([1, 2, 2]), 'URL': 'https://example.com/b'},
    {'Company': 'C社', 'Value': 'バランス重視', 'Vector': np.array([0, 0, 0]), 'URL': 'https://example.com/c'},
]

# スコア算出（ユークリッド距離ベース）
def calc_score(user, company):
    return 1 / (1 + np.linalg.norm(user - company))

for item in company_data:
    item['Score'] = round(calc_score(user_vector, item['Vector']), 3)

df = pd.DataFrame(company_data).sort_values(by='Score', ascending=False)

st.subheader('🔎 マッチ度ランキング')
st.dataframe(df[['Company', 'Value', 'Score', 'URL']], use_container_width=True)

# Stripe購入リンク
payment_url = 'https://buy.stripe.com/28E4gzevx5YV2Lv1VeeZ201'
if st.button('📄 このレポートを500円で購入する'):
    st.markdown(f'[こちらをクリックして決済ページへ移動]({payment_url})', unsafe_allow_html=True)
