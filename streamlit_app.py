import streamlit as st
from openai import OpenAI

st.title("🎬🎬 드라마 & 시네마 천국 🎬🎬")
st.write(
    "GPT-4.0 mini를 기반으로 재밌는 드라마, 영화를 추천해드립니다. "
    "드라마 & 시네마 천국으로 떠나 보아요"
)

openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("OpenAI 키를 입력하세요.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # 콘텐츠 유형
    content_type = st.radio("보고 싶은 콘텐츠는?", ["드라마", "영화", "둘다"])

    # 장르 선택
    genre_options = ["로맨스", "스릴러", "코미디", "공포", "판타지", "SF", "액션", "감동"]
    selected_genres = st.multiselect("좋아하는 장르를 골라보세요!", genre_options)

    # 국가 선택
    country_options = ["한국", "미국", "일본", "다좋아"]
    selected_countries = st.multiselect("선호하는 나라를 골라보세요!", country_options)

    # 제작 연도 범위 슬라이더
    selected_year_range = st.slider(
        "제작된 연도 범위를 선택하세요!",
        min_value=1895,
        max_value=2025,
        value=(2000, 2025),
        step=1
    )

    # 버튼 클릭 시 추천 시작
    if st.button("🎬🍿 드라마 & 시네마 탐색 🎬🍿"):

        # 요약 문장 출력
        summary = f"""
        저는 {content_type}를 좋아하고, 
        {' / '.join(selected_genres) if selected_genres else '모든 장르'} 장르를 선호하며, 
        {' / '.join(selected_countries) if selected_countries else '모든 국가'} 작품을 좋아해요. 
        그리고 {selected_year_range[0]}년부터 {selected_year_range[1]}년 사이의 작품을 찾고 있어요.
        """
        st.markdown(f"💬 {summary.strip()}")

        # 프롬프트 구성
        full_prompt = f"""
        아래 조건에 맞는 {content_type}를 5개 추천해주세요.

        [조건]
        - 장르: {', '.join(selected_genres) if selected_genres else '모든 장르'}
        - 국가: {', '.join(selected_countries) if selected_countries else '모든 국가'}
        - 제작 연도: {selected_year_range[0]}년 ~ {selected_year_range[1]}년
        - 형식: 리스트
        - 각 항목은 다음 정보 포함
          1. 제목 (제작 연도는 괄호에 표기, 예: 사랑의 불시착(2019))
          2. 간단한 설명 (5줄 이하)

        추천 시작!
        """

        # GPT 응답 받기
        messages = [{"role": "user", "content": full_prompt}]
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            stream=True,
        )

        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        # 저장
        st.session_state.messages = [{"role": "user", "content": full_prompt},
                                     {"role": "assistant", "content": response}]
