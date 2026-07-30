import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
import plotly.graph_objects as go
import base64
import random
import smtplib
import numpy as np
from plotly.subplots import make_subplots
from email.mime.text import MIMEText

# 페이지 설정
st.set_page_config(
    page_title="가톨릭관동대학교 국제성모병원 ASP DASHBOARD",
    layout="wide"
)
# =========================
# 로그인 세션
# =========================

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SENDER_EMAIL = "ckuasp@gmail.com"
try:
    APP_PASSWORD = st.secrets["gmail_password"]
    ADMIN_CODE = st.secrets["admin_code"]
except:
    APP_PASSWORD = "jymq rvhv siab farg"
    ADMIN_CODE = "CKUASP**"

if "verification_code" not in st.session_state:
    st.session_state.verification_code = None

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def send_email(recipient_email, code):

    msg = MIMEText(
        f"""
        인증번호는 {code} 입니다.

        본 사이트는 기관 내부 자료를 포함하고 있습니다.
        인증번호가 외부에 공유되지 않도록 관리하여 주시기 바랍니다.

        가톨릭관동대학교 국제성모병원
        ASP 전담팀

        관련문의
        양준원 / 내선.3449
        """
    )

    msg["Subject"] = "ASP DASHBOARD 인증번호"
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient_email

    server = smtplib.SMTP(
        SMTP_SERVER,
        SMTP_PORT
    )

    server.starttls()

    server.login(
        SENDER_EMAIL,
        APP_PASSWORD
    )

    server.send_message(msg)

    server.quit()

if not st.session_state.authenticated:

    st.markdown("""
    <div style="
        display:flex;
        justify-content:center;
        margin-top:10px;
    ">
    """, unsafe_allow_html=True)
    
    with open("circle1.png", "rb") as image_file:
        circle1_base64 = base64.b64encode(
            image_file.read()
        ).decode()

    col1, col2, col3 = st.columns([1,1.3,1])

    with col2:

        st.markdown(f"""
        <div style="
            background:#f9f9f9;
            border-radius:32px;
            padding:16px 40px;
            box-shadow:0 6px 20px rgba(0,0,0,0.12);
            text-align:center;
            margin-bottom:20px;
        ">

        <!-- 로고 -->
        <img src="data:image/png;base64,{circle1_base64}" style="
            width:260px;
            height:auto;
            margin-bottom:6px;
        ">

        <div style="
            font-size:30px;
            font-weight:800;
            color:#024ea2;
            margin-bottom:10px;
        ">
            ASP DASHBOARD
        </div>

        <div style="
            color:#024ea2;
            font-size:14px;
        ">
            기관 이메일 인증 후 이용 가능합니다
        </div>
        </div>
        """, unsafe_allow_html=True)

        email = st.text_input(
            "기관 이메일",
            placeholder="example@ish.ac.kr"
        )

        if st.button(
            "인증번호 발송",
            use_container_width=True
        ):

            if not email.endswith("@ish.ac.kr"):
                st.error(
                    "기관 이메일만 사용 가능합니다."
                )

            else:

                code = str(
                    random.randint(
                        100000,
                        999999
                    )
                )

                st.session_state.verification_code = code

                try:
                    send_email(email, code)

                    st.success(
                        "인증번호를 전송했습니다."
                    )

                except Exception as e:

                    st.error(
                        f"메일 전송 실패 : {e}"
                    )

        user_code = st.text_input(
            "인증번호 입력"
        )

        if st.button(
            "로그인",
            use_container_width=True
        ):

            # 관리자 코드 입력 시 즉시 로그인
            if user_code == ADMIN_CODE:

                st.session_state.authenticated = True
                st.rerun()

            # 일반 사용자 인증
            elif (
                user_code
                ==
                st.session_state.verification_code
            ):

                st.session_state.authenticated = True
                st.rerun()

            else:

                st.error(
                    "인증번호가 일치하지 않습니다."
                )

    st.stop()

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700;800&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Nanum Gothic';
}

.stApp {
    background-color: #f3f4f6;
}

[data-testid="stAppViewContainer"] {
    background-color: #f3f4f6;
}

/* 브라우저 기본 여백 제거 */
html, body, [class*="css"]  {
    margin: 0 !important;
    padding: 0 !important;
}

div[data-testid="stPlotlyChart"] {
    background: white;

    border-radius: 10px;

    padding: 0px;

    overflow: hidden;

    box-shadow: 0 2px 8px rgba(0,0,0,0.12);
}

/* 메인 제목 박스 */
.title-box {
    background: #0d4da2;
    padding: 8px 20px;
    border-radius: 28px;
    margin-bottom: 16px;

    /* 그림자 */
    box-shadow: 0 4px 14px rgba(0,0,0,0.14);

    display: flex;

    align-items: center;
    flex-direction: column;

    justify-content: center;

    gap: 0px;
}


/* 메인 제목 글씨 */
.title-text {
    color: #ffffff;
    font-size: 28px;
    font-weight: 500;
    text-align: center;
    margin-top: -26px;
    margin-bottom: 8px;
}

/* 그래프 제목 박스 */
.chart-title-box {

    background: #f1f7fe;

    padding: 14px 24px;

    border-radius: 18px;

    width: fit-content;

    margin-left: 28px;

    margin-bottom: -10px;

    position: relative;

    z-index: 100;

    pointer-events: none;

    box-shadow: 0 3px 8px rgba(0,0,0,0.10);

    border: 1px solid #c8d6e8;
}

/* 그래프 제목 글씨 */
.chart-title {

    font-size: 20px;

    font-weight: 800;

    color: #17406d;

    margin: 0;
}

/* 컬럼 제목 박스 */
.column-title-box {

    background-color: #f1f7fe;

    padding: 14px 24px;

    border-radius: 18px;

    width: fit-content;

    margin-left: 0px;

    margin-bottom: 5px;

    position: relative;

    pointer-events: none;

    box-shadow: 0 3px 8px rgba(0,0,0,0.10);

    border: 1px solid #c8d6e8;
}

/* 그래프 제목 글씨 */
.column-title {

    font-size: 18px;

    font-weight: 600;

    color: #17406d;

    margin: 0;
}


html, body {
    overflow-x: hidden;
}

html, body {
    overflow-x: hidden;
}

button[kind="header"] {
    display: none !important;
}

[data-testid="stHeaderActionElements"] {
    display: none !important;
}

[data-testid="stToolbarActions"] {
    display: none !important;
}

/* 버튼 focus 점 제거 */
button:focus {
    outline: none !important;
    box-shadow: none !important;
}

button:focus-visible {
    outline: none !important;
    box-shadow: none !important;
}

/* streamlit 내부 focus ring 제거 */
.stButton button:focus {
    outline: none !important;
    box-shadow: none !important;
}

.stButton button:focus-visible {
    outline: none !important;
    box-shadow: none !important;
}

/* 숨겨진 anchor 점 제거 */
a:focus,
a:focus-visible {
    outline: none !important;
}
div.stButton {
    outline: none !important;
}

div.stButton *:focus {
    outline: none !important;
    box-shadow: none !important;
}
iframe {
    min-height: 0px !important;
    height: 0px !important;
}

div[data-testid="stIFrame"] {
    display: none !important;
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

    color: #003bd6;

    margin-top: 20px;
}

.loading-sub {

    font-size: 16px;

    color: #003bd6;

    margin-top: 12px;
}
/* select 전체 */
/* 1. Selectbox 최외각 컨테이너 */
div[data-testid="stSelectbox"] {
    border-radius: 12px !important;
    padding: 16px;
    border: 2px solid #17406D !important; /* 선명한 네이비 테두리 강제 적용 */
    background-color: #ffffff !important;  /* 깔끔한 흰색 배경 */
    box-shadow: 0 2px 6px rgba(23, 64, 109, 0.12) !important;
    overflow: hidden !important;
    transition: all 0.2s ease-in-out;
}

/* 2. 내부 자식 div (BaseWeb 내부 테두리 및 배경 덮어쓰기 방지) */
div[data-testid="stSelectbox"] > div {
    border: none !important;              /* 자식 요쇼의 테두리를 지워 부모 테두리가 보이게 함 */
    background: transparent !important;   /* 배경을 투명하게 설정 */
    min-height: 44px;
    display: flex;
    align-items: center;
}

/* 3. Input 텍스트 영역 */
div[data-testid="stSelectbox"] input {
    background: transparent !important;
    caret-color: transparent !important;
}

/* 4. 마우스 Hover 시 (테두리 색상 및 진함 강화) */
div[data-testid="stSelectbox"] :hover {
    border-color: #0d2847 !important; /* 더 짙은 진한 파란색으로 강조 */
}

/* 5. 클릭(Focus/Active) 및 내부 선택 시 */
div[data-testid="stSelectbox"] :focus-within,
div[data-testid="stSelectbox"] :active {
    border-color: #2563eb !important; /* 포커스 시 또렷한 파란색 포인트 */
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.2) !important; /* 파란색 그림자 라인 */
    outline: none !important;
}

/* 6. 불필요한 포커스 링 완전 제거 */
div[data-testid="stSelectbox"] :focus-within {
    outline: none !important;
    box-shadow: none !important;
}


/* 하단 섹션 제목 박스 */
.section-title-box {

    background-color: #17406d;

    border-radius: 22px;

    padding: 12px 24px;

    margin-top: 10px;

    margin-bottom: 18px;

    box-shadow: 0 3px 8px rgba(0,0,0,0.08);

    text-align: center;

    border: 1px solid #c5d9f1;
}

