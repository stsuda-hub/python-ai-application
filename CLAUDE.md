# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 概要

個人用の AI ライティングツール。Streamlit のマルチページ構成で、ブログ記事・メール返信・要約・翻訳などの各機能を 1 つのアプリにまとめている。認証・DB・ユーザー管理は持たない。

## 開発コマンド

```bash
pip install -r requirements.txt
streamlit run app.py                         # アプリ起動 (デフォルト http://localhost:8501)
streamlit run app.py --server.port 8502      # ポート変更
python -c "from utils.gemini_client import generate_text; print(generate_text('ping'))"  # API疎通確認
```

`.env` は `.env.example` をコピーして作成。`GEMINI_API_KEY` 必須、`GEMINI_MODEL`（デフォルト `gemini-2.5-flash`）で差し替え可能。

## アーキテクチャ

### 3 層構成

1. **`app.py`** — ホーム画面（ランディング）。ツール紹介のみで、生成処理は持たない。
2. **`pages/N_<ツール名>.py`** — Streamlit 規約に従い `pages/` 配下のファイルが自動でサイドバーに並ぶ。各ページは独立しており、他ページを import しない。
3. **`utils/gemini_client.py`** — 全ページ共通の Gemini 呼び出し層。API キーの解決・クライアント生成・テキスト生成をここに集約。

ページ → `utils.gemini_client.generate_text_stream(...)` → Gemini API の一方向依存。ページ間でのデータ共有や状態永続化は意図的に持たない（個人用・ステートレス）。

### Gemini SDK

**新しい `google-genai` (from google import genai) を使用**。旧 `google-generativeai` ではない。API は `client.models.generate_content(model=..., contents=..., config=types.GenerateContentConfig(...))` の形。`system_instruction` と `temperature` は `GenerateContentConfig` 経由で渡す。

`utils/gemini_client.py` のクライアントは `@st.cache_resource` でシングルトン化されている。リロードしても再生成されない前提で設計している。

### ページの定型パターン

各ページは以下の共通構造を持つ。新しいツールを追加するときはこれを踏襲すること：

1. 冒頭で `sys.path.append(str(Path(__file__).resolve().parent.parent))` — Streamlit の `pages/` は親ディレクトリを自動で path に入れないので必要。
2. `st.set_page_config(page_title=..., page_icon=..., layout="wide")` — **各ページで必ず呼ぶ**（サイドバーのタイトル・タブ名になる）。
3. `with st.form(...)` で入力をまとめて受け取り、`st.form_submit_button` でまとめて送信。
4. `generate_text_stream(prompt, system_instruction, temperature)` を `st.write_stream(...)` に渡してストリーミング表示。

`system_instruction` には「役割（例: プロのコピーライター）」と「出力言語・フォーマットの制約」を書く。`prompt` 側はユーザー入力を構造化した Markdown 見出し形式（`# テーマ` `# トーン` など）で組み立てる — このプロジェクトの全ページが同じ書き方をしているので、揃えること。

### 新ツールを追加する場合

`pages/` に `N_<名前>.py` を作成し、既存ページ（例: `pages/3_文章要約.py`）をテンプレートとしてコピーするのが最短。番号 `N` がサイドバー表示順を決める。`app.py` のツール一覧テーブルにも 1 行追加する。

## 注意点

- ページファイル名・ホーム画面の文言は日本語。UI・プロンプト・出力も日本語前提。英語化する場合は `system_instruction` の「日本語で」という指示を忘れず変更する。
- `temperature` の既定値はツール特性で使い分けている（校正・翻訳・議事録は低め 0.2〜0.3、ブログ・SNS・コピーは高め 0.8〜1.0）。新ページを追加するときも用途に合わせること。
- `.streamlit/secrets.toml` からのキー読み込みもフォールバックとして対応済み（`utils/gemini_client.py:get_api_key`）。Streamlit Community Cloud にデプロイする場合はこちらを使う。
