import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("🎬🎬 드라마 & 시네마 천국 🎬🎬")
st.write(
    "GPT-4.0 mini를 기반으로 재밌는 드라마, 영화를 추천해드립니다. "
    "드라마 & 시네마 천국으로 떠나 보아요"
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("OpenAI 키를 입력하세요.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)
    
    #영화/드라마 종류 선택
    content_type = st.radio("보고 싶은 콘텐츠는?", ["드라마", "영화', "둘다"])

    # 장르 선택
    genre_options =["로맨스", "스릴러","코미디","공포","판타지","SF","액션","감동"]
    selected_genres = st.multiselect("좋아하는 장르를 골라보세요!", genre_options)

    # 영화, 드라마 제작국가 선택
    country_options =["한국","미국","일본","다좋아"]
    selected_countries = st.multiselect("선호하는 나라를 골라보세요!",country_options)

    #세션 상태로 메시지 저장
    if "messages" not in st.session_state:
        st.session_state.messages=[]

    # 기존 메시지 출력
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 유저 입력
    if prompt :=st.chat_input("어떤 분위기의 작품을 찾고 계신가요?"):
        
        #유저가 입력한 메시지 + 선택한 옵션들
        full_prompt = f"""
        [유저 입력]
        {prompt}

        [선택 정보]
        콘텐츠 종류:{content_type}
        선호 장르 :{', '.join(selected_genres) if selected_genres else '선택 없음'}
        선호 국가 : {country_options}

        [요청 조건]
        - {content_type}를 최소 5개 추천해주세요.
        - 각 추천에는 다음 정보를 포함해주세요 :
          1. 제목
          2. 제작 연도
          3. 간단한 설명 (5줄 이하)
        - 리스트 형식으로 정리해주세요.
        """

        # 저장
        st.session_state.messages.append({"role":"user","content":full_prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

    # GPT 응답 생성
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":m["role"],"content":m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )

    with st.caht_message("assistant"):
        response = st.write_stream(stream)

    st.session_state.messages.append({"role":"assistant","content":response})
    
        
