import streamlit as st
import requests
import pandas as pd
import altair as alt
from phone_models import phone_models

st.set_page_config(page_title="모델 비교 & 랭킹", page_icon="📉")

st.title("📉 모델 비교 & 감가 랭킹")
st.write("원하는 모델·용량·등급 조건을 직접 설정해 비교하거나, 특정 등급 기준 전체 랭킹을 확인해요.")


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


tab1, tab2 = st.tabs(["📊 모델 직접 비교", "🏆 전체 랭킹"])

# ══════════════════════════════════════════════════════
# 탭1: 사용자가 각 조건(모델+용량+등급)을 직접 설정해서 비교
# ══════════════════════════════════════════════════════
with tab1:
    st.subheader("비교할 조건 설정")

    num_items = st.radio("비교할 개수", [2, 3], horizontal=True)

    compare_items = []
    cols = st.columns(num_items)

    for i in range(num_items):
        with cols[i]:
            st.markdown(f"**조건 {i+1}**")
            m_name = st.selectbox("모델", list(phone_models.keys()), key=f"model_{i}")
            m_spec = phone_models[m_name]
            m_storage = st.selectbox("용량(GB)", list(m_spec["storage_options"].keys()), key=f"storage_{i}")
            m_condition = st.selectbox("등급", ["S", "A", "B", "F"], index=1, key=f"condition_{i}")

            if m_storage >= 512:
                st.caption("⚠️ 표본 적음, 참고용")

            compare_items.append({"model": m_name, "storage": m_storage, "condition": m_condition})

    if st.button("비교하기", type="primary"):
        compare_results = []

        for item in compare_items:
            price = get_predicted_price(item["model"], item["storage"], item["condition"])
            if price is not None:
                label = f"{item['model']} {item['storage']}GB ({item['condition']}등급)"
                compare_results.append({"조건": label, "예상가": price})

        if compare_results:
            compare_df = pd.DataFrame(compare_results).sort_values("예상가", ascending=True)

            bars = (
                alt.Chart(compare_df)
                .mark_bar(color="#3498db")
                .encode(
                    y=alt.Y("조건:N", sort="-x", title=None),
                    x=alt.X("예상가:Q", title="예상가(원)"),
                    tooltip=["조건", "예상가"]
                )
            )
            text = bars.mark_text(align="left", dx=5, fontSize=13).encode(
                text=alt.Text("예상가:Q", format=",")
            )

            st.altair_chart((bars + text).properties(height=100 + len(compare_df) * 60), use_container_width=True)
            st.dataframe(compare_df.sort_values("예상가", ascending=False).reset_index(drop=True), use_container_width=True)
        else:
            st.error("⚠️ 예측에 실패했습니다. FastAPI 서버가 켜져 있는지 확인해주세요.")

# ══════════════════════════════════════════════════════
# 탭2: 30개 모델 전체를 특정 등급 기준으로 순위 매기기
# (각 모델의 최대 저장용량 기준으로 통일해서 비교)
# ══════════════════════════════════════════════════════
with tab2:
    st.subheader("전체 모델 랭킹")
    ranking_condition = st.selectbox(
        "랭킹 기준 등급", ["S", "A", "B", "F"], index=1, key="ranking_condition"
    )

    if st.button("랭킹 생성", type="primary"):
        ranking_data = []
        progress = st.progress(0, text="계산 중...")

        model_list = list(phone_models.keys())
        for i, m in enumerate(model_list):
            top_storage = max(phone_models[m]["storage_options"].keys())
            price = get_predicted_price(m, top_storage, ranking_condition)

            if price is not None:
                ranking_data.append({
                    "모델": f"{m} ({top_storage}GB)",
                    "예상가(원)": price,
                    "최대용량": top_storage
                })

            progress.progress((i + 1) / len(model_list), text=f"계산 중... ({i+1}/{len(model_list)})")

        progress.empty()

        if ranking_data:
            ranking_df = pd.DataFrame(ranking_data).sort_values("예상가(원)", ascending=False).reset_index(drop=True)
            ranking_df.index = ranking_df.index + 1

            ranking_df["비고"] = ranking_df["최대용량"].apply(
                lambda x: "⚠️ 표본 적음" if x >= 512 else ""
            )
            display_df = ranking_df[["모델", "예상가(원)", "비고"]]

            st.write(f"**등급 '{ranking_condition}' 기준, 예상가 높은 순 랭킹**")
            st.dataframe(display_df, use_container_width=True)

            st.caption(
                "※ 각 모델의 최대 저장용량 기준이며, 번개장터 실거래 데이터 기반 "
                "회귀 모델 + 시장 벤치마크 등급 보정을 결합한 예측 결과입니다. "
                "'⚠️ 표본 적음' 표시가 있는 모델(저장용량 512GB 이상)은 학습 표본이 적어 "
                "예측 순서가 실제 신품가 순서와 다르게 나타날 수 있습니다."
            )