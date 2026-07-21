import streamlit as st
import numpy as np
from phone_models import phone_models
from llm_utils import ask_llm

st.set_page_config(page_title="거래 평가", page_icon="🔍")

EXCHANGE_RATE = 1479.26  # 2026-07-21 기준 USD/KRW 환율 (고정값, 실시간 아님)
RETENTION_A = 0.4562
RETENTION_B = 0.000267


def get_retention_ratio(days_used: int) -> float:
    """사용기간(일)을 받아 '신품가 대비 남은 가치 비율(0~1)'을 반환."""
    days_used_clamped = max(min(days_used, 1300), 0)
    return RETENTION_A * np.exp(-RETENTION_B * days_used_clamped)


st.title("🔍 거래 평가")
st.write("내가 실제로 사거나 팔려는 가격이, 그 조건(모델·용량·사용기간)의 적정 시세 대비 어떤지 비교해드려요.")

st.subheader("조건 입력")

model_name = st.selectbox("모델 선택", list(phone_models.keys()))
base_spec = phone_models[model_name]

storage_options = base_spec["storage_options"]
memory_list = list(storage_options.keys())
internal_memory = st.selectbox("저장용량 (GB)", memory_list)
new_price_log = storage_options[internal_memory]  # 이 모델·용량의 실제 신품 출고가(로그값)

days_used = st.number_input(
    "사용 기간 (일)", min_value=0, max_value=2000, value=300,
    help="거래 대상 기기가 실제로 사용된 기간을 입력해주세요."
)

my_price = st.number_input(
    "실제 거래 가격(원)", min_value=0, value=200000, step=10000,
    help="내가 실제로 사려는(또는 팔려는) 가격을 입력해주세요."
)

if st.button("비교하기", type="primary"):
    # 1. 이 조건(모델+용량+사용기간)의 '적정 예상가치' 계산
    new_price_usd = np.exp(new_price_log)
    new_price_krw = new_price_usd * EXCHANGE_RATE
    retention = get_retention_ratio(days_used)
    expected_value = new_price_krw * retention

    # 2. 실제 거래가와 비교
    diff = my_price - expected_value
    diff_percent = (diff / expected_value) * 100 if expected_value > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("적정 예상가치", f"{expected_value:,.0f}원")
    col2.metric("내 거래 가격", f"{my_price:,.0f}원")
    col3.metric("가치 비교", f"{diff_percent:+.1f}%", delta=f"{diff:,.0f}원")

    if diff_percent <= -10:
        st.success("📉 적정 예상가치보다 낮은 가격이에요. 잘 산 편일 가능성이 높아요!")
    elif diff_percent >= 10:
        st.warning("📈 적정 예상가치보다 높은 가격이에요. 조금 비싸게 거래하는 걸 수 있어요.")
    else:
        st.info("⚖️ 적정 예상가치와 비슷한 수준의 합리적인 가격이에요.")

    st.divider()

    with st.spinner("AI가 거래 평가 코멘트를 작성하는 중..."):
        system_prompt = "당신은 중고폰 거래를 도와주는 친절하고 실용적인 조언가입니다."
        user_prompt = (
            f"모델: {model_name} {internal_memory}GB\n"
            f"사용 기간: {days_used}일\n"
            f"적정 예상가치: {expected_value:,.0f}원\n"
            f"실제 거래 가격: {my_price:,.0f}원 (적정가 대비 {diff_percent:+.1f}%)\n\n"
            "이 거래가 적정 시세 대비 유리한지 불리한지 3줄 이내로 간단히 설명하고, "
            "거래 시 참고할 만한 조언을 해주세요."
        )
        explanation = ask_llm(system_prompt, user_prompt)

    st.subheader("🤖 AI 거래 평가 코멘트")
    st.info(explanation)

    st.caption(
        "※ 적정 예상가치는 해당 모델의 실제 신품 출고가에, 실제 Apple/Samsung/LG "
        "거래 데이터 기반 사용기간별 감가곡선을 적용한 추정치입니다."
    )