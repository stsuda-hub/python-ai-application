import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from utils.gemini_client import generate_text_stream, render_api_key_sidebar

st.set_page_config(page_title="議事録整形", page_icon="📋", layout="wide")
render_api_key_sidebar()

st.title("議事録整形")
st.caption("会議のメモや文字起こしを、構造化された議事録に整形します。")

with st.form("minutes_form"):
    memo = st.text_area(
        "会議メモ・文字起こし",
        height=320,
        placeholder="会議中のメモや文字起こしをそのまま貼り付けてください。",
    )

    col1, col2 = st.columns(2)
    with col1:
        meeting_name = st.text_input("会議名", placeholder="例: 4月プロダクト定例")
    with col2:
        meeting_date = st.text_input("開催日", placeholder="例: 2026-04-18")

    attendees = st.text_input("出席者", placeholder="例: 山田、佐藤、鈴木")

    col3, col4 = st.columns(2)
    with col3:
        style = st.selectbox(
            "出力スタイル",
            [
                "標準 (見出し + 箇条書き)",
                "詳細 (発言内容を時系列で再構成)",
                "簡潔 (決定事項・ToDoのみ)",
            ],
        )
    with col4:
        extract_todos = st.checkbox("ToDo を担当者付きで抽出", value=True)

    temperature = st.slider("創造性 (temperature)", 0.0, 0.8, 0.2, 0.1)
    submitted = st.form_submit_button("議事録を生成", type="primary")

if submitted:
    if not memo.strip():
        st.warning("会議メモを入力してください。")
        st.stop()

    system_instruction = (
        "あなたは議事録作成のプロです。会議の主要な論点、決定事項、次のアクションを"
        "抜け漏れなく整理し、読みやすい構造化された議事録を日本語で作成してください。"
        "原文にない内容は創作しないこと。"
    )

    todo_section = (
        "- ToDo は『担当者 / 期日 / 内容』の表形式でまとめる\n"
        if extract_todos
        else ""
    )

    prompt = f"""以下のメモから議事録を作成してください。

# 会議情報
- 会議名: {meeting_name or "（未指定）"}
- 開催日: {meeting_date or "（未指定）"}
- 出席者: {attendees or "（未指定）"}

# スタイル
{style}

# 出力要件
- 冒頭に会議情報をまとめる
- 議題ごとにセクション分け
- 決定事項を明確に記載
{todo_section}- 曖昧な点は『要確認』として残す

# 元メモ
---
{memo}
---
"""

    with st.spinner("議事録を作成中..."):
        st.write_stream(generate_text_stream(prompt, system_instruction, temperature))
