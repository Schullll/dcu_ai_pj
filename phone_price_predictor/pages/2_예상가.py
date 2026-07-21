"""
============================================================
📱 예상가 - 중고폰/태블릿 적정가 예측기 (Streamlit UI)
============================================================

[전체 구조]
Streamlit(이 파일) → FastAPI(server.py) → 학습된 회귀모델(price_model.joblib)
                                              ↓
                              스펙 기반 "기준가" 예측 (사용기간은 평균으로 고정)
                                              ↓
                    실측 데이터 기반 사용기간 감가 보정 (아래 개발 히스토리 참고)


[개발 히스토리 — 시행착오 및 개선 과정]

1. [저장용량 문제]
   - 초기: 저장용량을 바꿔도 예측가가 거의 안 변함
   - 원인: normalized_new_price(피처 중요도 58%, 가장 중요한 변수)가
           저장용량과 무관하게 고정값으로 들어가고 있었음
   - 해결: phone_models.py에서 모델별 · 저장용량별로 실제 신품 출고가를
           따로 매핑(storage_options 딕셔너리)하여 해결

2. [저장용량별 가격 계산 오류]
   - 초기: normalized_new_price(로그 스케일 값)에 배율을 곱해서 보정하려 함
   - 원인: 로그 스케일 값은 곱셈이 아니라 "덧셈"으로 보정해야 함
           (곱셈 시 지수적으로 값이 폭발함)
   - 해결: 아이폰X 실제 출고가(64GB 142만원 vs 256GB 163만원)를 검증 근거로,
           20개 모델 전부 실제 출고가를 검색 확인 후 ln(USD 환산가)로 재계산

3. [사용기간(days_used) 반영 문제 — 가장 많은 시행착오]
   3-1. 사용기간을 늘려도 모델 예측가가 불규칙하게 오르내림
        → 원인: days_used의 피처 중요도가 2.1%로 낮아 모델이 안정적
                 관계를 학습하지 못함
   3-2. 후처리로 "연 12% 감가율"을 임의로 적용 → 그래도 순서 뒤바뀜
        → 원인: 모델 예측값 자체에 이미 days_used가 반영되어 있어
                 후처리 보정과 이중으로 충�돌
   3-3. 모델 예측 시 days_used=0으로 고정 시도
        → 원인: 데이터셋의 실제 사용일수 범위는 91~1094일이라
                 0은 학습 범위 밖(외삽) → 비현실적으로 낮은 값 발생
   3-4. days_used를 데이터 평균(674일)로 변경
        → 그래도 신품가 대비 과도한 감가(약 83%↓) 문제 발견
   3-5. 실제 데이터의 "중고가/신품가 비율"을 검증
        → 최초 시도(단순 나눗셈)는 로그 스케일값을 그대로 나눠 오류
        → exp(로그차이)로 올바르게 재계산 (real_retention_ratio)
   3-6. 모델 예측값 기반으로 사용기간별 평균을 내려 했으나 여전히 불안정
        → 근본 원인 발견: 이 데이터셋은 "동일 기기의 시간 흐름 추적"이
          아니라 "서로 다른 거래 건들의 독립적 스냅샷"이라, 모델이
          감가 패턴을 학습할 재료 자체가 부족함
        → 결론: 모델의 days_used 학습 결과는 신뢰하지 않기로 결정
   3-7. 실측 데이터(Apple/Samsung/LG, 591건)를 200일 단위로 구간화
        → 0~200일(19건) vs 200~400일(76건) 구간에서 논리적 역전 발생
          (사용기간이 짧은데 오히려 유지율이 더 낮게 나옴)
        → 원인: 0~200일 구간 표본이 19건뿐이라 통계적으로 불안정
        → 해결: 두 구간을 병합(0~400일, 95건)하여 표본 확보 후 재계산
                → 5개 구간 모두 역전 없이 순감소하는 패턴 확인
   3-8. 5개 구간을 계단식으로 그대로 쓰면 100일 단위로는 예측가가
        같은 값에 머무는 구간이 생겨 "예측 모델"로서 부자연스러움
        → 해결: 5개 구간의 대표값에 지수감가곡선(y = a*exp(-b*x))을
                scipy.curve_fit으로 피팅하여, 임의의 사용일수 입력에도
                매끄럽게 우하향하는 곡선을 얻음 (전 구간 오차 1%p 내외)

4. [개념적 혼동 정리]
   - 이 프로젝트는 데이터 "분석"이 아니라 모델을 학습해 웹으로 서빙하는
     "구현" 프로젝트임
   - "예상가"는 미래 시세 예측(시계열)이 아니라, 데이터에 없는 스펙 조합의
     가격을 회귀 모델로 "추정"하는 것 (데이터에 시간 흐름 추적 정보가 없어
     시계열 예측 자체가 불가능함)
   - 본 예측은 "현재 실시간 시세"가 아니라 "2013~2020년 데이터에 나타난
     상대적 가격 패턴을 오늘 환율로 환산해본 참고용 추정치"임
   - "사기 위험도"라는 표현은 AI 판정처럼 오인될 수 있어 사용하지 않고,
     "예측가 대비 격차 %"로 순화하여 표현함
============================================================
"""

import streamlit as st
import requests
import numpy as np
from phone_models import phone_models

st.set_page_config(page_title="예상가", page_icon="📱")

# ── 상수 정의 ──────────────────────────────────────────────
EXCHANGE_RATE = 1479.26  # 2026-07-21 기준 USD/KRW 환율 (고정값, 실시간 아님)

