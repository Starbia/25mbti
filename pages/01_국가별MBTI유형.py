import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="MBTI 국가별 비율", layout="centered")
st.title("🌍 나라별 MBTI 비율 시각화")
st.write("나라를 선택하면 그 나라의 **MBTI 유형 비율**이 막대그래프로 나타납니다. 🎯")

# CSV 파일 로드
file_path = "countriesMBTI_16types.csv"
df = pd.read_csv(file_path)

# MBTI 유형 리스트
MBTI_TYPES = [
    "INTJ","INTP","ENTJ","ENTP",
    "INFJ","INFP","ENFJ","ENFP",
    "ISTJ","ISFJ","ESTJ","ESFJ",
    "ISTP","ISFP","ESTP","ESFP",
]

# 국가 선택
country_col = None
for c in df.columns:
    if "country" in c.lower() or "nation" in c.lower():
        country_col = c
        break

if country_col is None:
    st.error("CSV 파일에 국가명을 나타내는 열이 필요합니다. (예: 'Country')")
    st.stop()

countries = df[country_col].dropna().unique().tolist()
selected_country = st.selectbox("🌐 나라 선택", sorted(countries))

# 선택된 나라의 MBTI 데이터 추출
row = df[df[country_col] == selected_country]
if row.empty:
    st.warning("해당 나라 데이터가 없습니다.")
    st.stop()

mbti_data = row[MBTI_TYPES].T.reset_index()
mbti_data.columns = ["MBTI", "Value"]

# Plotly 막대그래프
fig = px.bar(
    mbti_data,
    x="MBTI",
    y="Value",
    color="MBTI",
    text="Value",
    title=f"📊 {selected_country}의 MBTI 비율",
    color_discrete_sequence=px.colors.qualitative.Safe  # 예쁜 색상 팔레트
)

fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
fig.update_layout(
    xaxis_title="MBTI 유형",
    yaxis_title="비율(%)",
    uniformtext_minsize=8,
    uniformtext_mode='hide',
    plot_bgcolor="white",
    title_font_size=20
)

# 그래프 출력
st.plotly_chart(fig, use_container_width=True)

# 데이터 표도 함께 표시
st.subheader("📄 데이터 표")
st.dataframe(mbti_data.style.format({"Value": "{:.2f}"}))
