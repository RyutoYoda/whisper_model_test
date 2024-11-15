import base64
import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
st.set_page_config(
    page_title="VoiceCat",
    page_icon="🐈"
)

# タイトルの表示
st.markdown('<h1 style="color: #FFA500;">VoiceCat🐈</h1>', unsafe_allow_html=True)

# 画像をタイトルの下に追加する関数
def load_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

image_path = "スクリーンショット 2024-05-16 12.33.11.png"  # 画像ファイルのパスを指定
image_base64 = load_image(image_path)
st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{image_base64}" alt="可愛い猫の画像" style="width: 100%;"/>
    </div>
    """,
    unsafe_allow_html=True
)

# スタイル設定
st.markdown("""
<style>
body {
    font-family: 'Helvetica Neue', sans-serif;
}
.big-font {
    font-size:50px !important;
    font-weight: bold;
    text-align: center;
    margin-bottom: 30px;
}
.header-font {
    font-size:30px !important;
    font-weight: bold;
    margin-bottom: 20px;
    color: #FFA500;
}
.subheader-font {
    font-size:20px !important;
    font-weight: bold;
    margin-bottom: 10px;
}
.container {
    border-radius: 10px;
    padding: 20px;
    box-shadow: none;
    margin-bottom: 20px;
    background-color: transparent !important;
}
.stButton>button {
    font-size: 16px !important;
    font-weight: bold !important;
    border-radius: 5px !important;
    width: 100%;
    padding: 10px;
}
.stTextInput>div>div>input {
    border-radius: 5px !important;
    border: 1px solid !important;
}
ul {
    list-style-type: none;
    padding: 0;
}
li {
    margin: 10px 0;
    padding: 10px;
    border-radius: 5px;
    box-shadow: none;
    background-color: transparent !important;
}
.header-container {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    text-align: center;
}
.sidebar-img {
    display: block;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 20px;
}
.main-content {
    display: flex;
    flex-direction: column;
    align-items: center;
}
.card {
    border-radius: 10px;
    box-shadow: none;
    margin: 20px;
    padding: 20px;
    width: 90%;
    max-width: 700px;
    text-align: left;
    background-color: transparent !important;
}
.card img {
    border-radius: 10px;
}
.sidebar .css-1d391kg {
    background-color: transparent !important;
}
@media (prefers-color-scheme: dark) {
    body {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    .big-font, .header-font {
        color: #FFA500;
    }
    .subheader-font {
        color: #a9a9a9;
    }
    .container, .card, li {
        background-color: transparent !important;
        box-shadow: none;
    }
    .stButton>button {
        background-color: #FFA500 !important;
        color: #282c34 !重要;
    }
    .stTextInput>div>div>input {
        border: 1px solid #FFA500 !重要;
        color: #ffffff !重要;
        background-color: #3c3f41 !重要;
    }
}
@media (prefers-color-scheme: light) {
    body {
        background-color: #f5f5f5;
        color: #333333;
    }
    .big-font, .header-font {
        color: #FFA500;
    }
    .subheader-font {
        color: #666666;
    }
    .container, .card, li {
        background-color: transparent !重要;
        box-shadow: none;
        color: #333333;
    }
    .stButton>button {
        background-color: #FFA500 !重要;
        color: #ffffff !重要;
    }
    .stTextInput>div>div>input {
        border: 1px solid #FFA500 !重要;
        color: #333333 !重要;
        background-color: #ffffff !重要;
    }
}
.stMarkdown {
    background-color: inherit;
    color: inherit;
}
</style>
""", unsafe_allow_html=True)

with st.expander("VoiceCatについて"):
    st.markdown("""
        VoiceCat🐈は、音声ファイルをテキストに変換し、そのテキストを指示に応じて処理、解析するアプリです。
        
        **使い方:**
        1. サイドバーからOpenAI APIキーを入力してください。(https://platform.openai.com/api-keys)
        2. 「処理内容の入力」に処理としてに行いたい指示を入力します（例: 「このテキストを要約してください」）。
        3. 「音声ファイルをアップロードしてください」セクションから、文字起こしを行いたい音声ファイルをアップロードしてください。
        4. 「音声文字起こしを実行する」ボタンを押して、アップロードした音声ファイルの文字起こしを行います。
        5. 文字起こし結果が表示された後、「処理を開始する」ボタンを押して、文字起こししたテキストの解析を行います。
        6. 処理結果が表示されます。必要に応じて処理結果をダウンロードすることもできます。
    """, unsafe_allow_html=True)

# APIキーの取得
api_key = st.sidebar.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY") or "")

if not api_key:
    st.error("サイドバーからAPIキーを入力してください。")
    st.stop()

client = OpenAI(api_key=api_key)

# プロンプトの入力（初期値を設定）
sidebar_prompt = st.sidebar.text_area(
    "処理内容の入力（例：このテキストを要約してください）",
    value="""以下のテンプレートを参考に音声を処理してください。　
    以下はあくまで参考です。
    この議事録について要点をまとめてください
"""
)

# 音声ファイルのアップロード
audio_file = st.file_uploader("音声ファイルをアップロードしてください", type=["m4a", "mp3", "webm", "mp4", "mpga", "wav"])

if audio_file is not None:
    st.audio(audio_file, format="audio/wav")

    if st.button("音声文字起こしを実行する"):
        with st.spinner("音声文字起こしを実行中です..."):
            transcript = client.audio.transcriptions.create(
                model="whisper-1", file=audio_file, response_format="text"
            )
        st.success("音声文字起こしが完了しました！")
        st.session_state.transcript = transcript  # 文字起こし結果をセッション状態に保存

# セッション状態に文字起こし結果がある場合に表示
if 'transcript' in st.session_state and st.session_state.transcript is not None:
    st.write(st.session_state.transcript)

# テキスト要約ボタン
if st.button("処理を開始する"):
    if 'transcript' in st.session_state and st.session_state.transcript is not None:
        prompt = sidebar_prompt + st.session_state.transcript  # promptにセッション状態の文字起こし結果を使用

        with st.spinner("処理を実行中です..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "ユーザーのプロンプトに基づき回答を生成してください"},
                    {"role": "user", "content": prompt}
                ]
            )
            summary_result = response.choices[0].message.content

            # 要約結果を表示
            st.write("処理結果:")
            st.write(summary_result)

            # 応答をバイトに変換し、それを base64 でエンコードする
            response_encoded = base64.b64encode(summary_result.encode()).decode()

            # ダウンロードリンクを作成
            st.markdown(
                f'<a href="data:file/txt;base64,{response_encoded}" download="summary_result.txt">処理結果をダウンロード</a>',
                unsafe_allow_html=True,
            )
    else:
        st.warning("音声文字起こしの結果がありません。音声文字起こしを実行してください。")

