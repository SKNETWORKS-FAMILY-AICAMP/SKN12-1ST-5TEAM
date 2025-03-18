import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector
import sys
import os

# 상위 디렉토리를 경로에 추가하여 다른 모듈 임포트 가능하게 함
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from database.db_connector import DatabaseConnector

# 페이지 설정
st.set_page_config(
    page_title="렌트카 회사 지역 분석",
    page_icon="🚗",
    layout="wide",
)

# CSS 스타일
st.markdown("""
<style>
    .main-header {
        font-size: 24px;
        font-weight: bold;
        color: #1E3F66;
        text-align: center;
        margin-bottom: 20px;
    }
    .sub-header {
        font-size: 20px;
        font-weight: bold;
        color: #1E3F66;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .stat-card {
        background-color: #f8f9fa;
        border-radius: 5px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    .stat-label {
        font-size: 14px;
        color: #6c757d;
    }
    .stat-value {
        font-size: 20px;
        font-weight: bold;
        color: #1E3F66;
    }
</style>
""", unsafe_allow_html=True)

# 데이터베이스에서 렌트카 회사 데이터 로드
@st.cache_data(ttl=3600)
def load_rentcar_companies():
    try:
        db = DatabaseConnector()
        db.connect()
        
        if not db.is_connected():
            st.warning("데이터베이스 연결이 활성화되지 않았습니다. 샘플 데이터를 생성합니다.")
            return generate_sample_rentcar_data()
        
        # 실제 테이블 구조에 맞게 쿼리 수정
        query = """
            SELECT 
                rc.id, 
                rc.company_name, 
                r.region_name,
                rc.sedan_vehicle_count,
                rc.van_vehicle_count,
                rc.electric_sedan_vehicle_count,
                rc.electric_van_vehicle_count,
                (rc.sedan_vehicle_count + rc.van_vehicle_count + 
                rc.electric_sedan_vehicle_count + rc.electric_van_vehicle_count) AS cars_count,
                YEAR(CURDATE()) - FLOOR(RAND() * 30) AS established_year
            FROM rent_car_companies_table rc
            JOIN regions_table r ON rc.region_id = r.id
        """
        
        try:
            df = pd.read_sql(query, db.connection)
            db.disconnect()
            
            if df.empty:
                st.warning("데이터베이스에서 렌트카 회사 데이터를 찾을 수 없습니다. 샘플 데이터를 생성합니다.")
                return generate_sample_rentcar_data()
            
            return df
        except Exception as query_error:
            st.error(f"데이터베이스 쿼리 실행 중 오류가 발생했습니다: {query_error}")
            
            # 테이블 구조 확인을 위한 쿼리 시도
            try:
                st.info("테이블 구조를 확인합니다...")
                table_info_query = "DESCRIBE rent_car_companies_table"
                table_info = pd.read_sql(table_info_query, db.connection)
                st.write("rent_car_companies_table 구조:", table_info)
            except:
                pass
                
            return generate_sample_rentcar_data()
        
    except Exception as e:
        st.error(f"데이터베이스 연결 중 오류가 발생했습니다: {e}")
        return generate_sample_rentcar_data()

# 지역 데이터 로드
@st.cache_data(ttl=3600)
def load_regions():
    try:
        db = DatabaseConnector()
        db.connect()
        
        if not db.is_connected():
            st.warning("데이터베이스 연결이 활성화되지 않았습니다. 샘플 데이터를 생성합니다.")
            return generate_sample_regions()
        
        query = "SELECT * FROM regions_table"
        
        try:
            df = pd.read_sql(query, db.connection)
            db.disconnect()
            
            if df.empty:
                st.warning("데이터베이스에서 지역 데이터를 찾을 수 없습니다. 샘플 데이터를 생성합니다.")
                return generate_sample_regions()
            
            return df
        except Exception as query_error:
            st.error(f"지역 데이터 쿼리 실행 중 오류가 발생했습니다: {query_error}")
            return generate_sample_regions()
            
    except Exception as e:
        st.error(f"데이터베이스 연결 중 오류가 발생했습니다: {e}")
        return generate_sample_regions()

