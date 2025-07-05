import streamlit as st
import pandas as pd
import numpy as np

# ページ状態の初期化
if 'page' not in st.session_state:
    st.session_state['page'] = 'intro'


# 志向性のスケール定義
scale = ['強くA寄り', 'ややA寄り', '中立', 'ややB寄り', '強くB寄り']
scale_map = {'強くA寄り': -2, 'ややA寄り': -1, '中立': 0, 'ややB寄り': 1, '強くB寄り': 2}

def centered_slider(label):
    left, center, right = st.columns([1, 2, 1])
    with center:
        return st.select_slider(label, options=scale, value='中立')

def calc_score(user, company):
    return 1 / (1 + np.linalg.norm(user - company))

# 会社データ（ベクトルは仮）
company_data = [
    {'Company': 'A社', 'Value': '本質と静けさを重視', 'Vector': np.array([-1, -2, -2]), 'URL': 'https://example.com/a'},
    {'Company': 'B社', 'Value': 'スピードと活気', 'Vector': np.array([1, 2, 2]), 'URL': 'https://example.com/b'},
    {'Company': 'C社', 'Value': 'バランス重視', 'Vector': np.array([0, 0, 0]), 'URL': 'https://example.com/c'},
    {'Company': 'D社', 'Value': '創造性と誠実さの融合', 'Vector': np.array([0, -1, -2]), 'URL': 'https://example.com/d'},
    {'Company': 'E社', 'Value': '成果主義と迅速な判断', 'Vector': np.array([2, 2, 2]), 'URL': 'https://example.com/e'},
]

# -------------------------------
# ページ1: 簡易マッチング
# -------------------------------
if st.session_state['page'] == 'intro':
    st.set_page_config(page_title="Value Matching App", layout="wide")
    st.title("🧭 価値観マッチング：あなたに合う企業は？")

    st.subheader("🧩 あなたに合いそうな企業ランキング（簡易）")
    score_placeholder = st.empty()

    st.subheader("🔍 あなたの志向性を教えてください")
    q1 = centered_slider('① 自由な裁量  ←→  明確なルール')
    q2 = centered_slider('② 静かな環境  ←→  活気ある環境')
    q3 = centered_slider('③ 本質重視  ←→  スピード重視')

    user_vector = np.array([scale_map[q1], scale_map[q2], scale_map[q3]])

    for item in company_data:
        item['Score'] = round(calc_score(user_vector, item['Vector']), 3)
    df = pd.DataFrame(company_data).sort_values(by='Score', ascending=False)

    # 上位3社のみ表示
    score_placeholder.dataframe(df[['Company', 'Value', 'Score', 'URL']].head(3), use_container_width=True)

    cols = st.columns([7, 1, 7])
    with cols[1]:
        if st.button('もっと見る'):
            st.session_state['user_vector'] = user_vector.tolist()
            st.session_state['page'] = 'detail'

# -------------------------------
# ページ2: 詳細マッチング + 思想
# -------------------------------
elif st.session_state['page'] == 'detail':
    st.title("🪞 思想と深いマッチング")

    st.write('')
    cols = st.columns([1, 3, 1])  # 左1 : 中央3 : 右1 の比率
    with cols[1]:    
        st.markdown("""
        ### なぜこのマッチングを提供するのか？
        私たちは、「リクルート的なもの」の対極を目指しています。  
        つまり、**表面的なスキルマッチや企業の都合に合わせた画一的なマッチング**ではなく、  
        **あなたの価値観、意思決定のスタイル、そして静かな成長意欲**に根ざした企業選びを支援します。
        """, unsafe_allow_html=True)

    st.divider()
    st.subheader("🔍 あなたの志向性（詳細）を教えてください")

    # 入力を復元 or 初期化
    user_vector = np.array(st.session_state.get('user_vector', [0, 0, 0]))

    # 追加質問
    q4 = centered_slider('④ 創造性を重視  ←→ 再現性を重視')
    q5 = centered_slider('⑤ 個人最適  ←→ 組織最適')

    extended_user_vector = np.concatenate([user_vector, np.array([
        scale_map[q4],
        scale_map[q5],
    ])])

    # 各社に仮ベクトル（拡張5次元）を追加（今回はランダムにしてますが、実際は事前設計）
    for item in company_data:
        vec = item['Vector']
        item['Vector'] = np.concatenate([vec, np.random.choice([-2, -1, 0, 1, 2], 2)])  # 仮: ランダム補完
        item['Score'] = round(calc_score(extended_user_vector, item['Vector']), 3)

    df = pd.DataFrame(company_data).sort_values(by='Score', ascending=False)
    st.subheader("🏆 あなたに本当に合いそうな企業ランキング（詳細）")
    st.dataframe(df[['Company', 'Value', 'Score', 'URL']], use_container_width=True)

    st.divider()
    payment_url = 'https://buy.stripe.com/28E4gzevx5YV2Lv1VeeZ201'
    if st.button('📄 このレポートを500円で購入する'):
        st.markdown(f'[こちらをクリックして決済ページへ移動]({payment_url})', unsafe_allow_html=True)
