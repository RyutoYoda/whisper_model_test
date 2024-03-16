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
sidebar_prompt = st.sidebar.text_area("要約のプロンプト", "このテキストを要約してください。")
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
    # 変数名を修正して、サイドバーのプロンプトとトランスクリプトを結合
    prompt = sidebar_prompt
    if 'transcript' in locals():
        prompt += f"\n\n{transcript}" 
    with st.spinner("テキスト要約を実行中です..."):
        
        response = client.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt},  # 変更: ユーザーメッセージを追加
                {"role": "assistant"}  # 変更: アシスタントの役割を定義
            ]
        )
        # 応答オブジェクトをそのまま表示
        st.text_area("要約結果", str(response))

        # 応答をバイトに変換し、それをbase64でエンコードする
        response_encoded = base64.b64encode(str(response).encode()).decode()

        # ダウンロードリンクを作成する
        st.markdown(
            f'<a href="data:file/txt;base64,{response_encoded}" download="summary_response.txt">要約結果をダウンロード</a>',
            unsafe_allow_html=True,
        )

