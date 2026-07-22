"""
중고폰 가격 예측 FastAPI 서버

[전체 구조]
Streamlit(각 페이지) → 이 서버의 /predict 엔드포인트 → 예측 결과 반환

[핵심 로직]
1. 브랜드(Apple/Samsung)에 따라 서로 다른 회귀 모델을 사용
   (Day3 실험 결과: 두 브랜드를 통합 학습했을 때보다, 분리 학습했을 때
    R²가 각각 개선됨을 확인 → Apple 전용, Samsung 전용 모델 두 개로 분리)
2. 회귀 모델은 등급(condition)을 "B(일반 사용감)"로 고정한 채 예측하여,
   브랜드/스펙/신품가 기반의 "기준가"만 산출
3. 실제 등급(S/A/B/F) 반영은 모델이 아니라, 실제 중고폰 시장 벤치마크
   기준의 배율(GRADE_MULTIPLIER)을 곱해서 후처리로 반영
   (회귀 모델이 등급을 안정적으로 학습하지 못하는 한계를 발견하여
    이렇게 역할을 분리함 — 자세한 배경은 README 참고)
"""

from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI()

# ── 브랜드별로 분리 학습된 모델과 컬럼 목록 로드 ──────────────
apple_model = joblib.load("apple_price_model.joblib")
apple_columns = joblib.load("apple_model_columns.joblib")

samsung_model = joblib.load("samsung_price_model.joblib")
samsung_columns = joblib.load("samsung_model_columns.joblib")

# ── 등급별 보정 배율 (A급을 기준 1.00으로 삼은 실제 중고폰 시장 벤치마크) ──
# 크롤링 데이터(781건)만으로 계산한 등급별 비율은 표본 부족(특히 F등급 6건)으로
# 신뢰도가 낮아, 실제 중고폰 시장에서 통용되는 벤치마크 수치로 대체함
GRADE_MULTIPLIER = {
    "S": 1.10,   # 미개봉/무잔상급 (A급보다 5~15% 높음)
    "A": 1.00,   # 상태 좋음 (기준)
    "B": 0.85,   # 일반 사용감 (10~20% 감가)
    "F": 0.20,   # 파손/고장/부품용 (70~90% 감가)
}


class PhoneInput(BaseModel):
    brand: str          # "Apple" 또는 "Samsung"
    condition: str       # "S", "A", "B", "F"
    screen_size: float
    ram: float
    battery: float
    weight: float
    release_year: int
    storage_gb: int
    new_price: int        # 해당 모델·용량의 실제 신품 출고가(원)


@app.get("/")
def read_root():
    return {"message": "중고폰 가격 예측 API (브랜드별 모델 + 등급 벤치마크 보정) 작동 중입니다"}


@app.post("/predict")
def predict_price(data: PhoneInput):
    # ── 1. 브랜드에 따라 모델 분기 ──────────────────────────
    if data.brand == "Apple":
        model = apple_model
        columns = apple_columns
    elif data.brand == "Samsung":
        model = samsung_model
        columns = samsung_columns
    else:
        return {"error": "지원하지 않는 브랜드입니다. Apple 또는 Samsung만 가능합니다."}

    # ── 2. 모델 예측 시 condition은 항상 "B"(기준 등급)로 고정 ──
    # 실제 사용자가 고른 등급은 이 예측에 반영하지 않고,
    # 아래 3번 단계에서 배율로만 반영함 (모델의 등급 불안정 문제 회피)
    input_dict = {
        "screen_size": data.screen_size,
        "ram": data.ram,
        "battery": data.battery,
        "weight": data.weight,
        "release_year": data.release_year,
        "storage_gb": data.storage_gb,
        "new_price": data.new_price,
        "condition_B": 1,
    }

    input_df = pd.DataFrame([input_dict])
    input_df = input_df.reindex(columns=columns, fill_value=0)  # 학습 시 컬럼 순서와 동일하게 맞춤

    base_prediction = model.predict(input_df)[0]  # "B등급 기준" 스펙 기반 예측가

    # ── 3. 실제 등급을 반영한 최종 가격 계산 ──────────────────
    # B등급 대비 상대 배율을 곱해서, 실제 요청된 등급(S/A/B/F)의 가격을 산출
    ratio = GRADE_MULTIPLIER.get(data.condition, 1.0) / GRADE_MULTIPLIER["B"]
    final_prediction = base_prediction * ratio

    return {"predicted_price": round(float(final_prediction))}