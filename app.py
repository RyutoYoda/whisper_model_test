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
  # ローカル変数 `transcript` の存在をチェック
  if 'transcript' in locals():
    # 音声文字起こしがある場合、そのテキストを使用
    text_to_summarize = transcript
  else:
    # 音声文字起こしがない場合、サイドバーからの入力を使用
    text_to_summarize = prompt

  # 要約するテキストのプロンプトを作成
  summary_prompt = f"このテキストを要約してください: {text_to_summarize}"

  with st.spinner("テキスト要約を実行中です..."):
    # テキスト要約を実行
    summary_response = client.Completion.create(
      engine="text-davinci-003", # あなたの使用しているモデルに適したエンジン名に置き換えてください
      prompt=summary_prompt,
      max_tokens=150,
      temperature=0.7
    )
    summary = summary_response['choices'][0]['text'].strip()
    st.success("テキスト要約が完了しました！")
    st.text_area("要約結果", summary, height=150)

    # 要約をバイトに変換し、それをbase64でエンコードする
    summary_encoded = base64.b64encode(summary.encode()).decode()

    # ダウンロードリンクを作成する
    st.markdown(
      f'<a href="data:file/txt;base64,{summary_encoded}" download="summary.txt">要約結果をダウンロード</a>',
      unsafe_allow_html=True,
    )
