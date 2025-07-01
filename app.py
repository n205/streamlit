import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Value Matching App", layout="wide")
st.title("🧭 価値観マッチング：あなたに合う企業は？")

st.subheader("🔍 あなたの志向性を教えてください")

# 選択肢の定義（左から右へ行くほど右寄りの志向）
scale = ['強くA寄り', 'ややA寄り', '中立', 'ややB寄り', '強くB寄り']

def centered_slider(label):
    left, center, right = st.columns([1, 2, 1])
    with center:
        return st.select_slider(label, options=scale, value='中立')

q1 = centered_slider('① 自由な裁量  ←→  明確なルール')
q2 = centered_slider('② 静かな環境  ←→  活気ある環境')
q3 = centered_slider('③ 本質重視  ←→  スピード重視')

# スライダーを数値に変換（-2〜+2）
scale_map = {'強くA寄り': -2, 'ややA寄り': -1, '中立': 0, 'ややB寄り': 1, '強くB寄り': 2}
user_vector = np.array([
    scale_map[q1],
    scale_map[q2],
    scale_map[q3],
])

# 企業の仮データ
company_data = [
    {'Company': 'A社', 'Value': '本質と静けさを重視', 'Vector': np.array([-1, -2, -2]), 'URL': 'https://example.com/a'},
    {'Company': 'B社', 'Value': 'スピードと活気', 'Vector': np.array([1, 2, 2]), 'URL': 'https://example.com/b'},
    {'Company': 'C社', 'Value': 'バランス重視', 'Vector': np.array([0, 0, 0]), 'URL': 'https://example.com/c'},
]

# スコア計算
def calc_score(user, company):
    return 1 / (1 + np.linalg.norm(user - company))

for item in company_data:
    item['Score'] = round(calc_score(user_vector, item['Vector']), 3)

df = pd.DataFrame(company_data)
df_sorted = df.sort_values(by='Score', ascending=False)

st.subheader("🧩 あなたに合いそうな企業ランキング")
st.dataframe(df_sorted[['Company', 'Value', 'Score', 'URL']], use_container_width=True)

# Stripeの支払いリンク
payment_url = 'https://buy.stripe.com/28E4gzevx5YV2Lv1VeeZ201'

if st.button('📄 このレポートを500円で購入する'):
    st.markdown(f'[こちらをクリックして決済ページへ移動]({payment_url})', unsafe_allow_html=True)
