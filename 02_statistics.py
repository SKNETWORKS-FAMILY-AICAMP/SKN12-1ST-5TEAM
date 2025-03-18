import os
import sys
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 상위 디렉토리 추가하여 database 모듈 import 가능하게 설정
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.db_connector import db
from database.models import (
    Region, CarType, Manufacturer, CarModel, CarRegistration
)

# 페이지 설정
st.set_page_config(
    page_title="통계 분석",
    page_icon="📊",
    layout="wide"
)

# 스타일 설정
st.markdown("""
<style>
    .main-header {
        font-size: 24px;
        font-weight: bold;
        color: #3498db;
        margin-bottom: 20px;
    }
    .sub-header {
        font-size: 20px;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 30px;
        margin-bottom: 10px;
    }
    .stat-card {
        background-color: #f8f9fa;
        border-radius: 5px;
        padding: 15px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .stat-value {
        font-size: 24px;
        font-weight: bold;
        color: #3498db;
    }
    .stat-label {
        font-size: 14px;
        color: #7f8c8d;
    }
</style>
""", unsafe_allow_html=True)

# 연도별 등록 현황 데이터 로드
@st.cache_data(ttl=3600)
def load_yearly_stats():
    try:
        # 데이터베이스 연결 상태 확인
        if not db.is_connected():
            st.warning("데이터베이스 연결이 끊어졌습니다. 다시 연결을 시도합니다.")
            db.connect()
        
        query = """
            SELECT 
                YEAR(registration_date) AS year,
                SUM(registration_count) AS total_count
            FROM 
                car_registration
            GROUP BY 
                YEAR(registration_date)
            ORDER BY 
                year
        """
        
        df = db.query_to_dataframe(query)
        
        # 데이터가 비어있는 경우 샘플 데이터 반환
        if df.empty:
            st.warning("연도별 등록 데이터가 없습니다. 샘플 데이터를 표시합니다.")
            # 샘플 데이터 생성
            df = pd.DataFrame({
                'year': [2020, 2021, 2022, 2023],
                'total_count': [1250000, 1320000, 1450000, 1560000]
            })
        
        return df
    except Exception as e:
        st.error(f"데이터 로드 중 오류 발생: {e}")
        # 오류 발생 시 샘플 데이터 반환
        return pd.DataFrame({
            'year': [2020, 2021, 2022, 2023],
            'total_count': [1250000, 1320000, 1450000, 1560000]
        })

# 연도별 차종 등록 현황 데이터 로드
@st.cache_data(ttl=3600)
def load_yearly_car_type_stats():
    query = """
        SELECT 
            YEAR(cr.registration_date) AS year,
            ct.name AS car_type,
            SUM(cr.registration_count) AS total_count
        FROM 
            car_registration cr
        JOIN 
            car_types ct ON cr.car_type_id = ct.id
        GROUP BY 
            YEAR(cr.registration_date), ct.name
        ORDER BY 
            year, ct.name
    """
    
    df = db.query_to_dataframe(query)
    return df

# 연도별 지역 등록 현황 데이터 로드
@st.cache_data(ttl=3600)
def load_yearly_region_stats():
    query = """
        SELECT 
            YEAR(cr.registration_date) AS year,
            r.name AS region,
            SUM(cr.registration_count) AS total_count
        FROM 
            car_registration cr
        JOIN 
            regions r ON cr.region_id = r.id
        GROUP BY 
            YEAR(cr.registration_date), r.name
        ORDER BY 
            year, r.name
    """
    
    df = db.query_to_dataframe(query)
    return df

# 연도별 제조사 등록 현황 데이터 로드
@st.cache_data(ttl=3600)
def load_yearly_manufacturer_stats():
    query = """
        SELECT 
            YEAR(cr.registration_date) AS year,
            m.name AS manufacturer,
            SUM(cr.registration_count) AS total_count
        FROM 
            car_registration cr
        JOIN 
            car_models cm ON cr.car_model_id = cm.id
        JOIN 
            manufacturers m ON cm.manufacturer_id = m.id
        GROUP BY 
            YEAR(cr.registration_date), m.name
        ORDER BY 
            year, m.name
    """
    
    df = db.query_to_dataframe(query)
    return df

# 전기차 등록 현황 데이터 로드
@st.cache_data(ttl=3600)
def load_ev_stats():
    query = """
        SELECT 
            YEAR(cr.registration_date) AS year,
            r.name AS region,
            SUM(cr.registration_count) AS ev_count
        FROM 
            car_registration cr
        JOIN 
            regions r ON cr.region_id = r.id
        JOIN 
            car_types ct ON cr.car_type_id = ct.id
        WHERE 
            ct.name = '전기차'
        GROUP BY 
            YEAR(cr.registration_date), r.name
        ORDER BY 
            year, r.name
    """
    
    df = db.query_to_dataframe(query)
    return df

