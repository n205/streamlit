import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Value Matching App", layout="wide")
st.title("🧭 価値観マッチング：あなたに合う企業は？")

# -----------------------------
# 初期化とデータ定義
# -----------------------------
scale = ['強くA寄り', 'ややA寄り', '中立', 'ややB寄り', '強くB寄り']
scale_map = {'強くA寄り': -2, 'ややA寄り': -1, '中立': 0, 'ややB寄り': 1, '強くB寄り': 2}

company_data = [
    {'Company': 'A社', 'Value': '本質と静けさを重視', 'Vector': np.array([-1, -2, -2]), 'URL': 'https://example.com/a'},
    {'Company': 'B社', 'Value': 'スピードと活気', 'Vector': np.array([1, 2, 2]), 'URL': 'https://example.com/b'},
    {'Company': 'C社', 'Value': 'バランス重視', 'Vector': np.array([0, 0, 0]), 'URL': 'https://example.com/c'},
    {'Company': 'D社', 'Value': '調和と柔軟性を重視', 'Vector': np.array([-1, 0, -1]), 'URL': 'https://example.com/d'},
    {'Company': 'E社', 'Value': '迅速な対応と革新性', 'Vector': np.array([2, 1, 2]), 'URL': 'https://example.com/e'},
    {'Company': 'F社', 'Value': '個の尊重と静かな裁量', 'Vector': np.array([-2, -1, -1]), 'URL': 'https://example.com/f'}
]

# -----------------------------
# スライダー入力
# -----------------------------
st.subheader("🔍 あなたの志向性を教えてください")

def centered_slider(label):
    left, center, right = st.columns([1, 2, 1])
    with center:
        return st.select_slider(label, options=scale, value='中立')

q1 = centered_slider('① 自由な裁量  ←→  明確なルール')
q2 = centered_slider('② 静かな環境  ←→  活気ある環境')
q3 = centered_slider('③ 本質重視  ←→  スピード重視')

user_vector = np.array([scale_map[q1], scale_map[q2], scale_map[q3]])

# -----------------------------
# スコア算出
# -----------------------------
def calc_score(user, company):
    return 1 / (1 + np.linalg.norm(user - company))

for item in company_data:
    item['Score'] = round(calc_score(user_vector, item['Vector']), 3)

df = pd.DataFrame(company_data)
df_sorted = df.sort_values(by='Score', ascending=False).reset_index(drop=True)

# -----------------------------
# セッション状態初期化
# -----------------------------
if 'num_display' not in st.session_state:
    st.session_state['num_display'] = 3
if 'show_explanation' not in st.session_state:
    st.session_state['show_explanation'] = False

# -----------------------------
# ランキング表示
# -----------------------------
st.subheader("🧩 あなたに合いそうな企業ランキング")
st.dataframe(df_sorted.iloc[:st.session_state['num_display']][['Company', 'Value', 'Score', 'URL']], use_container_width=True)

# -----------------------------
# 「もっと見る」導線
# -----------------------------
if st.session_state['num_display'] < len(df_sorted) and not st.session_state['show_explanation']:
    if st.button('🔽 もっと見る（+5社）'):
        st.session_state['show_explanation'] = True

if st.session_state['show_explanation']:
    st.markdown("""
    ### 🧭 このマッチングアプリの思想
    このアプリでは、たくさんの企業を見せて「いいね！」を押させるような設計はしていません。

    私たちは、「スピード」「活気」「自己PR力」だけで選ばれるような  
    従来の“リクルート的なマッチング”の対極にあるものを目指しています。

    **あなたの内面に静かにフィットする企業**  
    それは、たくさんの中から焦って選ぶものではなく、  
    自分の感覚と向き合って「見つける」ものです。

    それを支援するために、段階的にランキングを公開していきます。
    """)

    if st.button('🔓 続きを見る（あと5社表示）'):
        st.session_state['num_display'] += 5
        st.session_state['show_explanation'] = False

# -----------------------------
# 支払いリンク
# -----------------------------
payment_url = 'https://buy.stripe.com/28E4gzevx5YV2Lv1VeeZ201'
if st.button('📄 このレポートを500円で購入する'):
    st.markdown(f'[こちらをクリックして決済ページへ移動]({payment_url})', unsafe_allow_html=True)
