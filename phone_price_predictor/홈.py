import streamlit as st

# 1. 페이지 설정
st.set_page_config(
    page_title="중고폰 가격 예측 서비스",
    page_icon="📱",
    layout="wide"
)

# 2. 버튼 완벽 고정 및 줄바꿈 CSS
st.markdown("""
    <style>
    /* 전체 여백 */
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 1100px !important;
    }

    /* 버튼 전체를 160px 고정 규격 카드 상자로 변환 */
    div.stButton > button {
        width: 100% !important;
        height: 160px !important;
        min-height: 160px !important;
        max-height: 160px !important;
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
        border: 1px solid #334155 !important;
        border-radius: 16px !important;
        padding: 24px !important;
        text-align: left !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: flex-start !important;
        align-items: flex-start !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2) !important;
        cursor: pointer !important;
    }

    /* 카드 호버 효과 */
    div.stButton > button:hover {
        border-color: #3b82f6 !important;
        transform: translateY(-4px) !important;
        box-shadow: 0 12px 20px -5px rgba(59, 130, 246, 0.3) !important;
        background: linear-gradient(135deg, #1e293b 0%, #1e1b4b 100%) !important;
    }

    div.stButton > button:active {
        transform: translateY(-1px) !important;
    }

    /* 버튼 내부 텍스트 전체 설정 */
    div.stButton > button p {
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
        text-align: left !important;
        white-space: pre-line !important; /* \n 줄바꿈 인식 및 자동 줄바꿈 처리 */
        font-size: 0.9rem !important;
        color: #94a3b8 !important;
        line-height: 1.5 !important;
    }

    /* 첫 번째 줄(제목)만 흰색/굵게 강조 */
    div.stButton > button p::first-line {
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        color: #f8fafc !important;
        line-height: 2.2 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 헤더
st.title("📱 중고폰 가격 예측 서비스")
st.caption("아래 카드를 클릭하거나, 왼쪽 사이드바에서 원하는 기능을 선택하세요.")

st.divider()

# 4. 카드 그리드 배치 (첫 줄 = 제목 / 둘째 줄 = 설명)
col1, col2 = st.columns(2)

with col1:
    if st.button("📊  모델별 시세\n모델을 선택하면 스펙과 신품가, 사용기간별 예상 시세를 그래프로 확인해요.", key="card_1"):
        st.switch_page("pages/1_모델별_시세.py")
        
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    if st.button("📉  모델 비교 & 랭킹\n여러 모델의 예상가를 겹쳐 비교하거나, 시점별 가격 순위를 확인해요.", key="card_3"):
        st.switch_page("pages/3_모델_비교_랭킹.py")

    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    if st.button("🔍  거래 평가\n예전에 산 폰이 지금 얼마나 값어치가 남았는지 확인해요.", key="card_5"):
        st.switch_page("pages/5_거래_평가.py")

with col2:
    if st.button("💰  예상가\n모델·저장용량·사용기간을 입력하면 학습된 모델이 적정 예상가를 추정해요.", key="card_2"):
        st.switch_page("pages/2_예상가.py")

    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    if st.button("💸  예산 맞춤 추천\n예산을 입력하면 그 범위에서 살 수 있는 모델을 추천해요.", key="card_4"):
        st.switch_page("pages/4_예산_맞춤_추천.py")