import streamlit as st
import requests
import pandas as pd
import altair as alt
from phone_models import phone_models

st.set_page_config(page_title="모델별 시세", page_icon="📊")

st.title("📊 모델별 현재 시세")
st.write("모델을 선택하면 스펙과 신품가, 등급별 예상 시세를 확인할 수 있어요.")

model_name = st.selectbox("모델 선택", list(phone_models.keys()))
base_spec = phone_models[model_name]

storage_options = base_spec["storage_options"]
memory_list = list(storage_options.keys())
storage_gb = st.selectbox("저장용량 (GB)", memory_list)
new_price = storage_options[storage_gb]

st.subheader(f"{model_name} · {storage_gb}GB 스펙 정보")
display_spec = {k: v for k, v in base_spec.items() if k != "storage_options"}
display_spec["선택한 저장용량(GB)"] = storage_gb
display_spec["신품가(원)"] = f"{new_price:,}원"
st.json(display_spec)

st.divider()
st.subheader("📈 등급별 예상 시세")

if st.button("시세 확인하기", type="primary"):
    conditions = ["S", "A", "B", "F"]
    condition_labels = {
        "S": "S (미개봉/무잔상급)",
        "A": "A (상태 좋음)",
        "B": "B (일반 사용감)",
        "F": "F (파손/고장/부품용)"
    }
    # 등급별 고정 색상 (좋은 상태=초록계열 → 나쁜 상태=빨강계열로 직관적 표현)
    condition_colors = {
        "S": "#2ecc71",
        "A": "#3498db",
        "B": "#f39c12",
        "F": "#e74c3c"
    }

    results = []
    for cond in conditions:
        input_data = {
            "brand": base_spec["device_brand"],
            "condition": cond,
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
                predicted = response.json()["predicted_price"]
                results.append({
                    "등급": condition_labels[cond],
                    "등급코드": cond,
                    "예상가": predicted
                })
        except requests.exceptions.ConnectionError:
            st.error("⚠️ FastAPI 서버에 연결할 수 없습니다.")
            break

    if results:
        chart_df = pd.DataFrame(results)

        # 가로 막대그래프: y축에 등급, x축에 금액 → 막대 끝에 정확한 금액 라벨 표시
        bars = (
            alt.Chart(chart_df)
            .mark_bar()
            .encode(
                y=alt.Y("등급:N", sort=list(condition_labels.values()), title=None),
                x=alt.X("예상가:Q", title="예상가(원)"),
                color=alt.Color("등급코드:N",
                                 scale=alt.Scale(domain=list(condition_colors.keys()),
                                                  range=list(condition_colors.values())),
                                 legend=None),
                tooltip=["등급", "예상가"]
            )
        )
        # 막대 끝에 금액 텍스트 라벨 추가
        text = bars.mark_text(align="left", dx=5, fontSize=14).encode(
            text=alt.Text("예상가:Q", format=",")
        )

        st.altair_chart((bars + text).properties(height=250), use_container_width=True)

        st.caption(
            "※ 번개장터 실거래 데이터(781건) 기반 회귀 모델 + 실제 중고폰 시장 벤치마크 "
            "기준 등급별 보정(S/A/B/F)을 결합한 예측 결과입니다."
        )