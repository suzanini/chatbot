import streamlit as st
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO

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

    content_type = st.radio("보고 싶은 콘텐츠는?", ["드라마", "영화", "둘다"])
    genre_options = ["로맨스", "스릴러", "코미디", "공포", "판타지", "SF", "액션", "감동"]
    selected_genres = st.multiselect("좋아하는 장르를 골라보세요!", genre_options)
    country_options = ["한국", "미국", "일본", "다좋아"]
    selected_countries = st.multiselect("선호하는 나라를 골라보세요!", country_options)

    # 버튼 클릭 시 추천 시작
    if st.button("🎬🍿 드라마 & 시네마 탐색 🎬🍿"):

        # 유저 선택 문장 생성
        user_summary = f"저는 {content_type}를 좋아하고, "
        user_summary += f"{' / '.join(selected_genres) if selected_genres else '모든 장르'} 장르를 선호하며, "
        user_summary += f"{' / '.join(selected_countries) if selected_countries else '모든 국가'} 작품을 좋아해요."
        st.markdown(f"💬 {user_summary}")

        # 프롬프트 구성
        full_prompt = f"""
        아래 조건에 맞는 {content_type}를 5개 추천해주세요.

        [조건]
        - 장르: {', '.join(selected_genres) if selected_genres else '모든 장르'}
        - 국가: {', '.join(selected_countries) if selected_countries else '모든 국가'}
        - 형식: 리스트
        - 각 항목은 다음 정보 포함
          1. 제목 (제작 연도는 괄호에 표기, 예: 사랑의 불시착(2019))
          2. 간단한 설명 (5줄 이하)

        추천 시작!
        """

        # GPT 호출
        messages = [{"role": "user", "content": full_prompt}]
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            stream=True,
        )

        # 스트리밍 결과 표시
        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        # GPT 응답을 세션에 저장
        st.session_state.messages = [{"role": "user", "content": full_prompt},
                                     {"role": "assistant", "content": response}]

        # 첫 번째 추천 항목 제목 파싱
        import re
        first_item_match = re.search(r"\d\.\s*([^\(]+)\((\d{4})\)", response)
        if first_item_match:
            first_title = first_item_match.group(1).strip()
            first_year = first_item_match.group(2).strip()
            search_query = f"{first_title} {first_year} poster"

            # 이미지 검색 (DuckDuckGo or Bing 등 API 필요. 예시로 Unsplash 사용)
            try:
                img_url = f"https://source.unsplash.com/featured/?{first_title.replace(' ', '%20')},movie"
                response_img = requests.get(img_url)
                img = Image.open(BytesIO(response_img.content))
                st.image(img, caption=f"{first_title}({first_year}) 포스터 (예시 이미지)")
            except:
                st.warning("포스터 이미지를 불러오지 못했어요 😢")
