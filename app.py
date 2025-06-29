import streamlit as st
import pandas as pd

st.set_page_config(page_title="Value Matching App", layout="wide")

st.title("🧠 価値観マッチングスコアビューア")

# 仮のテーブル（動作確認用）
dummy_data = {
    "Company": ["A社", "B社", "C社"],
    "Value": ["誠実さと創造性", "スピードと結果", "協働と尊重"],
    "Score": [0.82, 0.74, 0.65],
    "URL": [
        "https://example.com/a",
        "https://example.com/b",
        "https://example.com/c",
    ],
}

df = pd.DataFrame(dummy_data)

# スコア順で表示
st.subheader("スコアの高い順")
st.dataframe(df.sort_values("Score", ascending=False), use_container_width=True)

# Stripeの支払いリンク
payment_url = 'https://buy.stripe.com/28E4gzevx5YV2Lv1VeeZ201'

# JavaScriptで遷移
st.markdown(
    f"""
    <form action="{payment_url}" method="get">
        <button style="padding: 0.75em 1.5em; font-size: 16px; background-color: #635BFF; color: white; border: none; border-radius: 4px; cursor: pointer;">
            📄 500円で購入する
        </button>
    </form>
    """,
    unsafe_allow_html=True
)
