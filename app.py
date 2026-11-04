import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정 및 레이아웃
st.set_page_config(
    page_title="Supermarket Sales 실시간 분석 대시보드",
    page_icon="📈",
    layout="wide"
)

# 데이터 로드 및 전처리 캐싱
@st.cache_data
def load_data():
    # Sales.xlsx의 supermarket_sales_test 시트에서 데이터 로드
    df = pd.read_excel("Sales.xlsx", sheet_name="supermarket_sales_test")
    # 결측치 즉시 제거
    df = df.dropna()
    return df

try:
    df = load_data()

    # 사이드바 스타일 및 지점 필터링
    st.sidebar.markdown("### 🛠️ 대시보드 컨트롤 타워")
    st.sidebar.info("원하는 지점을 선택하면 실시간으로 해당 지점의 데이터가 집계 및 분석됩니다.")
    
    branches = sorted(df["Branch"].unique())
    selected_branch = st.sidebar.selectbox("📍 분석 대상 지점 선택", branches, index=0)
    
    # 데이터 필터링
    filtered_df = df[df["Branch"] == selected_branch]

    # 메인 페이지 타이틀 및 메타 정보
    st.title("✨ Supermarket Sales 실시간 분석 대시보드")
    st.subheader(f"🏢 {selected_branch} 지점 핵심 성과 모니터링")
    st.markdown("""
    본 대시보드는 수집된 마트 매출 및 평점 데이터를 실시간으로 시각화하여 지점별 운영 효율성을 돕기 위해 설계되었습니다.  
    *데이터 소스: Sales.xlsx (supermarket_sales_test 시트)*
    """)
    st.markdown("<hr style='margin-top:0rem;margin-bottom:1.5rem;' />", unsafe_allow_html=True)

    # 핵심 Metric 3개 배치
    st.markdown("### 📊 핵심 운영 지표 (Key Metrics)")
    total_sales = filtered_df["Total"].sum()
    avg_sales = filtered_df["Total"].mean()
    avg_rating = filtered_df["Rating"].mean()

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div style='background-color:#F0F2F6;padding:15px;border-radius:10px;'>", unsafe_allow_html=True)
        st.metric(
            label="💰 누적 총 매출액 (Total Revenue)",
            value=f"${total_sales:,.2f}",
            delta=f"{len(filtered_df)}건 판매 완료"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div style='background-color:#F0F2F6;padding:15px;border-radius:10px;'>", unsafe_allow_html=True)
        st.metric(
            label="🛒 거래당 평균 매출 (Average Transaction)",
            value=f"${avg_sales:,.2f}"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col3:
        st.markdown("<div style='background-color:#F0F2F6;padding:15px;border-radius:10px;'>", unsafe_allow_html=True)
        st.metric(
            label="⭐ 고객 만족도 평균 평점 (Average Rating)",
            value=f"{avg_rating:.2f} / 10.0"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown("---")

    # 상품군별 평균 매출 막대그래프 영역
    st.markdown("### 🛍️ 상품 카테고리(Product line)별 매출 기여도")
    st.markdown("각 상품군 카테고리별 평균 판매 실적을 파악하여 주요 매출 드라이버를 확인할 수 있습니다.")

    # 그룹화 및 평균 계산
    category_avg = filtered_df.groupby("Product line")["Total"].mean().reset_index()
    category_avg = category_avg.sort_values(by="Total", ascending=False)

    # Plotly 시각화
    fig = px.bar(
        category_avg,
        x="Product line",
        y="Total",
        text="Total",
        labels={"Total": "평균 매출액 ($)", "Product line": "상품군 카테고리"},
        color="Total",
        color_continuous_scale=px.colors.sequential.Agsunset
    )

    # 그래프 레이아웃 커스텀 데코레이션
    fig.update_traces(
        texttemplate='${text:,.2f}', 
        textposition='outside',
        marker_line_color='rgb(8,48,107)',
        marker_line_width=1.5,
        opacity=0.85
    )
    
    fig.update_layout(
        xaxis_tickangle=-25,
        showlegend=False,
        margin=dict(t=30, b=40, l=40, r=40),
        height=550,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig, use_container_width=True)

except FileNotFoundError:
    st.error("❌ [오류] 'Sales.xlsx' 파일을 찾을 수 없습니다. 현재 작업 공간에 파일을 올바르게 업로드하였는지 확인해주세요.")
except Exception as e:
    st.error(f"❌ [에러 세부사항] {e}")
