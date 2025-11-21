import streamlit as st

st.title("🎈 탁구 선수의 직업 경력 통계 분석")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- 1. 앱 기본 설정 ---
st.set_page_config(
    page_title="乒乓球球员生涯统计分析",
    page_icon="🏓",
    layout="wide"
)

# --- 2. 제목 ---
st.title("🏓 乒乓球球员生涯统计分析 Dashboard")
st.markdown("""
本大시보드는 **真实世界乒乓球运动员** 的比赛表现、对手情况、胜率变化、技术特征  
进行可视化分析，便于观察运动员的竞技特点与生涯趋势。
""")

st.divider()

# --- 3. 真实球员名单 ---
players = [
    # 中国男乒
    "樊振东", "马龙", "王楚钦", "梁靖崑", "林高远",
    # 中国女乒
    "孙颖莎", "陈梦", "王曼昱", "王艺迪",
    # 日本
    "张本智和", "伊藤美诚", "早田希娜",
    # 韩国
    "张禹珍", "安宰贤", "申裕斌", "田志希",
    # 欧洲
    "Timo Boll", "Dimitrij Ovtcharov", "Mattias Falck"
]

# 真实世界对手（国际常见）
opponents = [
    "Fan Zhendong", "Ma Long", "Wang Chuqin", "Lin Gaoyuan",
    "Tomokazu Harimoto", "Mima Ito", "Hina Hayata",
    "Jang Woojin", "An Jaehyun", "Timo Boll",
    "Dimitrij Ovtcharov", "Mattias Falck"
]

# 技术动作
strokes = ["正手强攻", "反手拧拉", "发球抢攻", "接发挑打", "中远台对拉", "台内小球", "侧身进攻"]

# --- 4. 가상但真实风格的数据 ---
np.random.seed(42)
n = 1800

data = pd.DataFrame({
    "球员": np.random.choice(players, n),
    "年份": np.random.choice(range(2017, 2025), n),
    "赛事等级": np.random.choice(["WTT 冠军赛", "WTT 大满贯", "世界锦标赛", "亚运会", "世界杯"], n),
    "对手": np.random.choice(opponents, n),
    "局数": np.random.randint(3, 6),
    "得分": np.random.randint(5, 12),
    "失分": np.random.randint(5, 12),
    "关键分成功率": np.random.uniform(35, 85, n).round(2),
    "主要得分手段": np.random.choice(strokes, n),
})

data["是否胜利"] = np.where(data["得分"] > data["失分"], "胜", "负")

# --- 5. 侧边栏过滤 ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/861/861512.png", width=100)
    st.title("⚙️ 过滤条件")

    selected_player = st.selectbox("球员选择", sorted(players))
    years = st.multiselect("年份选择", sorted(data["年份"].unique()), default=[2023, 2024])
    match_types = st.multiselect("赛事等级", data["赛事等级"].unique(), default=data["赛事等级"].unique())

    show_raw = st.checkbox("📄 显示原始数据")

st.divider()

# --- 6. 数据过滤 ---
filtered = data[
    (data["球员"] == selected_player) &
    (data["年份"].isin(years)) &
    (data["赛事等级"].isin(match_types))
]

# --- 7. KPI ---
total_matches = len(filtered)
win_rate = (filtered["是否胜利"].value_counts().get("胜", 0) / total_matches * 100) if total_matches > 0 else 0
avg_key = filtered["关键分成功率"].mean().round(2) if total_matches > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("🏓 参赛场次", f"{total_matches} 场")
col2.metric("🥇 胜率", f"{win_rate:.1f}%")
col3.metric("🔥 关键分成功率", f"{avg_key}%")

st.divider()

# --- 8. 图表分析 ---

# (1) 年份胜率曲线
st.subheader("📈 年份胜率变化趋势")
win_trend = (
    filtered.groupby("年份")["是否胜利"]
    .apply(lambda x: (x == "胜").mean() * 100)
    .reset_index(name="胜率")
)

fig1 = px.line(
    win_trend,
    x="年份", y="胜率",
    markers=True,
    color_discrete_sequence=["#27ae60"]
)
st.plotly_chart(fig1, use_container_width=True)

# (2) 对手胜负柱状图
st.subheader("⚔️ 不同对手对战情况")
opponent_stats = (
    filtered.groupby(["对手", "是否胜利"])
    .size()
    .reset_index(name="场次")
)

fig2 = px.bar(
    opponent_stats,
    x="对手", y="场次", color="是否胜利",
    barmode="group",
    color_discrete_sequence=["#2980b9", "#c0392b"]
)
st.plotly_chart(fig2, use_container_width=True)

# (3) 得分技术动作分布
st.subheader("🎯 得分主要技术分布")
tech = filtered["主要得分手段"].value_counts().reset_index()
tech.columns = ["技术", "次数"]

fig3 = px.pie(
    tech,
    names="技术", values="次数",
    color_discrete_sequence=px.colors.qualitative.Set3
)
st.plotly_chart(fig3, use_container_width=True)

# --- 9. 显示原始数据 ---
if show_raw:
    st.divider()
    st.subheader("📄 过滤数据")
    st.dataframe(filtered, use_container_width=True)
