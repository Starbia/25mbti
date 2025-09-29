import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------
# 페이지 기본 설정
# ---------------------------
st.set_page_config(page_title="대륙별 MBTI 히트맵", layout="wide")
st.title("🌍 대륙별 MBTI 평균 비율 히트맵")
st.write("대륙별 MBTI 유형 분포를 한눈에 확인해보세요! 🔥")

# ---------------------------
# CSV 파일 불러오기
# ---------------------------
file_path = "countriesMBTI_16types.csv"  # 같은 폴더에 위치
df = pd.read_csv(file_path)

# ---------------------------
# MBTI 유형 및 열 확인
# ---------------------------
MBTI_TYPES = [
    "INTJ","INTP","ENTJ","ENTP",
    "INFJ","INFP","ENFJ","ENFP",
    "ISTJ","ISFJ","ESTJ","ESFJ",
    "ISTP","ISFP","ESTP","ESFP",
]

# 국가와 대륙 컬럼 자동 탐지
country_col = None
continent_col = None

for c in df.columns:
    if "country" in c.lower() or "nation" in c.lower():
        country_col = c
    if "continent" in c.lower() or "region" in c.lower():
        continent_col = c

# 필수 컬럼 체크
if country_col is None or continent_col is None:
    st.error("❌ CSV 파일에 국가(Country)와 대륙(Continent)을 나타내는 열이 있어야 합니다.")
    st.stop()

# ---------------------------
# 대륙별 평균 비율 계산
# ---------------------------
# MBTI 컬럼만 숫자로 변환
mbti_df = df[MBTI_TYPES].apply(pd.to_numeric, errors='coerce')

# 원본 데이터프레임에 숫자형 MBTI 합치기
df_clean = pd.concat([df[[country_col, continent_col]], mbti_df], axis=1)

# 대륙별 평균값 계산
continent_avg = df_clean.groupby(continent_col)[MBTI_TYPES].mean().round(2)

# 시각화를 위해 melt 변환 (세로형 데이터로 변환)
continent_melt = continent_avg.reset_index().melt(
    id_vars=continent_col,
    value_vars=MBTI_TYPES,
    var_name="MBTI",
    value_name="Average_Percent"
)

# ---------------------------
# Plotly 히트맵
# ---------------------------
fig = px.imshow(
    continent_avg[MBTI_TYPES],
    labels=dict(x="MBTI 유형", y="대륙", color="평균 비율(%)"),
    x=MBTI_TYPES,
    y=continent_avg.index,
    color_continuous_scale="RdYlBu_r",  # 빨강-노랑-파랑 반전
    aspect="auto",
    title="🌏 대륙별 MBTI 평균 비율 히트맵 🗺️"
)

# 레이아웃 조정
fig.update_layout(
    title_font_size=22,
    xaxis=dict(side="top"),
    yaxis_title="대륙",
    plot_bgcolor="white",
    margin=dict(l=50, r=50, t=100, b=50)
)

# ---------------------------
# Streamlit 출력
# ---------------------------
st.subheader("📊 대륙별 MBTI 평균 비율 히트맵")
st.plotly_chart(fig, use_container_width=True)

# 데이터프레임 표 표시
st.subheader("📄 대륙별 MBTI 평균 데이터")
st.dataframe(continent_avg.style.format("{:.2f}"), use_container_width=True)

# ---------------------------
# 탐구활동 힌트
# ---------------------------
st.markdown("""
### 🧪 탐구 질문
1. 어떤 MBTI 유형이 특정 대륙에서 두드러지게 높은가요? 🤔  
2. 동양과 서양에서의 MBTI 패턴은 어떤 차이가 있나요? 🌏 vs 🌍  
3. 두 대륙 간 가장 큰 차이를 보이는 MBTI 유형은 무엇인가요? 🔍
""")
