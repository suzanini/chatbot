import streamlit as st
from openai import OpenAI

# ✅ 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# ✅ 이미지 삽입 (선택 사항)
st.image("image.png", caption="김경식의 영화대영화 감성으로 출발!", use_column_width=True)

st.title("🎬🎬 드라마 & 시네마 천국 🎬🎬")
st.write("GPT-4.0 mini 기반으로 재밌는 드라마, 영화를 추천해드립니다. 기분 따라, 취향 따라 골라보세요!")

openai_api_key = st.text_input("🔑 OpenAI API Key를 입력하세요", type="password")
if not openai_api_key:
    st.info("OpenAI 키를 입력하시면 추천이 시작됩니다!", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # 콘텐츠 종류
    content_type = st.radio("🎞️ 보고 싶은 콘텐츠는?", ["드라마", "영화", "둘 다"])

    # 장르
    genre_options = ["로맨스", "스릴러", "코미디", "공포", "판타지", "SF", "액션", "감동"]
    selected_genres = st.multiselect("🎭 좋아하는 장르를 골라보세요!", genre_options)

    # 국가
    country_options = ["한국_

