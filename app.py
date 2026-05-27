import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(
    page_title="국제성모병원 ASP DASHBOARD",
    layout="wide"
)

st.markdown("""
<style>

/* 브라우저 기본 여백 제거 */
html, body, [class*="css"]  {
    margin: 0 !important;
    padding: 0 !important;
}

div[data-testid="stPlotlyChart"] {
    background: white;
    border-radius: 28px;
    padding: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.12);
}

/* 전체 배경 */
.stApp {
    background-color: #f3f4f6;
    font-family: 'Nanum Gothic', sans-serif;
}

/* 메인 제목 박스 */
.title-box {
    background-color: #102a43;
    padding: 22px 30px;
    border-radius: 24px;
    margin-bottom: 35px;

    /* 그림자 */
    box-shadow: 0 2px 8px rgba(0,0,0,0.12);

    /* 가운데 정렬 */
    text-align: center;
}

/* 메인 제목 글씨 */
.title-text {
    color: white;
    font-size: 42px;
    font-weight: 800;
    margin: 0;
}

/* 그래프 제목 박스 */
.chart-title-box {

    background-color: #d9d9d9;

    padding: 14px 24px;

    border-radius: 18px;

    width: fit-content;

    margin-left: 28px;

    margin-bottom: -25px;

    position: relative;

    z-index: 100;

    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
}

/* 그래프 제목 글씨 */
.chart-title {

    font-size: 20px;

    font-weight: 700;

    color: #1f1f1f;

    margin: 0;
}

html, body, [data-testid="stAppViewContainer"] {
    overflow-x: hidden;
}

iframe {
    min-height: 0px !important;
}

[data-testid="stPlotlyChart"] {
    height: 340px !important;
}


div[data-testid="stStatusWidget"] {
    display: none !important;
}

div[data-testid="stDecoration"] {
    display: none !important;
}

div[data-testid="stToolbar"] {
    display: none !important;
}

.loading-wrapper {

    display: flex;
    justify-content: center;
    align-items: center;

    height: 70vh;
}

.loading-box {

    background: white;
    border-radius: 32px;

    padding: 70px 120px;

    text-align: center;

    box-shadow: 0 6px 18px rgba(0,0,0,0.12);
}

.loading-text {

    font-size: 30px;
    font-weight: 800;

    color: #102a43;

    margin-top: 20px;
}

.loading-sub {

    font-size: 16px;

    color: #6b7280;

    margin-top: 12px;
}

div[data-baseweb="select"] {
    background-color: #e5e7eb;
    border-radius: 14px;
    border: 1px solid #cbd5e1;
}
/* 하단 섹션 제목 박스 */
.section-title-box {

    background-color: #102a43;

    border-radius: 24px;

    padding: 18px 28px;

    margin-top: 0px;

    margin-bottom: 12px;

    box-shadow: 0 4px 12px rgba(0,0,0,0.15);

    text-align: center;
}

/* 하단 섹션 제목 글씨 */
.section-title-text {

    color: white;

    font-size: 32px;

    font-weight: 800;

    margin: 0;
}


/* markdown 블록 간격 제거 */
.element-container {
    margin-bottom: 0rem !important;
}

/* 세로 block gap 제거 */
div[data-testid="stVerticalBlock"] > div {
    gap: 0rem !important;
}


</style>
""", unsafe_allow_html=True)

# 제목
st.markdown("""
<div class="title-box">
    <div class="title-text">
        국제성모병원 ASP DASHBOARD
    </div>
</div>
""", unsafe_allow_html=True)

# 엑셀 읽기
@st.cache_data(ttl=86400)
def load_data():

    return pd.read_excel(
        "DOT 대시보드.xlsx",
        sheet_name="ASP"
    )


# 로딩 화면
loading_placeholder = st.empty()