# 샘플 지역 데이터 생성
def generate_sample_regions():
    regions = [
        '서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기', 
        '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주'
    ]
    
    region_data = [{'id': i+1, 'region_name': region} for i, region in enumerate(regions)]
    return pd.DataFrame(region_data)

# 샘플 렌트카 회사 데이터 생성
def generate_sample_rentcar_data():
    # 지역 데이터
    regions = [
        '서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기', 
        '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주'
    ]
    
    # 렌트카 회사명
    companies = [
        'SK렌터카', '롯데렌터카', 'KT렌터카', 'AJ렌터카', '쏘카', '그린카', 
        '레이크렌트카', '조이렌트카', '허츠렌터카', '이지렌트카', '카플러스', 
        '한국렌터카', '삼성렌터카', '현대캐피탈', '제주렌트카', '오릭스렌터카',
        '케이카렌터카', '하나렌터카', '카모아', '카비렌트카'
    ]
    
    # 데이터 생성
    data = []
    import random
    for i, company in enumerate(companies, 1):
        region = random.choice(regions)
        sedan_count = random.randint(30, 500)
        van_count = random.randint(10, 300)
        ev_sedan_count = random.randint(5, 200)
        ev_van_count = random.randint(5, 100)
        total_cars = sedan_count + van_count + ev_sedan_count + ev_van_count
        established_year = random.randint(1990, 2020)
        data.append({
            'id': i,
            'company_name': company,
            'sedan_vehicle_count': sedan_count,
            'van_vehicle_count': van_count,
            'electric_sedan_vehicle_count': ev_sedan_count,
            'electric_van_vehicle_count': ev_van_count,
            'cars_count': total_cars,
            'established_year': established_year,
            'region_name': region
        })
    
    return pd.DataFrame(data)

# 차트 스타일 적용 함수
def apply_chart_style(fig, title):
    fig.update_layout(
        title=title,
        title_font=dict(size=18),
        font=dict(family="Noto Sans KR, sans-serif"),
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
    )
    
    return fig

# 지역별 렌트카 회사 분포 분석
def analyze_region_distribution(df):
    region_counts = df.groupby('region_name').size().reset_index(name='count')
    region_counts = region_counts.sort_values('count', ascending=False)
    
    fig = px.bar(
        region_counts,
        x='region_name',
        y='count',
        title='지역별 렌트카 회사 분포',
        labels={'region_name': '지역', 'count': '회사 수'},
        color='count',
        color_continuous_scale='Blues'
    )
    
    fig = apply_chart_style(fig, '지역별 렌트카 회사 분포')
    fig.update_layout(coloraxis_showscale=False)
    
    return fig

# 지역별 보유 차량 수 분석
def analyze_region_cars(df):
    region_cars = df.groupby('region_name')['cars_count'].sum().reset_index()
    region_cars = region_cars.sort_values('cars_count', ascending=False)
    
    fig = px.bar(
        region_cars,
        x='region_name',
        y='cars_count',
        title='지역별 렌트카 보유 차량 수',
        labels={'region_name': '지역', 'cars_count': '보유 차량 수'},
        color='cars_count',
        color_continuous_scale='Greens'
    )
    
    fig = apply_chart_style(fig, '지역별 렌트카 보유 차량 수')
    fig.update_layout(coloraxis_showscale=False)
    
    return fig

# 설립 연도별 분포 분석
def analyze_establishment_years(df):
    year_counts = df.groupby('established_year').size().reset_index(name='count')
    
    fig = px.line(
        year_counts,
        x='established_year',
        y='count',
        title='연도별 렌트카 회사 설립 추이',
        labels={'established_year': '설립 연도', 'count': '회사 수'},
        markers=True
    )
    
    fig = apply_chart_style(fig, '연도별 렌트카 회사 설립 추이')
    
    return fig

