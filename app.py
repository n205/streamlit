import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title='Value Matching App', layout='wide')
st.title('🧭 価値観マッチング：あなたに合う企業は？')

# 状態管理
if 'num_display' not in st.session_state:
    st.session_state['num_display'] = 3  # 最初に表示する件数
if 'show_explanation' not in st.session_state:
    st.session_state['show_explanation'] = False

# -----------------------------
# ユーザー入力
# -----------------------------
st.subheader('🔍 あなたの志向性を教えてください')

scale = ['強くA寄り', 'ややA寄り', '中立', 'ややB寄り', '強くB寄り']
scale_map = {'強くA寄り': -2, 'ややA寄り': -1, '中立': 0, 'ややB寄り': 1, '強くB寄り': 2}

def centered_slider(label):
    left, center, right = st.columns([1, 2, 1])
    with center:
        return st.select_slider(label, options=scale, value='中立')

q1 = centered_slider('① 自由な裁量  ←→  明確なルール')
q2 = centered_slider('② 静かな環境  ←→  活気ある環境')
q3 = centered_slider('③ 本質重視  ←→  スピード重視')

user_vector = np.array([
    scale_map[q1],
    scale_map[q2],
    scale_map[q3],
])

# -----------------------------
# データ定義 & スコア計算
# -----------------------------
def calc_score(user, company):
    return 1 / (1 + np.linalg.norm(user - company))

company_data = [
    {'Company': 'A社', 'Value': '本質と静けさを重視', 'Vector': np.array([-1, -2, -2]), 'URL': 'https://example.com/a'},
    {'Company': 'B社', 'Value': 'スピードと活気', 'Vector': np.array([1, 2, 2]), 'URL': 'https://example.com/b'},
    {'Company': 'C社', 'Value': 'バランス重視', 'Vector': np.array([0, 0, 0]), 'URL': 'https://example.com/c'},
    {'Company': 'D社', 'Value': '安定と誠実さを大切に', 'Vector': np.array([0, -1, -1]), 'URL': 'https://example.com/d'},
    {'Company': 'E社', 'Value': '挑戦とスピード感を重視', 'Vector': np.array([2, 2, 1]), 'URL': 'https://example.com/e'},
    {'Company': 'F社', 'Value': '内省と調和を重んじる', 'Vector': np.array([-2, 1, -1]), 'URL': 'https://example.com/f'},
]

for item in company_data:
    item['Score'] = round(calc_score(user_vector, item['Vector']), 3)

df = pd.DataFrame(company_data).sort_values(by='Score', ascending=False)

# -----------------------------
# ランキング表示 or 説明
# -----------------------------
st.subheader('🧩 あなたに合いそうな企業ランキング')
score_placeholder = st.empty()

if st.session_state['show_explanation']:
    st.markdown('''
    ### 🧭 なぜ、いきなりたくさんの企業を見せないのか？

    このマッチングツールは、いわゆる「リクルート的」なマッチング――  
    「早くたくさんの企業を見て、いいねを押して、応募して」という世界とは異なる設計です。

    私たちは、あなたの**内面の志向**に静かに合う企業を見つけることを大切にしています。

    そのために、段階的に企業を紹介します。<br>
    これは、“焦らず、静かに選ぶ”体験のための設計です。
    ''')

    if st.button('🔓 続きを見る（+3社表示）'):
        st.session_state['num_display'] += 3
        st.session_state['show_explanation'] = False
else:
    df_display = df.head(st.session_state['num_display'])
    score_placeholder.dataframe(df_display[['Company', 'Value', 'Score', 'URL']], use_container_width=True)

    if st.session_state['num_display'] < len(df):
        if st.button('🔽 もっと見る（+3社）'):
            st.session_state['show_explanation'] = True

# -----------------------------
# 支払いリンク
# -----------------------------
payment_url = 'https://buy.stripe.com/28E4gzevx5YV2Lv1VeeZ201'
if st.button('📄 このレポートを500円で購入する'):
    st.markdown(f'[こちらをクリックして決済ページへ移動]({payment_url})', unsafe_allow_html=True)
