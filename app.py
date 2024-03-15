import base64
import os
import streamlit as st
from dotenv import load_dotenv
import openai
from io import BytesIO

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

    # 音声を文字起こしするボタン
    if st.button("音声を文字起こしする"):
        with st.spinner("音声文字起こしを実行中です..."):
            # BytesIOオブジェクトを作成
            audio_bytes = BytesIO(audio_file.read())
            
            # 音声文字起こしを実行
            transcription = openai.Audio.transcribe("whisper-1", audio_bytes)

            st.success("音声文字起こしが完了しました！")
            st.text_area("文字起こし結果", transcription["text"], height=150)

            # 文字起こしをバイトに変換し、それをbase64でエンコードする
            transcript_encoded = base64.b64encode(transcription["text"].encode()).decode()

            # ダウンロードリンクを作成する
            st.markdown(
                f'<a href="data:file/txt;base64,{transcript_encoded}" download="transcript.txt">文字起こし結果をダウンロード</a>',
                unsafe_allow_html=True,
            )

    # テキストを要約するボタン
    if st.button("テキストを要約する"):
        if 'transcription' in locals():
            with st.spinner("テキスト要約を実行中です..."):
                # プロンプトとともにテキスト要約を実行
                summary_response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=f"{prompt}\n\n{transcription['text']}",
                    max_tokens=150,
                    temperature=0.7
                )
                summary = summary_response.choices[0].text.strip()
                st.success("テキスト要約が完了しました！")
                st.text_area("要約結果", summary, height=150)

                # 要約をバイトに変換し、それをbase64でエンコードする
                summary_encoded = base64.b64encode(summary.encode()).decode()

                # ダウンロードリンクを作成する
                st.markdown(
                    f'<a href="data:file/txt;base64,{summary_encoded}" download="summary.txt">要約結果をダウンロード</a>',
                    unsafe_allow_html=True,
                )
        else:
            st.error("まずは「音声を文字起こしする」を実行してください。")
