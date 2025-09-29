import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------
# 페이지 기본 설정
# ---------------------------
st.set_page_config(page_title="MBTI 영역별 세계 지도", layout="wide")
st.title("🌍 MBTI 영역별 국가 비율 히트맵")
st.write("MBTI의 4가지 주요 영역 중 하나를 선택해 국가별 분포를 시각화합니다. 🌈")

# ---------------------------
# CSV 파일 불러오기
# ---------------------------
file_path = "countriesMBTI_16types.csv"  # 같은 폴더에 있어야 합니다
df = pd.read_csv(file_path)

# MBTI 유형 리스트
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
# MBTI 영역 매핑
# ---------------------------
DIMENSIONS = {
    "E vs I (외향 vs 내향)": {"E": ["ENTJ","ENTP","ENFJ","ENFP","ESTJ","ESFJ","ESTP","ESFP"],
                              "I": ["INTJ","INTP","INFJ","INFP","ISTJ","ISFJ","ISTP","ISFP"]},
    "N vs S (직관 vs 감각)": {"N": ["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP"],
                              "S": ["ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]},
    "T vs F (사고 vs 감정)": {"T": ["INTJ","INTP","ENTJ","ENTP","ISTJ","ISTP","ESTJ","ESTP"],
                              "F": ["INFJ","INFP","ENFJ","ENFP","ISFJ","ISFP","ESFJ","ESFP"]},
    "J vs P (판단 vs 인식)": {"J": ["INTJ","INFJ","ENTJ","ENFJ","ISTJ","ISFJ","ESTJ","ESFJ"],
                              "P": ["INTP","INFP","ENTP","ENFP","ISTP","ISFP","ESTP","ESFP"]},
}

# 사용자 선택
selected_dim = st.selectbox("📌 MBTI 영역 선택", list(DIMENSIONS.keys()))

# ---------------------------
# 선택한 영역의 비율 계산
# ---------------------------
group = DIMENSIONS[selected_dim]
df_calc = pd.DataFrame()
df_calc[country_col] = df[country_col]

# E/I, N/S 등 두 축의 합과 비율 계산
for side, types in group.items():
    df_calc[side] = df[types].sum(axis=1)

df_calc["Total"] = df_calc[list(group.keys())].sum(axis=1)
# 비율(%)로 변환
for side in group.keys():
    df_calc[f"{side}_Percent"] = (df_calc[side] / df_calc["Total"] * 100).round(2)

# 시각화할 측면 선택
side_choice = st.radio("🎨 시각화할 측면 선택", list(group.keys()), horizontal=True)

map_df = df_calc[[country_col, f"{side_choice}_Percent"]].rename(columns={f"{side_choice}_Percent":"Value"})

# ---------------------------
# Plotly 세계 지도 히트맵
# ---------------------------
fig = px.choropleth(
    map_df,
    locations=country_col,
    locationmode="country names",
    color="Value",
    hover_name=country_col,
    color_continuous_scale="Spectral_r",  # 다채로운 스펙트럼
    title=f"🗺️ {selected_dim} - {side_choice} 비율 세계 지도",
)

fig.update_layout(
    title_font_size=22,
    geo=dict(showframe=False, showcoastlines=True, projection_type="natural earth"),
    margin=dict(l=20, r=20, t=60, b=20)
)

# ---------------------------
# Streamlit 출력
# ---------------------------
st.subheader(f"🌐 {selected_dim} - {side_choice} 비율")
st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# 국가별 데이터 표
# ---------------------------
st.subheader("📄 국가별 데이터")
st.dataframe(map_df.sort_values("Value", ascending=False).style.format({"Value": "{:.2f}"}))

# ---------------------------
# 탐구 활동 아이디어
# ---------------------------
st.markdown("""
### 🧪 탐구 질문
1. 어떤 대륙에서 **외향(E)** 혹은 **내향(I)** 성향이 두드러지나요? 🌍  
2. 국가의 문화, 경제 수준, 역사와 MBTI 영역 간에 어떤 연관성이 있을까요? 🤔  
3. **E vs I** 뿐 아니라 **N vs S**, **T vs F**, **J vs P**를 비교해보면 어떤 패턴이 보이나요? 🔍  
""")
