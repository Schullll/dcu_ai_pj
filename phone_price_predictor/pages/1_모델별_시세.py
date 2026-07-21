import streamlit as st
import requests
import numpy as np
import pandas as pd
import altair as alt
from phone_models import phone_models

st.set_page_config(page_title="모델별 시세", page_icon="📊")

EXCHANGE_RATE = 1479.26  # 2026-07-21 기준 USD/KRW 환율 (예상가 페이지와 동일 값 사용)
BASELINE_DAYS_USED = 674
RETENTION_A = 0.4562
RETENTION_B = 0.000267


def get_retention_ratio(days_used: int) -> float:
    days_used_clamped = max(min(days_used, 1300), 0)
    return RETENTION_A * np.exp(-RETENTION_B * days_used_clamped)


BASELINE_RETENTION = get_retention_ratio(BASELINE_DAYS_USED)

st.title("📊 모델별 현재 시세")
st.write("모델을 선택하면 스펙과 신품가, 사용기간별 예상 시세를 확인할 수 있어요.")

model_name = st.selectbox("모델 선택", list(phone_models.keys()))
base_spec = phone_models[model_name]

# 저장용량 선택 (예상가 페이지와 동일한 방식)
storage_options = base_spec["storage_options"]
memory_list = list(storage_options.keys())
internal_memory = st.selectbox("저장용량 (GB)", memory_list)
selected_new_price = storage_options[internal_memory]

st.subheader(f"{model_name} · {internal_memory}GB 스펙 정보")
display_spec = {k: v for k, v in base_spec.items() if k != "storage_options"}
display_spec["선택한 저장용량(GB)"] = internal_memory
st.json(display_spec)

st.divider()
st.subheader("📈 사용기간별 예상 시세 추이")

if st.button("그래프 생성하기", type="primary"):
    # FastAPI에 딱 한 번만 요청 (사용기간 고정 674일 → 스펙 기준가만 얻음)
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

    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=input_data, timeout=5)

        if response.status_code == 200:
            result = response.json()
            baseline_prediction_log = result["predicted_used_price"]

            # 91~1094일(데이터셋 실제 범위) 구간을 30일 간격으로 훑으며 그래프용 데이터 생성
            days_range = list(range(91, 1095, 30))
            prices_krw = []

            for d in days_range:
                retention = get_retention_ratio(d)
                factor = retention / BASELINE_RETENTION
                usd = np.exp(baseline_prediction_log) * factor
                krw = usd * EXCHANGE_RATE
                prices_krw.append(krw)

            chart_df = pd.DataFrame({"사용기간(일)": days_range, "예상 중고가(원)": prices_krw})

            # y축 범위를 데이터의 최소~최대값 근처로 좁혀서 하락폭을 더 극적으로 보이게 함
            y_min = min(prices_krw) * 0.9
            y_max = max(prices_krw) * 1.05

            chart = (
                alt.Chart(chart_df)
                .mark_line(point=True, color="#FF4B4B")
                .encode(
                    x=alt.X("사용기간(일):Q", title="사용기간(일)"),
                    y=alt.Y("예상 중고가(원):Q", title="예상 중고가(원)", scale=alt.Scale(domain=[y_min, y_max])),
                    tooltip=["사용기간(일)", "예상 중고가(원)"]
                )
                .properties(height=400)
            )

            st.altair_chart(chart, use_container_width=True)

            # 몇 개 대표 시점 숫자로도 보여주기
            st.subheader("주요 시점별 예상가")
            milestone_days = [91, 200, 400, 674, 1000, 1094]
            cols = st.columns(len(milestone_days))
            for col, d in zip(cols, milestone_days):
                retention = get_retention_ratio(d)
                factor = retention / BASELINE_RETENTION
                usd = np.exp(baseline_prediction_log) * factor
                krw = usd * EXCHANGE_RATE
                col.metric(f"{d}일", f"{krw:,.0f}원")

            st.caption(
                "※ 사용기간에 따른 가격 변화는 실제 Apple/Samsung/LG 거래 데이터(591건) 기반 "
                "감가곡선을 적용한 추정치입니다. 91~1094일은 학습 데이터의 실제 관측 범위입니다."
            )
        else:
            st.error(f"예측 실패 (상태 코드: {response.status_code})")

    except requests.exceptions.ConnectionError:
        st.error("⚠️ FastAPI 서버에 연결할 수 없습니다. 서버가 켜져 있는지 확인해주세요.")