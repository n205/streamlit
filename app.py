import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Value Matching App", layout="wide")

# -----------------------
# ページ遷移用セッション状態
# -----------------------
if 'page' not in st.session_state:
    st.session_state.page = 'top'

# -----------------------
# ページA: トップページ
# -----------------------
if st.session_state.page == 'top':
    st.title("🧭 価値観マッチング：あなたに合う企業は？")

    # ▼ 志向性スライダーなど
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

    # ▼ ランキング仮表示
    st.subheader("🧩 あなたに合いそうな企業ランキング")
    company_data = [
        {'Company': 'A社', 'Value': '本質と静けさを重視', 'Vector': np.array([-1, -2, -2]), 'URL': 'https://example.com/a'},
        {'Company': 'B社', 'Value': 'スピードと活気', 'Vector': np.array([1, 2, 2]), 'URL': 'https://example.com/b'},
        {'Company': 'C社', 'Value': 'バランス重視', 'Vector': np.array([0, 0, 0]), 'URL': 'https://example.com/c'},
    ]

    def calc_score(user, company):
        return 1 / (1 + np.linalg.norm(user - company))

    for item in company_data:
        item['Score'] = round(calc_score(user_vector, item['Vector']), 3)

    df = pd.DataFrame(company_data)
    df_sorted = df.sort_values(by='Score', ascending=False)
    st.dataframe(df_sorted[['Company', 'Value', 'Score', 'URL']], use_container_width=True)

    # ▼ 「もっと見る」（リンク風）
    col = st.columns(3)[1]  # 中央寄せ
    with col:
        if st.markdown('<a href="#" onclick="parent.location.reload()">🔽 もっと見る</a>', unsafe_allow_html=True):
            st.session_state.page = 'detail'

    if st.button('🔽 もっと見る', key='go_detail'):
        st.session_state.page = 'detail'

# -----------------------
# ページB: 詳細画面
# -----------------------
elif st.session_state.page == 'detail':
    st.title('🌱 思想とマッチング詳細')

    st.markdown('''
    ### リクルート的な思想からの離脱
    表面的な適合ではなく、価値観の深い一致を追求しています。  
    「自己決定・非依存・静かな選択」を重視するあなたに、本質的なマッチを提案します。
    ''')

    # ▼ 戻る
    col = st.columns(3)[1]
    with col:
        if st.button('◀ トップに戻る'):
            st.session_state.page = 'top'