with loading_placeholder:

    components.html(
        """
        <html>
        <head>
        <style>

        body{
            margin:0;
            background:#f3f4f6;
            display:flex;
            justify-content:center;
            align-items:center;
            height:70vh;
            font-family:sans-serif;
        }

        .loading-box{
            background:white;
            padding:70px 120px;
            border-radius:32px;
            text-align:center;
            box-shadow:0 6px 18px rgba(0,0,0,0.12);
        }

        .loading-icon{
            font-size:70px;
        }

        .loading-text{
            font-size:30px;
            font-weight:800;
            color:#102a43;
            margin-top:20px;
        }

        .loading-sub{
            font-size:16px;
            color:#6b7280;
            margin-top:12px;
        }

        </style>
        </head>

        <body>

            <div class="loading-box">

                <div class="loading-icon">
                    ⏳
                </div>

                <div class="loading-text">
                    데이터를 조회하고 있습니다
                </div>

                <div class="loading-sub">
                    잠시만 기다려주세요...
                </div>

            </div>

        </body>
        </html>
        """,
        height=500,
    )

# 데이터 로드
df = load_data()

# 로딩 제거
loading_placeholder.empty()



if st.button("🔄 파일 최신화"):

    load_data.clear()

    st.toast("데이터를 최신화했습니다.")


# 분기 변환 함수
def convert_quarter(month):

    month = str(month)

    quarter_map = {
        "24/11": "24년 4분기",
        "24/12": "24년 4분기",

        "25/01": "25년 1분기",
        "25/02": "25년 1분기",
        "25/03": "25년 1분기",

        "25/04": "25년 2분기",
        "25/05": "25년 2분기",
        "25/06": "25년 2분기",

        "25/07": "25년 3분기",
        "25/08": "25년 3분기",
        "25/09": "25년 3분기",

        "25/10": "25년 4분기",
        "25/11": "25년 4분기",
        "25/12": "25년 4분기",

        "26/01": "26년 1분기",
        "26/02": "26년 1분기",
        "26/03": "26년 1분기",

        "26/04": "26년 2분기"
    }

    return quarter_map.get(month)

# 분기 컬럼 생성
df["분기"] = df["처방 월"].apply(convert_quarter)



# =========================
# 첫번째 그래프
# 전체 항생제 사용량
# =========================

# 월별 고유키 개수 계산
monthly_total = (
    df
    .groupby(["분기", "처방 월"])["고유키"]
    .nunique()
    .reset_index()
)

# 분기별 평균 계산
summary1 = (
    monthly_total
    .groupby("분기")["고유키"]
    .mean()
    .reset_index()
)

# 컬럼명 변경
summary1.columns = [
    "분기",
    "항생제 사용량 (DOT/1,000 patients-day)"
]

# 분기 순서 지정
quarter_order = [
    "24년 4분기",
    "25년 1분기",
    "25년 2분기",
    "25년 3분기",
    "25년 4분기",
    "26년 1분기",
    "26년 2분기"
]

# 막대그래프 생성
fig1 = px.bar(
    summary1,
    x="분기",
    y="항생제 사용량 (DOT/1,000 patients-day)",
    text="항생제 사용량 (DOT/1,000 patients-day)",

    category_orders={
        "분기": quarter_order
    },

    color_discrete_sequence=["lightcoral"]
)

fig1.update_layout(

    height=480,

    xaxis_title=None,

    paper_bgcolor='rgba(255,255,255,0)',
    plot_bgcolor='rgba(255,255,255,0)',

    # 2번 그래프와 동일 margin
    margin=dict(
        l=20,
        r=60,
        t=20,
        b=40
    ),

    yaxis_tickformat=",",

    xaxis=dict(
    tickangle=15,
    tickfont=dict(
        size=10
    )
    )
)

# 데이터 레이블 형식 변경
# 데이터 레이블 형식 변경 + 막대 두께 조절
fig1.update_traces(
    texttemplate='%{text:,.0f}',
    textposition='outside',

 # 데이터 레이블 글자 크기
    textfont_size=14,

    # 막대 폭 줄이기
    width=0.55
)


# 제한항생제 O만 필터
abx_df = df[df["제한항생제"] == "O"]