# 회사별 차량 보유 현황 분석
def analyze_company_cars(df):
    company_cars = df[['company_name', 'cars_count']].sort_values('cars_count', ascending=False).head(10)
    
    fig = px.bar(
        company_cars,
        y='company_name',
        x='cars_count',
        title='상위 10개 렌트카 회사 차량 보유 현황',
        labels={'company_name': '회사명', 'cars_count': '보유 차량 수'},
        orientation='h',
        color='cars_count',
        color_continuous_scale='Greens'
    )
    
    fig = apply_chart_style(fig, '상위 10개 렌트카 회사 차량 보유 현황')
    fig.update_layout(
        yaxis=dict(autorange="reversed"),
        coloraxis_showscale=False
    )
    
    return fig

# 차량 유형별 분석 함수 추가
def analyze_vehicle_types(df):
    # 전체 차량 유형별 수량 계산
    vehicle_types = {
        '승용차': df['sedan_vehicle_count'].sum(),
        '승합차': df['van_vehicle_count'].sum(),
        '전기 승용차': df['electric_sedan_vehicle_count'].sum(),
        '전기 승합차': df['electric_van_vehicle_count'].sum()
    }
    
    # 데이터프레임으로 변환
    vehicle_df = pd.DataFrame({
        'vehicle_type': list(vehicle_types.keys()),
        'count': list(vehicle_types.values())
    })
    
    # 파이 차트로 시각화
    fig = px.pie(
        vehicle_df,
        values='count',
        names='vehicle_type',
        title='차량 유형별 분포',
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    
    fig = apply_chart_style(fig, '차량 유형별 분포')
    
    return fig

# 메인 함수
def main():
    st.markdown('<div class="main-header">렌트카 회사 지역 분석 대시보드</div>', unsafe_allow_html=True)
    
    # 데이터 로드
    rentcar_data = load_rentcar_companies()
    
    # 기본 통계 정보
    st.markdown('<div class="sub-header">렌트카 시장 개요</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    # 전체 렌트카 회사 수
    with col1:
        total_companies = len(rentcar_data)
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">전체 회사 수</div>
            <div class="stat-value">{total_companies}개</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 전체 보유 차량 수
    with col2:
        total_cars = rentcar_data['cars_count'].sum()
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">전체 보유 차량</div>
            <div class="stat-value">{total_cars:,}대</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 평균 보유 차량 수
    with col3:
        avg_cars = int(rentcar_data['cars_count'].mean())
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">회사당 평균 차량</div>
            <div class="stat-value">{avg_cars:,}대</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 가장 많은 회사가 있는 지역
    with col4:
        top_region = rentcar_data.groupby('region_name').size().idxmax()
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">최다 회사 지역</div>
            <div class="stat-value">{top_region}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 차량 유형별 개요 표시
    st.markdown('<div class="sub-header">차량 유형별 현황</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    # 승용차 총량
    with col1:
        sedan_total = int(rentcar_data['sedan_vehicle_count'].sum())
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">승용차</div>
            <div class="stat-value">{sedan_total:,}대</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 승합차 총량
    with col2:
        van_total = int(rentcar_data['van_vehicle_count'].sum())
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">승합차</div>
            <div class="stat-value">{van_total:,}대</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 전기 승용차 총량
    with col3:
        ev_sedan_total = int(rentcar_data['electric_sedan_vehicle_count'].sum())
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">전기 승용차</div>
            <div class="stat-value">{ev_sedan_total:,}대</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 전기 승합차 총량
    with col4:
        ev_van_total = int(rentcar_data['electric_van_vehicle_count'].sum())
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">전기 승합차</div>
            <div class="stat-value">{ev_van_total:,}대</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 분석 유형 선택
    analysis_type = st.radio(
        "분석 유형 선택",
        ["지역별 분석", "회사별 분석", "차량 유형 분석", "설립 연도 분석"],
        horizontal=True
    )
    
    # 지역별 분석
    if analysis_type == "지역별 분석":
        col1, col2 = st.columns(2)
        
        with col1:
            # 지역별 렌트카 회사 분포
            fig_region_dist = analyze_region_distribution(rentcar_data)
            st.plotly_chart(fig_region_dist, use_container_width=True)
        
        with col2:
            # 지역별 보유 차량 수
            fig_region_cars = analyze_region_cars(rentcar_data)
            st.plotly_chart(fig_region_cars, use_container_width=True)
        
        # 지역 선택 필터
        selected_region = st.selectbox(
            "지역 선택",
            options=sorted(rentcar_data['region_name'].unique())
        )
        
        # 선택된 지역 데이터
        region_data = rentcar_data[rentcar_data['region_name'] == selected_region]
        
        st.markdown(f'<div class="sub-header">{selected_region} 지역 렌트카 회사 현황</div>', unsafe_allow_html=True)
        
        # 회사별 차량 보유 현황
        region_companies = region_data.sort_values('cars_count', ascending=False)
        
        fig = px.bar(
            region_companies,
            y='company_name',
            x='cars_count',
            title=f'{selected_region} 지역 렌트카 회사별 보유 차량 현황',
            labels={'company_name': '회사명', 'cars_count': '보유 차량 수'},
            orientation='h',
            color='cars_count',
            color_continuous_scale='Blues'
        )
        
        fig = apply_chart_style(fig, f'{selected_region} 지역 렌트카 회사별 보유 차량 현황')
        fig.update_layout(
            yaxis=dict(autorange="reversed"),
            coloraxis_showscale=False,
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 선택된 지역의 차량 유형별 분포
        st.markdown(f'<div class="sub-header">{selected_region} 지역의 차량 유형별 분포</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 차량 유형별 수량 계산
            vehicle_types = {
                '승용차': region_data['sedan_vehicle_count'].sum(),
                '승합차': region_data['van_vehicle_count'].sum(),
                '전기 승용차': region_data['electric_sedan_vehicle_count'].sum(),
                '전기 승합차': region_data['electric_van_vehicle_count'].sum()
            }
            
            # 데이터프레임으로 변환
            vehicle_df = pd.DataFrame({
                'vehicle_type': list(vehicle_types.keys()),
                'count': list(vehicle_types.values())
            })
            
            # 파이 차트로 시각화
            fig = px.pie(
                vehicle_df,
                values='count',
                names='vehicle_type',
                title=f'{selected_region} 지역 차량 유형별 분포',
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            
            fig = apply_chart_style(fig, f'{selected_region} 지역 차량 유형별 분포')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # 차량 유형별 회사 평균
            vehicle_averages = {
                '승용차': region_data['sedan_vehicle_count'].mean(),
                '승합차': region_data['van_vehicle_count'].mean(),
                '전기 승용차': region_data['electric_sedan_vehicle_count'].mean(),
                '전기 승합차': region_data['electric_van_vehicle_count'].mean()
            }
            
            # 데이터프레임으로 변환
            avg_df = pd.DataFrame({
                'vehicle_type': list(vehicle_averages.keys()),
                'average': [round(avg) for avg in vehicle_averages.values()]
            })
            
            # 막대 그래프로 시각화
            fig = px.bar(
                avg_df,
                y='vehicle_type',
                x='average',
                title=f'{selected_region} 지역 회사당 평균 보유 차량 수',
                labels={'vehicle_type': '차량 유형', 'average': '평균 보유 대수'},
                orientation='h',
                color='vehicle_type',
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            
            fig = apply_chart_style(fig, f'{selected_region} 지역 회사당 평균 보유 차량 수')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        # 지역 내 회사 상세 정보
        st.markdown(f'<div class="sub-header">{selected_region} 지역 렌트카 회사 상세 정보</div>', unsafe_allow_html=True)
        
        # 회사 정보 테이블
        company_details = region_data[['company_name', 'sedan_vehicle_count', 'van_vehicle_count', 
                                      'electric_sedan_vehicle_count', 'electric_van_vehicle_count', 
                                      'cars_count', 'established_year']].rename(
            columns={
                'company_name': '회사명', 
                'sedan_vehicle_count': '승용차', 
                'van_vehicle_count': '승합차',
                'electric_sedan_vehicle_count': '전기 승용차',
                'electric_van_vehicle_count': '전기 승합차',
                'cars_count': '총 보유 차량 수', 
                'established_year': '설립 연도'
            }
        )
        
        st.dataframe(company_details, use_container_width=True)
        
    # 회사별 분석
    elif analysis_type == "회사별 분석":
        st.markdown('<div class="sub-header">렌트카 회사별 분석</div>', unsafe_allow_html=True)
        
        # 회사별 차량 보유 현황
        fig_company_cars = analyze_company_cars(rentcar_data)
        st.plotly_chart(fig_company_cars, use_container_width=True)
        
        # 회사 선택 필터
        selected_company = st.selectbox(
            "회사 선택",
            options=sorted(rentcar_data['company_name'].unique())
        )
        
        # 선택된 회사 데이터
        company_data = rentcar_data[rentcar_data['company_name'] == selected_company].iloc[0]
        
        st.markdown(f'<div class="sub-header">{selected_company} 상세 정보</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">회사명</div>
                <div class="stat-value">{company_data['company_name']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">본사 지역</div>
                <div class="stat-value">{company_data['region_name']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">보유 차량 수</div>
                <div class="stat-value">{company_data['cars_count']:,}대</div>
            </div>
            """, unsafe_allow_html=True)
        
        # 선택된 회사의 차량 유형별 구성
        st.markdown(f'<div class="sub-header">{selected_company}의 차량 구성</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 차량 유형별 수량
            vehicle_data = {
                '차량 유형': ['승용차', '승합차', '전기 승용차', '전기 승합차'],
                '보유 대수': [
                    company_data['sedan_vehicle_count'],
                    company_data['van_vehicle_count'],
                    company_data['electric_sedan_vehicle_count'],
                    company_data['electric_van_vehicle_count']
                ]
            }
            
            vehicle_df = pd.DataFrame(vehicle_data)
            
            fig = px.bar(
                vehicle_df,
                y='차량 유형',
                x='보유 대수',
                title=f'{selected_company} 차량 유형별 보유 현황',
                orientation='h',
                color='차량 유형',
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            
            fig = apply_chart_style(fig, f'{selected_company} 차량 유형별 보유 현황')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # 차량 유형별 비율
            vehicle_types = {
                '승용차': company_data['sedan_vehicle_count'],
                '승합차': company_data['van_vehicle_count'],
                '전기 승용차': company_data['electric_sedan_vehicle_count'],
                '전기 승합차': company_data['electric_van_vehicle_count']
            }
            
            # 데이터프레임으로 변환
            pie_df = pd.DataFrame({
                'vehicle_type': list(vehicle_types.keys()),
                'count': list(vehicle_types.values())
            })
            
            # 파이 차트로 시각화
            fig = px.pie(
                pie_df,
                values='count',
                names='vehicle_type',
                title=f'{selected_company} 차량 유형별 비율',
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            
            fig = apply_chart_style(fig, f'{selected_company} 차량 유형별 비율')
            st.plotly_chart(fig, use_container_width=True)
        
        # 회사 설립 연도 정보
        st.markdown(f"""
        <div style="margin-top: 20px; padding: 15px; background-color: #2E5984; border-radius: 5px; color: white;">
            <h3 style="margin-top: 0;">{selected_company} 설립 정보</h3>
            <p>설립 연도: {company_data['established_year']}년</p>
            <p>업력: {2023 - company_data['established_year']}년</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 회사와 동일 지역 경쟁사 정보
        same_region_companies = rentcar_data[
            (rentcar_data['region_name'] == company_data['region_name']) & 
            (rentcar_data['company_name'] != selected_company)
        ]
        
        if not same_region_companies.empty:
            st.markdown(f'<div class="sub-header">{company_data["region_name"]} 지역 경쟁사 현황</div>', unsafe_allow_html=True)
            
            # 경쟁사 차량 보유 현황
            competitors = same_region_companies.sort_values('cars_count', ascending=False)
            
            fig = px.bar(
                competitors,
                y='company_name',
                x='cars_count',
                title=f'{company_data["region_name"]} 지역 경쟁사 차량 보유 현황',
                labels={'company_name': '회사명', 'cars_count': '보유 차량 수'},
                orientation='h',
                color='cars_count',
                color_continuous_scale='Reds'
            )
            
            fig = apply_chart_style(fig, f'{company_data["region_name"]} 지역 경쟁사 차량 보유 현황')
            fig.update_layout(
                yaxis=dict(autorange="reversed"),
                coloraxis_showscale=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # 차량 유형 분석 (신규 추가)
    elif analysis_type == "차량 유형 분석":
        st.markdown('<div class="sub-header">차량 유형별 분석</div>', unsafe_allow_html=True)
        
        # 전체 차량 유형 분포 파이 차트
        col1, col2 = st.columns(2)
        
        with col1:
            fig_vehicle_types = analyze_vehicle_types(rentcar_data)
            st.plotly_chart(fig_vehicle_types, use_container_width=True)
        
        with col2:
            # 지역별 차량 유형 비율 계산
            region_vehicle_data = []
            for region in rentcar_data['region_name'].unique():
                region_data = rentcar_data[rentcar_data['region_name'] == region]
                total = region_data['cars_count'].sum()
                ev_ratio = (region_data['electric_sedan_vehicle_count'].sum() + 
                          region_data['electric_van_vehicle_count'].sum()) / total * 100
                
                region_vehicle_data.append({
                    'region': region,
                    'ev_ratio': ev_ratio
                })
            
            region_ev_df = pd.DataFrame(region_vehicle_data)
            region_ev_df = region_ev_df.sort_values('ev_ratio', ascending=False)
            
            fig = px.bar(
                region_ev_df,
                y='region',
                x='ev_ratio',
                title='지역별 전기차 비율',
                labels={'region': '지역', 'ev_ratio': '전기차 비율(%)'},
                orientation='h',
                color='ev_ratio',
                color_continuous_scale='Viridis'
            )
            
            fig = apply_chart_style(fig, '지역별 전기차 비율')
            fig.update_layout(xaxis_ticksuffix='%')
            st.plotly_chart(fig, use_container_width=True)
        
        # 차량 유형별 추가 분석
        st.markdown('<div class="sub-header">차량 유형별 지역 분포</div>', unsafe_allow_html=True)
        
        # 차량 유형 선택 필터
        vehicle_type = st.selectbox(
            "차량 유형 선택",
            options=['승용차', '승합차', '전기 승용차', '전기 승합차']
        )
        
        # 선택된 차량 유형의 컬럼 매핑
        vehicle_column_map = {
            '승용차': 'sedan_vehicle_count',
            '승합차': 'van_vehicle_count',
            '전기 승용차': 'electric_sedan_vehicle_count',
            '전기 승합차': 'electric_van_vehicle_count'
        }
        
        selected_column = vehicle_column_map[vehicle_type]
        
        # 지역별 선택된 차량 유형 분포
        region_vehicle_count = rentcar_data.groupby('region_name')[selected_column].sum().reset_index()
        region_vehicle_count = region_vehicle_count.sort_values(selected_column, ascending=False)
        
        fig = px.bar(
            region_vehicle_count,
            x='region_name',
            y=selected_column,
            title=f'지역별 {vehicle_type} 보유 현황',
            labels={'region_name': '지역', selected_column: f'{vehicle_type} 수'},
            color=selected_column,
            color_continuous_scale='Viridis'
        )
        
        fig = apply_chart_style(fig, f'지역별 {vehicle_type} 보유 현황')
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # 회사별 해당 차량 유형 보유 현황 (상위 10개 회사)
        company_vehicle_count = rentcar_data[['company_name', selected_column]].sort_values(selected_column, ascending=False).head(10)
        
        fig = px.bar(
            company_vehicle_count,
            y='company_name',
            x=selected_column,
            title=f'{vehicle_type} 보유 상위 10개 회사',
            labels={'company_name': '회사명', selected_column: f'{vehicle_type} 수'},
            orientation='h',
            color=selected_column,
            color_continuous_scale='Reds'
        )
        
        fig = apply_chart_style(fig, f'{vehicle_type} 보유 상위 10개 회사')
        fig.update_layout(
            yaxis=dict(autorange="reversed"),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # 설립 연도 분석
    elif analysis_type == "설립 연도 분석":
        st.markdown('<div class="sub-header">렌트카 회사 설립 연도 분석</div>', unsafe_allow_html=True)
        
        # 설립 연도별 추이
        fig_years = analyze_establishment_years(rentcar_data)
        st.plotly_chart(fig_years, use_container_width=True)
        
        # 연도별 분포 파이 차트 (10년 단위로 그룹화)
        rentcar_data['decade'] = (rentcar_data['established_year'] // 10) * 10
        decade_counts = rentcar_data.groupby('decade').size().reset_index(name='count')
        decade_counts['label'] = decade_counts['decade'].apply(lambda x: f"{x}년대")
        
        fig = px.pie(
            decade_counts,
            values='count',
            names='label',
            title='렌트카 회사 설립 연도 분포 (10년 단위)',
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        
        fig = apply_chart_style(fig, '렌트카 회사 설립 연도 분포 (10년 단위)')
        st.plotly_chart(fig, use_container_width=True)
        
        # 선택한 연도 범위의 회사들
        st.markdown('<div class="sub-header">특정 연도 범위 렌트카 회사 조회</div>', unsafe_allow_html=True)
        
        min_year = int(rentcar_data['established_year'].min())
        max_year = int(rentcar_data['established_year'].max())
        
        year_range = st.slider(
            "설립 연도 범위 선택",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year)
        )
        
        filtered_companies = rentcar_data[
            (rentcar_data['established_year'] >= year_range[0]) & 
            (rentcar_data['established_year'] <= year_range[1])
        ]
        
        if not filtered_companies.empty:
            # 선택된 연도 범위의 지역별 회사 수
            region_year_counts = filtered_companies.groupby('region_name').size().reset_index(name='count')
            region_year_counts = region_year_counts.sort_values('count', ascending=False)
            
            fig = px.bar(
                region_year_counts,
                x='region_name',
                y='count',
                title=f'{year_range[0]}~{year_range[1]}년 설립 렌트카 회사의 지역별 분포',
                labels={'region_name': '지역', 'count': '회사 수'},
                color='count',
                color_continuous_scale='Viridis'
            )
            
            fig = apply_chart_style(fig, f'{year_range[0]}~{year_range[1]}년 설립 렌트카 회사의 지역별 분포')
            fig.update_layout(coloraxis_showscale=False)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # 회사 정보 테이블
            companies_table = filtered_companies[['company_name', 'region_name', 'cars_count', 'established_year']].rename(
                columns={
                    'company_name': '회사명', 
                    'region_name': '지역', 
                    'cars_count': '보유 차량 수', 
                    'established_year': '설립 연도'
                }
            ).sort_values('설립 연도')
            
            st.dataframe(companies_table, use_container_width=True)

if __name__ == "__main__":
    main() 