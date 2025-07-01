import streamlit as st

st.title('🔍 あなたの価値観に合う企業を探す')

# 回答保存用
answers = {}

st.subheader('📌 働く上で最も大切にしたいことは？')
answers['q1'] = st.radio('',
    ['⬅️ 自由と裁量', '🟰 中間', '➡️ 安定と明確なルール'],
    horizontal=True)

st.subheader('🤝 チーム内でのあなたの役割は？')
answers['q2'] = st.radio('',
    ['⬅️ 静かに観察する', '🟰 中間', '➡️ 空気を変える'],
    horizontal=True)

st.subheader('🏢 理想の職場環境は？')
answers['q3'] = st.radio('',
    ['⬅️ 一人で集中できる', '🟰 中間', '➡️ 刺激が多い'],
    horizontal=True)

# 回答に基づいたダミースコアを表示（ここにロジックを追加予定）
if any(answers.values()):
    st.subheader('📊 仮のマッチング結果')
    st.write('（ここに企業スコアを動的に表示予定）')
