import base64
import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from io import BytesIO

# 環境変数を読み込む
load_dotenv()

st.title("VoiceCat🐈")

# サイドバーでAPIキーを設定
api_key = st.sidebar.text_input("OpenAI API Key", os.getenv("OPENAI_API_KEY"))
client = OpenAI(api_key=api_key)

# サイドバーにプロンプト入力フィールドを追加
prompt = st.sidebar.text_area("要約のプロンプト", "このテキストを要約してください。")
audio_file = st.file_uploader(
    "音声ファイルをアップロードしてください", type=["m4a", "mp3", "webm", "mp4", "mpga", "wav"]
)

if audio_file is not None:
    st.audio(audio_file, format="audio/wav")

    if st.button("音声文字起こしを実行する"):
        with st.spinner("音声文字起こしを実行中です..."):
            transcript = client.audio.transcriptions.create(
                model="whisper-1", file=audio_file, response_format="text"
            )
        st.success("音声文字起こしが完了しました！")
        st.write(transcript)

        # 文字起こしをバイトに変換し、それをbase64でエンコードする
        transcript_encoded = base64.b64encode(transcript.encode()).decode()
        # ダウンロードリンクを作成する
        st.markdown(
            f'<a href="data:file/txt;base64,{transcript_encoded}" download="transcript.txt">Download Result</a>',
            unsafe_allow_html=True,
        )

if st.button("テキストを要約する"):
    # 音声文字起こしの結果とサイドバーでの指示を組み合わせる
    combined_prompt = f"{prompt}\n\n{transcript}" if 'transcript' in locals() else prompt

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": combined_prompt}
    ]

    with st.spinner("テキスト要約を実行中です..."):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        # 応答から要約テキストを取得する方法を改善
        try:
            summary = response.choices[0].message['content'] if response.choices else "要約を取得できませんでした。"
        except AttributeError:
            summary = "要約テキストの取得中にエラーが発生しました。"

        st.success("テキスト要約が完了しました！")
        st.text_area("要約結果", summary, height=150)

        summary_encoded = base64.b64encode(summary.encode()).decode()
        st.markdown(
            f'<a href="data:file/txt;base64,{summary_encoded}" download="summary.txt">要約結果をダウンロード</a>',
            unsafe_allow_html=True,
        )