# 친환경 차량 등록 비율 데이터 로드
@st.cache_data(ttl=3600)
def load_eco_friendly_ratio():
    query = """
        SELECT 
            YEAR(cr.registration_date) AS year,
            ct.name AS car_type,
            SUM(cr.registration_count) AS count
        FROM 
            car_registration cr
        JOIN 
            car_types ct ON cr.car_type_id = ct.id
        WHERE 
            ct.name IN ('전기차', '하이브리드', '수소차')
            OR ct.name NOT IN ('전기차', '하이브리드', '수소차')
        GROUP BY 
            YEAR(cr.registration_date), ct.name
        ORDER BY 
            year, ct.name
    """
    
    df = db.query_to_dataframe(query)
    
    # 친환경 차량과 일반 차량으로 분류
    df['category'] = df['car_type'].apply(lambda x: '친환경 차량' if x in ['전기차', '하이브리드', '수소차'] else '일반 차량')
    
    # 연도별 카테고리별 합계 계산
    df_summary = df.groupby(['year', 'category'])['count'].sum().reset_index()
    
    # 연도별 총합 계산
    df_total = df_summary.groupby('year')['count'].sum().reset_index()
    df_total.rename(columns={'count': 'total'}, inplace=True)
    
    # 비율 계산을 위해 데이터 병합
    df_result = pd.merge(df_summary, df_total, on='year')
    df_result['ratio'] = df_result['count'] / df_result['total'] * 100
    
    return df_result

# 상위 10개 모델 데이터 로드
@st.cache_data(ttl=3600)
def load_top_models(year=None):
    params = []
    where_clause = ""
    
    if year:
        where_clause = "WHERE YEAR(cr.registration_date) = %s"
        params.append(year)
    
    query = f"""
        SELECT 
            cm.name AS model_name,
            m.name AS manufacturer_name,
            SUM(cr.registration_count) AS total_count
        FROM 
            car_registration cr
        JOIN 
            car_models cm ON cr.car_model_id = cm.id
        JOIN 
            manufacturers m ON cm.manufacturer_id = m.id
        {where_clause}
        GROUP BY 
            cm.name, m.name
        ORDER BY 
            total_count DESC
        LIMIT 10
    """
    
    df = db.query_to_dataframe(query, tuple(params) if params else None)
    return df

# 연도별 월별 등록 추이 데이터 로드
@st.cache_data(ttl=3600)
def load_monthly_trend_by_year(year=None):
    params = []
    where_clause = ""
    
    if year:
        where_clause = "WHERE YEAR(registration_date) = %s"
        params.append(year)
    
    query = f"""
        SELECT 
            YEAR(registration_date) AS year,
            MONTH(registration_date) AS month,
            SUM(registration_count) AS total_count
        FROM 
            car_registration
        {where_clause}
        GROUP BY 
            YEAR(registration_date), MONTH(registration_date)
        ORDER BY 
            year, month
    """
    
    df = db.query_to_dataframe(query, tuple(params) if params else None)
    return df

# 지역별 차종 선호도 데이터 로드
@st.cache_data(ttl=3600)
def load_region_car_type_preference():
    query = """
        SELECT 
            r.name AS region,
            ct.name AS car_type,
            SUM(cr.registration_count) AS total_count
        FROM 
            car_registration cr
        JOIN 
            regions r ON cr.region_id = r.id
        JOIN 
            car_types ct ON cr.car_type_id = ct.id
        GROUP BY 
            r.name, ct.name
        ORDER BY 
            r.name, total_count DESC
    """
    
    df = db.query_to_dataframe(query)
    
    # 각 지역별로 가장 선호하는 차종 찾기
    top_preferences = df.loc[df.groupby('region')['total_count'].idxmax()]
    
    return df, top_preferences

# 제조사별 상위 모델 데이터 로드
@st.cache_data(ttl=3600)
def load_top_models_by_manufacturer(year=None, manufacturer_id=None):
    params = []
    where_clauses = []
    
    if year:
        where_clauses.append("YEAR(cr.registration_date) = %s")
        params.append(year)
    
    if manufacturer_id:
        where_clauses.append("m.id = %s")
        params.append(manufacturer_id)
    
    where_clause = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
    
    query = f"""
        SELECT 
            cm.name AS model_name,
            m.name AS manufacturer_name,
            SUM(cr.registration_count) AS total_count
        FROM 
            car_registration cr
        JOIN 
            car_models cm ON cr.car_model_id = cm.id
        JOIN 
            manufacturers m ON cm.manufacturer_id = m.id
        {where_clause}
        GROUP BY 
            cm.name, m.name
        ORDER BY 
            total_count DESC
        LIMIT 20
    """
    
    df = db.query_to_dataframe(query, tuple(params) if params else None)
    return df

