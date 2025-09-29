import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------
# 페이지 기본 설정
# ---------------------------
st.set_page_config(page_title="국가별 MBTI 지도 히트맵", layout="wide")
st.title("🗺️ 국가별 MBTI 히트맵")
st.write("나라별 MBTI 유형의 평균 비율을 세계 지도 위에 시각화합니다. 🌍")

# ---------------------------
# CSV 파일 불러오기
# ---------------------------
file_path = "countriesMBTI_16types.csv"  # 같은 폴더에 위치
df = pd.read_csv(file_path)

# ---------------------------
# MBTI 유형 리스트
# ---------------------------
MBTI_TYPES = [
    "INTJ","INTP","ENTJ","ENTP",
    "INFJ","INFP","ENFJ","ENFP",
    "ISTJ","ISFJ","ESTJ","ESFJ",
    "ISTP","ISFP","ESTP","ESFP",
]

# 국가명 컬럼 자동 탐지
country_col = None
for c in df.columns:
    if "country" in c.lower() or "nation" in c.lower():
        country_col = c
        break

if country_col is None:
    st.error("❌ CSV 파일에 국가명을 나타내는 열이 필요합니다. (예: 'Country')")
    st.stop()

# ---------------------------
# 사용자 MBTI 선택
# ---------------------------
selected_mbti = st.selectbox("🌐 시각화할 MBTI 유형을 선택하세요", MBTI_TYPES, index=0)

# ---------------------------
# 지도용 데이터 준비
# ---------------------------
map_df = df[[country_col, selected_mbti]].copy()
map_df.columns = ["Country", "Value"]

# Plotly 세계 지도 히트맵
fig = px.choropleth(
    map_df,
    locations="Country",
    locationmode="country names",  # 국가명 자동 인식
    color="Value",
    hover_name="Country",
    color_continuous_scale="RdYlBu_r",
    title=f"🗺️ {selected_mbti} 국가별 평균 비율 히트맵",
)

fig.update_layout(
    title_font_size=22,
    geo=dict(showframe=False, showcoastlines=True, projection_type="natural earth"),
    margin=dict(l=20, r=20, t=60, b=20)
)

# ---------------------------
# Streamlit 출력
# ---------------------------
st.subheader(f"📊 {selected_mbti} 비율 세계 지도")
st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# 국가별 데이터 표
# ---------------------------
st.subheader("📄 국가별 데이터")
st.dataframe(map_df.sort_values("Value", ascending=False).style.format({"Value": "{:.2f}"}))

# ---------------------------
# 탐구활동 확장 아이디어
# ---------------------------
st.markdown("""
### 🧪 탐구 질문
1. 어떤 MBTI 유형이 특정 지역에서 유독 높게 나타나나요? 🌍  
2. 문화적, 사회적 요인과 MBTI 분포 간에 어떤 연관성이 있을까요? 🤔  
3. 국가별 경제력, 행복지수와 MBTI 유형 간의 상관관계를 분석해볼 수 있을까요? 💹
""")
