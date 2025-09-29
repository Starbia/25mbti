import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(page_title="MBTI 상위 10 유형", layout="centered")
st.title("MBTI 상위 10 유형 막대그래프 (Altair)")

# CSV 파일 경로 (같은 폴더)
FILE = "countriesMBTI_16types.csv"

# 16개 MBTI 유형 (대문자 기준)
MBTI_TYPES = [
    "INTJ","INTP","ENTJ","ENTP",
    "INFJ","INFP","ENFJ","ENFP",
    "ISTJ","ISFJ","ESTJ","ESFJ",
    "ISTP","ISFP","ESTP","ESFP",
]

# 데이터 읽기
df = pd.read_csv(FILE)

# MBTI 열 자동 감지 (대소문자 무시)
mbti_cols = []
for c in df.columns:
    if c.strip().upper() in MBTI_TYPES:
        mbti_cols.append(c)

if not mbti_cols:
    st.error("MBTI 열을 찾을 수 없습니다. CSV에 16개 유형(예: INTJ, ENTP 등) 열이 있어야 합니다.")
    st.stop()

# 숫자형으로 변환
mbti_df = df[mbti_cols].apply(pd.to_numeric, errors="coerce")

# 행 합으로 '백분율(국가별 합≈100)' 여부 추정
row_sums = mbti_df.sum(axis=1, skipna=True)
is_percent_guess = np.all((row_sums.dropna() >= 95) & (row_sums.dropna() <= 105))

# 사용자가 집계 방식 선택 가능 (기본은 자동감지)
st.sidebar.header("집계 설정")
mode = st.sidebar.radio(
    "집계 방식 선택",
    options=["자동(권장)", "백분율 평균", "카운트 합계"],
    index=0
)

if mode == "백분율 평균":
    agg_mode = "percent"
elif mode == "카운트 합계":
    agg_mode = "count"
else:
    agg_mode = "percent" if is_percent_guess else "count"

# 전세계 집계
if agg_mode == "percent":
    # 국가별 퍼센트라고 가정: 평균(%)을 사용
    global_series = mbti_df.mean(axis=0, skipna=True)
    y_title = "평균 비율(%)"
else:
    # 카운트라고 가정: 합계 사용
    global_series = mbti_df.sum(axis=0, skipna=True)
    y_title = "합계(Count)"

# 상위 10개 유형
top10 = (
    global_series.sort_values(ascending=False)
    .head(10)
    .reset_index()
)
top10.columns = ["MBTI", "Value"]

st.caption(
    f"집계 방식: **{'백분율 평균' if agg_mode=='percent' else '카운트 합계'}**  "
    f"(자동감지 결과: {'백분율' if is_percent_guess else '카운트'}로 추정)"
)

# Altair 차트
chart = (
    alt.Chart(top10)
    .mark_bar()
    .encode(
        x=alt.X("MBTI:N", sort="-y", title="MBTI 유형"),
        y=alt.Y("Value:Q", title=y_title),
        tooltip=[alt.Tooltip("MBTI:N", title="유형"),
                 alt.Tooltip("Value:Q", title=y_title, format=",.2f")]
    )
    .properties(width=640, height=400, title="전세계 기준 상위 10 MBTI 유형")
)

st.altair_chart(chart, use_container_width=True)

# 표도 함께 제공
st.subheader("상위 10개 유형 표")
st.dataframe(top10.style.format({"Value": "{:,.2f}"}), use_container_width=True)

# 부가 정보
with st.expander("데이터 및 열 감지 정보"):
    st.write("감지된 MBTI 열:", mbti_cols)
    st.write("원본 데이터 크기(행, 열):", df.shape)
    st.write("행 합(샘플 상위 5개):")
    st.write(row_sums.head())