BASELINE_DAYS_USED = 674  # 데이터셋 실제 평균 사용일수. FastAPI 예측 시
                          # 이 값으로 고정해 "스펙 기준 기준가"만 신뢰하고,
                          # 실제 사용기간 반영은 아래 감가곡선이 전담함

# 실측 데이터(Apple/Samsung/LG, 591건) 기반 사용기간별 평균 가격유지율에
# 지수감가곡선(y = a * exp(-b * x))을 scipy.curve_fit으로 피팅한 결과
# (검증: 200/500/700/900/1100일 실측값과 오차 1%p 내외로 일치)
RETENTION_A = 0.4562
RETENTION_B = 0.000267


def get_retention_ratio(days_used: int) -> float:
    """
    사용기간(일)을 받아 실측 데이터 기반 가격유지율(0~1)을 반환.
    데이터셋의 실제 관측 범위(91~1094일)를 크게 벗어나는 값은
    곡선이 비정상적으로 튀지 않도록 0~1300일 사이로 제한(clamp)함.
    """
    days_used_clamped = max(min(days_used, 1300), 0)
    return RETENTION_A * np.exp(-RETENTION_B * days_used_clamped)


BASELINE_RETENTION = get_retention_ratio(BASELINE_DAYS_USED)  # 674일 기준 유지율


# ── 화면 구성 ──────────────────────────────────────────────
st.title("📱 예상가")
st.write("모델을 선택하고 저장용량·사용기간을 입력하면, 학습된 모델이 적정 예상가를 추정해드려요.")

st.subheader("조건 입력")

# 1. 모델명 선택 (20개 모델, 실제 확인된 출고가 기반 매핑표)
model_name = st.selectbox("모델 선택", list(phone_models.keys()))
base_spec = phone_models[model_name]

# 2. 저장용량 — 모델별로 실제 출시됐던 용량만 표시
#    (예: 갤럭시S7에 512GB 옵션이 뜨는 등의 비현실적 조합 방지)
storage_options = base_spec["storage_options"]
memory_list = list(storage_options.keys())
internal_memory = st.selectbox("저장용량 (GB)", memory_list)
selected_new_price = storage_options[internal_memory]  # 선택 용량의 실제 신품가(ln 변환값)

# 3. 사용 기간 (일) — 데이터셋 실제 범위(91~1094일) 안내
days_used = st.number_input(
    "사용 기간 (일)", min_value=0, max_value=2000, value=300,
    help="사용 기간이 길수록 배터리 효율 등 전반적인 상태가 낮게 반영됩니다. "
         "(참고: 학습 데이터의 실제 사용기간 범위는 91~1094일입니다)"
)

st.divider()
with st.expander("자동으로 채워진 스펙 정보 보기"):
    display_spec = {k: v for k, v in base_spec.items() if k != "storage_options"}
    display_spec["선택한 저장용량(GB)"] = internal_memory
    display_spec["해당 용량 신품가(로그값)"] = round(selected_new_price, 3)
    st.json(display_spec)

st.divider()

# ── 예측 실행 ──────────────────────────────────────────────
if st.button("💰 예상가 확인하기", type="primary"):

    # FastAPI 요청 시 days_used는 데이터 평균(674일)로 고정.
    # → 회귀 모델은 브랜드·용량·배터리 등 "스펙"의 영향만 담당하고,
    #   사용기간의 영향은 아래 실측 감가곡선이 전담하는 역할 분리 구조.
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
            baseline_prediction_log = result["predicted_used_price"]  # 로그 스케일 기준가

            # 실제 사용자가 입력한 사용기간에 맞는 유지율을,
            # 674일(기준) 유지율 대비 상대 배율로 환산해 적용
            user_retention = get_retention_ratio(days_used)
            adjustment_factor = user_retention / BASELINE_RETENTION

            estimated_usd = np.exp(baseline_prediction_log) * adjustment_factor
            estimated_krw = estimated_usd * EXCHANGE_RATE

            st.success(f"### 예상 중고가: 약 **{estimated_krw:,.0f}원**")

            st.caption(
                f"모델 기준가(로그, 사용기간 {BASELINE_DAYS_USED}일 기준): {baseline_prediction_log:.3f} → "
                f"실측 사용기간 보정 배율 {adjustment_factor:.2f} 적용 → "
                f"USD 환산 후 2026년 7월 21일 기준 고정 환율(1,479.26원/달러)로 원화 환산."
            )
            st.caption(
                "※ 스펙(브랜드·용량·배터리 등)은 회귀 모델의 예측을 반영했으며, "
                "사용기간에 따른 가격 변화는 회귀 모델이 안정적으로 학습하지 못해 "
                "실제 Apple/Samsung/LG 거래 데이터(591건)에서 집계·곡선피팅한 "
                "사용기간별 평균 가격유지율로 대체 적용했습니다."
            )
            st.caption(
                "※ 본 예측은 2013~2020년 수집된 데이터를 기반으로 하며, "
                "현재 시점의 실시간 시세와는 차이가 있을 수 있습니다."
            )
        else:
            st.error(f"예측 실패 (상태 코드: {response.status_code})")
            st.json(response.json())

    except requests.exceptions.ConnectionError:
        st.error(
            "⚠️ FastAPI 서버에 연결할 수 없습니다. "
            "서버가 켜져 있는지 확인해주세요. (uvicorn server:app --reload)"
        )