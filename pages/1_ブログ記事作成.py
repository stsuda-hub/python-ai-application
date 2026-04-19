import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from utils.gemini_client import generate_text_stream

st.set_page_config(page_title="ブログ記事作成", page_icon="📝", layout="wide")

st.title("ブログ記事作成")
st.caption("テーマとキーワードから本格的なブログ記事を生成します。")

with st.form("blog_form"):
    topic = st.text_input("記事のテーマ", placeholder="例: 在宅ワークの生産性を上げる方法")
    keywords = st.text_input("含めたいキーワード（カンマ区切り）", placeholder="例: ポモドーロ, 集中力, リモートワーク")
    target = st.text_input("想定読者", value="ビジネスパーソン", placeholder="例: 副業を始めたい会社員")

    col1, col2, col3 = st.columns(3)
    with col1:
        tone = st.selectbox(
            "文章のトーン",
            ["丁寧・フォーマル", "フレンドリー・カジュアル", "専門的・解説的", "情熱的・モチベーショナル"],
        )
    with col2:
        length = st.selectbox("記事のボリューム", ["短め (約800字)", "標準 (約2000字)", "長め (約4000字)"])
    with col3:
        structure = st.selectbox(
            "構成",
            ["見出し付きの解説記事", "リスト形式のまとめ記事", "ストーリー仕立ての体験談", "Q&A形式"],
        )

    temperature = st.slider("創造性 (temperature)", 0.0, 1.5, 0.8, 0.1)
    submitted = st.form_submit_button("記事を生成", type="primary")

if submitted:
    if not topic:
        st.warning("テーマを入力してください。")
        st.stop()

    system_instruction = (
        "あなたはプロのブログライターです。読者の興味を引く構成で、"
        "わかりやすく説得力のある記事を日本語で執筆してください。"
        "見出しは Markdown 形式 (##, ###) を使用してください。"
    )

    prompt = f"""以下の条件でブログ記事を執筆してください。

# テーマ
{topic}

# 含めたいキーワード
{keywords or "（指定なし）"}

# 想定読者
{target}

# 文章のトーン
{tone}

# ボリューム
{length}

# 構成
{structure}

# 要件
- 冒頭に読者の関心を引く導入文を書く
- 本文は論理的な流れで構成する
- 最後に要点をまとめる
- SEO を意識して自然にキーワードを含める
"""

    with st.spinner("記事を生成中..."):
        st.write_stream(generate_text_stream(prompt, system_instruction, temperature))
