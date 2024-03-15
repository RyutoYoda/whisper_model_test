import base64
import os
import openai
from dotenv import load_dotenv
import streamlit as st

# 環境変数を読み込む
load_dotenv()

st.title("VoiceCat🐈")

# サイドバーでAPIキーを設定
api_key = st.sidebar.text_input("OpenAI API Key", os.getenv("OPENAI_API_KEY"))
client = OpenAI(api_key=api_key)

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
            # 音声ファイルをバイナリモードで開く処理を削除し、直接file_uploaderからのファイルを渡す
            # 音声文字起こしを実行
            transcript_response = client.audio.transcriptions.create(
                model="whisper-1", file=audio_file, response_format="text"
            )
            transcript = transcript_response['data'][0]['text']
        st.success("音声文字起こしが完了しました！")
        st.text_area("文字起こし結果", transcript, height=250)
        # 文字起こし結果をダウンロードリンクで提供
        transcript_encoded = base64.b64encode(transcript.encode()).decode()
        st.markdown(
            f'<a href="data:file/txt;base64,{transcript_encoded}" download="transcript.txt">文字起こし結果をダウンロード</a>',
            unsafe_allow_html=True,
        )

    # 以下の要約処理は変更なし
    if transcript and st.button("テキストを要約する"):
        with st.spinner("テキスト要約を実行中です..."):
            # プロンプトとともにテキスト要約を実行
            summary_response = client.completions.create(
                model="text-davinci-003",  # または 'gpt-3.5-turbo' など、使用したいモデルに応じて変更
                prompt=f"{prompt}\n\n{transcript}",
                max_tokens=150,  # 要約の最大トークン数
                temperature=0.7
            )
            summary = summary_response.choices[0].text.strip()
        st.success("テキスト要約が完了しました！")
        st.text_area("要約結果", summary, height=150)
        # 要約結果をダウンロードリンクで提供
        summary_encoded = base64.b64encode(summary.encode()).decode()
        st.markdown(
            f'<a href="data:file/txt;base64,{summary_encoded}" download="summary.txt">要約結果をダウンロード</a>',
            unsafe_allow_html=True,
        )
else:
    st.info('音声ファイルをアップロードしてください。')

