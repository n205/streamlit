import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Value Matching App", layout="wide")
st.title("🧭 価値観マッチング：あなたに合う企業は？")

# セッションステートの初期化
if 'num_display' not in st.session_state:
    st.session_state['num_display'] = 3
if 'show_explanation' not in st.session_state:
    st.session_state['show_explanation'] = False

# -----------------------------
# スコア計算ロジック
# -----------------------------
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

def calc_score(user, company):
    return 1 / (1 + np.linalg.norm(user - company))

company_data = [
    {'Company': 'A社', 'Value': '本質と静けさを重視', 'Vector': np.array([-1, -2, -2]), 'URL': 'https://example.com/a'},
    {'Company': 'B社', 'Value': 'スピードと活気', 'Vector': np.array([1, 2, 2]), 'URL': 'https://example.com/b'},
    {'Company': 'C社', 'Value': 'バランス重視', 'Vector': np.array([0, 0, 0]), 'URL': 'https://example.com/c'},
    {'Company': 'D社', 'Value': '静かな集中力と探究心を尊重', 'Vector': np.array([-2, -1, -2]), 'URL': 'https://example.com/d'},
    {'Company': 'E社', 'Value': 'スピード重視で成果を出す文化', 'Vector': np.array([2, 1, 2]), 'URL': 'https://example.com/e'},
    {'Company': 'F社', 'Value': '明確なガイドラインとチーム連携', 'Vector': np.array([1, 1, -1]), 'URL': 'https://example.com/f'},
    {'Company': 'G社', 'Value': '自己裁量と内省が尊重される', 'Vector': np.array([-2, -2, -1]), 'URL': 'https://example.com/g'},
]

for item in company_data:
    item['Score'] = round(calc_score(user_vector, item['Vector']), 3)

df = pd.DataFrame(company_data)
df_sorted = df.sort_values(by='Score', ascending=False)

# -----------------------------
# ランキング表示（上部）
# -----------------------------
st.subheader("🧩 あなたに合いそうな企業ランキング")
score_placeholder = st.empty()
score_placeholder.dataframe(
    df_sorted.head(st.session_state['num_display'])[['Company', 'Value', 'Score', 'URL']],
    use_container_width=True
)

# -----------------------------
# 「もっと見る」導線
# -----------------------------
if st.session_state['num_display'] < len(df_sorted) and not st.session_state['show_explanation']:
    if st.button('🔽 もっと見る（+5社）'):
        st.session_state['show_explanation'] = True

if st.session_state['show_explanation']:
    st.markdown("""
    ### 🧭 このマッチングアプリの思想

    このアプリでは、たくさんの企業を「右スワイプ」させるような体験ではなく、  
    **あなたの内面に静かにフィットする企業**を見つけることを大切にしています。

    「スピード」や「活気」、「自己PR力」による表層的な適合性ではなく、  
    あなたの価値観、志向性、本質に合う企業と静かに出会う——  
    それがこのアプリの目指す体験です。

    そのため、ランキングは段階的に公開しています。
    """)

    if st.button('🔓 続きを見る（あと5社表示）'):
        st.session_state['num_display'] += 5
        st.session_state['show_explanation'] = False

# -----------------------------
# 志向性入力（下部）
# -----------------------------
st.subheader("🔍 あなたの志向性を教えてください")

# （← スライダーはすでに上部で定義済）
# ここでは、必要であれば志向性の内容や説明文などを追加表示できます

# -----------------------------
# 支払い導線
# -----------------------------
payment_url = 'https://buy.stripe.com/28E4gzevx5YV2Lv1VeeZ201'
if st.button('📄 このレポートを500円で購入する'):
    st.markdown(f'[こちらをクリックして決済ページへ移動]({payment_url})', unsafe_allow_html=True)
