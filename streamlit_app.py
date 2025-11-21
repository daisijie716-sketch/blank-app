import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# -------------------------------
# 1. 기본 설정
# -------------------------------
st.set_page_config(
    page_title="탁구 선수 경력 통계 분석",
    page_icon="🏓",
    layout="wide"
)

# -------------------------------
# 2. 제목
# -------------------------------
st.title("🏓 탁구 선수의 직업 경력 통계 분석")
st.write("프로 탁구 선수들의 경기 수, 승률, 우승 기록 등을 시각화하여 한눈에 분석할 수 있는 대시보드입니다.")

# -------------------------------
# 3. 예시 데이터 생성
# -------------------------------
players = {
    "선수명": ["판젠동", "마롱", "장본", "이상수", "장우진", "티모 볼"],
    "국가": ["중국", "중국", "중국", "한국", "한국", "독일"],
    "나이": [27, 36, 25, 33, 28, 43],
    "세계랭킹 최고": [1, 1, 3, 6, 5, 1],
    "우승 횟수": [23, 30, 12, 5, 8, 27],
    "커리어 경기 수": [420, 680, 350, 500, 410, 900],
    "승률(%)": [89, 86, 78, 74, 76, 80]
}

df = pd.DataFrame(players)

# -------------------------------
# 4. 사이드바 추가
# -------------------------------
st.sidebar.header("⚙️ 필터 설정")

# 국가 선택
country_filter = st.sidebar.multiselect(
    "국가 선택:",
    options=df["국가"].unique(),
    default=df["국가"].unique()
)

# 선수 검색
search_name = st.sidebar.text_input("선수 검색 (예: 마롱)")

# 정렬 옵션
sort_option = st.sidebar.selectbox(
    "정렬 기준:",
    ["승률(%)", "우승 횟수", "커리어 경기 수"]
)

# 데이터 보이기 여부
show_table = st.sidebar.checkbox("선수 데이터 표시", value=True)

# 그래프 선택
graph_type = st.sidebar.radio(
    "그래프 종류 선택:",
    ["승률 비교", "경기 수 비교", "우승 횟수 비교", "국가 분포"]
)

# -------------------------------
# 5. 필터 적용
# -------------------------------
filtered_df = df[df["국가"].isin(country_filter)]

if search_name:
    filtered_df = filtered_df[filtered_df["선수명"].str.contains(search_name)]

filtered_df = filtered_df.sort_values(by=sort_option, ascending=False)

# -------------------------------
# 6. 데이터 테이블 표시
# -------------------------------
if show_table:
    st.subheader("📋 선수 기본 데이터")
    st.dataframe(filtered_df, use_container_width=True)

# -------------------------------
# 7. 선택된 그래프 출력
# -------------------------------
if graph_type == "승률 비교":
    st.subheader("📈 선수별 승률 비교")
    fig = px.bar(filtered_df, x="선수명", y="승률(%)", color="국가", text="승률(%)")
    st.plotly_chart(fig, use_container_width=True)

elif graph_type == "경기 수 비교":
    st.subheader("🏆 선수별 커리어 경기 수")
    fig = px.line(filtered_df, x="선수명", y="커리어 경기 수", markers=True)
    st.plotly_chart(fig, use_container_width=True)

elif graph_type == "우승 횟수 비교":
    st.subheader("🥇 선수 우승 횟수 비교")
    fig = px.bar(filtered_df, x="선수명", y="우승 횟수", color="선수명")
    st.plotly_chart(fig, use_container_width=True)

elif graph_type == "국가 분포":
    st.subheader("🌍 국가별 선수 분포")
    fig = px.pie(filtered_df, names="국가")
    st.plotly_chart(fig, use_container_width=True)


