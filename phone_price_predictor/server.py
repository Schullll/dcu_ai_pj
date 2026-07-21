from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI()

# 모델과 컬럼 목록 불러오기
model = joblib.load("price_model.joblib")
model_columns = joblib.load("model_columns.joblib")

# 사용자가 보낼 입력 형태 정의
class PhoneInput(BaseModel):
    device_brand: str
    os: str
    screen_size: float
    rear_camera_mp: float
    front_camera_mp: float
    internal_memory: float
    ram: float
    battery: float
    weight: float
    release_year: int
    days_used: int
    normalized_new_price: float
    is_4g: bool
    is_5g: bool

@app.get("/")
def read_root():
    return {"message": "중고폰 가격 예측 API가 작동 중입니다"}

@app.post("/predict")
def predict_price(data: PhoneInput):
    # 입력값을 딕셔너리로 변환
    input_dict = {
        "screen_size": data.screen_size,
        "rear_camera_mp": data.rear_camera_mp,
        "front_camera_mp": data.front_camera_mp,
        "internal_memory": data.internal_memory,
        "ram": data.ram,
        "battery": data.battery,
        "weight": data.weight,
        "release_year": data.release_year,
        "days_used": data.days_used,
        "normalized_new_price": data.normalized_new_price,
        f"device_brand_{data.device_brand}": 1,
        f"os_{data.os}": 1,
        "4g_yes": 1 if data.is_4g else 0,
        "5g_yes": 1 if data.is_5g else 0,
    }

    # 학습 때와 동일한 48개 컬럼 형태로 맞추기 (없는 값은 0으로 채움)
    input_df = pd.DataFrame([input_dict])
    input_df = input_df.reindex(columns=model_columns, fill_value=0)

    # 예측
    prediction = model.predict(input_df)[0]

    return {"predicted_used_price": round(float(prediction), 3)}