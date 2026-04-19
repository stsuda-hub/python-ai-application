import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from utils.gemini_client import generate_text_stream, render_api_key_sidebar

st.set_page_config(page_title="文章リライト・校正", page_icon="✏️", layout="wide")
render_api_key_sidebar()

st.title("文章リライト・校正")
st.caption("誤字脱字のチェックや、文体の改善・リライトを行います。")

with st.form("rewrite_form"):
    source = st.text_area("元の文章", height=280, placeholder="リライト・校正したい文章を入力してください。")

    mode = st.radio(
        "処理モード",
        [
            "校正のみ (誤字脱字・表記ゆれを修正)",
            "文体改善 (読みやすく自然に)",
            "フルリライト (意味を保ちつつ書き直し)",
            "トーン変換",
        ],
        horizontal=False,
    )

    col1, col2 = st.columns(2)
    with col1:
        tone = st.selectbox(
            "目指す文体",
            [
                "ビジネス・丁寧",
                "カジュアル・親しみやすい",
                "専門的・論理的",
                "ですます調",
                "だ・である調",
                "やわらかく優しい",
            ],
        )
    with col2:
        show_diff = st.checkbox("修正ポイントの解説を付ける", value=True)

    instructions = st.text_input(
        "追加の指示 (任意)",
        placeholder="例: 冗長な表現を削って簡潔に。主語を明確に。",
    )

    temperature = st.slider("創造性 (temperature)", 0.0, 1.0, 0.3, 0.1)
    submitted = st.form_submit_button("リライトを実行", type="primary")

if submitted:
    if not source.strip():
        st.warning("元の文章を入力してください。")
        st.stop()

    system_instruction = (
        "あなたはプロの日本語編集者・校正者です。原文の意図を尊重しつつ、"
        "自然で読みやすい日本語に仕上げてください。"
    )

    output_format = (
        "# 修正後の文章\n（リライト後の本文）\n\n# 主な修正ポイント\n- ..."
        if show_diff
        else "リライト後の文章のみを出力してください。"
    )

    prompt = f"""以下の文章を処理してください。

# 処理モード
{mode}

# 目指す文体
{tone}

# 追加の指示
{instructions or "（なし）"}

# 原文
---
{source}
---

# 出力フォーマット
{output_format}
"""

    with st.spinner("リライト中..."):
        st.write_stream(generate_text_stream(prompt, system_instruction, temperature))
