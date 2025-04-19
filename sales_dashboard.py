# sales_dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="판매 실적 대시보드", layout="wide")

st.title("📊 판매 실적 대시보드")

# 1. CSV 업로드
uploaded_file = st.file_uploader("CSV 파일 업로드", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # 숫자형 컬럼 변환
    for col in ["Sales", "Profit", "Discount", "Quantity"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 요약 지표 계산
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    profit_margin = (total_profit / total_sales * 100) if total_sales != 0 else 0

    # KPI 지표
    col1, col2, col3 = st.columns(3)
    col1.metric("총 매출", f"${total_sales:,.2f}")
    col2.metric("총 이익", f"${total_profit:,.2f}")
    col3.metric("이익률", f"{profit_margin:.2f}%")

    st.markdown("---")

    # 1. 카테고리별 매출
    cat_sales = df.groupby("Category")["Sales"].sum().reset_index()
    fig1 = px.bar(cat_sales, x="Category", y="Sales", title="카테고리별 매출", text_auto=".2s")
    st.plotly_chart(fig1, use_container_width=True)

    # 2. 지역별 매출
    region_sales = df.groupby("Region")["Sales"].sum().reset_index()
    fig2 = px.bar(region_sales, x="Region", y="Sales", title="지역별 매출", text_auto=".2s")
    st.plotly_chart(fig2, use_container_width=True)

    # 3. 서브카테고리별 이익 상위 10개
    subcat_profit = df.groupby("Sub-Category")["Profit"].sum().reset_index().sort_values("Profit", ascending=False).head(10)
    fig3 = px.bar(subcat_profit, x="Sub-Category", y="Profit", title="서브카테고리별 이익 Top 10", text_auto=".2s")
    st.plotly_chart(fig3, use_container_width=True)

    # 4. 할인율 vs 이익 산점도
    fig4 = px.scatter(df, x="Discount", y="Profit", size="Sales", color="Category",
                      title="할인율 vs 이익 (Sales 크기 기준)", hover_data=["Product Name"])
    st.plotly_chart(fig4, use_container_width=True)

    # 5. 주(State)별 매출 지도 (미국 기준)
    if "State" in df.columns:
        state_sales = df.groupby("State")["Sales"].sum().reset_index()
        fig5 = px.choropleth(state_sales, locations="State", locationmode="USA-states",
                             color="Sales", scope="usa", title="주(State)별 매출 지도")
        st.plotly_chart(fig5, use_container_width=True)

else:
    st.info("왼쪽 사이드바에서 판매 CSV 파일을 업로드하세요.")