# 월별 / 성분별 고유키 개수 계산
monthly = (
    abx_df
    .groupby(["분기", "처방 월", "성분통합키"])["고유키"]
    .nunique()
    .reset_index()
)

# 분기별 평균 계산
summary2 = (
    monthly
    .groupby(["분기", "성분통합키"])["고유키"]
    .mean()
    .reset_index()
)

# 컬럼명 변경
summary2.columns = ["분기", "성분통합키", "항생제 사용량(DOT/1,000 patients-day)"]

# TOP10 계산
top10 = (
    summary2
    .groupby("성분통합키")["항생제 사용량(DOT/1,000 patients-day)"]
    .sum()
    .reset_index()
)

top10 = (
    top10
    .sort_values("항생제 사용량(DOT/1,000 patients-day)", ascending=False)
    .head(10)
)

top10_list = top10["성분통합키"].tolist()

# TOP10만 남기기
summary2 = summary2[
    summary2["성분통합키"].isin(top10_list)
]

# 분기 순서 지정
quarter_order = [
    "24년 4분기",
    "25년 1분기",
    "25년 2분기",
    "25년 3분기",
    "25년 4분기",
    "26년 1분기",
    "26년 2분기"
]

# 범례 순서
category_order = top10["성분통합키"].tolist()

# 꺾은선 그래프
fig2 = px.line(
    summary2,
    x="분기",
    y="항생제 사용량(DOT/1,000 patients-day)",
    color="성분통합키",
    markers=True,

    category_orders={
        "분기": quarter_order,
        "성분통합키": category_order
    },

    color_discrete_sequence=px.colors.qualitative.Dark24
)

# 마지막 분기
last_quarter = "26년 2분기"

# 마지막 분기 데이터
last_points = summary2[
    summary2["분기"] == last_quarter
]


fig2.update_layout(

    height=480,

    xaxis_title=None,

    paper_bgcolor='rgba(255,255,255,0)',
    plot_bgcolor='rgba(255,255,255,0)',

    # 그래프 영역 최대화
    margin=dict(
        l=20,
        r=60,
        t=20,
        b=40
    ),

    # x축 글자 회전
    xaxis_tickangle=20,

   legend=dict(
    orientation="v",

    # 세로 중앙
    yanchor="middle",
    y=0.5,

    xanchor="left",
    x=1.02,

    # 글씨 약간 키우기
    font=dict(
        size=10
    )

),

    # 범례 제목 제거
    legend_title_text=""
)


# 좌우 컬럼 생성
col1, col2 = st.columns([0.8, 1.2])

