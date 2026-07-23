import streamlit as st
import requests
import pandas as pd
from phone_models import phone_models
from llm_utils import ask_llm

st.set_page_config(page_title="예산 맞춤 추천", page_icon="💰")

st.title("💰 예산 맞춤 추천")
st.write("예산과 원하는 상태 등급을 입력하면, 그 조건에 맞는 모델을 추천해드려요.")


def get_predicted_price(model_name, storage_gb, condition):
    """모델+용량+등급 조건으로 FastAPI에 예측 요청을 보내는 공통 함수"""
    base_spec = phone_models[model_name]
    new_price = base_spec["storage_options"][storage_gb]

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
            return response.json()["predicted_price"]
    except requests.exceptions.ConnectionError:
        return None
    return None


budget = st.number_input("예산 (원)", min_value=0, max_value=4000000, value=500000, step=50000)
target_condition = st.selectbox(
    "원하는 상태 등급",
    ["S", "A", "B", "F"],
    index=2,
    help="S: 미개봉/무잔상, A: 상태 좋음, B: 일반 사용감, F: 파손/고장/부품용"
)

if st.button("추천받기", type="primary"):
    results = []
    progress = st.progress(0, text="모든 모델 확인 중...")

    all_combinations = []
    for m, spec in phone_models.items():
        for storage in spec["storage_options"].keys():
            all_combinations.append((m, storage))

    for i, (m, storage) in enumerate(all_combinations):
        price = get_predicted_price(m, storage, target_condition)
        if price is not None:
            results.append({
                "모델": f"{m} {storage}GB",
                "예상가(원)": price,
                "용량": storage
            })
        progress.progress((i + 1) / len(all_combinations), text=f"확인 중... ({i+1}/{len(all_combinations)})")

    progress.empty()

    result_df = pd.DataFrame(results)
    within_budget = result_df[result_df["예상가(원)"] <= budget].sort_values("예상가(원)", ascending=False)

    if len(within_budget) > 0:
        st.success(f"예산 {budget:,}원 이내, 등급 '{target_condition}' 기준으로 {len(within_budget)}개 조합을 찾았어요!")

        within_budget = within_budget.copy()
        within_budget["비고"] = within_budget["용량"].apply(lambda x: "⚠️ 표본 적음" if x >= 512 else "")
        display_df = within_budget[["모델", "예상가(원)", "비고"]]

        st.dataframe(display_df.reset_index(drop=True), use_container_width=True)

        with st.spinner("AI가 추천 이유를 정리하는 중..."):
            top5 = within_budget.head(5).to_dict(orient="records")
            candidates_text = "\n".join([f"- {r['모델']}: 약 {r['예상가(원)']:,}원" for r in top5])

            system_prompt = "당신은 중고폰 구매를 도와주는 친절하고 실용적인 조언가입니다."
            user_prompt = (
                f"예산 {budget:,}원, 상태 등급 '{target_condition}' 조건에서 "
                f"아래 후보들을 찾았습니다.\n\n{candidates_text}\n\n"
                "이 중 가장 추천할 만한 1~2개를 골라, 그 이유를 3줄 이내로 간단히 설명해주세요. "
                "가격대비 스펙 관점에서 설명해주세요."
            )
            explanation = ask_llm(system_prompt, user_prompt)

        st.subheader("🤖 AI 추천 코멘트")
        st.info(explanation)

    else:
        st.warning("해당 예산으로는 조건에 맞는 모델이 없어요. 예산을 늘리거나 등급을 조정해보세요.")

    st.caption(
        "※ 번개장터 실거래 데이터 기반 회귀 모델 + 시장 벤치마크 등급 보정을 "
        "결합한 예측 결과입니다. '⚠️ 표본 적음' 표시가 있는 조합(저장용량 512GB 이상)은 "
        "학습 표본이 적어 예측 신뢰도가 낮을 수 있습니다."
    )