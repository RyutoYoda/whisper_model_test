import base64
import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="VoiceCat",
    page_icon="🐈",
    layout="centered"
)

# Custom CSS for styling
st.markdown("""
    <style>
        body {
            background-color: #000000;
            color: #FFFFFF;
        }
        .main {
            background-color: #333333;
            color: #FFFFFF;
            padding: 20px;
            border-radius: 10px;
        }
        .stButton > button {
            background-color: #007BFF;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
        }
        .stTextInput > div > input {
            border-radius: 10px;
            background-color: #555555;
            color: #FFFFFF;
        }
        .stFileUploader > div > div {
            background-color: #555555;
        }
        .header {
            text-align: center;
            padding: 20px;
            background-color: #000000;
        }
        .header img {
            width: 200px;
            margin: 0 auto;
        }
        .header h1 {
            color: #007BFF;
        }
        .stExpander {
            background-color: #222222;
            border-radius: 10px;
        }
        .stExpander > div > div {
            color: #FFFFFF;
        }
    </style>
""", unsafe_allow_html=True)

# Page title with logo
st.markdown("""
    <div class="header">
        <img src="https://example.com/logo.png" alt="VoiceCat Logo">
        <h1>VoiceCat🐈</h1>
    </div>
""", unsafe_allow_html=True)

# About section
with st.expander("VoiceCatについて"):
    st.write("""
        VoiceCat🐈は、音声ファイルをテキストに変換し、そのテキストを指示に応じて処理、解析するアプリです。
        
        **使い方:**
        1. サイドバーからOpenAI APIキーを入力してください。(https://platform.openai.com/api-keys)
        2. 「処理内容の入力」に処理としてに行いたい指示を入力します（例: 「このテキストを要約してください」）。
        3. 「音声ファイルをアップロードしてください」セクションから、文字起こしを行いたい音声ファイルをアップロードしてください。
        4. 「音声文字起こしを実行する」ボタンを押して、アップロードした音声ファイルの文字起こしを行います。
        5. 文字起こし結果が表示された後、「処理を開始する」ボタンを押して、文字起こししたテキストの解析を行います。
        6. 処理結果が表示されます。必要に応じて処理結果をダウンロードすることもできます。
    """)

# Get API key from sidebar
api_key = st.sidebar.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY") or "")

if not api_key:
    st.error("サイドバーからAPIキーを入力してください。")
    st.stop()

client = OpenAI(api_key=api_key)

# Get prompt from sidebar
sidebar_prompt = st.sidebar.text_input("処理内容の入力（例：このテキストを要約してください）")

# Upload audio file
audio_file = st.file_uploader("音声ファイルをアップロードしてください", type=["m4a", "mp3", "webm", "mp4", "mpga", "wav"])

if audio_file is not None:
    st.audio(audio_file, format="audio/wav")

    if st.button("音声文字起こしを実行する"):
        with st.spinner("音声文字起こしを実行中です..."):
            transcript = client.audio.transcriptions.create(
                model="whisper-1", file=audio_file, response_format="text"
            )
        st.success("音声文字起こしが完了しました！")
        st.session_state.transcript = transcript  # Save transcription result to session state

# Display transcription result if available
if 'transcript' in st.session_state and st.session_state.transcript is not None:
    st.write(st.session_state.transcript)

# Button to process transcription
if st.button("処理を開始する"):
    if 'transcript' in st.session_state and st.session_state.transcript is not None:
        prompt = sidebar_prompt + st.session_state.transcript  # Use transcription result in prompt

        with st.spinner("処理を実行中です..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "ユーザーのプロンプトに基づき回答を生成してください"},
                    {"role": "user", "content": prompt}
                ]
            )
            summary_result = response.choices[0].message.content

            # Display summary result
            st.write("処理結果:")
            st.write(summary_result)

            # Convert response to bytes and encode it in base64
            response_encoded = base64.b64encode(summary_result.encode()).decode()

            # Create download link
            st.markdown(
                f'<a href="data:file/txt;base64,{response_encoded}" download="summary_result.txt">処理結果をダウンロード</a>',
                unsafe_allow_html=True,
            )
    else:
        st.warning("音声文字起こしの結果がありません。音声文字起こしを実行してください。")
