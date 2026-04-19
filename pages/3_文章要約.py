import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from utils.gemini_client import generate_text_stream

st.set_page_config(page_title="文章要約", page_icon="📄", layout="wide")

st.title("文章要約")
st.caption("長い文章を、指定の形式・長さで要約します。")

with st.form("summary_form"):
    source = st.text_area("要約したい文章", height=320, placeholder="要約したい文章をここに貼り付けてください。")

    col1, col2 = st.columns(2)
    with col1:
        style = st.selectbox(
            "要約の形式",
            [
                "3行要約",
                "箇条書き (5項目程度)",
                "段落形式の要約",
                "TL;DR (一文)",
                "見出しと箇条書きの構造化要約",
            ],
        )
    with col2:
        length = st.selectbox(
            "要約のボリューム",
            ["非常に短く", "短め", "標準", "しっかり詳しめ"],
        )

    focus = st.text_input(
        "特に重視してほしい観点 (任意)",
        placeholder="例: ビジネス上のインパクト、技術的な仕組み、など",
    )

    temperature = st.slider("創造性 (temperature)", 0.0, 1.0, 0.3, 0.1)
    submitted = st.form_submit_button("要約を生成", type="primary")

if submitted:
    if not source.strip():
        st.warning("要約したい文章を入力してください。")
        st.stop()

    system_instruction = (
        "あなたは文章要約の専門家です。原文の重要な情報を漏らさず、"
        "簡潔かつ正確に日本語で要約してください。原文にない情報は加えないこと。"
    )

    prompt = f"""以下の文章を要約してください。

# 要約の形式
{style}

# ボリューム
{length}

# 重視する観点
{focus or "（指定なし。全体をバランスよく）"}

# 原文
---
{source}
---
"""

    with st.spinner("要約中..."):
        st.write_stream(generate_text_stream(prompt, system_instruction, temperature))
