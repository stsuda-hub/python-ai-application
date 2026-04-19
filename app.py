import streamlit as st

from utils.gemini_client import render_api_key_sidebar

st.set_page_config(
    page_title="AIライティングツール",
    page_icon="✍️",
    layout="wide",
)
render_api_key_sidebar()

st.title("AIライティングツール")
st.caption("Gemini API を使った個人用ライティングアシスタント")

st.markdown(
    """
    左のサイドバーから使いたいツールを選んでください。

    ### 利用できるツール

    | ツール | 用途 |
    | --- | --- |
    | ブログ記事作成 | テーマから本格的なブログ記事を生成 |
    | メール返信作成 | 受信メールへの返信文を作成 |
    | 文章要約 | 長文を指定の長さに要約 |
    | 文章リライト・校正 | 誤字脱字チェック・文体改善 |
    | 翻訳 | 多言語に対応した翻訳 |
    | SNS投稿文作成 | X / Instagram などへの投稿文を作成 |
    | キャッチコピー生成 | 商品・サービスのキャッチコピーを提案 |
    | 議事録整形 | 会議メモを構造化された議事録に整形 |

    ### 使い方

    1. 画面左のサイドバーに、[Google AI Studio](https://aistudio.google.com/) で取得した Gemini API キーを入力
    2. 使いたいツールのページを開く
    3. フォームに内容を入力して生成

    API キーはブラウザのセッションのみに保持され、サーバーには保存されません。
    ページを閉じると入力した API キーはクリアされます。
    """
)

with st.sidebar:
    st.header("このアプリについて")
    st.write(
        "複数のAIライティング機能を一つにまとめた個人用ツールです。"
        "各ページで入力内容を変えて、自由に文章を生成できます。"
    )
