import streamlit as st
import numpy as np
from phone_models import phone_models
from llm_utils import ask_llm

st.set_page_config(page_title="내 폰 진단", page_icon="🔍")

RETENTION_A = 0.4562
RETENTION_B = 0.000267


def get_retention_ratio(days_used: int) -> float:
    """
    사용기간(일)을 받아 '신품가 대비 남은 가치 비율(0~1)'을 반환.
    이 값은 이미 신품가 기준 완결된 비율이므로, 다른 시점 값으로
    다시 나누지 않고 구매가에 바로 곱해서 사용해야 함.
    (과거 버전에서 0일 시점 값으로 한 번 더 나누는 이중 계산 오류가 있었음 → 수정됨)
    """
    days_used_clamped = max(min(days_used, 1300), 0)
    return RETENTION_A * np.exp(-RETENTION_B * days_used_clamped)


st.title("🔍 내 폰 진단")
st.write("예전에 산 폰이 지금 얼마나 값어치가 남았는지 확인해요.")

model_name = st.selectbox("내 모델 선택", list(phone_models.keys()))
purchase_price = st.number_input("구매 당시 가격(원)", min_value=0, value=1000000, step=10000)
days_since_purchase = st.number_input(
    "구매 후 사용 기간 (일)", min_value=0, max_value=2000, value=300,
    help="오늘까지 이 폰을 사용한 일수를 입력해주세요."
)

if st.button("진단하기", type="primary"):
    # retention_now: '신품가 대비 남은 가치 비율' → 구매가에 바로 곱하면 현재 가치
    retention_now = get_retention_ratio(days_since_purchase)
    current_value = purchase_price * retention_now

    lost_value = purchase_price - current_value
    lost_percent = (lost_value / purchase_price) * 100 if purchase_price > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("구매가", f"{purchase_price:,.0f}원")
    col2.metric("현재 예상 가치", f"{current_value:,.0f}원")
    col3.metric("가치 하락", f"-{lost_percent:.1f}%")

    st.divider()

    with st.spinner("AI가 진단 코멘트를 작성하는 중..."):
        system_prompt = "당신은 중고폰 거래를 도와주는 친절하고 실용적인 조언가입니다."
        user_prompt = (
            f"모델: {model_name}\n"
            f"구매가: {purchase_price:,.0f}원\n"
            f"사용 기간: {days_since_purchase}일\n"
            f"현재 예상 가치: {current_value:,.0f}원 (구매가 대비 {lost_percent:.1f}% 하락)\n\n"
            "이 정보를 바탕으로, 사용자에게 지금 상태를 3줄 이내로 간단히 설명하고 "
            "지금 파는 게 나을지 더 쓰는 게 나을지 참고할 만한 조언을 해주세요."
        )
        explanation = ask_llm(system_prompt, user_prompt)

    st.subheader("🤖 AI 진단 코멘트")
    st.info(explanation)

    st.caption(
        "※ 현재 가치는 실제 Apple/Samsung/LG 거래 데이터 기반 감가곡선을 "
        "사용자의 실제 구매가에 적용한 추정치입니다."
    )