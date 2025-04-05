import streamlit as st
from openai import OpenAI
import os  # 파일 존재 여부를 확인하기 위해 추가

# ✅ 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 제목과 설명
st.title("🎬🎬 드라마 & 시네마 천국 🎬🎬")
st.write("GPT-4.0 mini 기반으로 재밌는 드라마, 영화를 추천해드립니다. 기분 따라, 취향 따라 골라보세요!")

# ✅ 이미지 삽입 (요청된 위치에 추가)
image_path = r"C:\Users\mylap\Desktop\hi\image.png"  # 요청된 경로와 파일 이름 반영
if os.path.exists(image_path):
    st.image(image_path, caption="영화와 드라마를 즐겨보세요!", width=None)
else:
    st.warning(f"이미지 파일 '{image_path}'을 찾을 수 없습니다. 파일 경로를 확인해주세요!", icon="⚠️")

# OpenAI API 키 입력
openai_api_key = st.text_input("🔑 OpenAI API Key를 입력하세요", type="password")
if not openai_api_key:
    st.info("OpenAI 키를 입력하시면 추천이 시작됩니다!", icon="🗝️")
else:
    try:
        client = OpenAI(api_key=openai_api_key)
        st.success("API 키가 정상적으로 입력되었습니다!", icon="✅")
    except Exception as e:
        st.error(f"OpenAI API 키 인증에 실패했습니다: {str(e)}", icon="❌")
        st.stop()  # API 키 인증 실패 시 더 이상 진행하지 않음

    # 콘텐츠 종류
    content_type = st.radio("🎞️ 보고 싶은 콘텐츠는?", ["드라마", "영화", "둘 다"])

    # 장르
    genre_options = ["로맨스", "스릴러", "코미디", "공포", "판타지", "SF", "액션", "감동"]
    selected_genres = st.multiselect("🎭 좋아하는 장르를 골라보세요!", genre_options)

    # 국가
    country_options = ["한국", "미국", "일본", "기타/다 좋아요"]
    selected_countries = st.multiselect("🌍 선호하는 나라를 선택하세요!", country_options)

    # 연도 필터
    year_range = st.slider("📆 원하는 제작 연도 범위를 선택하세요!", 1895, 2025, (2000, 2025))

    # 분위기 기반
    mood_options = ["😊 힐링하고 싶어요", "😢 눈물 나는 게 좋아요", "😲 반전 있는 작품이 좋아요", "❤️ 설레는 분위기 원해요"]
    selected_moods = st.multiselect("🎈 지금 기분에 어울리는 분위기를 골라보세요!", mood_options)

    # 이전에 본 작품
    seen_titles = st.text_input("👀 이미 본 작품이 있다면 입력해주세요! (예: 기생충, 더글로리)")

    # 플랫폼 필터
    platform_options = ["Netflix", "Disney+", "TVING", "웨이브", "왓챠", "관계없음"]
    selected_platforms = st.multiselect("📺 자주 이용하는 플랫폼이 있나요?", platform_options)

    # 추천 버튼
    if st.button("🍿 드라마 & 시네마 탐색 시작!"):
        # 최소한 하나의 장르를 선택했는지 확인
        if not selected_genres:
            st.warning("최소한 하나의 장르를 선택해주세요!", icon="⚠️")
        else:
            user_summary = f"저는 {content_type}를 좋아하고요"
            if selected_genres:
                user_summary += f", {', '.join(selected_genres)} 장르를 좋아하고"
            if selected_countries:
                user_summary += f", {', '.join(selected_countries)} 작품을 선호해요"
            if selected_moods:
                user_summary += f", 분위기는 {' / '.join(selected_moods)} 느낌을 원해요"
            if selected_platforms:
                user_summary += f", 플랫폼은 {', '.join(selected_platforms)}를 자주 써요"
            user_summary += f". 제작 연도는 {year_range[0]}년부터 {year_range[1]}년 사이로 보고 싶어요."

            st.chat_message("user").markdown(user_summary)

            prompt = f"""
            [사용자 취향 요약]
            {user_summary}

            [추가 정보]
            이미 본 작품: {seen_titles if seen_titles else "없음"}

            [요청 조건]
            - {content_type}를 최소 5개 추천해주세요.
            - 제목(연도), 간단한 설명(5줄 이하), 분위기 키워드, 그리고 이 콘텐츠를 볼 수 있는 플랫폼(예: Netflix, Disney+, TVING 등)을 포함해주세요.
            - 중복 추천 없이 다양한 스타일을 보여주세요.
            - 카드 형식 리스트로 깔끔하게 정리해주세요.
            - 플랫폼 정보는 정확하고 최신 정보를 기반으로 제공해주세요.
            """

            st.session_state.messages.append({"role": "user", "content": prompt})

            try:
                stream = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state.messages,
                    stream=True,
                )

                with st.chat_message("assistant"):
                    response = st.write_stream(stream)

                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"추천 중 오류가 발생했습니다: {str(e)}", icon="❌")

    # 랜덤 추천 기능
    if st.button("🎲 오늘의 랜덤 추천 받기!"):
        random_prompt = """
        [요청]
        - 장르, 국가, 플랫폼 관계없이 랜덤하게 드라마나 영화를 1편 추천해주세요.
        - 포맷:
            🎬 제목(연도)
            - 💬 간단한 설명 (5줄 이내)
            - 💡 분위기 키워드 2~3개
            - 📺 볼 수 있는 플랫폼 (예: Netflix, Disney+, TVING 등)
        - 플랫폼 정보는 정확하고 최신 정보를 기반으로 제공해주세요.
        """

        st.session_state.messages.append({"role": "user", "content": random_prompt})

        try:
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages,
                stream=True,
            )

            with st.chat_message("assistant"):
                response = st.write_stream(stream)

            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"랜덤 추천 중 오류가 발생했습니다: {str(e)}", icon="❌")
