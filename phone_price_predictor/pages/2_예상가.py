import streamlit as st
import requests
from phone_models import phone_models
from llm_utils import ask_llm

st.set_page_config(page_title="예상가", page_icon="📱")

st.title("📱 예상가")
st.write("모델·저장용량·상태 등급을 선택하면, 실거래 데이터 기반 모델이 예상가를 알려드려요.")

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
    index=1,
    help="S: 미개봉/무잔상, A: 상태 좋음(S급 표기), B: 일반 사용감, F: 파손/고장/부품용"
)

st.divider()
with st.expander("자동으로 채워진 스펙 정보 보기"):
    display_spec = {k: v for k, v in base_spec.items() if k != "storage_options"}
    display_spec["선택한 저장용량(GB)"] = storage_gb
    display_spec["신품가(원)"] = f"{new_price:,}원"
    st.json(display_spec)

st.divider()

if st.button("💰 예상가 확인하기", type="primary"):
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
            result = response.json()
            predicted_price = result["predicted_price"]
            percent_of_new = (predicted_price / new_price) * 100

            st.success(f"### 예상 중고가: 약 **{predicted_price:,}원**")
            st.caption(f"신품가 {new_price:,}원 대비 약 {percent_of_new:.1f}% 수준입니다.")

            st.divider()

            with st.spinner("AI가 시세 설명을 작성하는 중..."):
                condition_label = {
                    "S": "미개봉/무잔상급",
                    "A": "상태 좋음",
                    "B": "일반 사용감",
                    "F": "파손/고장"
                }[condition]

                system_prompt = "당신은 중고폰 거래를 도와주는 친절하고 실용적인 조언가입니다."
                user_prompt = (
                    f"모델: {model_name} {storage_gb}GB\n"
                    f"상태 등급: {condition_label}\n"
                    f"신품가: {new_price:,}원\n"
                    f"예상 중고가: {predicted_price:,}원 (신품가 대비 {percent_of_new:.1f}%)\n\n"
                    "이 예상가가 해당 등급 기준으로 합리적인지 3줄 이내로 간단히 설명하고, "
                    "이 조건으로 거래할 때 참고할 만한 조언을 해주세요."
                )
                explanation = ask_llm(system_prompt, user_prompt)

            st.subheader("🤖 AI 시세 코멘트")
            st.info(explanation)

        else:
            st.error(f"예측 실패: {response.json()}")

    except requests.exceptions.ConnectionError:
        st.error("⚠️ FastAPI 서버에 연결할 수 없습니다. 서버가 켜져 있는지 확인해주세요.")

    st.caption(
        "※ 번개장터 실거래 데이터 기반 회귀 모델 + 실제 중고폰 시장 벤치마크 "
        "기준 등급별 보정(S/A/B/F)을 결합한 예측입니다. "
    )
