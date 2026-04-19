import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from utils.gemini_client import generate_text_stream, render_api_key_sidebar

st.set_page_config(page_title="SNS投稿文作成", page_icon="📱", layout="wide")
render_api_key_sidebar()

st.title("SNS投稿文作成")
st.caption("伝えたい内容から、各SNSに最適化された投稿文を作成します。")

PLATFORMS = {
    "X (旧Twitter)": "140〜280字以内。簡潔でインパクトがあり、ハッシュタグは2〜3個まで。",
    "Instagram": "親しみやすく、絵文字は使わず、5〜10個のハッシュタグを末尾にまとめる。300字前後。",
    "Facebook": "少し長めでストーリー性のある文章。読者への問いかけを含める。400〜600字。",
    "LinkedIn": "プロフェッショナルで示唆に富んだ文体。業界インサイトや学びを含める。500〜800字。",
    "note": "見出しと本文で構成された、読みやすいエッセイ風の投稿。800〜1500字。",
    "TikTok / Reels キャプション": "短くキャッチーで、動画を見たくなる引きのある一文。",
}

with st.form("sns_form"):
    content = st.text_area(
        "投稿で伝えたい内容",
        height=160,
        placeholder="例: 新しく発売したオンライン講座の告知。対象は副業を始めたい会社員。",
    )

    col1, col2 = st.columns(2)
    with col1:
        platforms = st.multiselect(
            "対象プラットフォーム",
            list(PLATFORMS.keys()),
            default=["X (旧Twitter)", "Instagram"],
        )
    with col2:
        tone = st.selectbox(
            "トーン",
            ["親しみやすい", "プロフェッショナル", "熱量高め・煽り気味", "冷静・論理的", "ユーモラス"],
        )

    col3, col4 = st.columns(2)
    with col3:
        cta = st.text_input("促したい行動 (CTA)", placeholder="例: プロフィールのリンクから申込み")
    with col4:
        variants = st.number_input("バリエーション数", 1, 5, 3)

    temperature = st.slider("創造性 (temperature)", 0.0, 1.5, 0.9, 0.1)
    submitted = st.form_submit_button("投稿文を作成", type="primary")

if submitted:
    if not content.strip() or not platforms:
        st.warning("投稿内容と対象プラットフォームを指定してください。")
        st.stop()

    system_instruction = (
        "あなたはSNSマーケティングのプロです。各プラットフォームの特性を理解し、"
        "ユーザーの反応を最大化する投稿文を日本語で作成してください。"
    )

    platform_specs = "\n".join(f"- {p}: {PLATFORMS[p]}" for p in platforms)

    prompt = f"""以下の条件でSNS投稿文を作成してください。

# 伝えたい内容
{content}

# 対象プラットフォームと特性
{platform_specs}

# トーン
{tone}

# 促したい行動 (CTA)
{cta or "（特になし）"}

# バリエーション数
各プラットフォームにつき {variants} 案

# 出力フォーマット
プラットフォームごとにセクションを分け、案ごとに番号を付けてください。
"""

    with st.spinner("投稿文を作成中..."):
        st.write_stream(generate_text_stream(prompt, system_instruction, temperature))