# 왼쪽 그래프
with col1:

    st.markdown("""
    <div class="chart-title-box">
        <div class="chart-title">
            분기별 총 항생제 사용량
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.plotly_chart(
        fig1,
        use_container_width=True,
        config={"displayModeBar": False},
        key="graph1"
)


# 오른쪽 그래프
with col2:

    st.markdown("""
    <div class="chart-title-box">
        <div class="chart-title">
            분기별 제한항생제 사용량
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.plotly_chart(
        fig2,
        use_container_width=True,
        config={"displayModeBar": False},
        key="graph2"
)

    # =========================
# 진료과 선택
# =========================

dept_list = sorted(df["진료과한글"].dropna().unique(),
    key=lambda x: (x == "기타", x))

st.markdown("""
<div class="section-title-box">
    <div class="section-title-text">
        진료과별 항생제 사용량
    </div>
</div>
""", unsafe_allow_html=True)

selected_dept = st.selectbox(
    "진료과 선택",
    ["전체"] + dept_list
)

# 선택 진료과 필터
if selected_dept != "전체":
    filtered_df = df[df["진료과한글"] == selected_dept]
else:
    filtered_df = df.copy()

        # =========================
# Cephamycin vs 3세대 Cephalosporins
# =========================

target_df = filtered_df[
    filtered_df["분류"].isin([
        "Cephamycin",
        "3세대 Cephalosporins"
    ])
]
monthly_compare = (
    target_df
    .groupby(["분기", "처방 월", "분류"])["고유키"]
    .nunique()
    .reset_index()
)
summary_compare = (
    monthly_compare
    .groupby(["분기", "분류"])["고유키"]
    .mean()
    .reset_index()
)

summary_compare.columns = [
    "분기",
    "분류",
    "사용량"
]

fig_compare = px.bar(
    summary_compare,
    x="분기",
    y="사용량",
    color="분류",
    barmode="group",

    category_orders={
        "분기": quarter_order
    },

    color_discrete_map={
        "Cephamycin": "#4e79a7",
        "3세대 Cephalosporins": "#f28e2b"
    },

    text="사용량"
)
fig_compare.update_layout(

    height=500,

    xaxis_title=None,
    yaxis_title="항생제 사용량 (DOT/1,000 patients-day)",

    paper_bgcolor='rgba(255,255,255,0)',
    plot_bgcolor='rgba(255,255,255,0)',

    margin=dict(
        l=20,
        r=20,
        t=20,
        b=40
    ),

    legend_title_text=""
)

fig_compare.update_traces(
    texttemplate='%{text:,.0f}',
    textposition='outside'
)
st.markdown("""
<div class="chart-title-box">
    <div class="chart-title">
        분기별 3세대 Cephalosporins 및 Cephamycin 사용량
    </div>
</div>
""", unsafe_allow_html=True)

st.plotly_chart(
    fig_compare,
    use_container_width=True,
    config={"displayModeBar": False},
    key="graph3"
)

st.markdown("<div style='margin-top:-40px'></div>",
unsafe_allow_html=True)


# =========================
# 4번 그래프
# 진료과별 TOP10 성분 사용량
# =========================

# 월별 / 성분별 고유키 개수
monthly_top10 = (
    filtered_df
    .groupby(
        ["분기", "처방 월", "성분통합키"]
    )["고유키"]
    .nunique()
    .reset_index()
)

# 분기별 평균
summary4 = (
    monthly_top10
    .groupby(["분기", "성분통합키"])["고유키"]
    .mean()
    .reset_index()
)

# 컬럼명 변경
summary4.columns = [
    "분기",
    "성분통합키",
    "항생제 사용량"
]

# 전체 기간 기준 TOP10 계산
top10_drug = (
    summary4
    .groupby("성분통합키")["항생제 사용량"]
    .sum()
    .reset_index()
)

top10_drug = (
    top10_drug
    .sort_values(
        "항생제 사용량",
        ascending=False
    )
    .head(10)
)

# TOP10 리스트
top10_drug_list = top10_drug["성분통합키"].tolist()

# TOP10만 필터
summary4 = summary4[
    summary4["성분통합키"].isin(top10_drug_list)
]

# 범례 순서
legend_order = top10_drug["성분통합키"].tolist()

# 꺾은선 그래프
fig4 = px.line(
    summary4,
    x="분기",
    y="항생제 사용량",
    color="성분통합키",
    markers=True,

    category_orders={
        "분기": quarter_order,
        "성분통합키": legend_order
    },

    color_discrete_sequence=px.colors.qualitative.Dark24
)

fig4.update_layout(

    height=520,

    xaxis_title=None,
    yaxis_title="항생제 사용량 (DOT/1,000 patients-day)",

    paper_bgcolor='rgba(255,255,255,0)',
    plot_bgcolor='rgba(255,255,255,0)',

    margin=dict(
        l=20,
        r=60,
        t=20,
        b=40
    ),

    xaxis_tickangle=20,

    legend=dict(

        orientation="v",

        yanchor="middle",
        y=0.5,

        xanchor="left",
        x=1.02,

        font=dict(
            size=10
        )
    ),

    legend_title_text=""
)
st.markdown("""
<div class="chart-title-box">
    <div class="chart-title">
        분기별 TOP10 항생제 사용량
    </div>
</div>
""", unsafe_allow_html=True)

st.plotly_chart(
    fig4,
    use_container_width=True,
    config={"displayModeBar": False},
    key="graph4"
)
