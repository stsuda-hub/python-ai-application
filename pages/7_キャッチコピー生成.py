import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from utils.gemini_client import generate_text_stream

st.set_page_config(page_title="キャッチコピー生成", page_icon="💡", layout="wide")

st.title("キャッチコピー生成")
st.caption("商品・サービス・イベントなどのキャッチコピーを複数案提案します。")

with st.form("catch_form"):
    product = st.text_input("対象 (商品・サービス・イベント名)", placeholder="例: オンライン英会話サービス『LingoFlow』")
    features = st.text_area(
        "特徴・売り・独自性",
        height=140,
        placeholder="例: AI がレベルに合わせた会話相手になる / 24時間いつでも練習可能 / 月額1,980円",
    )
    target = st.text_input("ターゲット", placeholder="例: 仕事で英語を使う必要が出てきた20〜40代ビジネスパーソン")

    col1, col2 = st.columns(2)
    with col1:
        style = st.multiselect(
            "コピーのテイスト (複数選択可)",
            [
                "感情に訴えるエモーショナル",
                "シンプルで覚えやすい",
                "ベネフィット訴求",
                "問いかけ型",
                "擬音・リズム感",
                "逆説・意外性",
                "数字を使った具体性",
                "ストーリー型",
            ],
            default=["シンプルで覚えやすい", "ベネフィット訴求"],
        )
    with col2:
        count = st.number_input("提案数", 3, 20, 10)

    length_type = st.selectbox(
        "長さのタイプ",
        ["キャッチコピー (短め・15字前後)", "タグライン (中くらい・30字前後)", "ボディコピー (説明的・2〜3行)"],
    )

    temperature = st.slider("創造性 (temperature)", 0.0, 1.5, 1.0, 0.1)
    submitted = st.form_submit_button("コピーを生成", type="primary")

if submitted:
    if not product.strip() or not features.strip():
        st.warning("対象と特徴を入力してください。")
        st.stop()

    system_instruction = (
        "あなたは広告業界で活躍するコピーライターです。短く鋭く、記憶に残るコピーを日本語で提案してください。"
        "ありきたりな表現は避け、多様な切り口で提案します。"
    )

    style_text = "、".join(style) if style else "自由"

    prompt = f"""以下の情報からキャッチコピーを {count} 案提案してください。

# 対象
{product}

# 特徴・売り・独自性
{features}

# ターゲット
{target or "（特に指定なし）"}

# テイスト
{style_text}

# 長さのタイプ
{length_type}

# 出力フォーマット
番号付きリストで出力し、各案に「狙い」を一行で添えてください。

例:
1. コピー本文
   狙い: なぜこのコピーが刺さるかの一行説明
"""

    with st.spinner("コピーを生成中..."):
        st.write_stream(generate_text_stream(prompt, system_instruction, temperature))
