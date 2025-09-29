import streamlit as st
import pandas as pd

# 제목
st.title("MBTI 국가 데이터 미리보기")

# CSV 파일 경로
file_path = "countriesMBTI_16types.csv"  # 같은 폴더에 있다고 가정

# 데이터 읽기
df = pd.read_csv(file_path)

# 데이터프레임 상위 5줄 출력
st.subheader("데이터 상위 5줄 미리보기")
st.dataframe(df.head())

