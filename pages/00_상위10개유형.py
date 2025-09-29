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
    opti
