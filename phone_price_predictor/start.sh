#!/usr/bin/env bash
# FastAPI는 컨테이너 내부 전용(127.0.0.1)으로 띄운다
uvicorn server:app --host 127.0.0.1 --port 8000 &

# Streamlit(화면 진입점: 홈.py)만 외부로 노출
streamlit run 홈.py \
  --server.port "${PORT:-7860}" \
  --server.address 0.0.0.0