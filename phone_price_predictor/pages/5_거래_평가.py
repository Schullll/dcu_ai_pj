import streamlit as st
import requests
from phone_models import phone_models
from llm_utils import ask_llm

st.set_page_config(page_title="거래 평가", page_icon="🔍")

st.title("🔍 거래 평가")
st.write("내가 실제로 사거나 팔려는 가격이, 그 조건(모델·용량·등급)의 적정 시세 대비 어떤지 비교해드려요.")

st.subheader("조건 입력")

model_name = st.selectbox("모델 선택", list(phone_models.keys()))
base_spec = phone_models[model_name]

storage_options = base_spec["storage_options"]
memory_list = list(storage_options.keys())
storage_gb = st.selectbox("저장용량 (GB)", memory_list)
new_price = storage_options[storage_gb]

# 표본이 적은 고용량 옵션에 대한 신뢰도 안내
if storage_gb >= 512:
    st.warning("⚠️ 해당 저장용량은 학습 표본이 적어 예측 신뢰도가 낮을 수 있습니다. 참고용으로만 확인해주세요.")

condition = st.selectbox(
    "상태 등급",
    ["S", "A", "B", "F"],
    index=2,
    help="거래 대상 기기의 실제 상태를 선택해주세요. S: 미개봉/무잔상, A: 상태 좋음, B: 일반 사용감, F: 파손/고장"
)

my_price = st.number_input(
    "실제 거래 가격(원)", min_value=0, value=200000, step=10000,
    help="내가 실제로 사려는(또는 팔려는) 가격을 입력해주세요."
)

if st.button("비교하기", type="primary"):
    input_data = {
        "brand": base_spec["device_brand"],
        "condition": condition,
        "screen_size": base_spec["screen_size"],
        "ram": base_spec["ram"],
        "battery": base_spec["battery"],
        "weight": base_spec["weight"],
        "release_year": base_spec["release_year"],
        "storage_gb": storage_gb,
        "new_price": new_price
    }

    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=input_data, timeout=5)

        if response.status_code == 200:
            expected_value = response.json()["predicted_price"]

            diff = my_price - expected_value
            diff_percent = (diff / expected_value) * 100 if expected_value > 0 else 0

            col1, col2, col3 = st.columns(3)
            col1.metric("적정 예상가치", f"{expected_value:,}원")
            col2.metric("내 거래 가격", f"{my_price:,}원")
            col3.metric("가치 비교", f"{diff_percent:+.1f}%", delta=f"{diff:,}원")

            if diff_percent <= -10:
                st.success("📉 적정 예상가치보다 낮은 가격이에요. 잘 산 편일 가능성이 높아요!")
            elif diff_percent >= 10:
                st.warning("📈 적정 예상가치보다 높은 가격이에요. 조금 비싸게 거래하는 걸 수 있어요.")
            else:
                st.info("⚖️ 적정 예상가치와 비슷한 수준의 합리적인 가격이에요.")

            st.divider()

            with st.spinner("AI가 거래 평가 코멘트를 작성하는 중..."):
                condition_label = {
                    "S": "미개봉/무잔상급", "A": "상태 좋음", "B": "일반 사용감", "F": "파손/고장"
                }[condition]

                system_prompt = "당신은 중고폰 거래를 도와주는 친절하고 실용적인 조언가입니다."
                user_prompt = (
                    f"모델: {model_name} {storage_gb}GB\n"
                    f"상태 등급: {condition_label}\n"
                    f"적정 예상가치: {expected_value:,}원\n"
                    f"실제 거래 가격: {my_price:,}원 (적정가 대비 {diff_percent:+.1f}%)\n\n"
                    "이 거래가 적정 시세 대비 유리한지 불리한지 3줄 이내로 간단히 설명하고, "
                    "거래 시 참고할 만한 조언을 해주세요."
                )
                explanation = ask_llm(system_prompt, user_prompt)

            st.subheader("🤖 AI 거래 평가 코멘트")
            st.info(explanation)

            st.caption(
                "※ 적정 예상가치는 번개장터 실거래 데이터 기반 회귀 모델과 "
                "실제 중고폰 시장 벤치마크 기준 등급 보정을 결합한 예측치입니다."
            )
        else:
            st.error(f"예측 실패: {response.json()}")

    except requests.exceptions.ConnectionError:
        st.error("⚠️ FastAPI 서버에 연결할 수 없습니다. 서버가 켜져 있는지 확인해주세요.")