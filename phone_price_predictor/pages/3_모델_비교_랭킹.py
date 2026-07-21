import streamlit as st
import requests
import numpy as np
import pandas as pd
import altair as alt
from phone_models import phone_models

st.set_page_config(page_title="모델 비교 & 랭킹", page_icon="📉")

EXCHANGE_RATE = 1479.26
BASELINE_DAYS_USED = 674
RETENTION_A = 0.4562
RETENTION_B = 0.000267


def get_retention_ratio(days_used: int) -> float:
    days_used_clamped = max(min(days_used, 1300), 0)
    return RETENTION_A * np.exp(-RETENTION_B * days_used_clamped)


BASELINE_RETENTION = get_retention_ratio(BASELINE_DAYS_USED)


def get_baseline_prediction(model_name, internal_memory):
    """특정 모델+용량의 스펙 기준가(로그값)를 FastAPI로 조회"""
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


st.title("📉 모델 비교 & 감가 랭킹")
st.write("여러 모델의 예상가를 겹쳐 비교하거나, 특정 시점 기준 가격 순위를 확인해요.")

tab1, tab2 = st.tabs(["📊 모델 직접 비교", "🏆 감가 랭킹 (Top / Bottom)"])

# ── 탭1: 선택한 모델 여러 개 비교 ──
with tab1:
    st.subheader("비교할 모델 선택 (2~3개)")
    selected_models = st.multiselect(
        "모델 선택", list(phone_models.keys()), max_selections=3,
        default=list(phone_models.keys())[:2]
    )

    if len(selected_models) >= 2 and st.button("비교 그래프 생성", type="primary"):
        days_range = list(range(91, 1095, 30))
        all_data = []

        for m in selected_models:
            base_spec = phone_models[m]
            # 각 모델의 최대 저장용량으로 비교(가장 대표적인 상위 모델 기준)
            top_memory = max(base_spec["storage_options"].keys())
            baseline_log = get_baseline_prediction(m, top_memory)

            if baseline_log is not None:
                for d in days_range:
                    price = price_at_days(baseline_log, d)
                    all_data.append({"모델": f"{m} ({top_memory}GB)", "사용기간(일)": d, "예상가(원)": price})

        compare_df = pd.DataFrame(all_data)

        chart = (
            alt.Chart(compare_df)
            .mark_line(point=True)
            .encode(
                x=alt.X("사용기간(일):Q"),
                y=alt.Y("예상가(원):Q"),
                color=alt.Color("모델:N", legend=alt.Legend(title="모델")),
                tooltip=["모델", "사용기간(일)", "예상가(원)"]
            )
            .properties(height=450)
        )
        st.altair_chart(chart, use_container_width=True)

        st.caption(
            "※ 감가 속도(%)는 전 모델에 동일한 곡선을 적용했으므로, 이 그래프는 "
            "'절대 금액 차이'(초기 가격 격차)를 비교하는 용도입니다. "
            "브랜드별 감가 속도 차이는 표본 부족으로 이 그래프에는 반영하지 않았습니다."
        )

# ── 탭2: 전체 20개 모델 랭킹 ──
with tab2:
    st.subheader("특정 시점 기준 가격 랭킹")
    ranking_day = st.slider("기준 사용기간(일)", 91, 1094, 365, step=30)

    if st.button("랭킹 생성", type="primary"):
        ranking_data = []
        progress = st.progress(0, text="계산 중...")

        for i, m in enumerate(phone_models.keys()):
            base_spec = phone_models[m]
            top_memory = max(base_spec["storage_options"].keys())
            baseline_log = get_baseline_prediction(m, top_memory)

            if baseline_log is not None:
                price = price_at_days(baseline_log, ranking_day)
                ranking_data.append({"모델": f"{m} ({top_memory}GB)", "예상가(원)": round(price)})

            progress.progress((i + 1) / len(phone_models), text=f"계산 중... ({i+1}/{len(phone_models)})")

        progress.empty()

        ranking_df = pd.DataFrame(ranking_data).sort_values("예상가(원)", ascending=False).reset_index(drop=True)
        ranking_df.index = ranking_df.index + 1

        st.write(f"**사용기간 {ranking_day}일 기준, 예상가 높은 순 랭킹**")
        st.dataframe(ranking_df, use_container_width=True)

        st.caption(
            "※ 이 랭킹은 각 모델의 최대 저장용량 기준이며, 감가 속도는 전 모델 동일 곡선을 적용했으므로 "
            "순위는 사실상 '신품가 자체의 순위'와 거의 동일하게 나타납니다. "
            "이는 감가 속도의 브랜드별 차이를 반영하지 못한 현재 모델의 한계입니다."
        )