/* 하단 섹션 제목 글씨 */
.section-title-text {

    color: white;

    font-size: 28px;

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

div.stButton > button {
    border-radius: 14px;
    height: 48px;
    font-weight: 700;
    font-size: 34px !important;
}
/* 상단 메뉴 영역 */
.top-menu-wrap {

    display: flex;

    justify-content: center;

    margin-top: 8px;

    margin-bottom: 28px;
}

/* 버튼 컨테이너 */
.top-menu-inner {

    display: flex;

    gap: 0;

    background: rgba(255,255,255,0.72);

    padding: 8px;

    border-radius: 28px;

    box-shadow: 0 4px 14px rgba(0,0,0,0.08);

    backdrop-filter: blur(6px);
}

/* 메뉴 버튼 공통 */
/* 버튼 기본 */
div.stButton > button {

    height: 82px !important;

    border-radius: 22px !important;

    border: 1px solid #d6dce5 !important;

    background: white !important;

    color: #1f2d3d !important;

    font-size: 34px !important;

    font-weight: 900 !important;

    letter-spacing: -0.5px;

    transition: 0.2s;

    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* hover */
div.stButton > button:hover {

    background: #eef4ff !important;
}

/* 선택된 메뉴 버튼 */
div.stButton > button[kind="secondary"] {

    background: linear-gradient(
        135deg,
        #5a9cf5,
        #3d7fe0
    ) !important;

    color: white !important;

    border: none !important;

    box-shadow: 0 4px 14px rgba(61,127,224,0.25);
}

/* 선택 안된 버튼 hover */
div.stButton > button[kind="primary"]:hover {

    background: #eef4ff !important;
}

/* status 영역 숨김 */
div[data-testid="stStatus"] {
    display:none !important;
}

/* status container 숨김 */
div[data-testid="stStatusWidget"] {
    display:none !important;
}

/* cache spinner 완전 숨김 */
.stCacheSpinner {
    display: none !important;
}

div[data-testid="stSpinner"].stCacheSpinner {
    display: none !important;
}
.class-tooltip{
    position:relative;
    cursor:pointer;
    margin-left:8px;
    color:#17406D;
}

.class-tooltip-text{

    visibility:hidden;

    position:absolute;

    left:50%;
    top:28px;

    transform:translateX(-50%);

    width:260px;

    background:#17406D;
    color:white;

    padding:12px;

    border-radius:10px;

    text-align:left;
    font-size:12px;
    font-weight:400;
    line-height:1.6;

    z-index:999;
}

.class-tooltip:hover .class-tooltip-text{
    visibility:visible;
}

.loading-overlay {
    position: fixed;
    top:0;
    left:0;
    width:100%;
    height:100%;
    background:white;
    z-index:99999;

    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
}

.drug-table{
    width:100%;
    border-collapse:collapse;
    font-size:15px;
}

.drug-table th{
    background:#f8fafc;
    color:#17406d;
    font-weight:550;
    font-size:15px;
    text-align:center;
    padding:8px;
    border:1px solid #ddd;
}

.drug-table td{
    background:white;
    color:#222;
    text-align:center;
    padding:6px;
    border:1px solid #eee;
}

.drug-table th:first-child{
    text-align:center;
    background:#f8fafc;
}

.drug-table tbody tr:first-child td{
    background:#dbe7f5;      /* 일반 행보다 조금 진한 배경 */
    font-weight:bold;
    text-align:center;       /* 전체 행 가운데 정렬 */
    border-top:2px solid #b7c9e2;
    border-bottom:2px solid #b7c9e2;
}

/* 첫 번째 열의 데이터(성분명)는 왼쪽 */
.drug-table td:first-child{
    background:#f1f5f9;
    font-weight:500;
    text-align:left;
    white-space:nowrap;
    padding-left:12px;
}

.notice-table{
    width:100%;
    border-collapse:collapse;
    margin-top:15px;
}

.notice-table th{
    background:#eef5ff;
    color:#17406D;
    padding:10px;
    text-align:center;
    border:1px solid #d7e3f4;
}

.notice-table td{
    padding:10px;
    border:1px solid #e8edf5;
    text-align:center;
}

.notice-table tbody tr:hover{
    background:#f8fbff;
}

</style>
""", unsafe_allow_html=True)

import base64

with open("long2.png", "rb") as image_file:
    long2_base64 = base64.b64encode(
        image_file.read()
    ).decode()

title_html = f"""
<div class="title-box">

<!-- 로고 영역 -->
<div style="
    display:flex;
    align-items:center;
    gap:0px;
">

<img src="data:image/png;base64,{long2_base64}" style="
    height:110px;
    width:auto;
">
</div>

<!-- 제목 -->
<div class="title-text">
    ASP DASHBOARD
</div>

</div>
"""

st.markdown(title_html, unsafe_allow_html=True)

# 기본 메뉴
if "menu" not in st.session_state:
    st.session_state.menu = "안내사항"

if "abx_loaded" not in st.session_state:
    st.session_state.abx_loaded = False

sp1, center, sp2 = st.columns([1, 4, 1])

with center:

    st.markdown("""
    <style>
    .menu-button-wrap {
        display:flex;
        gap:16px;
    }
    /* 버튼 전체 */
    div.stButton > button {
        font-size:23px !important;
        font-weight:700 !important;
        height:70px !important;
        border-radius:16px !important;
    }

    /* 버튼 hover */
    div.stButton > button:hover {
        transform:translateY(-1px);
        transition:0.2s;
    }

    .graph-card {
        background:white;
        border-radius:28px;
        padding:20px;
        box-shadow:0 2px 10px rgba(0,0,0,0.08);
        margin-bottom:20px;
    }

    .fade-in {
        animation: fadeIn 0.4s ease-in;
    }

    @keyframes fadeIn {
        from {
            opacity:0;
            transform:translateY(5px);
        }
        to {
            opacity:1;
            transform:translateY(0);
        }
    }

    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.button(
            "📌 안내사항",
            use_container_width=True,
            key="menu0",
            type=(
                "secondary"
                if st.session_state.menu == "안내사항"
                else "primary"
            ),
            on_click=lambda: st.session_state.update(
                menu="안내사항"
            )
        )

    # 왼쪽 버튼
    with col2:

        st.button(
            "📊 항생제 사용량",
            use_container_width=True,
            key="menu1",
            type=(
                "secondary"
                if st.session_state.menu == "항생제 사용량"
                else "primary"
            ),
            on_click=lambda: st.session_state.update(
                menu="항생제 사용량"
            )
        )

    with col3:

        st.button(
            "📋 ASP 중재",
            use_container_width=True,
            key="menu2",
            type=(
                "secondary"
                if st.session_state.menu == "ASP 중재"
                else "primary"
            ),
            on_click=lambda: st.session_state.update(
                menu="ASP 중재"
            )
        )

    # 오른쪽 버튼
    with col4:

        st.button(
            "👨‍⚕️ASP팀 활동",
            use_container_width=True,
            key="menu3",
            type=(
                "secondary"
                if st.session_state.menu == "ASP팀 활동"
                else "primary"
            ),
            on_click=lambda: st.session_state.update(
                menu="ASP팀 활동"
            )
        )

if st.session_state.menu == "안내사항":

    with open("pill2.png", "rb") as image_file:
        pill_base64 = base64.b64encode(
            image_file.read()
        ).decode()

    st.markdown(f"""
    <div style="
        background:#ebf1fb;
        border-radius:28px;
        padding:28px 40px;
        box-shadow:0 2px 10px rgba(0,0,0,0.08);
        display:flex;
        align-items:center;
        gap:40px;
        margin-bottom:20px;
    ">

    <div style="flex:1.4;">

    <div style="
        font-size:30px;
        font-weight:800;
        color:#17406D;
        margin-left:8px;
        margin-bottom:12px;
    ">
        📌 안내사항
    </div>

    <div style="
        background:#f8fbff;
        border-radius:20px;
        padding:16px 28px;
        box-shadow:0 2px 8px rgba(0,0,0,0.05);    
        font-size:16px;
        font-family:'Nanum Gothic';
        line-height:1.8;
        color:#374151;
        margin-bottom:16px;
    ">
    [공지] 2026년 6월 자료가 업데이트 되었습니다.
    <br><br>

    1. 본 홈페이지는 기관 자료를 포함하고 있습니다.
    무단 전재, 복사 또는 외부 유출을 금하며, 열람 및 취급 시 유의하여 주시기 바랍니다.
    <br>
    2. 본 자료는 실시간 데이터를 반영하지 않습니다.
    매월 초 한 달간의 자료를 업데이트하고 있으며,
    항생제 적정사용관리 시범사업 참여 시점인
    2024년 11월 이후의 자료를 기준으로 작성되었습니다.
    <br>
    3. 홈페이지 및 자료와 관련된 문의는 다음으로 연락주시기 바랍니다.
    <br>(양준원 / 내선. 3449)
    <br>
    감사합니다.
    <br>
    가톨릭관동대학교 국제성모병원 ASP 전담팀
    </div>

    </div>

    <div style="
        flex:1;
        text-align:center;
    ">
        <img src="data:image/png;base64,{pill_base64}"
                style="
                width:100%;
                max-width:420px;
                ">
    </div>

    </div>
    """, unsafe_allow_html=True)


    st.markdown("""
    <div class="section-title-box">
        <div class="section-title-text">
            항생제 관련 안내사항
        </div>
    </div>
    """, unsafe_allow_html=True)


    if "notice_tab" not in st.session_state:
        st.session_state.notice_tab = "신약"

    st.markdown("""
    <style>

    /* 게시판 카드 */
    .notice-board{
        background:white;
        border-radius:28px;
        padding:28px;
        box-shadow:0 2px 10px rgba(0,0,0,0.08);
        border:1px solid #e5edf7;
        margin-bottom:20px;
    }

    /* 내용 제목 */
    .notice-title{
        font-size:26px;
        font-weight:800;
        color:#17406D;
        margin-bottom:16px;
    }

    /* 내용 */
    .notice-content{
        background:#f8fbff;
        border-radius:18px;
        padding:22px;
        font-size:18px;
        line-height:1.9;
        color:#444;
        border:1px solid #dbe7f5;
    }

    </style>
    """, unsafe_allow_html=True)

    sp3, sp4, sp5 = st.columns([1, 4, 1])

    with sp4:

        col1, col2, col3 = st.columns(3)

        with col1:
            st.button(
                "🆕 항생제 신약 정보",
                use_container_width=True,
                type="secondary" if st.session_state.notice_tab=="신약" else "primary",
                on_click=lambda: st.session_state.update(notice_tab="신약")
            )

        with col2:
            st.button(
                "📦 항생제 품절 정보",
                use_container_width=True,
                type="secondary" if st.session_state.notice_tab=="품절" else "primary",
                on_click=lambda: st.session_state.update(notice_tab="품절")
            )

        with col3:
            st.button(
                "📄 항생제 허가사항 변경",
                use_container_width=True,
                type="secondary" if st.session_state.notice_tab=="허가" else "primary",
                on_click=lambda: st.session_state.update(notice_tab="허가")
            )

        # --------------------
        # 내용
        # --------------------

    def get_base64_image(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    aug_base64 = get_base64_image("aug.png")
    gem_base64 = get_base64_image("gem.png")
    com_base64 = get_base64_image("com.png") # 1 | 병합(중복)

    if st.session_state.notice_tab == "신약":

        st.markdown(f"""
        <div class="notice-board">
            <div class="notice-title">
            🆕 항생제 신약 정보
            </div>
            <div class="notice-content">
            <p><b>1) 2026년도 1분기 항생제 신약</b></p>
            <table class="notice-table">
            <thead>
            <tr>
                <th> </th>
                <th>항목명</th>
                <th>코드명</th>
                <th>성분명</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>
                    <img
                        src="data:image/png;base64,{aug_base64}"
                        style="
                            width:160px;
                            border-radius:10px;
                        "> 
                </td>
                <td><b>크라목신 주 600MG</b></td>
                <td>W-AUG6J</td>
                <td>Amoxicillin/clavulanate</td>
            </tr>
                        <tr>
                <td>
                    <img
                        src="data:image/png;base64,{gem_base64}"
                        style="
                            width:160px;
                            border-radius:10px;
                        "> 
                </td>
                <td><b>팩티브 정 320MG</b></td>
                <td>W-GMF320</td>
                <td>Gemifloxacin</td>
            </tr>
            </tbody>
            </table>
            <p><b>2) 2025년도 하반기 항생제 신약</b></p>
            <table class="notice-table">
            <thead>
            <tr>
                <th> </th>
                <th>항목명</th>
                <th>코드명</th>
                <th>성분명</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>
                    <img
                        src="data:image/png;base64,{com_base64}"
                        style="
                            width:160px;
                            border-radius:10px;
                        "> 
                </td>
                <td><b>콤비신 주 4.5G</b></td>
                <td>W-PSB4GJ</td>
                <td>Piperacillin/Sulbactam</td>
            </tr>
            </tbody>
            </table>
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif st.session_state.notice_tab == "품절":

        st.markdown(f"""
        <div class="notice-board">   
            <div class="notice-title">
            📦 항생제 품절 정보
            </div>
            <div class="notice-content">
            <p><b>1) 현재 품절 중인 항생제</b></p>
            <table class="notice-table">
            <thead>
            <tr>
                <th>항목명</th>
                <th>코드명</th>
                <th>성분명</th>
                <th>품절 기한</th>
                <th>대체 약품</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td><b>칸시다스 주 70MG</b></td>
                <td>CSF70J</td>
                <td>Caspofungin</td>
                <td><b>26/08/31</b></td>
                <td><b>동일성분, 동일계열 대체 약품 없음</b></td>
            </tr>
            <tr>
                <td><b>오큐프록스 안연고</b></td>
                <td>O-OFLOC</td>
                <td>Ofloxacin</td>
                <td><b>생산 중단</b></td>
                <td>동일 성분 <b>퀴노비드 안연고</b> 입고 예정</td>
            </tr>
            </tbody>
            </table>
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown(f"""
        <div class="notice-board"> 
            <div class="notice-title">
            📄 항생제 허가사항 변경
            </div>
            <div class="notice-content">
            <p><b>1) 허가사항 변경명령 알림</b></p>
            <table class="notice-table">
            <thead>
            <tr>
                <th>성분명</th>
                <th>본원 해당 약품</th>
                <th>변경 항목</th>
                <th>변경 내용</th>
                <th>반영 일자</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td><b>Ampicillin/Sulbactam</b></td>
                <td>박타신 주 750MG</td>
                <td>이상반응</td>
                <td style="text-align:left;"><b><신설></b><br>호산구 증가 및 전산 증상 동반 약물 반응(DRESS)</td>
                <td>26/08/18</td>
            </tr>
            <tr>
                <td><b>Minocycline</b></td>
                <td>미노씬 캡슐 50MG</td>
                <td>이상반응</td>
                <td style="text-align:left;"><b><변경></b><br>가성뇌종양(양성두개내고혈압)<br>▶ 가성뇌종양(특발성 두개 내압 항진증)
                <br><b><신설></b><br>1. 투약을 중단하면 대개 증상이 해소되지만<br>영구적으로 시력이 손상될 가능성도 있으므로...<br>2. 약물 투여를 중단하더라도<br>두개 내압 상승이 수주 동안 지속될 수 있으므로...</td>
                <td>26/08/18</td>
            </tr>
            <tr>
                <td><b>Tigecycline</b></td>
                <td>타이가실 주 50MG</td>
                <td>이상반응</td>
                <td style="text-align:left;"><b><신설></b><br>테트라사이클린계 항생제와<br> 유사한 이상반응을 보일 수 있다.</td>
                <td>26/09/16</td>
            </tr>
            <tr>
                <td><b>Cefixime</b></td>
                <td>슈프락스 캅셀 100MG<br>슈프락스 산 50MG/G</td>
                <td>이상반응</td>
                <td style="text-align:left;"><b><신설></b><br>뇌병증</td>
                <td>26/09/16</td>
            </tr>
            <tr>
                <td><b>Meropenem</b></td>
                <td>메바페넴 주 1G<br>메바페넴 주 500MG</td>
                <td>이상반응</td>
                <td style="text-align:left;"><b><변경></b><br>간부전 ▶ 약물-유발 간 손상(간염 및 간부전 포함)
                <br><b><신설></b><br>중증 약물 유발 간 손상이 발생한 경우,<br> 투여 중단을 고려해야 하며 치료에 필수적인 것으로<br> 평가될 경우에만 투여를 재개해야 한다.</td>
                <td>26/10/16</td>
            </tr>
            </tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)



elif st.session_state.menu == "항생제 사용량":

    @st.cache_data(ttl=86400)
    def load_data():

        df = pd.read_parquet("ASP.parquet")

        day_df = pd.read_parquet("재원일수.parquet")

        master_df = pd.read_parquet("마스터.parquet")

        return df, day_df, master_df

    @st.cache_data(ttl=86400)
    def create_summary1(df, day_df):

        day_dict = dict(
            zip(
                day_df["처방 월"],
                day_df["재원일수"]
            )
        )

        monthly_total = (
            df
            .groupby(["분기", "처방 월"])["고유키"]
            .nunique()
            .reset_index(name="DOT")
        )

        monthly_total["DOT"] = (
            monthly_total["DOT"]
            /
            monthly_total["처방 월"].map(day_dict)
            * 1000
        )

        summary1 = (
            monthly_total
            .groupby("분기")["DOT"]
            .mean()
            .reset_index()
        )

        return summary1

    @st.cache_data
    def load_images():

        with open("pill.png", "rb") as f:
            pill = base64.b64encode(f.read()).decode()

        with open("icon1.png", "rb") as f:
            icon1 = base64.b64encode(f.read()).decode()

        with open("icon2.png", "rb") as f:
            icon2 = base64.b64encode(f.read()).decode()

        return pill, icon1, icon2

    pill_base64, icon1_base64, icon2_base64 = load_images()

    if not st.session_state.abx_loaded:

        with open("rotation1.gif", "rb") as f:
            gif_base64 = base64.b64encode(f.read()).decode()

        loading = st.empty()

        with loading.container():

            st.markdown(
                f"""
                <div style="text-align:center;">
                    <img src="data:image/gif;base64,{gif_base64}" width="250">
                    <h2 style="
                        color:#0339dd;
                        font-weight:800;
                    ">
                        데이터를 조회하고 있습니다...
                    </h2>
                </div>
                """,
                unsafe_allow_html=True
            )

        df, day_df, master_df = load_data()

        loading.empty()

        st.session_state.abx_loaded = True

    else:

        df, day_df, master_df = load_data()

    st.markdown("""
    <div class="section-title-box">
        <div class="section-title-text">
            총 항생제 사용량
        </div>
    </div>
    """, unsafe_allow_html=True)

    day_dict = dict(
        zip(
            day_df["처방 월"],
            day_df["재원일수"]
        )
    )


    # 분기 변환 함수
    def convert_quarter(month):

        month = str(month)

        quarter_map = {
            "24/11": "24년도 4분기",
            "24/12": "24년도 4분기",

            "25/01": "25년도 1분기",
            "25/02": "25년도 1분기",
            "25/03": "25년도 1분기",

            "25/04": "25년도 2분기",
            "25/05": "25년도 2분기",
            "25/06": "25년도 2분기",

            "25/07": "25년도 3분기",
            "25/08": "25년도 3분기",
            "25/09": "25년도 3분기",

            "25/10": "25년도 4분기",
            "25/11": "25년도 4분기",
            "25/12": "25년도 4분기",

            "26/01": "26년도 1분기",
            "26/02": "26년도 1분기",
            "26/03": "26년도 1분기",

            "26/04": "26년도 2분기",
            "26/05": "26년도 2분기",
            "26/06": "26년도 2분기"
        }
        return quarter_map.get(month)

    # 분기 컬럼 생성
    df["분기"] = df["처방 월"].apply(convert_quarter)

    # =========================
    # KPI 카드용 데이터 계산
    # =========================

    # 처방월 정렬
    month_order = sorted(df["처방 월"].dropna().unique())

    # 최근 월 / 직전 월
    latest_month = month_order[-1]
    prev_month = month_order[-2]

    # KPI 제목용 월 표시
    year, month = latest_month.split("/")
    latest_month_text = f"20{year}년 {int(month)}월"

    # =========================
    # 총 항생제 사용량
    # =========================

    latest_total = (
        df[df["처방 월"] == latest_month]["고유키"]
        .nunique()
        / day_dict[latest_month]
        *1000
    )
    latest_total = round(latest_total, 1)

    prev_total = (
        df[df["처방 월"] == prev_month]["고유키"]
        .nunique()
        / day_dict[prev_month]
        *1000
    )
    prev_total = round(prev_total, 1)

    total_change = (
        (latest_total - prev_total)
        / prev_total
    ) * 100

    # =========================
    # 제한항생제 사용량
    # =========================

    latest_restricted = (
        df[
            (df["처방 월"] == latest_month)
            & (df["제한항생제"] == "O")
        ]["고유키"]
        .nunique()
        / day_dict[latest_month]
        *1000
    )
    latest_restricted = round(latest_restricted, 1)

    prev_restricted = (
        df[
            (df["처방 월"] == prev_month)
            & (df["제한항생제"] == "O")
        ]["고유키"]
        .nunique()
        / day_dict[prev_month]
        *1000
    )
    prev_restricted = round(prev_restricted, 1)

    restricted_change = (
        (latest_restricted - prev_restricted)
        / prev_restricted
    ) * 100

    # 총 사용량 상승/하락 표시
    if total_change >= 0:
        total_arrow = "▲"
        total_color = "#f08080"
    else:
        total_arrow = "▼"
        total_color = "#10B981"

    # 제한항생제 상승/하락 표시
    if restricted_change >= 0:
        restricted_arrow = "▲"
        restricted_color = "#f08080"
    else:
        restricted_arrow = "▼"
        restricted_color = "#10B981"

    total_change_text = f"{total_arrow} {abs(total_change):.1f}%"

    # KPI 카드
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="
            background:white;
            border-radius:28px;
            padding:28px 36px;
            box-shadow:0 2px 10px rgba(0,0,0,0.08);
            margin-bottom:20px;
        ">

        <!-- 타이틀 -->
        <div style="
            font-size:20px;
            font-weight:800;
            color:#102a43;
            margin-bottom:22px;
        ">
            이달의 총 항생제 사용량
            <span style="
                font-size:13px;
                font-weight:500;
                color:#6b7280;
                margin-left:6px;
            ">
                ({latest_month_text} 기준)
            </span>
        </div>

        <!-- 본문 -->
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
        ">

        <!-- 왼쪽 숫자 + 단위 -->
        <div>

        <div style="
            font-size:58px;
            font-weight:800;
            color:#17406D;
            line-height:1.0;
            margin-bottom:8px;
        ">
            {latest_total:,}
        </div>

        <div style="
            font-size:18px;
            font-weight:400;
            color:#6b7280;
        ">
            DOT/1,000 patient-days
        </div>

        </div>

        <!-- 오른쪽 변화율 -->
        <div style="
            text-align:center;
            padding-left:30px;
            border-left:1px solid #d1d5db;
        ">

        <div style="
            font-size:18px;
            font-weight:700;
            color:#374151;
            margin-bottom:8px;
        ">
            지난 달 대비
        </div>

        <div style="
            font-size:36px;
            font-weight:800;
            color:{total_color};
        ">
            {total_change_text}
        </div>

        </div>

        </div>

        </div>
        """, unsafe_allow_html=True)


    with col2:
        st.markdown(f"""
        <div style="
            background:white;
            border-radius:28px;
            padding:28px 36px;
            box-shadow:0 2px 10px rgba(0,0,0,0.08);
            margin-bottom:20px;
        ">

        <!-- 제목 영역 -->
        <div style="
            margin-bottom:0px;
        ">

        <!-- 타이틀 + 안내 아이콘 -->
        <div style="
            display:flex;
            align-items:center;
            gap:10px;
        ">

        <div style="
            font-size:20px;
            font-weight:800;
            color:#102a43;
        ">
            이달의 제한항생제 사용량
            <span style="
                font-size:13px;
                font-weight:500;
                color:#6b7280;
                margin-left:6px;
            ">
                ({latest_month_text} 기준)
            </span>
        </div>

        <!-- i 아이콘 -->
        <div class="tooltip-container" style="
            position:relative;
            display:inline-block;
            cursor:pointer;
        ">

        <!-- 동그란 i -->
        <div style="
            width:24px;
            height:24px;
            border-radius:50%;
            background:#e8eef7;
            color:#17406D;
            font-size:16px;
            font-weight:700;
            display:flex;
            align-items:center;
            justify-content:center;
        ">
            i
        </div>

        <!-- 툴팁 -->
        <div class="tooltip-box" style="
            visibility:hidden;
            opacity:0;
            transition:0.2s;
            position:absolute;
            top:35px;
            right:40px;
            left:auto;
            width:540px;
            background:#0F2E4F;
            color:white;
            padding:18px 20px;
            border-radius:16px;
            box-shadow:0 8px 24px rgba(0,0,0,0.18);
            z-index:999;
            font-size:15px;
            line-height:1.6;
        ">

        <div style="
            font-size:17px;
            font-weight:800;
            margin-bottom:10px;
        ">
            제한항생제란?
        </div>

        무분별하고 광범위한 사용 시 항생제 내성을 유발하거나,
        기타의 이유로<br> 별도의 전문적인 관리가 필요하다고 판단되는 항생제로
        감염내과 전문의의<br> 승인 후 사용 가능한 항생제입니다.
        <br>
        -----------------------------------------------------------------------------------------------------------<br>
        <table style="
            width:100%;
            border-collapse:collapse;
            margin-top:8px;
            font-size:14px;
        ">

        <tr>
        <td style="
            background:rgba(255,255,255,0.12);
            padding:10px 12px;
            font-weight:700;
            border-radius:8px 0 0 8px;
            width:90px;
        ">
            Cephalosporins
        </td>

        <td style="
            padding:10px 12px;
        ">
            Ceftazidime, Ceftazidime/Avibactam, Cefepime, Ceftolozane/Tazobactam
        </td>
        </tr>

        <tr>
        <td style="
            background:rgba(255,255,255,0.12);
            padding:10px 12px;
            font-weight:700;
            border-radius:8px 0 0 8px;
            width:90px;
        ">
            Penicillins
        </td>

        <td style="
            padding:10px 12px;
        ">
            Piperacillin/Tazobactam, Piperacillin/Sulbactam
        </td>
        </tr>
        
        <tr>
        <td style="
            background:rgba(255,255,255,0.12);
            padding:10px 12px;
            font-weight:700;
            border-radius:8px 0 0 8px;
            width:90px;
        ">
            Carbapenems
        </td>

        <td style="
            padding:10px 12px;
        ">
            Ertapenem, Imipenem/Cilastatin, Meropenem
        </td>
        </tr>

       <tr>
        <td style="
            background:rgba(255,255,255,0.12);
            padding:10px 12px;
            font-weight:700;
            border-radius:8px 0 0 8px;
            width:90px;
        ">
            Glycopeptides
        </td>

        <td style="
            padding:10px 12px;
        ">
            Vancomycin, Teicoplanin
        </td>
        </tr>

       <tr>
        <td style="
            background:rgba(255,255,255,0.12);
            padding:10px 12px;
            font-weight:700;
            border-radius:8px 0 0 8px;
            width:90px;
        ">
            Quinolones
        </td>

        <td style="
            padding:10px 12px;
        ">
            Moxifloxacin
        </td>
        </tr>

       <tr>
        <td style="
            background:rgba(255,255,255,0.12);
            padding:10px 12px;
            font-weight:700;
            border-radius:8px 0 0 8px;
            width:90px;
        ">
            Tetracyclines
        </td>

        <td style="
            padding:10px 12px;
        ">
            Tigecycline
        </td>
        </tr>

       <tr>
        <td style="
            background:rgba(255,255,255,0.12);
            padding:10px 12px;
            font-weight:700;
            border-radius:8px 0 0 8px;
            width:90px;
        ">
            기타
        </td>

        <td style="
            padding:10px 12px;
        ">
            Linezolid, Colistin 등
        </td>
        </tr>

        </table>


        </div>
        </div>
        </div>
        <div style="height:22px;"></div>

        <style>
        .tooltip-container:hover .tooltip-box {{
            visibility:visible !important;
            opacity:1 !important;
        }}


        </style>

        <!-- 본문 -->
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
        ">

        <!-- 왼쪽 숫자 + 단위 -->
        <div>

        <div style="
            font-size:58px;
            font-weight:800;
            color:#17406D;
            line-height:1.0;
            margin-bottom:8px;
        ">
            {latest_restricted:,}
        </div>

        <div style="
            font-size:18px;
            font-weight:400;
            color:#6b7280;
        ">
            DOT/1,000 patient-days
        </div>

        </div>

        <!-- 오른쪽 변화율 -->
        <div style="
            text-align:center;
            padding-left:30px;
            border-left:1px solid #d1d5db;
        ">

        <div style="
            font-size:18px;
            font-weight:700;
            color:#374151;
            margin-bottom:8px;
        ">
            지난 달 대비
        </div>

        <div style="
            font-size:36px;
            font-weight:800;
            color:{restricted_color};
        ">
            {restricted_arrow} {abs(restricted_change):.1f}%
        </div>

        </div>

        </div>

        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="
        background:#f1f7fe;
        border:1px solid #d8e2ee;
        border-radius:28px;
        padding:24px 24px;
        margin-top:18px;
        box-shadow:0 4px 14px rgba(0,0,0,0.05);
        display:flex;
        align-items:center;
        margin-bottom:36px;
    ">

    <!-- 왼쪽 pill -->
    <div style="
        width:30%;
        text-align:center;
    "> 
        <img src="data:image/png;base64,{pill_base64}" style="width:260px;">
    </div>

    <!-- 가운데 세로선 -->
    <div style="
        width:1px;
        align-self:stretch;
        background:#d9e4ef;
        margin:0 40px;
    "></div>

    <!-- 오른쪽 설명 -->
    <div style="
        flex:1;
    ">

    <!-- 위 compartment -->
    <div style="
        display:flex;
        align-items:flex-start;
        gap:24px;
    ">

    <!-- 아이콘 -->
    <img src="data:image/png;base64,{icon1_base64}" style=" width:72px; height:72px;">

    <!-- 텍스트 -->
    <div>

    <div style="
        font-size:24px;
        font-weight:800;
        color:#1d4ed8;
        margin-bottom:12px;
    ">
        DOT (Days of Therapy)의 정의
    </div>

    <div style="
        font-size:18px;
        line-height:1.8;
        color:#374151;
        font-weight:700;
    ">
        환자에게 항생제가 투여된 일 수의 총합을 의미합니다.<br>
        같은 날 두 가지 항생제를 사용한 경우 각각 1일로 계산합니다.
    </div>

    </div>

    </div>

    <!-- 중간 점선 -->
    <div style="
        border-top:2px dashed #d7e3f0;
        margin:34px 0;
    "></div>

    <!-- 아래 compartment -->
    <div style="
        display:flex;
        align-items:flex-start;
        gap:24px;
    ">

    <!-- 아이콘 -->
    <img src="data:image/png;base64,{icon2_base64}" style=" width:72px; height:72px;">

    <!-- 텍스트 -->
    <div>

    <div style="
        font-size:24px;
        font-weight:800;
        color:#10b981;
        margin-bottom:12px;
    ">
        DOT/1,000 patient-days의 정의
    </div>

    <div style="
        font-size:18px;
        line-height:1.8;
        color:#374151;
        font-weight:700;
    ">
        전체 환자의 재원일수 1,000일당 항생제 투여일수(DOT)로,<br>
        기간별 입원 규모를 보정한 항생제 사용량 지표입니다.
    </div>

    </div>

    </div>

    </div>

    </div>
    """, unsafe_allow_html=True)

    # =========================
    # 첫번째 그래프
    # 전체 항생제 사용량
    # =========================

    # 월별 고유키 개수 계산
    summary1 = create_summary1(df, day_df)
    # 컬럼명 변경
    summary1.columns = [
        "분기",
        "항생제 사용량 (DOT/1,000 patient-days)"
    ]

    # 분기 순서 지정
    quarter_order = [
        "24년도 4분기",
        "25년도 1분기",
        "25년도 2분기",
        "25년도 3분기",
        "25년도 4분기",
        "26년도 1분기",
        "26년도 2분기"
    ]

    # 막대그래프 생성
    fig1 = px.bar(
        summary1,
        x="분기",
        y="항생제 사용량 (DOT/1,000 patient-days)",
        text="항생제 사용량 (DOT/1,000 patient-days)",

        category_orders={
            "분기": quarter_order
        },

        color_discrete_sequence=["lightcoral"]
    )

    fig1.update_layout(

        height=360,

        xaxis_title=None,

        yaxis=dict(
            range=[0, summary1["항생제 사용량 (DOT/1,000 patient-days)"].max() * 1.15]
        ),

        paper_bgcolor='white',
        plot_bgcolor='white',

        # 2번 그래프와 동일 margin
        margin=dict(
            l=20,
            r=60,
            t=20,
            b=20
        ),

        yaxis_tickformat=",",

        xaxis=dict(
        tickfont=dict(
            size=14
        )
        )
    )

    # 데이터 레이블 형식 변경
    # 데이터 레이블 형식 변경 + 막대 두께 조절
    fig1.update_traces(
        texttemplate='%{text:,.1f}',
        textposition='outside',

    # 데이터 레이블 글자 크기
        textfont_size=14,

        # 막대 폭 줄이기
        width=0.35,

        hovertemplate=
        "<b>%{fullData.name}</b><br>" +
        "분기: %{x}<br>" +
        "항생제 사용량: %{y:.1f}<extra></extra>"   
    )
    # x축을 숫자로 변환
    x_num = np.arange(len(summary1))

    # 선형회귀
    coef = np.polyfit(
        x_num,
        summary1["항생제 사용량 (DOT/1,000 patient-days)"],
        1
    )

    trend = np.poly1d(coef)

    slope = coef[0]

    if slope > 0:
        trend_text = f"<b>+{slope:.2f}</b> DOT/1,000 patient-days"
    elif slope < 0:
        trend_text = f"<b> {slope:.2f}</b> DOT/1,000 patient-days"
    else:
        trend_text = f"<b>0.00</b> DOT/1,000 patient-days"

    # 추세선 추가
    fig1.add_trace(
        go.Scatter(
            x=summary1["분기"],
            y=trend(x_num),
            mode="lines",
            name="Trend",
            showlegend=False,
            line=dict(
                color="#17406D",
                width=1,
                dash="dot"
            ),
             hovertemplate=
            "기울기<br>" +
            f"{trend_text}<extra></extra>"
        )
    )

    # 제한항생제 O만 필터
    abx_df = df[df["제한항생제"] == "O"]

    # 월별 / 성분별 고유키 개수 계산
    monthly = (
        abx_df
        .groupby(["분기", "처방 월", "성분통합키"])["고유키"]
        .nunique()
        .reset_index(name="DOT")
    )
    monthly["DOT"] = (
        monthly["DOT"]
        /
        monthly["처방 월"].map(day_dict)
        * 1000
    )

    # 분기별 평균 계산
    summary2 = (
        monthly
        .groupby(["분기", "성분통합키"])["DOT"]
        .mean()
        .reset_index()
    )

    # 컬럼명 변경
    summary2.columns = ["분기", "성분통합키", "항생제 사용량(DOT/1,000 patient-days)"]

    # TOP7 계산
    top7 = (
        summary2
        .groupby("성분통합키")["항생제 사용량(DOT/1,000 patient-days)"]
        .sum()
        .reset_index()
    )

    top7 = (
        top7
        .sort_values("항생제 사용량(DOT/1,000 patient-days)", ascending=False)
        .head(7)
    )

    top7_list = top7["성분통합키"].tolist()

    # TOP7만 남기기
    summary2 = summary2[
        summary2["성분통합키"].isin(top7_list)
    ]

    # 분기 순서 지정
    quarter_order = [
        "24년도 4분기",
        "25년도 1분기",
        "25년도 2분기",
        "25년도 3분기",
        "25년도 4분기",
        "26년도 1분기",
        "26년도 2분기"
    ]

    # 범례 순서
    category_order = top7["성분통합키"].tolist()

    # 꺾은선 그래프
    fig2 = px.bar(
        summary2,
        x="분기",
        y="항생제 사용량(DOT/1,000 patient-days)",
        color="성분통합키",

        category_orders={
            "분기": quarter_order,
            "성분통합키": category_order
        },

        color_discrete_sequence=[
            "#8DBBFF",  # blue
            "#9FD08F",  # green
            "#F5B56E",  # orange
            "#EE8F8F",  # red
            "#C99AF5",  # purple
            "#82DDF0",  # cyan
            "#F2A9D1",  # pink
        ],
    )

    # 마지막 분기
    last_quarter = "26년도 2분기"

    # 마지막 분기 데이터
    last_points = summary2[
        summary2["분기"] == last_quarter
    ]


    fig2.update_layout(

        barmode="stack",

        height=440,

        xaxis_title=None,

        yaxis=dict(
            range=[0,225]
        ),

        paper_bgcolor='white',
        plot_bgcolor='white',

        # 그래프 영역 최대화
        margin=dict(
            l=20,
            r=60,
            t=20,
            b=20
        ),

    legend=dict(
        orientation="v",

        # 세로 중앙
        yanchor="top",
        y=0.7,

        xanchor="left",
        x=1.02,

        # 글씨 약간 키우기
        font=dict(
            size=11
        )

    ),
    legend_traceorder="reversed",

        # 범례 제목 제거
        legend_title_text=""
    )


    fig2.update_traces(
        width=0.45,   # 0~1 사이, 작을수록 얇아짐
        hovertemplate=
        "<b>%{fullData.name}</b><br>" +
        "분기: %{x}<br>" +
        "항생제 사용량: %{y:.1f}<extra></extra>"
    )



    # =========================
    # 총 항생제 사용량
    # =========================

    st.markdown("""
    <div class="chart-title-box">
        <div class="chart-title">
            📊 분기별 총 항생제 사용량 평균
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.plotly_chart(
        fig1,
        use_container_width=True,
        config={"displayModeBar": False},
        key="graph1"
    )

    # 그래프 사이 간격
    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    # =========================
    # 제한항생제 사용량
    # =========================

    st.markdown("""
    <div class="chart-title-box">
        <div class="chart-title">
            💊 분기별 주요 제한항생제 사용량 평균
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
    # 제한항생제 표
    # =========================

    colors = [
        "#8DBBFF",
        "#9FD08F",
        "#F5B56E",
        "#EE8F8F",
        "#C99AF5",
        "#82DDF0",
        "#F2A9D1",
    ]

    color_map = {
        drug: colors[i % len(colors)]
        for i, drug in enumerate(category_order)
    }

    # -------------------------
    # TOP7 표 생성
    # -------------------------

    table_df = (
        summary2
        .pivot(
            index="성분통합키",
            columns="분기",
            values="항생제 사용량(DOT/1,000 patient-days)"
        )
        .reindex(category_order)
        .reindex(columns=quarter_order)
        .fillna(0)
        .round(1)
    )

    table_df.columns.name = None

    latest_q = quarter_order[-1]
    prev_q = quarter_order[-2]

    # -------------------------
    # 모든 제한항생제 총합
    # (TOP7이 아니라 전체)
    # -------------------------

    monthly_total = (
        abx_df
        .groupby(["분기", "처방 월"])["고유키"]
        .nunique()
        .reset_index(name="DOT")
    )

    monthly_total["DOT"] = (
        monthly_total["DOT"]
        /
        monthly_total["처방 월"].map(day_dict)
        * 1000
    )

    total_row = (
        monthly_total
        .groupby("분기")["DOT"]
        .mean()
        .reindex(quarter_order)
        .fillna(0)
        .round(1)
    )

    def add_arrow(current, previous):

        current = float(current)
        previous = float(previous)

        if current > previous:
            return (
                f"{current:.1f} "
                '<span style="color:#e53935;font-size:16px;font-weight:bold;">▲</span>'
            )

        elif current < previous:
            return (
                f"{current:.1f} "
                '<span style="color:#1e88e5;font-size:16px;font-weight:bold;">▼</span>'
            )

        else:
            return f"{current:.1f}"


    # 첫 행 추가
    table_df = pd.concat(
        [pd.DataFrame([total_row], index=["TOTAL"]), table_df]
    )

    # 마지막 분기 화살표
    table_df[latest_q] = table_df.apply(
        lambda row: add_arrow(
            row[latest_q],
            row[prev_q]
        ),
        axis=1
    )

    # 나머지 분기 문자열 변환
    for q in quarter_order[:-1]:
        table_df[q] = table_df[q].map(lambda x: f"{x:.1f}")

    # 첫 번째 열 생성
    name_col = ["<b>제한항생제 총합</b>"] + [
        f'<span style="display:inline-block;width:10px;height:10px;'
        f'border-radius:50%;background:{color_map[d]};'
        f'margin-right:8px;vertical-align:middle;"></span>{d}'
        for d in category_order
    ]

    table_df.insert(0, "", name_col)

    table_df = table_df.reset_index(drop=True)

    # 출력
    st.markdown(
        table_df.to_html(
            escape=False,
            index=False,
            classes="drug-table"
        ),
        unsafe_allow_html=True
    )


        # =========================
    # 진료과 선택
    # =========================

    dept_list1 = sorted(
        [x for x in df["분류"].dropna().unique() if x != "0x2a"],
        key=lambda x: (x == "기타", x)
    )
    st.markdown("""
    <div class="section-title-box">
        <div class="section-title-text">
            계열별 항생제 사용량
        </div>
    </div>
    """, unsafe_allow_html=True)


            # =========================
    # Cephamycin vs 3세대 Cephalosporins
    # =========================
    

    selected_dept = st.selectbox(
        "계열 선택",
        ["전체"] + dept_list1
    )

    if selected_dept != "전체":
        filtered_df = df[df["분류"] == selected_dept]
    else:
        filtered_df = df.copy()

    # =========================
    # 4번 그래프
    # 계열별 TOP10 성분 사용량
    # =========================

    # 월별 / 성분별 고유키 개수
    monthly_top8 = (
        filtered_df
        .groupby(
            ["분기", "처방 월", "성분통합키"]
        )["고유키"]
        .nunique()
        .reset_index(name="DOT")
    )

    monthly_top8["DOT"] = (
        monthly_top8["DOT"]
        /
        monthly_top8["처방 월"].map(day_dict)
        * 1000
    )

    # 분기별 평균
    summary4 = (
        monthly_top8
        .groupby(["분기", "성분통합키"])["DOT"]
        .mean()
        .reset_index()
    )

    # 컬럼명 변경
    summary4.columns = [
        "분기",
        "성분통합키",
        "항생제 사용량"
    ]

    # 전체 기간 기준 TOP8 계산
    top8_drug = (
        summary4
        .groupby("성분통합키")["항생제 사용량"]
        .sum()
        .reset_index()
    )

    top8_drug = (
        top8_drug
        .sort_values(
            "항생제 사용량",
            ascending=False
        )
        .head(8)
    )

    # TOP10 리스트
    top8_drug_list = top8_drug["성분통합키"].tolist()

    # TOP10만 필터
    summary4 = summary4[
        summary4["성분통합키"].isin(top8_drug_list)
    ]

    # 모든 분기 × 성분 조합 생성
    all_combinations = pd.MultiIndex.from_product(
        [
            quarter_order,
            top8_drug_list
        ],
        names=["분기", "성분통합키"]
    ).to_frame(index=False)

    summary4 = (
        all_combinations
        .merge(
            summary4,
            on=["분기", "성분통합키"],
            how="left"
        )
        .fillna(0)
    )

    # 범례 순서
    legend_order = top8_drug["성분통합키"].tolist()

    # 가장 최근 분기
    latest_quarter = quarter_order[-1]

    latest_df = (
        summary4[summary4["분기"] == latest_quarter]
        .sort_values("항생제 사용량", ascending=False)
        .head(8)
    )
    table_text = (
        f"<b>{latest_quarter} TOP8</b><br>"
        "<br>"
    )

    for _, row in latest_df.iterrows():
        table_text += (
            f"{row['성분통합키'][:18]} "
            f"{row['항생제 사용량']:.1f}<br>"
        )

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

    max_y = summary4["항생제 사용량"].max()

    fig4.update_layout(

        height=450,

        xaxis_title=None,
        yaxis_title="항생제 사용량 (DOT/1,000 patient-days)",

        yaxis=dict(
            range=[0, 180]
        ),

        paper_bgcolor='rgba(255,255,255,0)',
        plot_bgcolor='rgba(255,255,255,0)',

        margin=dict(
            l=20,
            r=80,
            t=20,
            b=20
        ),

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

    fig4.update_traces(
        hovertemplate=
        "<b>%{fullData.name}</b><br>" +
        "분기: %{x}<br>" +
        "항생제 사용량: %{y:.1f}<extra></extra>"   
    )
    st.markdown("""
    <div class="chart-title-box">
        <div class="chart-title">
            📈 분기별 항생제 사용량 평균 (계열별)
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.plotly_chart(
        fig4,
        use_container_width=True,
        config={"displayModeBar": False},
        key="graph4"
    )

    colors = px.colors.qualitative.Dark24

    color_map = {
        drug: colors[i % len(colors)]
        for i, drug in enumerate(legend_order)
    }

    # 표 형태로 변환
# 표 형태로 변환
    table_df = (
        summary4
        .pivot(
            index="성분통합키",
            columns="분기",
            values="항생제 사용량"
        )
        .reindex(legend_order)
        .reindex(columns=quarter_order)
        .fillna(0)
        .round(1)
    )

    table_df.columns.name = None

    # =========================
    # 계열 전체 행 생성
    # =========================

    latest_q = quarter_order[-1]
    prev_q = quarter_order[-2]

# fig_compare와 동일한 방식으로 계열 전체 사용량 계산
    monthly_total = (
        filtered_df
        .groupby(["분기", "처방 월"])["고유키"]
        .nunique()
        .reset_index(name="DOT")
    )

    monthly_total["DOT"] = (
        monthly_total["DOT"]
        /
        monthly_total["처방 월"].map(day_dict)
        * 1000
    )

    total_row = (
        monthly_total
        .groupby("분기")["DOT"]
        .mean()
        .reindex(quarter_order)
        .fillna(0)
        .round(1)
    )

    def add_arrow(current, previous):
        current = float(current)
        previous = float(previous)

        if current > previous:
            return (
                f'{current:.1f} '
                '<span style="color:#e53935;font-size:16px;font-weight:bold;">▲</span>'
            )
        elif current < previous:
            return (
                f'{current:.1f} '
                '<span style="color:#1e88e5;font-size:16px;font-weight:bold;">▼</span>'
            )
        else:
            return f'{current:.1f}'


    # 첫 번째 행(계열명)
    if selected_dept == "전체":
        total_name = "<b>전체</b>"
    else:
        total_name = f"<b>{selected_dept}</b>"

    total_html = total_row.to_dict()

    table_df = pd.concat(
        [pd.DataFrame([total_html], index=["TOTAL"]), table_df]
    )

    table_df[latest_q] = table_df.apply(
        lambda row: add_arrow(
            float(row[latest_q]),
            float(row[prev_q])
        ),
        axis=1
    )

    for q in quarter_order[:-1]:
        table_df[q] = table_df[q].map(lambda x: f"{x:.1f}") 


    # 첫 번째 열(성분명) 추가
    name_col = [total_name] + [
        f'<span style="display:inline-block;width:10px;height:10px;'
        f'border-radius:50%;background:{color_map[d]};'
        f'margin-right:8px;vertical-align:middle;"></span>{d}'
        for d in legend_order
    ]

    table_df.insert(0, "", name_col)

    table_df = table_df.reset_index(drop=True)

    # HTML 출력
    st.markdown(
        table_df.to_html(
            escape=False,
            index=False,
            classes="drug-table"
        ),
        unsafe_allow_html=True
    )


    target_df = df[
        df["분류"].isin([
            "3세대 Cephalosporins",
            "Cephamycins"
        ])
    ]
    monthly_compare = (
        target_df
        .groupby(["분기", "처방 월", "분류"])["고유키"]
        .nunique()
        .reset_index(name="DOT")
    )

    monthly_compare["DOT"] = (
        monthly_compare["DOT"]
        /
        monthly_compare["처방 월"].map(day_dict)
        * 1000
    )

    summary_compare = (
        monthly_compare
        .groupby(["분기", "분류"])["DOT"]
        .mean()
         .reset_index()
    )

    summary_compare.columns = [
        "분기",
        "분류",
        "사용량"
    ]

    # 모든 분기 × 분류 조합 생성
    all_combinations = pd.MultiIndex.from_product(
        [
            quarter_order,
            ["3세대 Cephalosporins", "Cephamycins"]
        ],
        names=["분기", "분류"]
    ).to_frame(index=False)

    # 없는 분기는 0으로 채우기
    summary_compare = (
        all_combinations
        .merge(
            summary_compare,
            on=["분기", "분류"],
            how="left"
        )
        .fillna(0)
    )


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
            "3세대 Cephalosporins": "#6FC7C0",   # 중간 초록
            "Cephamycins": "#F2A0A0"              # 파스텔 블루
        },

        text="사용량"
    )
    fig_compare.update_layout(

        height=440,

        xaxis_title=None,
        yaxis_title="항생제 사용량 (DOT/1,000 patient-days)",

        yaxis=dict(
            range=[0, summary_compare["사용량"].max() * 1.25]
        ),


        paper_bgcolor='white',
        plot_bgcolor='white',

        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        ),

        legend_title_text=""
    )
    fig_compare.add_annotation(
        x=1.19,
        y=0.60,
        xref="paper",
        yref="paper",
         text=(
            "<b>3세대 Cephalosporins</b><br>"
            "Cefpodoxime, Cefixime,<br>"
            "Cefditoren, Cefcapene,<br>"
            "Ceftriaxone, Cefotaxime,<br>"
            "Ceftizoxime, Ceftazidime"
        ),
        showarrow=False,

        # 박스 스타일
        bgcolor="white",
        bordercolor="#6fc7c0",
        borderwidth=1,
        borderpad=8,

        align="left",

        font=dict(
            size=11,
            color="#102a43"
        )
    )

    fig_compare.add_annotation(
        x=1.19,
        y=0.40,
        xref="paper",
        yref="paper",
         text=(
            "<b>Cephamycins          </b><br>"
            "Cefotetan, Flomoxef          "
        ),
        showarrow=False,

        # 박스 스타일
        bgcolor="white",
        bordercolor="#f2a0a0",
        borderwidth=1,
        borderpad=8,

        align="left",

        font=dict(
            size=11,
            color="#102a43"
        )
    )

    fig_compare.update_traces(
        texttemplate='%{text:,.1f}',
        textposition='auto',
        hovertemplate=
        "<b>%{fullData.name}</b><br>" +
        "분기: %{x}<br>" +
        "항생제 사용량: %{y:.1f}<extra></extra>"   
    )
    
    st.markdown("""
    <div class="chart-title-box">
         <div style="
            display:flex;
            align-items:center;
            gap:10px;
        ">
        <div class="chart-title">
            🏥 분기별 3세대 Cephalosporins 및 Cephamycins 사용량 평균
        </div>


    </div>
    """, unsafe_allow_html=True)

    st.plotly_chart(
        fig_compare,
        use_container_width=True,
        config={"displayModeBar": False},
        key="graph3"
    )

    st.markdown("""
    <div style="
        background:#f1f7fe;
        border:1px solid #dbeafe;
        border-left:6px solid #60a5fa;
        border-radius:14px;
        padding:6px 22px;
        margin-top:8px;
        margin-bottom:15px;
        box-shadow:0 2px 6px rgba(0,0,0,0.05);
    ">
    <div style="
        display:flex;
        gap:30px;
        align-items:flex-start;
    ">

    <!-- 좌측 설명 -->
    <div style="
        flex:2;
        padding-right:0px;
        border-right:1px solid #d6e4f0;
    ">

    <div style="
        font-size:22px;
        font-weight:800;
        color:#17406D;
        margin-top:6px;
        margin-bottom:10px;
    ">
    💡 Cephamycin이란?
    </div>

    <div style="
        font-size:14px;
        line-height:1.8;
        color:#374151;
    ">

    <b>Cephamycin</b>은 2세대 Cephalosporin으로 분류되나 Cefaclor와는 특성이 다릅니다.
    <br>
    주요 특징은 <b>광범위 베타락탐분해효소(extended-spectrum <i>β</i>-lactamase, ESBL)</b>에 저항성을 가지고 있으며,
    <i>Bacteroides fragilis</i>와 같은 혐기균에 효과가 있습니다.
    <br><br>
    <b>그러나 최근들어 <i>B. fragilis</i>에 대한 내성이 지속적으로 증가하고 있어 적정사용에 대한 관리가 필요합니다.</b>
    </div>
    </div>

    <!-- 우측 표 -->
    <div style="
        flex:1;
        padding-left:0px;
        min-width:320px;
        display:flex;
        flex-direction:column;
        justify-content:center;
        align-items:center;
        min-height:180px;
    ">
    <div style="
        width:100%;
        max-width:400px;
        background:#d9e9ff;
        color:#17406D;
        text-align:center;
        font-weight:800;
        padding:8px;
        margin-top:8px;
        margin-bottom:10px;
        border-radius:8px;
    ">
    본원 Cephamycin계 항생제
    </div>

    <table style="
        width:100%;
        max-width:400px;
        border-collapse:collapse;
        border-radius:8px;
        overflow:hidden;
        font-size:14px;
        text-align:center;
    ">

    <tr style="
        background:#214d99;
        color:white;
    ">
        <th style="padding:8px;">약품코드</th>
        <th style="padding:8px;">약품명</th>
        <th style="padding:8px;">성분명</th>
    </tr>

    <tr>
        <td style="padding:8px;border-bottom:1px solid #e5e7eb;">W-CTT1GDJ</td>
        <td style="padding:8px;border-bottom:1px solid #e5e7eb;">종근당 세포테탄 주 1G</td>
        <td style="padding:8px;border-bottom:1px solid #e5e7eb;"><i>CEFOTETAN</i></td>
    </tr>

    <tr>
        <td style="padding:8px;">W-FX500J</td>
        <td style="padding:8px;">후루마린주 0.5G</td>
        <td style="padding:8px;"><i>FLOMOXEF</i></td>
    </tr>

    </table>

    </div>

    </div>

    </div>
    """, unsafe_allow_html=True)


    dept_list2 = sorted([
        x for x in df["성분통합키"].dropna().unique()
        if str(x) != "0x2a" and str(x) != "Cefoperazone/sulbactam"
    ])
    
    st.markdown("""
    <div class="section-title-box">
        <div class="section-title-text">
            올해의 월별 항생제 사용량
        </div>
    </div>
    """, unsafe_allow_html=True)

    latest_month = df["처방 월"].max()

    latest_df = df[df["처방 월"] == latest_month]

    if selected_dept != "전체":
        latest_df = latest_df[
            latest_df["분류"] == selected_dept
        ]
    
    drug_usage = (
        latest_df
        .groupby("성분통합키")["고유키"]
        .nunique()
        .reset_index(name="DOT")
    )

    drug_usage["DOT"] = (
        drug_usage["DOT"]
        / day_dict[latest_month]
        * 1000
    )
    drug_usage = drug_usage[
        drug_usage["성분통합키"] != "0x2a"
    ]


    drug_usage = drug_usage.sort_values(
        "DOT",
        ascending=False
    )

    dept_list2 = drug_usage["성분통합키"].tolist()

    display_map = {
        row["성분통합키"]:
        f"{row['성분통합키']} ▶ [{row['DOT']:.1f}]"
        for _, row in drug_usage.iterrows()
    }

    if selected_dept == "전체":

        drug_options = drug_usage["성분통합키"].tolist()

    else:

        drug_options = [selected_dept] + drug_usage["성분통합키"].tolist()

    selected_drug = st.selectbox(
        "항생제 성분 선택",
        drug_options,
        index=0,
        format_func=lambda x:
            display_map.get(x, x)
    )

    # 선택 성분 필터
    if selected_dept != "전체" and selected_drug == selected_dept:

        # 계열 전체 선택
        filtered_df = df[
            df["분류"] == selected_dept
        ]

    else:

        # 성분 선택
        filtered_df = df[
            df["성분통합키"] == selected_drug
        ]

    # 선택 성분 KPI
    selected_latest = (
        filtered_df[
            filtered_df["처방 월"] == latest_month
        ]["고유키"]
        .nunique()
        / day_dict[latest_month]
        * 1000
    )

    selected_latest = round(selected_latest, 1)

    selected_prev = (
        filtered_df[
            filtered_df["처방 월"] == prev_month
        ]["고유키"]
        .nunique()
        / day_dict[prev_month]
        * 1000
    )

    selected_prev = round(selected_prev, 1)

    if selected_prev > 0:

        selected_change = (
            (selected_latest - selected_prev)
            / selected_prev
        ) * 100

    else:

        selected_change = 0

    if selected_change >= 0:
        selected_arrow = "▲"
        selected_color = "#f08080"
    else:
        selected_arrow = "▼"
        selected_color = "#10B981"


    selected_change_text = f"{selected_arrow} {abs(selected_change):.1f}%"

    # KPI 카드
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="
            background:white;
            border-radius:28px;
            padding:28px 36px;
            box-shadow:0 2px 10px rgba(0,0,0,0.08);
            margin-bottom:20px;
        ">

        <!-- 타이틀 -->
        <div style="
            font-size:20px;
            font-weight:800;
            color:#102a43;
            margin-bottom:22px;
        ">
            이달의 {selected_drug} 사용량
            <span style="
                font-size:13px;
                font-weight:500;
                color:#6b7280;
                margin-left:6px;
            ">
                ({latest_month_text} 기준)
            </span>
        </div>

        <!-- 본문 -->
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
        ">

        <!-- 왼쪽 숫자 + 단위 -->
        <div>

        <div style="
            font-size:58px;
            font-weight:800;
            color:#17406D;
            line-height:1.0;
            margin-bottom:8px;
        ">
            {selected_latest:,.1f}
        </div>

        <div style="
            font-size:18px;
            font-weight:400;
            color:#6b7280;
        ">
            DOT/1,000 patient-days
        </div>

        </div>

        <!-- 오른쪽 변화율 -->
        <div style="
            text-align:center;
            padding-left:30px;
            border-left:1px solid #d1d5db;
        ">

        <div style="
            font-size:18px;
            font-weight:700;
            color:#374151;
            margin-bottom:8px;
        ">
            지난 달 대비
        </div>

        <div style="
            font-size:36px;
            font-weight:800;
            color:{selected_color};
        ">
            {selected_change_text}
        </div>

        </div>

        </div>

        </div>
        """, unsafe_allow_html=True)

                            # 선택 성분의 항목코드 목록
        if selected_dept != "전체" and selected_drug == selected_dept:

            selected_components = drug_usage["성분통합키"].tolist()

            drug_info = (
                master_df[
                    master_df["성분통합키"].isin(selected_components)
                ][["항목코드","약품명"]]
                .drop_duplicates()
            )

        else:

            drug_info = (
                master_df[
                    master_df["성분통합키"] == selected_drug
                ][["항목코드","약품명"]]
                .drop_duplicates()
            )

            drug_info = drug_info[
                drug_info["약품명"].notna()
            ]

            drug_info = drug_info[
                drug_info["약품명"].astype(str).str.strip() != ""
            ]

            drug_info = drug_info.sort_values(
                "항목코드"
            )

        drug_info.columns = [
            "약품 코드",
            "약품명"
        ]

        drug_info = drug_info[
            drug_info["약품명"].notna()
        ]

        drug_info = drug_info[
            drug_info["약품명"].astype(str).str.strip() != ""
        ]

        drug_info = drug_info.sort_values(
            "약품 코드"
        )

        with st.container():

            st.markdown("""
            <div style="
                background:white;
                border-radius:10px 10px 0 0;
                padding:20px 24px;
                box-shadow:0 2px 10px rgba(0,0,0,0.08);
                font-size:20px;
                font-weight:800;
                color:#102a43;
                text-align:center;
            ">
                🏥 본원 원내 해당 성분
            </div>
            """, unsafe_allow_html=True)

            st.dataframe(
                drug_info,
                use_container_width=True,
                hide_index=True
            )   


 

    with col2:

        if selected_dept == "전체":

            # 전체 선택 → 선택한 성분 그래프
            class_df = df[
                (df["성분통합키"] == selected_drug)
                &
                (df["처방 월"].isin([
                    "26/01",
                    "26/02",
                    "26/03",
                    "26/04",
                    "26/05",
                    "26/06"
                ]))
            ].copy()


        elif selected_drug == selected_dept:

            # 특정 계열 선택 + 계열명 선택 → 계열 전체 그래프
            class_df = df[
                (df["분류"] == selected_dept)
                &
                (df["처방 월"].isin([
                    "26/01",
                    "26/02",
                    "26/03",
                    "26/04",
                    "26/05",
                    "26/06"
                ]))
            ].copy()


        else:

            # 특정 계열 선택 + 개별 성분 선택 → 성분 그래프
            class_df = df[
                (df["성분통합키"] == selected_drug)
                &
                (df["처방 월"].isin([
                    "26/01",
                    "26/02",
                    "26/03",
                    "26/04",
                    "26/05",
                    "26/06"
                ]))
            ].copy()

        class_trend = (
            class_df
            .groupby("처방 월")["고유키"]
            .nunique()
            .reset_index(name="DOT")
        )

        class_trend["DOT"] = (
            class_trend["DOT"]
            /
            class_trend["처방 월"].map(day_dict)
            * 1000
        )

        month_order_2026 = [
            "26/01",
            "26/02",
            "26/03",
            "26/04",
            "26/05",
            "26/06"
        ]

        class_trend["처방 월"] = pd.Categorical(
            class_trend["처방 월"],
            categories=month_order_2026,
            ordered=True
        )

        class_trend = class_trend.sort_values(
            "처방 월"
        )

        class_trend["월표시"] = (
            class_trend["처방 월"]
            .astype(str)
            .map({
                "26/01": "26년 1월",
                "26/02": "26년 2월",
                "26/03": "26년 3월",
                "26/04": "26년 4월",
                "26/05": "26년 5월",
                "26/06": "26년 6월"
            })
        )

        fig_class = px.bar(
            class_trend,
            x="월표시",
            y="DOT",
            text="DOT"
        )

        fig_class.update_traces(
            texttemplate="%{y:.1f}",
            textposition="outside",
            marker_color="#82D4BB",
            width=0.45,
            hovertemplate=
            "<b>" + str(selected_drug) + "</b><br>" +
            "처방월: %{x}<br>" +
            "항생제 사용량: %{y:.1f}<br>" +
            "<extra></extra>"
        )

            # x축을 숫자로 변환
        x_num = np.arange(len(class_trend))

        # 선형회귀
        coef = np.polyfit(
            x_num,
            class_trend["DOT"],
            1
        )

        trend = np.poly1d(coef)

        slope = coef[0]

        if slope > 0:
            trend_text = f"<b>+{slope:.2f}</b> DOT/1,000 patient-days"
        elif slope < 0:
            trend_text = f"<b> {slope:.2f}</b> DOT/1,000 patient-days"
        else:
            trend_text = f"<b>0.00</b> DOT/1,000 patient-days"

        # 추세선 추가
        fig_class.add_trace(
            go.Scatter(
                x=class_trend["월표시"],
                y=trend(x_num),
                mode="lines",
                name="Trend",
                showlegend=False,
                line=dict(
                    color="#17406D",
                    width=2,
                    dash="dot"
                ),
                hovertemplate=
                "기울기<br>" +
                f"{trend_text}<extra></extra>"
            )
        )

        y_max = class_trend["DOT"].max() * 1.25

        fig_class.update_layout(
            height=400,

            margin=dict(
                l=60,
                r=20,
                t=20,
                b=10
            ),

            xaxis_title=None,
            yaxis_title="항생제 사용량 (DOT/1,000 patient-days)",
            yaxis=dict(
                range=[0, y_max]
            ),
            paper_bgcolor="rgba(255,255,255,0)",
            plot_bgcolor="rgba(255,255,255,0)"
        )

        st.markdown(f"""
        <div style="margin-top:15px;">
        <div class="column-title-box">
            <div class="column-title">
                📊올해의 월별 {str(selected_drug)} 사용량 추이
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.plotly_chart(
            fig_class,
            use_container_width=True,
            config={"displayModeBar": False}
        )



    # =========================
    # 하단 우측 최신화 버튼
    # =========================

    left_space, button_col = st.columns([9, 1])

    with button_col:

        if st.button("🔄Refresh"):

            load_data.clear()
            st.session_state.abx_loaded = False

            st.toast("페이지를 새로고침했습니다.")

elif st.session_state.menu == "ASP 중재":

    @st.cache_data(ttl=86400)
    def load_inter_data():

        return pd.read_excel(
            "DOT 대시보드.xlsb",
            sheet_name="중재",
            engine="pyxlsb"
        ) 
    
    df_inter_data = load_inter_data()

    st.markdown("""
    <div class="section-title-box">
        <div class="section-title-text">
            ASP 중재 활동
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------
    # 최근 월 / 직전 월
    # -------------------------

    month_order = sorted(
        df_inter_data["월"].dropna().unique()
    )

    latest_month = month_order[-1]
    prev_month = month_order[-2]

    # KPI 제목용 월 표시
    year, month = latest_month.split("/")
    latest_month_text = f"20{year}년 {int(month)}월"

    # -------------------------
    # 중재 건수
    # -------------------------

    latest_intervention = (
        df_inter_data[
            df_inter_data["월"] == latest_month
        ]["중재건수"].iloc[0]
    )

    prev_intervention = (
        df_inter_data[
            df_inter_data["월"] == prev_month
        ]["중재건수"].iloc[0]
    )

    intervention_change = (
        (latest_intervention - prev_intervention)
        / prev_intervention
    ) * 100

    # 상승 / 하락 표시
    if intervention_change >= 0:

        intervention_arrow = "▲"
        intervention_color = "#f08080"

    else:

        intervention_arrow = "▼"
        intervention_color = "#10B981"

    # -------------------------
    # 수용률
    # -------------------------

    latest_accept = (
        df_inter_data[
            df_inter_data["월"] == latest_month
        ]["수용률"].iloc[0]
    ) * 100

    prev_accept = (
        df_inter_data[
            df_inter_data["월"] == prev_month
        ]["수용률"].iloc[0]
    ) * 100

    accept_change = (
        (latest_accept - prev_accept)
        / prev_accept
    ) * 100

    # 상승 / 하락 표시
    if accept_change >= 0:

        accept_arrow = "▲"
        accept_color = "#f08080"

    else:

        accept_arrow = "▼"
        accept_color = "#10B981"

    # =========================
    # KPI 카드
    # =========================

    col1, col2 = st.columns(2)

    # -------------------------
    # 좌측 KPI
    # -------------------------

    with col1:

        st.markdown(f"""
        <div style="
            background:white;
            border-radius:28px;
            padding:28px 36px;
            box-shadow:0 2px 10px rgba(0,0,0,0.08);
            margin-bottom:20px;
        ">

        <!-- 제목 영역 -->
        <div style="
            margin-bottom:0px;
        ">

        <!-- 타이틀 + 안내 아이콘 -->
        <div style="
            display:flex;
            align-items:center;
            gap:10px;
        ">

        <!-- 제목 -->
        <div style="
            font-size:20px;
            font-weight:800;
            color:#102a43;
        ">
            이달의 ASP 중재건수
            <span style="
                font-size:13px;
                font-weight:500;
                color:#6b7280;
                margin-left:6px;
            ">
                ({latest_month_text} 기준)
            </span>
        </div>

        <!-- i 아이콘 -->
        <div class="tooltip-container" style="
            position:relative;
            display:inline-block;
            cursor:pointer;
        ">

        <!-- 동그란 i -->
        <div style="
            width:24px;
            height:24px;
            border-radius:50%;
            background:#e8eef7;
            color:#17406D;
            font-size:16px;
            font-weight:700;
            display:flex;
            align-items:center;
            justify-content:center;
        ">
            i
        </div>

        <!-- 툴팁 -->
        <div class="tooltip-box" style="
            visibility:hidden;
            opacity:0;
            transition:0.2s;
            position:absolute;
            top:35px;
            left:0;
            width:540px;
            background:#0F2E4F;
            color:white;
            padding:18px 20px;
            border-radius:16px;
            box-shadow:0 8px 24px rgba(0,0,0,0.18);
            z-index:999;
            font-size:15px;
            line-height:1.7;
        ">

        <div style="
            font-size:17px;
            font-weight:700;
            margin-bottom:10px;
        ">
            ASP(Antimicrobial Stewardship Program)란?
        </div>

        항생제 적정사용 관리 프로그램(Antimicrobial Stewardship
        Program, ASP)은<br> 전문관리팀이 기관 내 항생제 처방과정을 중재, 관리
        함으로써 부적절한<br> 항생제 사용을 줄이고 적절한 사용을 유도하기 위한 체계입니다.<br>
        -----------------------------------------------------------------------------------------------------------<br>
        본원은 2024년 11월부터 항생제 적정사용관리 시범사업에 참여하여<br>
        항생제 적정사용관리 활동 및 항생제 중재를 수행하고 있습니다.
        <table style="
            width:100%;
            border-collapse:collapse;
            margin-top:8px;
            font-size:14px;
        ">

        <tr>
        <td style="
            background:rgba(255,255,255,0.12);
            padding:10px 12px;
            font-weight:700;
            border-radius:8px 0 0 8px;
            width:90px;
        ">
            24년 11월
        </td>

        <td style="
            padding:10px 12px;
        ">
            ASP 시범사업 참여 및 ASP 전담팀 구성
        </td>
        </tr>

        <tr>
        <td style="
            background:rgba(255,255,255,0.12);
            padding:10px 12px;
            font-weight:700;
            border-radius:8px 0 0 8px;
            width:90px;
        ">
            24년 12월
        </td>

        <td style="
            padding:10px 12px;
        ">
            항생제 처방 지침 교육 및 항생제 적정사용 전직원 교육
        </td>
        </tr>
        
        <tr>
        <td style="
            background:rgba(255,255,255,0.12);
            padding:10px 12px;
            font-weight:700;
            border-radius:8px 0 0 8px;
            width:90px;
        ">
            25년 2월
        </td>

        <td style="
            padding:10px 12px;
        ">
            ASP 중재 활동을 위한 전산 구축 완료
        </td>
        </tr>

       <tr>
        <td style="
            background:rgba(255,255,255,0.12);
            padding:10px 12px;
            font-weight:700;
            border-radius:8px 0 0 8px;
            width:90px;
        ">
            25년 4월
        </td>

        <td style="
            padding:10px 12px;
        ">
            원내 항생제 사용 지침 제정
        </td>
        </tr>

       <tr>
        <td style="
            background:rgba(255,255,255,0.12);
            padding:10px 12px;
            font-weight:700;
            border-radius:8px 0 0 8px;
            width:90px;
        ">
            25년 7월
        </td>

        <td style="
            padding:10px 12px;
        ">
            항생제 처방 지침 교육 및 항생제 적정사용 전직원 교육
        </td>
        </tr>

       <tr>
        <td style="
            background:rgba(255,255,255,0.12);
            padding:10px 12px;
            font-weight:700;
            border-radius:8px 0 0 8px;
            width:90px;
        ">
            25년 11월
        </td>

        <td style="
            padding:10px 12px;
        ">
            항생제 처방 지침 전공의 교육 및 항생제 사용 지침 전산화
        </td>
        </tr>

       <tr>
        <td style="
            background:rgba(255,255,255,0.12);
            padding:10px 12px;
            font-weight:700;
            border-radius:8px 0 0 8px;
            width:90px;
        ">
            26년 1월
        </td>

        <td style="
            padding:10px 12px;
        ">
            1차년도 시범사업 결과 보고 및 2차년도 시범사업 참여
        </td>
        </tr>

        <tr>
        <td style="
            background:rgba(255,255,255,0.12);
            padding:10px 12px;
            font-weight:700;
            border-radius:8px 0 0 8px;
            width:90px;
        ">
            26년 5월
        </td>

        <td style="
            padding:10px 12px;
        ">
            1차년도 시범사업 평가 완료
        </td>
        </tr>

        </table>

        </div>

        </div>

        </div>

        </div>

        <!-- 제목과 숫자 간격 유지 -->
        <div style="height:22px;"></div>

        <style>
        .tooltip-container:hover .tooltip-box {{
            visibility:visible !important;
            opacity:1 !important;
        }}


        </style>

        <!-- 본문 -->
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
        ">

        <!-- 왼쪽 숫자 -->
        <div style="
            font-size:58px;
            font-weight:800;
            color:#17406D;
            line-height:1.0;
            margin-bottom:8px;
        ">
            {latest_intervention:,}
        </div>

        <div style="
            font-size:18px;
            font-weight:400;
            color:#6b7280;
        ">
        건
        </div>

        <!-- 오른쪽 변화율 -->
        <div style="
            text-align:center;
            padding-left:30px;
            border-left:1px solid #d1d5db;
        ">

        <div style="
            font-size:18px;
            font-weight:700;
            color:#374151;
            margin-bottom:8px;
        ">
            지난 달 대비
        </div>

        <div style="
            font-size:36px;
            font-weight:800;
            color:{intervention_color};
        ">
            {intervention_arrow} {abs(intervention_change):.1f}%
        </div>

        </div>

        </div>

        </div>
        """, unsafe_allow_html=True)

    # -------------------------
    # 우측 KPI
    # -------------------------

    with col2:

        st.markdown(f"""
        <div style="
            background:white;
            border-radius:28px;
            padding:28px 36px;
            box-shadow:0 2px 10px rgba(0,0,0,0.08);
            margin-bottom:20px;
        ">

        <!-- 타이틀 -->
        <div style="
            font-size:20px;
            font-weight:800;
            color:#102a43;
            margin-bottom:22px;
        ">
            이달의 ASP 중재 수용률
            <span style="
                font-size:13px;
                font-weight:500;
                color:#6b7280;
                margin-left:6px;
            ">
                ({latest_month_text} 기준)
            </span>
        </div>

        <!-- 본문 -->
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
        ">

        <!-- 왼쪽 숫자 -->
        <div style="
            font-size:58px;
            font-weight:800;
            color:#17406D;
            line-height:1.0;
            margin-bottom:8px;
        ">
            {latest_accept:.1f}%
        </div>

        <!-- 오른쪽 변화율 -->
        <div style="
            text-align:center;
            padding-left:30px;
            border-left:1px solid #d1d5db;
        ">

        <div style="
            font-size:18px;
            font-weight:700;
            color:#374151;
            margin-bottom:8px;
        ">
            지난 달 대비
        </div>

        <div style="
            font-size:36px;
            font-weight:800;
            color:{accept_color};
        ">
            {accept_arrow} {abs(accept_change):.1f}%
        </div>

        </div>

        </div>

        </div>
        """, unsafe_allow_html=True)

    # =========================
    # 월별 ASP 중재 건수
    # =========================

    graph_df = df_inter_data.copy()

    # 수용률 % 변환
    graph_df["수용률_percent"] = (
        graph_df["수용률"] * 100
    )

    # 콤보 그래프
    fig_intervention = px.bar(
        graph_df,
        x="월",
        y="중재건수",
        text="중재건수",
    )

    # 막대 스타일
    fig_intervention.update_traces(

        marker_color="#5a9cf5",

        texttemplate='%{text:,.0f}',

        textposition='inside',

        insidetextanchor='end',

        name="중재건수"
    )

    # 수용률 선 추가
    fig_intervention.add_scatter(

        x=graph_df["월"],

        y=graph_df["수용률_percent"],

        mode="lines+markers+text",

        name="수용률",

        yaxis="y2",

        text=[
            f"{v:.1f}%"
            for v in graph_df["수용률_percent"]
        ],

        textposition="top center",

        line=dict(
            color="#ef4444",
            width=3
        ),

        marker=dict(
            size=9,
            color="#ef4444"
        )
    )

    # 레이아웃
    fig_intervention.update_layout(

        height=480,

        xaxis_title=None,

        # 좌측 Y축
        yaxis=dict(

            title="중재건수",

            range=[0, 850],

            showgrid=False
        ),

        # 우측 Y축
        yaxis2=dict(

            title="수용률 (%)",

            overlaying="y",

            side="right",

            range=[90, 101],

            tickformat=".0f"
        ),

        paper_bgcolor='rgba(255,255,255,0)',
        plot_bgcolor='rgba(255,255,255,0)',

        margin=dict(
            l=20,
            r=20,
            t=40,
            b=20
        ),

        legend=dict(

            orientation="h",

            yanchor="bottom",
            y=1.02,

            xanchor="right",
            x=1
        ),

        legend_title_text=""
    )

    # 제목 박스
    st.markdown("""
    <div class="chart-title-box">
        <div class="chart-title">
            📈 월별 ASP 중재 건수
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 그래프 출력
    st.plotly_chart(
        fig_intervention,
        use_container_width=True,
        config={"displayModeBar": False},
        key="asp_intervention_graph"
    )

    # =========================
    # 월 선택 슬라이서
    # =========================

    # 월 변환 함수


    def convert_month_label(month_text):
        year = "20" + month_text[:2]
        month = month_text[-2:]
        return f"{year}년 {int(month)}월"


    # 월 리스트
    month_list = df_inter_data["월"].dropna().unique().tolist()

    # 최신순 정렬
    month_list = sorted(month_list, reverse=True)

    # 표시용 dictionary
    month_display_map = {m: convert_month_label(m) for m in month_list}

    # 선택창
    selected_month = st.selectbox(
        "월별 현황",
        month_list,
        index=0,
        format_func=lambda x: month_display_map[x],
    )
    st.markdown(
        """
        <div class="chart-title-box">
        <div class="chart-title">
            📊 중재활동 항목별 중재 현황
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # =========================
    # 선택 월 데이터
    # =========================

    selected_row = df_inter_data[df_inter_data["월"] == selected_month].iloc[0]

    # 그래프 데이터
    category_df = pd.DataFrame({
        "항목": [
            "1.항생제 병합(중복) 처방 중재",
            "2.항생제 장기투여 중재",
            "3.주사 항생제의 경구 전환",
            "4.항생제 하강 치료",
            "5.미생물 검사 기반의 항생제 처방 중재",
            "6.가이드라인에 맞는 항생제 처방",
            "7.특정 항생제에 대한 치료 약물 모니터링",
        ],
        "건수": [
            selected_row["중복"],
            selected_row["장기"],
            selected_row["경구"],
            selected_row["하강"],
            selected_row["미생물"],
            selected_row["지침"],
            selected_row["농도"],
        ],
    })

    # =========================
    # Bar of Pie (도넛 + 서브 막대) 그래프
    # =========================

    # 1~4번 기타 항목과 5~7번 메인 항목 데이터 분리
    sub_items = [
        "1.항생제 병합(중복) 처방 중재",
        "2.항생제 장기투여 중재",
        "3.주사 항생제의 경구 전환",
        "4.항생제 하강 치료",
    ]

    sub_df = category_df[category_df["항목"].isin(sub_items)].copy()
    main_df = category_df[~category_df["항목"].isin(sub_items)].copy()

    sub_df["항목"] = sub_df["항목"].str.replace(".", " | ", regex=False)

    # 기타 항목(1~4번) 건수 합계
    other_sum = sub_df["건수"].sum()

    main_values = [other_sum] + main_df["건수"].tolist()

    # 메인 도넛 차트용 라벨/값 데이터
    pie_text_labels = ["1~4","5", "6", "7"]

    # 2. 하단 범례(Legend)에 표시할 범례 텍스트
    pie_legend_labels = [
        "1~4",
        "5 | 미생물 검사 기반의 항생제 처방 중재",
        "6 | 가이드라인에 맞는 항생제 처방",
        "7 | 특정 항생제에 대한 치료 약물 모니터링",
    ]

    # 지정하신 파스텔 컬러 유지
    main_colors = [
        "#AFCBFF",
        "#F8C89A",
        "#F4A7A7",
        "#BFDDB5",
    ]  # 5번(파랑), 6번(남색), 7번(보라), 기타(회색)
    sub_colors = [
        "#a7c7ff",
        "#BFC4F5",
        "#D8B4F8",
        "#CBD5E1",
    ]  # 1번(빨강), 2번(주황), 3번(노랑), 4번(초록)

    # 서브플롯 생성 (1행 2열)
    fig_category = make_subplots(
        rows=1,
        cols=2,
        specs=[[{"type": "domain"}, {"type": "xy"}]],
        column_widths=[0.6, 0.4],
        horizontal_spacing=0.18,
        subplot_titles=("<b>전체 항목 중재 건수</b>", "<b>1~4번 항목 중재 건수</b>"),
    )

    # [왼쪽] 메인 도넛 차트
    fig_category.add_trace(
        go.Pie(
            labels=pie_legend_labels,  # 하단 범례용 텍스트
            values=main_values,
            text=pie_text_labels,  # 파이 상에 보일 번호 (1~4, 5, 6, 7)
            texttemplate="%{text} | <b>%{value}</b> <br>%{percent}",  # "번호 (퍼센트)" 만 표시
            textposition="inside",
            insidetextorientation="horizontal",
            insidetextfont=dict(
                size=16,  # 글자 크기 (기본값 약 12 -> 16~18 정도로 키움)
                color="#595959",  # 글자 색상 (필요시 '#000000' 등으로 변경)
            ),
            marker=dict(
                colors=main_colors, line=dict(color="rgba(0,0,0,0.18)", width=1.5)
            ),
            hovertemplate="<b>%{label}</b><br>건수: %{value}건 (%{percent})<extra></extra>",
            showlegend=True,
            sort=False,
        ),
        row=1,
        col=1,
    )

    # [오른쪽] 소수 항목 가로 막대 차트
    fig_category.add_trace(
        go.Bar(
            x=sub_df["건수"],
            y=sub_df["항목"],
            orientation="h",
            text=sub_df["건수"],
            texttemplate="%{text:,.0f}",
            textposition="outside",
            marker=dict(
                color=sub_colors, line=dict(color="rgba(0,0,0,0.18)", width=1.5)
            ),
            width=0.35,
            opacity=0.95,
            hovertemplate="<b>%{y}</b><br>건수: %{x}건<extra></extra>",
            showlegend=False,
        ),
        row=1,
        col=2,
    )

    # 레이아웃 및 스타일
    max_sub_val = max(sub_df["건수"].max(), 1)
    fig_category.update_layout(
        height=600,# 하단 범례 공간을 확보하기 위해 높이 살짝 조정
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        margin=dict(l=20, r=40, t=100, b=80),  # 상단 여백 최소화, 하단 여백 확보
        # 하단 범례 설정
        showlegend=True,
        legend=dict(
            orientation="v",  # 세로 배치
            yanchor="top",
            y=-0.15,  # 그래프 아래쪽으로 배치
            xanchor="center",
            x=0.5,
            traceorder="normal",
            font=dict(size=14),
        ),
        xaxis=dict(
            title="중재 건수",
            range=[0, max_sub_val * 1.35],
            showline=True,
            linewidth=1,
            linecolor="#9ca3af",
            showgrid=True,
            gridcolor="#e5e7eb",
            gridwidth=1,
        ),
        yaxis=dict(
            autorange="reversed",  # 1번부터 위에서 아래로 순서 정렬
            showline=False,
            showgrid=False,
            tickfont=dict(
                size=14,  # 글자 크기 (필요시 조정)
                color="#111827",  # 또렷하고 진한 검은색 계열 (Slate 900)  # 굵은 폰트 스타일 적용 (또는 'sans-serif')
            ),
        ),
    )

    fig_category.for_each_annotation(
        lambda a: a.update(
            y=a.y + 0.1,
            font=dict(
                size=18,
                color="#595959",
            ),
        ),
    )    


    # 출력
    st.plotly_chart(
        fig_category,
        use_container_width=True,
        config={"displayModeBar": False},
        key="asp_category_graph",
    )

    
    def get_base64_image(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    char_img = get_base64_image("check.png")
    icon1_img = get_base64_image("중1.png") # 1 | 병합(중복)
    icon2_img = get_base64_image("중2.png")# 2 | 장기투여
    icon3_img = get_base64_image("중3.png")    # 3 | 경구전환
    icon4_img = get_base64_image("중4.png") # 4 | 하강치료
    icon5_img = get_base64_image("중5.png") # 5 | 미생물검사
    icon6_img = get_base64_image("중6.png")    # 6 | 가이드라인
    icon7_img = get_base64_image("중7.png")   # 7 | 모니터링

    st.markdown("""
    <style>
        .antibiotic-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            grid-template-rows: repeat(2, 1fr);
            gap: 20px;
            padding: 20px;
            background-color: #f1f7fe;
            border-radius: 28px;
            border: 1px solid #d8e2ee;
            box-shadow: 0 4px 14px rgba(0,0,0,0.05);
            margin-bottom: 36px;
        }

        /* 공통 카드 스타일 */
        .grid-item {
            background-color: white;
            border-radius: 20px;
            padding: 20px;
            border: 1px solid #e1e9f1;
            display: flex;
            flex-direction: column;
            align-items: center;  /* 수평 중앙 정렬 */
            text-align: center;    /* 텍스트 중앙 정렬 */
            transition: transform 0.2s, box-shadow 0.2s;
            cursor: pointer;       /* 마우스 포인터 변경 */
            height: 100%;          /* 카드 높이 고정 */
            box-sizing: border-radius;
        }
        
        .grid-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
            background-color: #fafafa; /* 호버 시 배경색 소폭 변경 */
        }

        /* 1. 상단 제목 스타일 */
        .card-title {
            font-size: 20px;
            font-weight: 800;
            margin-bottom: 8px;
            width: 100%;
        }

        /* 2. 가운데 이미지 스타일 */
        .card-img-container {
            height: 120px;         /* 이미지 영역 높이 고정 */
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 12px;
            width: 100%;
            transition: margin 0.3s; /* 호버 시 여백 애니메이션 */
        }
        
        .card-img {
            max-height: 120px;
            max-width: 100%;
            object-fit: contain;
            border-radius: 12px;
        }

        /* 캐릭터 구획 전용 이미지 크기 */
        .char-img {
            max-height: 80px;
        }

        /* 캐릭터 카드는 호버 효과 제외 (선택사항) */
        .char-card:hover {
            transform: none;
            box-shadow: 0 4px 14px rgba(0,0,0,0.05);
            background-color: white;
        }

        /* 3. 하단 설명 스타일 */
        .card-content {
            font-size: 16px;
            line-height: 1.5;
            color: #444;
            font-weight: 400;
            display: none;       /* 평소에는 숨김 */
            opacity: 0;           /* 투명도 0 */
            transition: opacity 0.3s; /* 나타날 때 애니메이션 */
            width: 100%;
        }
        
        /* 호버 시 설명 스타일 */
        .grid-item:hover .card-content {
            display: block;      /* 마우스를 올리면 나타남 */
            opacity: 1;           /* 투명도 1 (보임) */
        }
        
        /* 호버 시 이미지 여백 조정 (설명이 들어갈 공간 확보) */
        .grid-item:hover .card-img-container {
            margin-bottom: 12px;
        }

        /* 본문 강조 텍스트 */
        .card-content b {
            color: #333;
            display: block;
            margin-bottom: 6px;
        }

        .example-text {
            font-size: 14px;
            color: #888;
            margin-top: 6px;
        }

        @media (max-width: 1200px) { .antibiotic-grid { grid-template-columns: repeat(2, 1fr); } }
        @media (max-width: 600px) { .antibiotic-grid { grid-template-columns: 1fr; } }
    </style>
    """, unsafe_allow_html=True)


    # 그리드 HTML 구조 작성
    st.markdown(f"""
    <div class="antibiotic-grid">

    <!-- 1번 구획: 캐릭터 -->
    <div class="grid-item char-card">
        <div class="card-title" style="color:#17406d;">
            <span class="title-number"> ASP 중재 활동 목록
        </div>
        <img src="data:image/png;base64,{char_img}" alt="Robot Character">
    </div>

    <!-- 2번 구획: 내용 1 -->
    <div class="grid-item">
        <div class="card-title" style="color:#3E84F7;">
            <span class="title-number">1 | 병합 처방 중재
        </div>
        <div class="card-img-container">
            <img class="card-img" src="data:image/png;base64,{icon1_img}">
        </div>        
        <div class="card-content">
            <b>항균 범위가 중복되는<br>항생제들의 병합 사용<br>중단을 권고합니다.</b>
            <div class="example-text">ex) Pip/tazo + Clindamycin<br>→ Pip/tazo 단독 투여</div>
        </div>
    </div>

    <!-- 3번 구획: 내용 2 -->
    <div class="grid-item">
        <div class="card-title" style="color:#6875EE;">
            <span class="title-number">2 | 장기투여 중재
        </div>
        <div class="card-img-container">
            <img class="card-img" src="data:image/png;base64,{icon2_img}">
        </div>
        <div class="card-content">
            <b>최적 투약 기간을 초과한<br>항생제 장기 사용<br>중단을 권고합니다.</b>
            <div class="example-text">ex) 3세대 Cephalosporin 장기 투여<br>→ 투여 지속 재평가</div>
        </div>
    </div>

    <!-- 4번 구획: 내용 3 -->
    <div class="grid-item">
        <div class="card-title" style="color:#9D44EC;">
            <span class="title-number">3 | 경구 전환
        </div>
        <div class="card-img-container">
            <img class="card-img" src="data:image/png;base64,{icon3_img}">
        </div>
        <div class="card-content">
            <b>경구 생체이용률이 높은<br>주사 항생제의<br>경구 전환을 권고합니다.</b>
            <div class="example-text">ex) Quinolone 일주일 IV 투여<br>→ PO 항생제 전환</div>
        </div>
    </div>

    <!-- 5번 구획: 내용 4 -->
    <div class="grid-item">
        <div class="card-title" style="color:#6F8FBA;">
            <span class="title-number">4 | De-escalation
        </div>
        <div class="card-img-container">
            <img class="card-img" src="data:image/png;base64,{icon4_img}">
        </div>
        <div class="card-content">
            <b>광범위 항생제의 지속 사용을 모니터링하여 소범위 항생제 전환을 권고합니다.</b>
            <div class="example-text">ex) Carbapenem계 4주 이상 사용<br>→ 소범위 항생제로 변경</div>
        </div>
    </div>

    <!-- 6번 구획: 내용 5 -->
    <div class="grid-item">
        <div class="card-title" style="color:#F1840D;">
            <span class="title-number">5 | 검사 기반 중재
        </div>
        <div class="card-img-container">
            <img class="card-img" src="data:image/png;base64,{icon5_img}">
        </div>
        <div class="card-content">
            <b>미생물 검사 결과에 따라<br>감수성이 있는 항생제로의<br>전환을 권고합니다.</b>
            <div class="example-text">ex) 혈액 배양 Candida 검출<br>→ Caspofungin 신속 투여</div>
        </div>
    </div>

    <!-- 7번 구획: 내용 6 -->
    <div class="grid-item">
        <div class="card-title" style="color:#E94C4C;">
            <span class="title-number">6 | 지침 기반 중재
                    </div>
        <div class="card-img-container">
            <img class="card-img" src="data:image/png;base64,{icon6_img}">
        </div>
        <div class="card-content">
            <b>항생제 사용 지침에 따라<br>상황에 맞는 적절한 항생제<br>사용을 권고합니다.</b>
            <div class="example-text">ex) 신기능 저하/투석 환자<br>→ 적절한 용량 변경 권고</div>
        </div>
    </div>

    <!-- 8번 구획: 내용 7 -->
    <div class="grid-item">
        <div class="card-title" style="color:#5EAF4C;">
            <span class="title-number">7 | TDM
        </div>
        <div class="card-img-container">
            <img class="card-img" src="data:image/png;base64,{icon7_img}">
        </div>
        <div class="card-content">
            <b>항생제 혈중 농도를 모니터링하여 치료 목표 도달 및 부작용 최소화 용량을 권고합니다.</b>
            <div class="example-text">ex) IV Vancomycin 투여 환자<br>→ 적정 용량 및 투여 간격 권고</div>
        </div>
    </div>

    </div>
    """, unsafe_allow_html=True)
    # =========================
    # 제한항생제 승인 현황
    # =========================

    st.markdown("""
    <div class="section-title-box">
        <div class="section-title-text">
            제한항생제 승인 현황
        </div>
    </div>
    """, unsafe_allow_html=True)  

    # =========================
    # 월별 데이터 정리
    # =========================

    approval_df = df_inter_data.copy()

    # 승인률 %
    approval_df["승인률(%)"] = (
        approval_df["승인률"] * 100
    )

    # =========================
    # 콤보 그래프 생성
    # =========================

    from plotly.subplots import make_subplots
    import plotly.graph_objects as go

    fig_approval = make_subplots(
        specs=[[{"secondary_y": True}]]
    )

    # =========================
    # 승인 건수 막대
    # =========================

    fig_approval.add_trace(

        go.Bar(

            x=approval_df["월"],

            y=approval_df["승인 건수"],

            name="승인 건수",

            marker_color="#A7C7FF",

            text=approval_df["승인 건수"],

            textposition="outside",

            textfont=dict(
                size=13,
                color="#111827"
            )
        ),

        secondary_y=False
    )

    # =========================
    # 미승인 건수 막대
    # =========================

    fig_approval.add_trace(

        go.Bar(

            x=approval_df["월"],

            y=approval_df["미승인 건수"],

            name="미승인 건수",

            marker_color="#FFB4B4",

            text=approval_df["미승인 건수"],

            textposition="outside",

            textfont=dict(
                size=13,
                color="#111827"
            )
        ),

        secondary_y=False
    )

    # =========================
    # 승인률 선 그래프
    # =========================

    fig_approval.add_trace(

        go.Scatter(

            x=approval_df["월"],

            y=approval_df["승인률(%)"],

            name="승인률",

            mode="lines+markers+text",

            line=dict(
                color="#2563eb",
                width=3
            ),

            marker=dict(
                size=9
            ),

            text=[
                f"{v:.1f}%"
                for v in approval_df["승인률(%)"]
            ],

            textposition="top center",

            textfont=dict(
                size=13,
                color="#1e3a8a"
            )
        ),

        secondary_y=True
    )

    # =========================
    # 레이아웃
    # =========================

    fig_approval.update_layout(

        height=520,

        barmode="group",

        paper_bgcolor='rgba(255,255,255,0)',
        plot_bgcolor='rgba(255,255,255,0)',

        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        ),

        legend=dict(

            orientation="h",

            yanchor="bottom",
            y=1.02,

            xanchor="right",
            x=1
        ),

        xaxis=dict(

            showline=False,

            showgrid=False
        ),
        yaxis=dict(

            title="건수",

            range=[0, 1000],

            showline=False,

            showgrid=True,
            gridcolor="#e5e7eb",

            dtick=100
        ),

        font=dict(
            color="#111827"
        )
    )

    # =========================
    # 우측 Y축
    # =========================

    fig_approval.update_yaxes(

        title_text="승인률 (%)",

        range=[0, 100],

        secondary_y=True
    )

    # =========================
    # 그래프 제목
    # =========================

    st.markdown("""
    <div class="chart-title-box">
        <div class="chart-title">
            📋 월별 제한항생제 승인 현황
        </div>
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # 출력
    # =========================

    st.plotly_chart(
        fig_approval,
        use_container_width=True,
        config={"displayModeBar": False},
        key="approval_graph"
    )

    with open("제한.png", "rb") as f:
        restricted_base64 = base64.b64encode(
            f.read()
        ).decode()

    with open("물음표.png", "rb") as f:
        question_base64 = base64.b64encode(
            f.read()
        ).decode()

    # 맨 아래 여백
    st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)

    # 제한.png 표시 박스
    st.markdown(f"""
    <div style="
        background:#a9d8ff;        /* 박스 배경색 (하늘색) */
        border:1px solid #dbe7f3;
        border-radius:28px;
        padding:18px;             /* 내부 여백 (소폭 증가) */
        margin-top:0px;
        margin-bottom:15px;
        box-shadow:0 4px 14px rgba(0,0,0,0.05);
        display:flex;             /* 자식 요소를 수평으로 배치 */
        align-items:center;       /* 수직 중앙 정렬 */
        gap: 30px;                /* 두 칼럼 사이의 간격 */
    ">

    <!-- 왼쪽 COLUMN: 이미지 -->
    <div style="
        flex: 1.3;              /* 왼쪽 칼럼 비율 */
        display: flex;
        justify-content: center; /* 이미지 중앙 정렬 */
    ">
        <img src="data:image/png;base64,{restricted_base64}" style="
                width:100%;
                height:550px;  /* 이미지 최대 크기 조정 (텍스트 공간 확보) */
                border-radius:20px;
                object-fit: contain; /* 이미지 비율 유지 */
        ">
    </div>

    <!-- 오른쪽 COLUMN: 흰색 뭉툭한 박스 내부 텍스트 -->
    <div style="
        flex: 1;              /* 오른쪽 칼럼 비율 */
        background: white;     /* 흰색 박스 배경색 */
        border-radius: 20px;  /* 뭉툭한 라운딩 */
        padding: 30px;        /* 흰색 박스 내부 여백 */
        box-shadow: inset 0 8px 20px rgba(0,0,0,0.06); /* 은은한 안쪽 그림자 효과 */
        border: 1px solid #e1e9f1; /* 은은한 테두리 */
        color: #17406d;       /* 텍스트 기본 색상 */
    ">
        <!-- 제목 -->
        <div style="
            font-size: 24px;
            font-weight: 800;
            margin-bottom: 15px; /* 제목과 본문 사이 간격 */
            line-height: 1.3;
            display: center;
            color: #0f2b48;
        ">
            항생제 처방에 왜 승인이 필요한가요?
        </div>
        <!-- 구분선 (선택사항) -->
        <div style="
            border-top: 2px dashed #a9d8ff;
            margin: 15px 0;
            opacity: 0.7;
        "></div>
        <div style="text-align: center;">
            <img src="data:image/png;base64,{question_base64}" style="
                width:100%;
                height:260px;  /* 이미지 최대 크기 조정 (텍스트 공간 확보) */
                object-fit: contain;
                margin: 5px 0 15px 0;
                mix-blend-mode: multiply; /* 흰색 사각 배경을 카드와 자연스럽게 융합 */
            ">
        </div>
         <!-- 3. 핵심 강조 한 줄 (뱃지 + 주황색 포인트) -->
        <div style="
            text-align: center;
            font-size: 20px;
            font-weight: 800;
            margin-bottom: 18px;
            color: #222;
        ">
            제한항생제 승인 체계는 
            <span style="
                background-color: #f4f8fc;
                color: #2563eb;
                padding: 3px 10px;
                border-radius: 8px;
                border: 2px solid #2563eb;
            ">ASP 필수 항목</span>입니다.
        </div>
        <!-- 4. 본문 설명 박스 (포인트 바 + 형광펜 효과) -->
            <div style="
                font-size: 15px;
                line-height: 1.7;
                color: #333;
                background-color: #c6dbff;
                padding: 10px 8px;
                border-radius: 12px;
            ">
                질병관리청 권고 상 제한항생제는 광범위하게 사용될 경우 <br>
                <mark style="background-color: #fff3bf; padding: 2px 4px; border-radius: 4px; font-weight: bold;">항생제 내성을 유발</mark>할 수 있으므로 
                ASP팀에서 관리해야 하며, <br>제한항생제 사용량은 <mark style="background-color: #fff3bf; padding: 2px 4px; border-radius: 4px; font-weight: bold;">경영진 보고 필수 항목</mark>입니다.
            </div>
        </div>
        """, unsafe_allow_html=True)

    left_space, button_col = st.columns([9, 1])

    with button_col:

        if st.button("🔄Refresh"):

            load_inter_data.clear()

            st.toast("페이지를 새로고침했습니다.")

elif st.session_state.menu == "ASP팀 활동":

    @st.cache_data
    def load_image(path):
        with open(path, "rb") as f:
             return base64.b64encode(
                f.read()
             ).decode()
    team_base64 = load_image("team1.png")

    st.markdown("""
    <div class="section-title-box">
        <div class="section-title-text">
            ASP 전담팀 구성
        </div>
    </div>
    """, unsafe_allow_html=True)
    # =========================
    # 좌우 컬럼
    # =========================

    left_col, right_col = st.columns([1, 1])

    # =========================
    # 왼쪽 컬럼 (사진)
    # =========================

    with left_col:

        st.markdown(f"""
        <div style="
            background:white;
            border-radius:28px;
            padding:28px;
            box-shadow:0 2px 10px rgba(0,0,0,0.08);
            margin-bottom:24px;
            height:100%;
        ">

        <div style="
            display:flex;
            flex-direction:column;
            align-items:center;
        ">

        <div style="
            background:#dbeafe;
            color:#17406D;
            padding:5px 26px;
            border-radius:18px;
            font-size:18px;
            font-weight:800;
            box-shadow:0 2px 6px rgba(0,0,0,0.06);
            border:1px solid #cfe0f5;
            margin-bottom:18px;
        ">
            2차년도 ASP 전담팀
        </div>

        <div style="
            display:flex;
            flex-direction:column;
            align-items:center;
        ">
            <img src="data:image/png;base64,{team_base64}" style="
                width:100%;
                border-radius:20px;
            ">
        </div>

        </div>
        """, unsafe_allow_html=True)

    # =========================
    # 오른쪽 컬럼
    # =========================

    with right_col:

        st.markdown("""
        <div style="
            background:white;
            border-radius:28px;
            padding:28px 28px 19px 28px;
            box-shadow:0 2px 10px rgba(0,0,0,0.08);
            margin-bottom:14px;
        ">

        <div style="
            display:flex;
            gap:8px;
            align-items:flex-start;
        ">

        <!-- ===================== -->
        <!-- 왼쪽 표 -->
        <!-- ===================== -->

        <div style="
            flex:1;
        ">

        <div style="
            display:flex;
            flex-direction:column;
            align-items:center;
            margin-bottom:18px;
        ">

        <div style="
            background:#dbeafe;
            color:#17406D;
            padding:5px 26px;
            border-radius:18px;
            font-size:18px;
            font-weight:800;
            box-shadow:0 2px 6px rgba(0,0,0,0.06);
            border:1px solid #cfe0f5;
            margin-bottom:18px;
        ">
            의사 / 약사 현황
        </div>

        </div>

        <table style="
            width:100%;
            border-collapse:collapse;
            text-align:center;
            overflow:hidden;
            border-radius:8px;
        ">

        <tr style="
            background:#214d99;
            color:white;
        ">
            <th style="padding:12px;">소속</th>
            <th style="padding:12px;">성명</th>
        </tr>

        <tr><td style="padding:10px;">감염내과</td><td>신소연</td></tr>
        <tr><td style="padding:10px;">감염내과</td><td>김준형</td></tr>
        <tr><td style="padding:10px;">알레르기면역내과</td><td>이용원</td></tr>
        <tr><td style="padding:10px;">신장내과</td><td>김찬호</td></tr>
        <tr><td style="padding:10px;">심장내과</td><td>박형복</td></tr>
        <tr><td style="padding:10px;">중환자내과</td><td>조은섭</td></tr>
        <tr><td style="padding:10px;">약제팀</td><td>양준원</td></tr>
        <tr><td style="padding:10px;">약제팀</td><td>최경진</td></tr>

        </table>

        </div>

        <!-- ===================== -->
        <!-- 오른쪽 표 -->
        <!-- ===================== -->

        <div style="
            flex:1;
        ">

        <div style="
            display:flex;
            flex-direction:column;
            align-items:center;
            margin-bottom:18px;
        ">

        <div style="
            background:#dbeafe;
            color:#17406D;
            padding:5px 26px;
            border-radius:18px;
            font-size:18px;
            font-weight:800;
            box-shadow:0 2px 6px rgba(0,0,0,0.06);
            border:1px solid #cfe0f5;
            margin-bottom:18px;
        ">
            다학제 인력 현황
        </div>

        </div>

        <table style="
            width:100%;
            border-collapse:collapse;
            text-align:center;
            overflow:hidden;
            border-radius:8px;
        ">

        <tr style="
            background:#214d99;
            color:white;
        ">
            <th style="padding:12px;">소속</th>
            <th style="padding:12px;">성명</th>
        </tr>

        <tr><td style="padding:10px;">간호부</td><td>이태경</td></tr>
        <tr><td style="padding:10px;">간호부</td><td>이고은</td></tr>
        <tr><td style="padding:10px;">전산정보팀</td><td>정의철</td></tr>
        <tr><td style="padding:10px;">전산정보팀</td><td>홍성규</td></tr>
        <tr><td style="padding:10px;">감염관리실</td><td>박세정</td></tr>
        <tr><td style="padding:10px;">기획팀</td><td>김지영</td></tr>
        <tr><td style="padding:10px;">진단검사의학팀</td><td>김지우</td></tr>

        </table>

        </div>

        </div>

        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        """
    <div class="section-title-box">
        <div class="section-title-text">ASP 전담팀 연도별 활동 내역</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    timeline_css = """
    <style>
    /* 카드 전체 영역 - 스크롤 숨김 및 내부 여백 확보 */
    .timeline-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 30px 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
        margin-bottom: 40px;
        border: 1px solid #e2e8f0;
        overflow: hidden; /* 스크롤 완전히 방지 */
    }

    .timeline-title {
        font-size: 20px;
        font-weight: 800;
        color: #0d4da2;
        margin-bottom: 10px;
        border-bottom: 2px solid #f1f5f9;
        padding-bottom: 10px;
    }

    /* 컨테이너 상하 여백을 높여 위쪽 박스가 바깥으로 나가는 것 방지 */
    .timeline-container {
        position: relative;
        display: flex;
        justify-content: space-between; /* 5개가 화면에 균등 배치되도록 설정 */
        align-items: center;
        padding: 300px 10px; /* 상하 여백 300px로 확대하여 위/아래 공간 확보 */
        margin: 10px 0;
        width: 100%;
        box-sizing: border-box;
    }

    /* 가로 중심선 */
    .timeline-line {
        position: absolute;
        top: 50%;
        left: 20px;
        right: 20px;
        height: 4px;
        background: #2563eb;
        z-index: 1;
        transform: translateY(-50%);
    }

    /* 각 아이템 너비 - 5개가 한 화면에 쏙 들어가도록 170px 설정 */
    .timeline-item {
        position: relative;
        z-index: 2;
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 300px;
    }

    /* 중앙 파란선 위 동그라미 */
    .timeline-dot {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 20px;
        height: 20px;
        background: #ffffff;
        border: 4px solid #2563eb;
        border-radius: 50%;
        z-index: 4;
        box-shadow: 0 0 6px rgba(0,0,0,0.15);
    }

    /* --- 기본 월 태그 스타일 (공통) --- */
    .timeline-month {
        position: absolute;
        /* 수평 중앙 정렬 유지 */
        left: 50%;
        transform: translateX(-50%);
        
        /* 기존 스타일 유지 */
        font-weight: 800;
        font-size: 16px;
        color: #1e3a8a;
        background: #eff6ff;
        padding: 3px 12px;
        border-radius: 12px;
        border: 1px solid #bfdbfe;
        white-space: nowrap;
        z-index: 5;
        
        /* 위치 변경 시 부드러운 전환 효과 (선택사항) */
        transition: top 0.3s ease;
    }

    /* --- [핵심] 위치 조건부 설정 --- */

    /* Case 1: 컨텐츠 카드가 위에(.top) 있을 때 -> 월 태그는 동그라미 아래에 배치 */
    /* 동그라미 중심(50%)에서 아래로 16px 이격 */
    .timeline-content.top + .timeline-month {
        top: calc(50% + 16px); 
    }

    /* Case 2: 컨텐츠 카드가 아래에(.bottom) 있을 때 -> 월 태그는 동그라미 위에 배치 */
    /* 동그라미 중심(50%)에서 위로 월 태그 높이(약 30px) + 이격(16px) 만큼 차감 */
    /* 계산값: -(30 + 16) = -46px */
    .timeline-content.bottom + .timeline-month {
        top: calc(50% - 46px);
    }

    /* 콘텐츠 카드 너비 및 위치 고정 */
    .timeline-content {
        position: absolute;
        width: 250px;
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 14px;
        padding: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        z-index: 3;
        box-sizing: border-box;
    }

    /* 위쪽 배치 카드 (중앙선에서 위로 75px 떨어짐) */
    .timeline-content.top {
        bottom: 50px;
    }

    /* 아래쪽 배치 카드 (중앙선에서 아래로 75px 떨어짐) */
    .timeline-content.bottom {
        top: 50px;
    }

    /* 수직 연결선 - 길이와 위치 완벽 보정 (75px) */
    .timeline-content.top::after {
        content: '';
        position: absolute;
        bottom: -50px;
        left: 50%;
        transform: translateX(-50%);
        width: 2px;
        height: 50px;
        background: #2563eb;
    }

    .timeline-content.bottom::before {
        content: '';
        position: absolute;
        top: -50px;
        left: 50%;
        transform: translateX(-50%);
        width: 2px;
        height: 50px;
        background: #2563eb;
    }

    /* 이미지 높이 (110px로 알맞게 조정) */
    .timeline-img {
        width: 100%;
        height: 170px;
        object-fit: cover;
        border-radius: 8px;
        margin-bottom: 8px;
        background-color: #f1f5f9;
    }

    /* 텍스트 크기 */
    .timeline-desc {
        font-size: 16px;
        font-weight: 700;
        color: #1e293b;
        line-height: 1.3;
    }

    .timeline-subdesc {
        font-size: 14px;
        color: #64748b;
        margin-top: 4px;
    }
    </style>
    """
    st.markdown(timeline_css, unsafe_allow_html=True) 

    # 이미지를 base64로 변환해주는 helper 함수
    def get_img_base64(filepath):
        try:
            with open(filepath, "rb") as f:
                return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
        except:
            # 파일이 없을 시 보여줄 더미 이미지
            return "https://via.placeholder.com/300x200?text=No+Image"

    # 타임라인 데이터 구성 (사진 파일명 및 설명 수정)
    years_data = {
        "1차년도 (2024년 11월 ~ 2025년 12월)": [
            {"month": "24년 11월", "pos": "top", "img": get_img_base64("2411 출범.jpg"), "title": "ASP 전담팀 출범", "sub": "인원 구성 및 사업 계획 수립"},
            {"month": "25년 2월", "pos": "bottom", "img": get_img_base64("2503 전산.jpg"), "title": "ASP 친화적 전산 시스템 개발", "sub": "원내 모니터링 구축"},
            {"month": "25년 7월", "pos": "top", "img": get_img_base64("2507 교육.jpg"), "title": "항생제 적정사용 교육", "sub": "직원 대상 ASP 중요성 인식 제고"},
            {"month": "25년 11월", "pos": "bottom", "img": get_img_base64("2511 전공의.jpg"), "title": "항생제 사용지침 교육", "sub": "전공의 대상 항생제 가이드라인 교육"},
            {"month": "25년 12월", "pos": "top", "img": get_img_base64("2512보고.jpg"), "title": "1차년도 결과보고", "sub": "사업 최종 성과 검토 및 결과 보고"}
        ],
        "2차년도 (2026년)": [
            {"month": "26년 1월", "pos": "top", "img": get_img_base64("2601출범.jpg"), "title": "2차년도 ASP 전담팀 구성", "sub": "인력 보강으로 사업 확장 계획 수립"},
            {"month": "26년 5월", "pos": "bottom", "img": get_img_base64("2605 세미나.jpg"), "title": "ASP 네트워크 세미나 참석", "sub": "타 기관 사업 현황 벤치마킹"},
            {"month": "26년 6월", "pos": "top", "img": get_img_base64("2606리포트.jpg"), "title": "ASP 리포트 도입", "sub": "ASP팀과 진료과의 소통 체계 구축"},
            {"month": "26년 7월", "pos": "bottom", "img": get_img_base64("2607 지침.jpg"), "title": "항생제 사용지침 개정", "sub": "본원 진료 현장에 적합한 지침서 제작"}
        ]
    }

        # 차년도별 렌더링
    for year_title, events in years_data.items():
        items_html = "".join(
            [
                f'''<div class="timeline-item">
                    <div class="timeline-content {ev["pos"]}">
                        <img src="{ev["img"]}" class="timeline-img">
                        <div class="timeline-desc">{ev["title"]}</div>
                        <div class="timeline-subdesc">{ev["sub"]}</div>
                    </div>
                    <div class="timeline-month">{ev["month"]}</div>
                    <div class="timeline-dot"></div>
                </div>'''
                for ev in events
            ]
        )

        full_html = f'<div class="timeline-card"><div class="timeline-title">🗓️ {year_title}</div><div class="timeline-container"><div class="timeline-line"></div>{items_html}</div></div>'

        st.markdown(full_html, unsafe_allow_html=True)
        
    st.markdown("""
    <div class="section-title-box">
        <div class="section-title-text">
            ASP 전담팀 이후 활동 PLAN
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
        background:white;
        border-radius:28px;
        padding:30px;
        box-shadow:0 2px 10px rgba(0,0,0,0.08);
    ">

    <!-- 1 -->
    <div style="display:flex; gap:16px; margin-bottom:18px;">
    <div style="
        width:70px;
        min-width:70px;
        height:70px;
        background:#dbeafe;
        border-radius:14px;
        display:flex;
        align-items:center;
        justify-content:center;
        font-size:34px;
        font-weight:900;
        color:#3b82f6;
    ">
        1
    </div>

    <div style="
        flex:1;
        height:70px;
        background:#e6eefb;
        border-radius:14px;
        display:flex;
        align-items:center;
        padding-left:28px;
        font-size:22px;
        font-weight:700;
        color:#1f2937;
    ">
        진료 지원 편의성 증대를 위한 AI 기반 항생제 사용 가이드 챗봇 개발
    </div>
    </div>

    <!-- 2 -->
    <div style="display:flex; gap:16px; margin-bottom:18px;">
    <div style="
        width:70px;
        min-width:70px;
        height:70px;
        background:#eef2f8;
        border-radius:14px;
        display:flex;
        align-items:center;
        justify-content:center;
        font-size:34px;
        font-weight:900;
        color:#3b82f6;
    ">
        2
    </div>

    <div style="
        flex:1;
        height:70px;
        background:#eef2f8;
        border-radius:14px;
        display:flex;
        align-items:center;
        padding-left:28px;
        font-size:22px;
        font-weight:700;
        color:#1f2937;
    ">
        수술의 예방적 항생제 적정사용 관리
    </div>
    </div>

    <!-- 3 -->
    <div style="display:flex; gap:16px; margin-bottom:18px;">
    <div style="
        width:70px;
        min-width:70px;
        height:70px;
        background:#dbeafe;
        border-radius:14px;
        display:flex;
        align-items:center;
        justify-content:center;
        font-size:34px;
        font-weight:900;
        color:#3b82f6;
    ">
        3
    </div>

    <div style="
        flex:1;
        height:70px;
        background:#e6eefb;
        border-radius:14px;
        display:flex;
        align-items:center;
        padding-left:28px;
        font-size:22px;
        font-weight:700;
        color:#1f2937;
    ">
        중환자실 항생제 적정사용 관리
    </div>
    </div>

    <!-- 4 -->
    <div style="display:flex; gap:16px; margin-bottom:18px;">
    <div style="
        width:70px;
        min-width:70px;
        height:70px;
        background:#eef2f8;
        border-radius:14px;
        display:flex;
        align-items:center;
        justify-content:center;
        font-size:34px;
        font-weight:900;
        color:#3b82f6;
    ">
        4
    </div>

    <div style="
        flex:1;
        height:70px;
        background:#eef2f8;
        border-radius:14px;
        display:flex;
        align-items:center;
        padding-left:28px;
        font-size:22px;
        font-weight:700;
        color:#1f2937;
    ">
        3세대 세팔로스포린(Cephalosporin) 계열 항생제 장기 처방에 대한 집중 중재
    </div>
    </div>

    <!-- 5 -->
    <div style="display:flex; gap:16px; margin-bottom:18px;">
    <div style="
        width:70px;
        min-width:70px;
        height:70px;
        background:#dbeafe;
        border-radius:14px;
        display:flex;
        align-items:center;
        justify-content:center;
        font-size:34px;
        font-weight:900;
        color:#3b82f6;
    ">
        5
    </div>

    <div style="
        flex:1;
        height:70px;
        background:#e6eefb;
        border-radius:14px;
        display:flex;
        align-items:center;
        padding-left:28px;
        font-size:22px;
        font-weight:700;
        color:#1f2937;
    ">
        세파마이신(Cephamycin) 계열 항생제 처방 감시 및 중재 강화
    </div>
    </div>

    <!-- 5 -->
    <div style="display:flex; gap:16px; margin-bottom:18px;">

    </div>

    </div>
    """, unsafe_allow_html=True)

