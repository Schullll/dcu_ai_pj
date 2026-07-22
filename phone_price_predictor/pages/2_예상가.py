import streamlit as st
import requests
from phone_models import phone_models
from llm_utils import ask_llm  # 공통 LLM 호출 함수 (GPT-5 mini, 학교 제공 API)

st.set_page_config(page_title="예상가", page_icon="📱")

st.title("📱 예상가")
st.write("모델·저장용량·상태 등급을 선택하면, 실거래 데이터 기반 모델이 예상가를 알려드려요.")

st.subheader("조건 입력")

# ── 1. 모델 및 저장용량 선택 ──────────────────────────────
model_name = st.selectbox("모델 선택", list(phone_models.keys()))
base_spec = phone_models[model_name]

# 선택한 모델이 실제로 출시했던 저장용량만 옵션으로 나옴
storage_options = base_spec["storage_options"]
memory_list = list(storage_options.keys())
storage_gb = st.selectbox("저장용량 (GB)", memory_list)
new_price = storage_options[storage_gb]  # 검증된 실제 신품 출고가(원)

# ── 2. 상태 등급 선택 (S/A/B/F, 4단계) ───────────────────
# 등급별 가격 반영은 server.py에서 실제 시장 벤치마크 배율로 처리됨
condition = st.selectbox(
    "상태 등급",
    ["S", "A", "B", "F"],
    index=1,  # 기본값 A (상태 좋음)
    help="S: 미개봉/무잔상, A: 상태 좋음(S급 표기), B: 일반 사용감, F: 파손/고장/부품용"
)

st.divider()
# 자동으로 채워진 스펙을 펼쳐서 확인할 수 있게 (투명성 확보용)
with st.expander("자동으로 채워진 스펙 정보 보기"):
    display_spec = {k: v for k, v in base_spec.items() if k != "storage_options"}
    display_spec["선택한 저장용량(GB)"] = storage_gb
    display_spec["신품가(원)"] = f"{new_price:,}원"
    st.json(display_spec)

st.divider()

if st.button("💰 예상가 확인하기", type="primary"):
    # ── 3. FastAPI에 예측 요청 ────────────────────────────
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

            # ── 4. 예측 결과 표시 ─────────────────────────
            st.success(f"### 예상 중고가: 약 **{predicted_price:,}원**")
            st.caption(f"신품가 {new_price:,}원 대비 약 {percent_of_new:.1f}% 수준입니다.")

            st.divider()

            # ── 5. LLM에게 예측 결과를 바탕으로 자연어 설명 요청 ──
            # 숫자 결과(예상가, 등급, 비율)를 프롬프트에 담아 전달하고,
            # 사람이 이해하기 쉬운 코멘트를 생성하도록 함
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

    # ── 6. 데이터 출처 및 방법론 안내 (신뢰성 확보) ─────────
    st.caption(
        "※ 번개장터 실거래 데이터(781건) 기반 회귀 모델 + 실제 중고폰 시장 벤치마크 "
        "기준 등급별 보정(S/A/B/F)을 결합한 예측입니다."
    )