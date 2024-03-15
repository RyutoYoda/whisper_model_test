import base64
import os

import streamlit as st
from dotenv import load_dotenv
import openai

# 環境変数を読み込む
load_dotenv()

st.title("VoiceCat🐈")

# サイドバーでAPIキーを設定
api_key = st.sidebar.text_input("OpenAI API Key", os.getenv("OPENAI_API_KEY"))
openai.api_key = api_key

# サイドバーにプロンプト入力フィールドを追加
prompt = st.sidebar.text_area("要約のプロンプト", "このテキストを要約してください。")

# 音声ファイルをアップロードしてください
audio_file = st.file_uploader("音声ファイルをアップロードしてください", type=["m4a", "mp3", "webm", "mp4", "mpga", "wav"])

if audio_file is not None:
    st.audio(audio_file, format="audio/wav")
    transcript = ""  # 文字起こし結果を格納する変数

    # 音声を文字起こしするボタン
    if st.button("音声を文字起こしする"):
        with st.spinner("音声文字起こしを実行中です..."):
            # 音声文字起こしを実行
            transcript_response = openai.Audio.create(
                audio=audio_file.getvalue(), 
                model="whisper-1"
            )
            transcript = transcript_response['data'][0]['text']
        st.success("音声文字起こしが完了しました！")
        st.text_area("文字起こし結果", transcript, height=250)

    # テキストを要約するボタン（文字起こし結果が存在する場合のみ表示）
    if transcript and st.button("テキストを要約する"):
        with st.spinner("テキスト要約を実行中です..."):
            # プロンプトとともにテキスト要約を実行
            summary_response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"{prompt}\n\n{transcript}",
                max_tokens=150,
                temperature=0.7
            )
            summary = summary_response['choices'][0]['text'].strip()
        st.success("テキスト要約が完了しました！")
        st.text_area("要約結果", summary, height=150)
else:
    st.info('音声ファイルをアップロードしてください。')

