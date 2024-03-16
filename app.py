import base64
import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

st.title("VoiceCat🐈")

api_key = st.sidebar.text_input("OpenAI API Key", os.getenv("OPENAI_API_KEY"))
client = OpenAI(api_key=api_key)
sidebar_prompt = st.sidebar.text_input("プロンプトの入力（例：このテキストを要約してください）")

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

if st.button("テキストを要約する"):
    if 'transcript' in locals():
        prompt = sidebar_prompt + transcript

        if prompt.strip() != "":
            with st.spinner("テキスト要約を実行中です..."): 
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "ユーザーのプロンプトに基づき回答を生成してください"},
                        {"role": "user", "content": prompt}
                    ]
                )
                summary_result = response.choices[0].message.content

                # 要約結果を表示
                st.write(summary_result)

                # 応答をバイトに変換し、それを base64 でエンコードする
                response_encoded = base64.b64encode(summary_result.encode()).decode()

                # ダウンロードリンクを作成する際に、ファイル名を明示的に指定
                st.markdown(
                    f'<a href="data:file/txt;base64,{response_encoded}" download="summary_result.txt">要約結果をダウンロード</a>',
                    unsafe_allow_html=True,
                )
        else:
            st.warning("要約のプロンプトが空です。テキスト要約のプロンプトを入力してください。")
