import streamlit as st
import requests
import numpy as np
import pandas as pd
from phone_models import phone_models
from llm_utils import ask_llm

st.set_page_config(page_title="예산 맞춤 추천", page_icon="💰")

EXCHANGE_RATE = 1479.26
BASELINE_DAYS_USED = 674
RETENTION_A = 0.4562
RETENTION_B = 0.000267


def get_retention_ratio(days_used: int) -> float:
    days_used_clamped = max(min(days_used, 1300), 0)
    return RETENTION_A * np.exp(-RETENTION_B * days_used_clamped)


BASELINE_RETENTION = get_retention_ratio(BASELINE_DAYS_USED)


def get_baseline_prediction(model_name, internal_memory):
    base_spec = phone_models[model_name]
    selected_new_price = base_spec["storage_options"][internal_memory]

    input_data = {
        "device_brand": base_spec["device_brand"],
        "os": base_spec["os"],
        "screen_size": base_spec["screen_size"],
        "rear_camera_mp": base_spec["rear_camera_mp"],
        "front_camera_mp": base_spec["front_camera_mp"],
        "internal_memory": internal_memory,
        "ram": base_spec["ram"],
        "battery": base_spec["battery"],
        "weight": base_spec["weight"],
        "release_year": base_spec["release_year"],
        "days_used": BASELINE_DAYS_USED,
        "normalized_new_price": selected_new_price,
        "is_4g": base_spec["is_4g"],
        "is_5g": base_spec["is_5g"]
    }
    response = requests.post("http://127.0.0.1:8000/predict", json=input_data, timeout=5)
    if response.status_code == 200:
        return response.json()["predicted_used_price"]
    return None


def price_at_days(baseline_log, days):
    retention = get_retention_ratio(days)
    factor = retention / BASELINE_RETENTION
    usd = np.exp(baseline_log) * factor
    return usd * EXCHANGE_RATE


st.title("💰 예산 맞춤 추천")
st.write("예산과 원하는 사용기간(중고 상태)을 입력하면, 그 조건에 맞는 모델을 추천해드려요.")

budget = st.number_input("예산 (원)", min_value=0, max_value=3000000, value=500000, step=50000)
target_days = st.slider("찾으시는 중고폰의 예상 사용기간(일)", 91, 1094, 500, step=30, help="이 사용기간 기준으로 예산 안에 들어오는 모델을 찾아드려요.")

if st.button("추천받기", type="primary"):
    results = []
    progress = st.progress(0, text="모든 모델 확인 중...")

    all_combinations = []
    for m, spec in phone_models.items():
        for mem in spec["storage_options"].keys():
            all_combinations.append((m, mem))

    for i, (m, mem) in enumerate(all_combinations):
        baseline_log = get_baseline_prediction(m, mem)
        if baseline_log is not None:
            price = price_at_days(baseline_log, target_days)
            results.append({"모델": f"{m} {mem}GB", "예상가(원)": round(price)})
        progress.progress((i + 1) / len(all_combinations), text=f"확인 중... ({i+1}/{len(all_combinations)})")

    progress.empty()

    result_df = pd.DataFrame(results)
    within_budget = result_df[result_df["예상가(원)"] <= budget].sort_values("예상가(원)", ascending=False)

    if len(within_budget) > 0:
        st.success(f"예산 {budget:,}원 이내, 사용기간 {target_days}일 기준으로 {len(within_budget)}개 조합을 찾았어요!")
        st.dataframe(within_budget.reset_index(drop=True), use_container_width=True)

        with st.spinner("AI가 추천 이유를 정리하는 중..."):
            top5 = within_budget.head(5).to_dict(orient="records")
            candidates_text = "\n".join([f"- {r['모델']}: 약 {r['예상가(원)']:,}원" for r in top5])
            system_prompt = "당신은 중고폰 구매를 도와주는 친절하고 실용적인 조언가입니다."
            user_prompt = f"예산 {budget:,}원, 사용기간 약 {target_days}일 조건에서 아래 후보들을 찾았습니다.\n\n{candidates_text}\n\n이 중 가장 추천할 만한 1~2개를 골라, 그 이유를 3줄 이내로 간단히 설명해주세요. 가격대비 스펙 관점에서 설명해주세요."
            explanation = ask_llm(system_prompt, user_prompt)

        st.subheader("🤖 AI 추천 코멘트")
        st.info(explanation)
    else:
        st.warning("해당 예산으로는 조건에 맞는 모델이 없어요. 예산을 늘리거나 사용기간을 조정해보세요.")

    st.caption("※ 예상가는 각 모델의 실제 신품 출고가와 사용기간별 실측 감가곡선을 기반으로 계산되었습니다.")