# 제조사 데이터 로드
@st.cache_data(ttl=3600)
def load_manufacturers():
    query = """
        SELECT id, name
        FROM manufacturers
        ORDER BY name
    """
    
    df = db.query_to_dataframe(query)
    return df

# 국산차 vs 수입차 비교 데이터 로드
@st.cache_data(ttl=3600)
def load_domestic_vs_import_data():
    query = """
        SELECT 
            YEAR(cr.registration_date) AS year,
            CASE 
                WHEN m.country = '대한민국' THEN '국산차'
                ELSE '수입차'
            END AS car_origin,
            SUM(cr.registration_count) AS total_count
        FROM 
            car_registration cr
        JOIN 
            car_models cm ON cr.car_model_id = cm.id
        JOIN 
            manufacturers m ON cm.manufacturer_id = m.id
        GROUP BY 
            YEAR(cr.registration_date),
            CASE 
                WHEN m.country = '대한민국' THEN '국산차'
                ELSE '수입차'
            END
        ORDER BY 
            year, car_origin
    """
    
    df = db.query_to_dataframe(query)
    return df

# 국가별 등록 데이터 로드
@st.cache_data(ttl=3600)
def load_country_registration_data(year=None):
    params = []
    where_clause = ""
    
    if year:
        where_clause = "WHERE YEAR(cr.registration_date) = %s"
        params.append(year)
    
    query = f"""
        SELECT 
            m.country,
            SUM(cr.registration_count) AS total_count
        FROM 
            car_registration cr
        JOIN 
            car_models cm ON cr.car_model_id = cm.id
        JOIN 
            manufacturers m ON cm.manufacturer_id = m.id
        {where_clause}
        GROUP BY 
            m.country
        ORDER BY 
            total_count DESC
    """
    
    df = db.query_to_dataframe(query, tuple(params) if params else None)
    return df

# 제조사 시장점유율 데이터 로드
@st.cache_data(ttl=3600)
def load_manufacturer_market_share(year=None):
    params = []
    where_clause = ""
    
    if year:
        where_clause = "WHERE YEAR(cr.registration_date) = %s"
        params.append(year)
    
    query = f"""
        SELECT 
            m.name AS manufacturer,
            SUM(cr.registration_count) AS total_count
        FROM 
            car_registration cr
        JOIN 
            car_models cm ON cr.car_model_id = cm.id
        JOIN 
            manufacturers m ON cm.manufacturer_id = m.id
        {where_clause}
        GROUP BY 
            m.name
        ORDER BY 
            total_count DESC
    """
    
    df = db.query_to_dataframe(query, tuple(params) if params else None)
    
    # 총 등록대수 계산
    total = df['total_count'].sum()
    
    # 상위 5개 제조사 선택 및 나머지는 '기타'로 처리
    top_5 = df.head(5).copy()
    others = pd.DataFrame([{
        'manufacturer': '기타',
        'total_count': df.iloc[5:]['total_count'].sum() if len(df) > 5 else 0
    }])
    
    result = pd.concat([top_5, others])
    
    # 점유율 계산
    result['share'] = result['total_count'] / total * 100
    
    return result

# 연도별 제조사 점유율 추이 데이터
@st.cache_data(ttl=3600)
def load_manufacturer_share_trend(top_n=5):
    query = f"""
        SELECT 
            YEAR(cr.registration_date) AS year,
            m.name AS manufacturer,
            SUM(cr.registration_count) AS total_count
        FROM 
            car_registration cr
        JOIN 
            car_models cm ON cr.car_model_id = cm.id
        JOIN 
            manufacturers m ON cm.manufacturer_id = m.id
        GROUP BY 
            YEAR(cr.registration_date), m.name
        ORDER BY 
            year, total_count DESC
    """
    
    df = db.query_to_dataframe(query)
    
    # 각 연도별 총 등록대수 계산
    yearly_total = df.groupby('year')['total_count'].sum().reset_index()
    yearly_total.rename(columns={'total_count': 'yearly_total'}, inplace=True)
    
    # 연도별 데이터와 총합 병합
    df = pd.merge(df, yearly_total, on='year')
    
    # 점유율 계산
    df['share'] = df['total_count'] / df['yearly_total'] * 100
    
    # 연도별 상위 제조사 구하기
    top_manufacturers = set()
    for year in df['year'].unique():
        year_data = df[df['year'] == year].sort_values('total_count', ascending=False)
        top_manufacturers.update(year_data.head(top_n)['manufacturer'].tolist())
    
    # 상위 제조사만 필터링
    df_filtered = df[df['manufacturer'].isin(top_manufacturers)]
    
    return df_filtered

