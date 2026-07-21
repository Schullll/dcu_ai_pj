import streamlit as st

st.set_page_config(page_title="예상가 - 중고폰 가격 예측 서비스", page_icon="📱", layout="wide")

st.title("📱 예상가 — 중고폰 가격 예측 서비스")
st.write("아래 카드를 클릭하거나, 왼쪽 사이드바에서 원하는 기능을 선택하세요.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("📊 모델별 시세")
        st.write("모델을 선택하면 스펙과 신품가, 사용기간별 예상 시세를 그래프로 확인해요.")
        st.page_link("pages/1_모델별_시세.py", label="바로가기 →", icon="📊")

    with st.container(border=True):
        st.subheader("📉 모델 비교 & 랭킹")
        st.write("여러 모델의 예상가를 겹쳐 비교하거나, 시점별 가격 순위를 확인해요.")
        st.page_link("pages/3_모델_비교_랭킹.py", label="바로가기 →", icon="📉")

    with st.container(border=True):
        st.subheader("🔍 거래 평가")
        st.write("예전에 산 폰이 지금 얼마나 값어치가 남았는지 확인해요.")
        st.page_link("pages/5_거래_평가.py", label="바로가기 →", icon="🔍")

with col2:
    with st.container(border=True):
        st.subheader("💰 예상가")
        st.write("모델·저장용량·사용기간을 입력하면 학습된 모델이 적정 예상가를 추정해요.")
        st.page_link("pages/2_예상가.py", label="바로가기 →", icon="💰")

    with st.container(border=True):
        st.subheader("💸 예산 맞춤 추천")
        st.write("예산을 입력하면 그 범위에서 살 수 있는 모델을 추천해요.")
        st.page_link("pages/4_예산_맞춤_추천.py", label="바로가기 →", icon="💸")