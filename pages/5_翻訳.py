import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from utils.gemini_client import generate_text_stream

st.set_page_config(page_title="翻訳", page_icon="🌐", layout="wide")

st.title("翻訳")
st.caption("多言語間の翻訳を行います。トーンや用途に合わせた自然な訳文を生成します。")

LANGUAGES = [
    "自動検出",
    "日本語",
    "英語",
    "中国語 (簡体字)",
    "中国語 (繁体字)",
    "韓国語",
    "フランス語",
    "ドイツ語",
    "スペイン語",
    "イタリア語",
    "ポルトガル語",
    "ロシア語",
    "タイ語",
    "ベトナム語",
    "インドネシア語",
]

with st.form("translate_form"):
    source = st.text_area("翻訳したい文章", height=240, placeholder="翻訳元の文章を入力してください。")

    col1, col2 = st.columns(2)
    with col1:
        source_lang = st.selectbox("翻訳元の言語", LANGUAGES, index=0)
    with col2:
        target_lang = st.selectbox(
            "翻訳先の言語",
            [lang for lang in LANGUAGES if lang != "自動検出"],
            index=1,
        )

    col3, col4 = st.columns(2)
    with col3:
        style = st.selectbox(
            "翻訳のスタイル",
            ["自然な口語", "ビジネス・フォーマル", "学術的・正確", "カジュアル・親しみやすい", "文学的・豊かな表現"],
        )
    with col4:
        include_notes = st.checkbox("訳注・補足説明を付ける", value=False)

    temperature = st.slider("創造性 (temperature)", 0.0, 1.0, 0.3, 0.1)
    submitted = st.form_submit_button("翻訳する", type="primary")

if submitted:
    if not source.strip():
        st.warning("翻訳したい文章を入力してください。")
        st.stop()

    system_instruction = (
        "あなたは熟練した翻訳者です。原文のニュアンスを保ちつつ、"
        "ターゲット言語として自然で読みやすい訳文を作成してください。"
    )

    notes_requirement = (
        "翻訳本文のあとに、訳しにくかった箇所や文化的な補足があれば『# 訳注』のセクションを追加してください。"
        if include_notes
        else "訳文のみを出力してください。"
    )

    prompt = f"""以下の文章を翻訳してください。

# 翻訳元の言語
{source_lang}

# 翻訳先の言語
{target_lang}

# スタイル
{style}

# 原文
---
{source}
---

# 出力要件
{notes_requirement}
"""

    with st.spinner("翻訳中..."):
        st.write_stream(generate_text_stream(prompt, system_instruction, temperature))
