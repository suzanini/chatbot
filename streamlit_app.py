import streamlit as st
import openai  # 기존의 `from openai import OpenAI` 대신 이걸 사용하세요

# OpenAI 키 입력
openai_api_key = st.text_input("🔑 OpenAI API Key를 입력하세요", type="password")
if not openai_api_key:
    st.info("OpenAI 키를 입력하시면 추천이 시작됩니다!", icon="🗝️")
else:
    openai.api_key = openai_api_key  # 이렇게 설정해줘야 함

    # 추천 버튼 누르면 실행
    if st.button("🍿 드라마 & 시네마 탐색 시작!"):
        ...
        # GPT 호출 (스트리밍 미지원이므로 수정!)
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # 또는 "gpt-4", "gpt-3.5-turbo" 등
            messages=st.session_state.messages,
        )
        result = response["choices"][0]["message"]["content"]
        with st.chat_message("assistant"):
            st.markdown(result)
        st.session_state.messages.append({"role": "assistant", "content": result})
