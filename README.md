# 2026 인공지능 부트캠프 프로젝트
## 주제 : 중고폰/태블릿 적정가 예측
### [설명]
중고폰/태블릿의 조건(브랜드, 저장용량, 배터리, 사용기간, 신품가)을 입력하면, Scikit-learn 회귀 모델이 실제 공개 데이터셋(Kaggle)으로 학습한 패턴을 바탕으로 예측 중고가를 산출합니다. 예측가 대비 사용자가 확인한 실제 판매가의 격차를 계산해 보여주고, LLM이 이 격차를 바탕으로 거래 시 확인할 체크리스트를 생성합니다.

### [사용 기술 & 데이터]
- 언어: Python 3.14.6
- ML 모델: Scikit-learn (RandomForestRegressor)
- 백엔드: FastAPI
- 프론트엔드: Streamlit
- LLM: OpenAI API (또는 학교 제공 API) — 거래 체크리스트 생성용
- 버전 관리: Git / GitHub
- 출처: Kaggle - Used Phones & Tablets Pricing Dataset
  (https://www.kaggle.com/datasets/ahsan81/used-handheld-device-data)


### [개발 일정]
7.20 - Kaggle 데이터셋 다운로드, 컬럼 분석/전처리, RandomForestRegressor 베이스라인 학습
7.21 - 피처 엔지니어링으로 모델 성능 개선 + FastAPI /predict 엔드포인트 구현
7.22 - Streamlit UI 연동 (조건 5개 입력 → 예측가 + 격차 출력)
7.23 - 에러 처리 + LLM 체크리스트 생성 기능 추가 + GitHub 정리
7.24 - 발표 자료 준비 및 리허설