# 메인 함수
def main():
    st.markdown('<div class="main-header">통계 분석</div>', unsafe_allow_html=True)
    
    # 사이드바 - 분석 유형 선택
    analysis_type = st.sidebar.radio(
        "분석 유형 선택",
        ["연도별 등록 추이", "차종별 분석", "지역별 분석", "제조사/모델 분석", "친환경 차량 분석", "국산차 vs 수입차 분석", "제조사 시장점유율 분석"]
    )
    
    # 연도별 등록 추이 분석
    if analysis_type == "연도별 등록 추이":
        st.markdown('<div class="sub-header">연도별 등록 추이 분석</div>', unsafe_allow_html=True)
        
        yearly_stats = load_yearly_stats()
        
        if not yearly_stats.empty:
            # 연도별 등록 추이 차트
            fig = px.bar(
                yearly_stats,
                x='year',
                y='total_count',
                title='연도별 자동차 등록 추이',
                labels={'year': '연도', 'total_count': '등록 대수'},
                color='total_count',
                color_continuous_scale='Blues'
            )
            
            # 추세선 추가
            fig.add_trace(
                go.Scatter(
                    x=yearly_stats['year'],
                    y=yearly_stats['total_count'],
                    mode='lines+markers',
                    name='추세선',
                    line=dict(color='red', width=2)
                )
            )
            
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # 연도별 증감률 계산
            yearly_stats['prev_year_count'] = yearly_stats['total_count'].shift(1)
            yearly_stats['growth_rate'] = (yearly_stats['total_count'] - yearly_stats['prev_year_count']) / yearly_stats['prev_year_count'] * 100
            yearly_stats['growth_rate'] = yearly_stats['growth_rate'].fillna(0)
            
            # 증감률 차트
            fig = px.line(
                yearly_stats,
                x='year',
                y='growth_rate',
                title='연도별 등록 증감률',
                labels={'year': '연도', 'growth_rate': '증감률 (%)'},
                markers=True
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # 월별 등록 추이
            st.markdown('<div class="sub-header">월별 등록 추이</div>', unsafe_allow_html=True)
            
            # 연도 선택
            available_years = sorted(yearly_stats['year'].unique())
            selected_year = st.selectbox("연도 선택", available_years, index=len(available_years)-1 if available_years else 0)
            
            monthly_trend = load_monthly_trend_by_year(selected_year)
            
            if not monthly_trend.empty:
                # 월 이름 추가
                month_names = ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월']
                monthly_trend['month_name'] = monthly_trend['month'].apply(lambda x: month_names[x-1])
                
                # 월별 등록 추이 차트
                fig = px.bar(
                    monthly_trend,
                    x='month_name',
                    y='total_count',
                    title=f'{selected_year}년 월별 자동차 등록 추이',
                    labels={'month_name': '월', 'total_count': '등록 대수'},
                    color='total_count',
                    color_continuous_scale='Viridis'
                )
                
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("연도별 등록 데이터가 없습니다.")
    
    # 차종별 분석
    elif analysis_type == "차종별 분석":
        st.markdown('<div class="sub-header">차종별 분석</div>', unsafe_allow_html=True)
        
        yearly_car_type_stats = load_yearly_car_type_stats()
        
        if not yearly_car_type_stats.empty:
            # 연도별 차종 등록 현황 차트
            fig = px.line(
                yearly_car_type_stats,
                x='year',
                y='total_count',
                color='car_type',
                title='연도별 차종 등록 추이',
                labels={'year': '연도', 'total_count': '등록 대수', 'car_type': '차종'},
                markers=True
            )
            
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # 연도 선택
            available_years = sorted(yearly_car_type_stats['year'].unique())
            selected_year = st.selectbox("연도 선택", available_years, index=len(available_years)-1 if available_years else 0)
            
            # 선택된 연도의 차종별 등록 현황
            year_data = yearly_car_type_stats[yearly_car_type_stats['year'] == selected_year]
            
            if not year_data.empty:
                # 파이 차트
                fig = px.pie(
                    year_data,
                    values='total_count',
                    names='car_type',
                    title=f'{selected_year}년 차종별 등록 비율',
                    hole=0.4
                )
                
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
                
                # 차종별 등록 대수 표시
                st.markdown('<div class="sub-header">차종별 등록 대수</div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                for i, (index, row) in enumerate(year_data.iterrows()):
                    with col1 if i % 2 == 0 else col2:
                        st.markdown(f"""
                        <div class="stat-card">
                            <div class="stat-label">{row['car_type']}</div>
                            <div class="stat-value">{int(row['total_count']):,}대</div>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.warning("차종별 등록 데이터가 없습니다.")
    
    # 지역별 분석
    elif analysis_type == "지역별 분석":
        st.markdown('<div class="sub-header">지역별 분석</div>', unsafe_allow_html=True)
        
        yearly_region_stats = load_yearly_region_stats()
        
        if not yearly_region_stats.empty:
            # 연도 선택
            available_years = sorted(yearly_region_stats['year'].unique())
            selected_year = st.selectbox("연도 선택", available_years, index=len(available_years)-1 if available_years else 0)
            
            # 선택된 연도의 지역별 등록 현황
            year_data = yearly_region_stats[yearly_region_stats['year'] == selected_year]
            
            if not year_data.empty:
                # 지역별 등록 현황 차트
                fig = px.bar(
                    year_data,
                    x='region',
                    y='total_count',
                    title=f'{selected_year}년 지역별 등록 현황',
                    labels={'region': '지역', 'total_count': '등록 대수'},
                    color='total_count',
                    color_continuous_scale='Blues'
                )
                
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
            
            # 지역별 차종 선호도 분석
            st.markdown('<div class="sub-header">지역별 차종 선호도 분석</div>', unsafe_allow_html=True)
            
            region_preference_data, top_preferences = load_region_car_type_preference()
            
            if not region_preference_data.empty:
                # 히트맵 데이터 준비
                pivot_data = region_preference_data.pivot(index='region', columns='car_type', values='total_count')
                pivot_data = pivot_data.fillna(0)
                
                # 히트맵 그리기
                fig = px.imshow(
                    pivot_data,
                    labels=dict(x="차종", y="지역", color="등록 대수"),
                    x=pivot_data.columns,
                    y=pivot_data.index,
                    color_continuous_scale='Viridis',
                    title='지역별 차종 선호도 히트맵'
                )
                
                fig.update_layout(height=600)
                st.plotly_chart(fig, use_container_width=True)
                
                # 지역별 가장 선호하는 차종 표시
                st.markdown('<div class="sub-header">지역별 가장 선호하는 차종</div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                for i, (index, row) in enumerate(top_preferences.iterrows()):
                    with col1 if i % 2 == 0 else col2:
                        st.markdown(f"""
                        <div class="stat-card">
                            <div class="stat-label">{row['region']}</div>
                            <div class="stat-value">{row['car_type']}</div>
                            <div>{int(row['total_count']):,}대</div>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.warning("지역별 등록 데이터가 없습니다.")
    
    # 제조사/모델 분석
    elif analysis_type == "제조사/모델 분석":
        st.markdown('<div class="sub-header">제조사/모델 분석</div>', unsafe_allow_html=True)
        
        yearly_manufacturer_stats = load_yearly_manufacturer_stats()
        
        if not yearly_manufacturer_stats.empty:
            # 연도 선택
            available_years = sorted(yearly_manufacturer_stats['year'].unique())
            selected_year = st.selectbox("연도 선택", available_years, index=len(available_years)-1 if available_years else 0)
            
            # 선택된 연도의 제조사별 등록 현황
            year_data = yearly_manufacturer_stats[yearly_manufacturer_stats['year'] == selected_year]
            
            if not year_data.empty:
                # 상위 10개 제조사 추출
                top_manufacturers = year_data.sort_values('total_count', ascending=False).head(10)
                
                # 제조사별 등록 현황 차트
                fig = px.bar(
                    top_manufacturers,
                    x='manufacturer',
                    y='total_count',
                    title=f'{selected_year}년 제조사별 등록 현황 (상위 10개)',
                    labels={'manufacturer': '제조사', 'total_count': '등록 대수'},
                    color='total_count',
                    color_continuous_scale='Viridis'
                )
                
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
            
            # 인기 모델 분석
            st.markdown('<div class="sub-header">인기 모델 분석</div>', unsafe_allow_html=True)
            
            # 분석 방식 선택
            model_analysis_type = st.radio(
                "모델 분석 방식",
                ["전체 인기 모델", "제조사별 인기 모델"],
                horizontal=True
            )
            
            if model_analysis_type == "전체 인기 모델":
                # 전체 인기 모델 조회
                top_models = load_top_models(selected_year)
                
                if not top_models.empty:
                    # 상위 10개 모델 차트
                    fig = px.bar(
                        top_models,
                        x='model_name',
                        y='total_count',
                        title=f'{selected_year}년 인기 모델 (상위 10개)',
                        labels={'model_name': '모델명', 'total_count': '등록 대수'},
                        color='manufacturer_name',
                        hover_data=['manufacturer_name']
                    )
                    
                    fig.update_layout(height=500)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # 데이터 테이블
                    display_df = top_models.copy()
                    display_df = display_df.rename(columns={
                        'model_name': '모델명',
                        'manufacturer_name': '제조사',
                        'total_count': '등록대수'
                    })
                    
                    st.dataframe(display_df.reset_index(drop=True), use_container_width=True)
            else:
                # 제조사별 인기 모델 조회
                manufacturers = load_manufacturers()
                
                if not manufacturers.empty:
                    # 제조사 선택
                    selected_manufacturer_id = st.selectbox(
                        "제조사 선택",
                        options=manufacturers['id'],
                        format_func=lambda x: manufacturers[manufacturers['id'] == x]['name'].iloc[0],
                        index=0
                    )
                    
                    selected_manufacturer_name = manufacturers[manufacturers['id'] == selected_manufacturer_id]['name'].iloc[0]
                    
                    # 선택된 제조사의 인기 모델 조회
                    manufacturer_models = load_top_models_by_manufacturer(selected_year, selected_manufacturer_id)
                    
                    if not manufacturer_models.empty:
                        # 제조사 인기 모델 차트
                        fig = px.bar(
                            manufacturer_models,
                            x='model_name',
                            y='total_count',
                            title=f'{selected_year}년 {selected_manufacturer_name} 인기 모델',
                            labels={'model_name': '모델명', 'total_count': '등록 대수'},
                            color='total_count',
                            color_continuous_scale='Viridis'
                        )
                        
                        fig.update_layout(height=500)
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # 데이터 테이블
                        display_df = manufacturer_models.copy()
                        display_df = display_df.rename(columns={
                            'model_name': '모델명',
                            'manufacturer_name': '제조사',
                            'total_count': '등록대수'
                        })
                        
                        st.dataframe(display_df.reset_index(drop=True), use_container_width=True)
                    else:
                        st.warning(f"{selected_manufacturer_name}의 모델 데이터가 없습니다.")
                else:
                    st.warning("제조사 데이터가 없습니다.")
        else:
            st.warning("제조사별 등록 데이터가 없습니다.")
    
    # 친환경 차량 분석
    elif analysis_type == "친환경 차량 분석":
        st.markdown('<div class="sub-header">친환경 차량 분석</div>', unsafe_allow_html=True)
        
        # 전기차 등록 현황
        ev_stats = load_ev_stats()
        
        if not ev_stats.empty:
            # 연도별 전기차 등록 추이
            ev_yearly = ev_stats.groupby('year')['ev_count'].sum().reset_index()
            
            fig = px.bar(
                ev_yearly,
                x='year',
                y='ev_count',
                title='연도별 전기차 등록 추이',
                labels={'year': '연도', 'ev_count': '등록 대수'},
                color='ev_count',
                color_continuous_scale='Greens'
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # 연도 선택
            available_years = sorted(ev_stats['year'].unique())
            selected_year = st.selectbox("연도 선택", available_years, index=len(available_years)-1 if available_years else 0)
            
            # 선택된 연도의 지역별 전기차 등록 현황
            year_data = ev_stats[ev_stats['year'] == selected_year]
            
            if not year_data.empty:
                # 지역별 전기차 등록 현황 차트
                fig = px.bar(
                    year_data,
                    x='region',
                    y='ev_count',
                    title=f'{selected_year}년 지역별 전기차 등록 현황',
                    labels={'region': '지역', 'ev_count': '등록 대수'},
                    color='ev_count',
                    color_continuous_scale='Greens'
                )
                
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
            
            # 친환경 차량 비율 분석
            st.markdown('<div class="sub-header">친환경 차량 비율 분석</div>', unsafe_allow_html=True)
            
            eco_friendly_data = load_eco_friendly_ratio()
            
            if not eco_friendly_data.empty:
                # 친환경 차량 비율만 추출
                eco_friendly_ratio = eco_friendly_data[eco_friendly_data['category'] == '친환경 차량']
                
                # 연도별 친환경 차량 비율 차트
                fig = px.line(
                    eco_friendly_ratio,
                    x='year',
                    y='ratio',
                    title='연도별 친환경 차량 등록 비율',
                    labels={'year': '연도', 'ratio': '비율 (%)'},
                    markers=True
                )
                
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                
                # 연도별 친환경 차량 vs 일반 차량 비율 차트
                fig = px.bar(
                    eco_friendly_data,
                    x='year',
                    y='count',
                    color='category',
                    title='연도별 친환경 차량 vs 일반 차량 등록 대수',
                    labels={'year': '연도', 'count': '등록 대수', 'category': '분류'},
                    barmode='group'
                )
                
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
                
                # 연도별 친환경 차량 비율 표시
                st.markdown('<div class="sub-header">연도별 친환경 차량 비율</div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                for i, (index, row) in enumerate(eco_friendly_ratio.iterrows()):
                    with col1 if i % 2 == 0 else col2:
                        st.markdown(f"""
                        <div class="stat-card">
                            <div class="stat-label">{int(row['year'])}년</div>
                            <div class="stat-value">{row['ratio']:.2f}%</div>
                            <div>등록 대수: {int(row['count']):,}대</div>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.warning("친환경 차량 등록 데이터가 없습니다.")
    
    # 국산차 vs 수입차 분석
    elif analysis_type == "국산차 vs 수입차 분석":
        st.markdown('<div class="sub-header">국산차 vs 수입차 분석</div>', unsafe_allow_html=True)
        
        # 국산차 vs 수입차 데이터 로드
        domestic_vs_import = load_domestic_vs_import_data()
        
        if not domestic_vs_import.empty:
            # 연도별 국산차 vs 수입차 등록 비율 변화
            pivot_df = domestic_vs_import.pivot(index='year', columns='car_origin', values='total_count').reset_index()
            pivot_df.fillna(0, inplace=True)
            
            # 총 등록대수 및 비율 계산
            pivot_df['total'] = pivot_df['국산차'] + pivot_df['수입차']
            pivot_df['국산차_비율'] = pivot_df['국산차'] / pivot_df['total'] * 100
            pivot_df['수입차_비율'] = pivot_df['수입차'] / pivot_df['total'] * 100
            
            # 연도별 등록 대수 차트
            st.markdown('<div class="sub-header">연도별 국산차 vs 수입차 등록 대수</div>', unsafe_allow_html=True)
            
            fig1 = px.bar(
                domestic_vs_import,
                x='year',
                y='total_count',
                color='car_origin',
                barmode='group',
                title='연도별 국산차/수입차, 등록 대수 비교',
                labels={'year': '연도', 'total_count': '등록 대수', 'car_origin': '구분'},
                color_discrete_map={'국산차': '#3498db', '수입차': '#e74c3c'}
            )
            
            fig1.update_layout(height=500)
            st.plotly_chart(fig1, use_container_width=True)
            
            # 연도별 등록 비율 차트
            st.markdown('<div class="sub-header">연도별 국산차 vs 수입차 등록 비율</div>', unsafe_allow_html=True)
            
            fig2 = px.area(
                pivot_df,
                x='year',
                y=['국산차_비율', '수입차_비율'],
                title='연도별 국산차/수입차 등록 비율',
                labels={'year': '연도', 'value': '비율 (%)', 'variable': '구분'},
                color_discrete_map={'국산차_비율': '#3498db', '수입차_비율': '#e74c3c'}
            )
            
            fig2.update_layout(
                height=500,
                yaxis=dict(ticksuffix='%'),
                legend=dict(
                    title='',
                    orientation='h',
                    y=1.1
                )
            )
            
            st.plotly_chart(fig2, use_container_width=True)
            
            # 연도 선택
            available_years = sorted(domestic_vs_import['year'].unique())
            selected_year = st.selectbox(
                "연도 선택", 
                available_years, 
                index=len(available_years)-1 if available_years else 0,
                key="domestic_import_year"
            )
            
            # 선택한 연도의 국가별 등록 현황
            country_data = load_country_registration_data(selected_year)
            
            if not country_data.empty:
                st.markdown(f'<div class="sub-header">{selected_year}년 국가별 등록 현황</div>', unsafe_allow_html=True)
                
                # 국가 데이터 준비
                country_data['country'].fillna('기타', inplace=True)
                
                # 총합에 대한 백분율 계산
                total_count = country_data['total_count'].sum()
                country_data['percentage'] = country_data['total_count'] / total_count * 100
                
                # 파이 차트
                fig3 = px.pie(
                    country_data,
                    values='total_count',
                    names='country',
                    title=f'{selected_year}년 제조국가별 등록 비율',
                    hover_data=['percentage'],
                    labels={'percentage': '비율 (%)'},
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                
                fig3.update_traces(
                    textposition='inside',
                    textinfo='percent+label',
                    hovertemplate='%{label}: %{value:,} 대<br>비율: %{customdata[0]:.1f}%'
                )
                
                fig3.update_layout(height=500)
                st.plotly_chart(fig3, use_container_width=True)
                
                # 데이터 테이블 표시
                display_df = country_data.copy()
                display_df['total_count'] = display_df['total_count'].apply(lambda x: f"{int(x):,} 대")
                display_df['percentage'] = display_df['percentage'].apply(lambda x: f"{x:.2f}%")
                display_df.columns = ['제조국가', '등록대수', '비율']
                
                st.dataframe(display_df, use_container_width=True)
            else:
                st.warning(f"{selected_year}년 국가별 등록 데이터가 없습니다.")
        else:
            st.warning("국산차 vs 수입차 비교 데이터가 없습니다.")
    
    # 제조사 시장점유율 분석
    elif analysis_type == "제조사 시장점유율 분석":
        st.markdown('<div class="sub-header">제조사 시장점유율 분석</div>', unsafe_allow_html=True)
        
        # 연도별 제조사 점유율 추이 데이터 로드
        share_trend = load_manufacturer_share_trend()
        
        if not share_trend.empty:
            # 연도별 상위 제조사 점유율 변화 추이
            st.markdown('<div class="sub-header">연도별 상위 제조사 점유율 변화 추이</div>', unsafe_allow_html=True)
            
            fig1 = px.line(
                share_trend,
                x='year',
                y='share',
                color='manufacturer',
                markers=True,
                title='연도별 상위 제조사 점유율 변화 추이',
                labels={'year': '연도', 'share': '점유율 (%)', 'manufacturer': '제조사'},
                color_discrete_sequence=px.colors.qualitative.Plotly
            )
            
            fig1.update_layout(
                height=500,
                yaxis=dict(
                    ticksuffix='%',
                    title='시장 점유율 (%)'
                ),
                legend=dict(
                    orientation='h',
                    yanchor='bottom',
                    y=1.02,
                    xanchor='right',
                    x=1
                )
            )
            
            st.plotly_chart(fig1, use_container_width=True)
            
            # 연도 선택
            available_years = sorted(share_trend['year'].unique())
            selected_year = st.selectbox(
                "연도 선택", 
                available_years, 
                index=len(available_years)-1 if available_years else 0,
                key="market_share_year"
            )
            
            # 선택된 연도의 제조사 점유율
            market_share = load_manufacturer_market_share(selected_year)
            
            if not market_share.empty:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f'<div class="sub-header">{selected_year}년 제조사 시장점유율</div>', unsafe_allow_html=True)
                    
                    # 파이 차트
                    fig2 = px.pie(
                        market_share,
                        values='total_count',
                        names='manufacturer',
                        title=f'{selected_year}년 제조사별 시장점유율',
                        color_discrete_sequence=px.colors.qualitative.Plotly
                    )
                    
                    fig2.update_traces(
                        textposition='inside',
                        textinfo='percent+label',
                        hovertemplate='%{label}: %{value:,} 대<br>점유율: %{percent:.1%}'
                    )
                    
                    fig2.update_layout(height=500)
                    st.plotly_chart(fig2, use_container_width=True)
                
                with col2:
                    st.markdown(f'<div class="sub-header">점유율 상위 제조사</div>', unsafe_allow_html=True)
                    
                    for i, row in market_share.iterrows():
                        if row['manufacturer'] != '기타':
                            st.markdown(f"""
                            <div class="stat-card">
                                <div class="stat-value">{row['manufacturer']}</div>
                                <div class="stat-label">{int(row['total_count']):,} 대</div>
                                <div style="font-size: 16px; color: #3498db;">{row['share']:.1f}%</div>
                            </div>
                            """, unsafe_allow_html=True)
                
                # 데이터 테이블 표시
                st.markdown(f'<div class="sub-header">제조사별 등록 데이터</div>', unsafe_allow_html=True)
                
                display_df = market_share.copy()
                display_df['total_count'] = display_df['total_count'].apply(lambda x: f"{int(x):,} 대")
                display_df['share'] = display_df['share'].apply(lambda x: f"{x:.2f}%")
                display_df.columns = ['제조사', '등록대수', '점유율']
                
                st.dataframe(display_df, use_container_width=True)
            else:
                st.warning(f"{selected_year}년 제조사 점유율 데이터가 없습니다.")
        else:
            st.warning("제조사 점유율 추이 데이터가 없습니다.")

if __name__ == "__main__":
    main() 