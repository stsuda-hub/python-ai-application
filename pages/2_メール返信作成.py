import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from utils.gemini_client import generate_text_stream

st.set_page_config(page_title="メール返信作成", page_icon="✉️", layout="wide")

st.title("メール返信作成")
st.caption("受信したメールと返信の意図を入力すると、返信文を作成します。")

with st.form("mail_form"):
    received = st.text_area(
        "受信したメール本文",
        height=220,
        placeholder="受け取ったメールの本文をそのまま貼り付けてください。",
    )
    intent = st.text_area(
        "返信で伝えたい内容",
        height=120,
        placeholder="例: 依頼は引き受ける。スケジュールは来週月曜からで調整したい。",
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        relation = st.selectbox(
            "相手との関係",
            ["社外・取引先", "社内・上司", "社内・同僚", "社内・部下", "顧客・お客様", "友人・知人"],
        )
    with col2:
        tone = st.selectbox(
            "文章のトーン",
            ["丁寧・ビジネス", "フォーマル (非常に丁寧)", "カジュアル", "簡潔・端的"],
        )
    with col3:
        length = st.selectbox("長さ", ["短め", "標準", "やや詳しめ"])

    sender_name = st.text_input("差出人の署名 (任意)", placeholder="例: 山田 太郎 / 株式会社〇〇")

    temperature = st.slider("創造性 (temperature)", 0.0, 1.2, 0.4, 0.1)
    submitted = st.form_submit_button("返信文を作成", type="primary")

if submitted:
    if not received or not intent:
        st.warning("受信メールと返信内容の両方を入力してください。")
        st.stop()

    system_instruction = (
        "あなたは日本語ビジネスメールの作成に長けたアシスタントです。"
        "受信メールの文脈と送信者の意図を汲み取り、失礼のない自然な返信を作成してください。"
        "件名、宛名、本文、結びの挨拶、署名を含む完全なメール形式で出力します。"
    )

    prompt = f"""以下の条件で返信メールを作成してください。

# 受信したメール
{received}

# 返信で伝えたい内容
{intent}

# 相手との関係
{relation}

# トーン
{tone}

# 長さ
{length}

# 差出人の署名
{sender_name or "（未指定。「〇〇」などのプレースホルダで記載）"}

# 出力フォーマット
件名: ...
---
（本文）
"""

    with st.spinner("返信文を作成中..."):
        st.write_stream(generate_text_stream(prompt, system_instruction, temperature))
