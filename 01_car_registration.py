import os
import sys
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# 상위 디렉토리 추가하여 database 모듈 import 가능하게 설정
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.db_connector import db
from database.models import (
    Region, CarType, Manufacturer, CarModel, CarRegistration
)

# 페이지 설정
st.set_page_config(
    page_title="자동차 등록 현황 조회 - 전국 자동차 등록 현황 및 기업 FAQ 조회시스템",
    page_icon="🚗",
    layout="wide"
)

# 데이터베이스 연결 확인
@st.cache_resource
def check_db_connection():
    try:
        return db.connect()
    except Exception as e:
        st.warning(f"데이터베이스 연결에 실패했습니다: {e}")
        st.info("샘플 데이터로 실행됩니다. 일부 기능이 제한됩니다.")
        return False

# 샘플 지역 데이터 생성
def create_sample_regions():
    return [
        {'id': 1, 'name': '서울'},
        {'id': 2, 'name': '부산'},
        {'id': 3, 'name': '대구'},
        {'id': 4, 'name': '인천'},
        {'id': 5, 'name': '광주'},
        {'id': 6, 'name': '대전'},
        {'id': 7, 'name': '울산'},
        {'id': 8, 'name': '경기'},
        {'id': 9, 'name': '강원'},
        {'id': 10, 'name': '충북'}
    ]

# 샘플 차종 데이터 생성
def create_sample_car_types():
    return [
        {'id': 1, 'name': '승용차'},
        {'id': 2, 'name': 'SUV'},
        {'id': 3, 'name': '승합차'},
        {'id': 4, 'name': '화물차'},
        {'id': 5, 'name': '특수차'}
    ]

# 샘플 제조사 데이터 생성
def create_sample_manufacturers():
    return [
        {'id': 1, 'name': '현대'},
        {'id': 2, 'name': '기아'},
        {'id': 3, 'name': '쌍용'},
        {'id': 4, 'name': '르노코리아'},
        {'id': 5, 'name': 'BMW'},
        {'id': 6, 'name': '벤츠'},
        {'id': 7, 'name': '아우디'},
        {'id': 8, 'name': '폭스바겐'},
        {'id': 9, 'name': '도요타'},
        {'id': 10, 'name': '혼다'},
        {'id': 11, 'name': '닛산'},
        {'id': 12, 'name': '렉서스'},
        {'id': 13, 'name': '볼보'},
        {'id': 14, 'name': '포르쉐'},
        {'id': 15, 'name': '테슬라'},
        {'id': 16, 'name': '페라리'},
        {'id': 17, 'name': '람보르기니'},
        {'id': 18, 'name': '재규어'},
        {'id': 19, 'name': '마세라티'},
        {'id': 20, 'name': '푸조'}
    ]

# 샘플 차량 모델 데이터 생성
def create_sample_car_models(manufacturer_id=None):
    all_models = [
        {'id': 1, 'name': '아반떼', 'manufacturer_id': 1},
        {'id': 2, 'name': '쏘나타', 'manufacturer_id': 1},
        {'id': 3, 'name': '그랜저', 'manufacturer_id': 1},
        {'id': 4, 'name': '싼타페', 'manufacturer_id': 1},
        {'id': 5, 'name': '팰리세이드', 'manufacturer_id': 1},
        {'id': 6, 'name': 'K3', 'manufacturer_id': 2},
        {'id': 7, 'name': 'K5', 'manufacturer_id': 2},
        {'id': 8, 'name': 'K8', 'manufacturer_id': 2},
        {'id': 9, 'name': '쏘렌토', 'manufacturer_id': 2},
        {'id': 10, 'name': '카니발', 'manufacturer_id': 2},
        {'id': 11, 'name': '티볼리', 'manufacturer_id': 3},
        {'id': 12, 'name': '코란도', 'manufacturer_id': 3},
        {'id': 13, 'name': 'SM6', 'manufacturer_id': 4},
        {'id': 14, 'name': 'XM3', 'manufacturer_id': 4},
        {'id': 15, 'name': '3시리즈', 'manufacturer_id': 5},
        {'id': 16, 'name': '5시리즈', 'manufacturer_id': 5},
        {'id': 17, 'name': 'X5', 'manufacturer_id': 5},
        {'id': 18, 'name': 'E클래스', 'manufacturer_id': 6},
        {'id': 19, 'name': 'S클래스', 'manufacturer_id': 6},
        {'id': 20, 'name': 'GLE', 'manufacturer_id': 6},
        {'id': 21, 'name': 'A4', 'manufacturer_id': 7},
        {'id': 22, 'name': 'Q5', 'manufacturer_id': 7},
        {'id': 23, 'name': '골프', 'manufacturer_id': 8},
        {'id': 24, 'name': '티구안', 'manufacturer_id': 8},
        {'id': 25, 'name': '캠리', 'manufacturer_id': 9},
        {'id': 26, 'name': 'RAV4', 'manufacturer_id': 9},
        {'id': 27, 'name': '아코드', 'manufacturer_id': 10},
        {'id': 28, 'name': 'CR-V', 'manufacturer_id': 10},
        {'id': 29, 'name': '알티마', 'manufacturer_id': 11},
        {'id': 30, 'name': 'X-트레일', 'manufacturer_id': 11},
        {'id': 31, 'name': 'ES', 'manufacturer_id': 12},
        {'id': 32, 'name': 'RX', 'manufacturer_id': 12},
        {'id': 33, 'name': 'XC60', 'manufacturer_id': 13},
        {'id': 34, 'name': 'XC90', 'manufacturer_id': 13},
        {'id': 35, 'name': '911', 'manufacturer_id': 14},
        {'id': 36, 'name': '카이엔', 'manufacturer_id': 14},
        {'id': 37, 'name': '모델 3', 'manufacturer_id': 15},
        {'id': 38, 'name': '모델 Y', 'manufacturer_id': 15},
        {'id': 39, 'name': 'F8 트리뷰토', 'manufacturer_id': 16},
        {'id': 40, 'name': 'SF90', 'manufacturer_id': 16},
        {'id': 41, 'name': '우라칸', 'manufacturer_id': 17},
        {'id': 42, 'name': '아벤타도르', 'manufacturer_id': 17},
        {'id': 43, 'name': 'F-PACE', 'manufacturer_id': 18},
        {'id': 44, 'name': 'XF', 'manufacturer_id': 18},
        {'id': 45, 'name': '콰트로포르테', 'manufacturer_id': 19},
        {'id': 46, 'name': '르반떼', 'manufacturer_id': 19},
        {'id': 47, 'name': '3008', 'manufacturer_id': 20},
        {'id': 48, 'name': '5008', 'manufacturer_id': 20}
    ]
    
    if manufacturer_id:
        return [model for model in all_models if model['manufacturer_id'] == manufacturer_id]
    return all_models

# 샘플 등록 데이터 생성
def create_sample_registration_data(region_id=None, car_type_id=None, start_date=None, end_date=None):
    # 기본값 설정
    if not start_date:
        start_date = datetime.now() - timedelta(days=365)
    if not end_date:
        end_date = datetime.now()
    
    # 샘플 데이터 생성
    regions = create_sample_regions()
    car_types = create_sample_car_types()
    manufacturers = create_sample_manufacturers()
    
    data = []
    for i in range(100):  # 100개의 샘플 데이터 생성
        region = np.random.choice([r['id'] for r in regions])
        car_type = np.random.choice([c['id'] for c in car_types])
        manufacturer = np.random.choice([m['id'] for m in manufacturers])
        reg_date = start_date + timedelta(days=np.random.randint(0, (end_date - start_date).days))
        count = np.random.randint(50, 1000)
        
        if (region_id is None or region == region_id) and (car_type_id is None or car_type == car_type_id):
            data.append({
                'region_id': region,
                'region_name': next(r['name'] for r in regions if r['id'] == region),
                'car_type_id': car_type,
                'car_type_name': next(c['name'] for c in car_types if c['id'] == car_type),
                'manufacturer_id': manufacturer,
                'manufacturer_name': next(m['name'] for m in manufacturers if m['id'] == manufacturer),
                'registration_date': reg_date,
                'registration_count': count
            })
    
    return pd.DataFrame(data)

# 샘플 지역 통계 생성
def create_sample_region_stats(car_type_id=None, start_date=None, end_date=None):
    regions = create_sample_regions()
    data = []
    
    for region in regions:
        count = np.random.randint(5000, 50000)
        data.append({
            'region_name': region['name'],
            'total_count': count
        })
    
    return pd.DataFrame(data).sort_values('total_count', ascending=False)

# 샘플 차종 통계 생성
def create_sample_car_type_stats(region_id=None, start_date=None, end_date=None):
    car_types = create_sample_car_types()
    data = []
    
    for car_type in car_types:
        count = np.random.randint(5000, 50000)
        data.append({
            'car_type': car_type['name'],
            'total_count': count
        })
    
    return pd.DataFrame(data).sort_values('total_count', ascending=False)

# 샘플 제조사 통계 생성
def create_sample_manufacturer_stats(region_id=None, car_type_id=None, start_date=None, end_date=None):
    manufacturers = create_sample_manufacturers()
    data = []
    
    for manufacturer in manufacturers:
        count = np.random.randint(5000, 50000)
        data.append({
            'manufacturer_name': manufacturer['name'],
            'total_count': count
        })
    
    return pd.DataFrame(data).sort_values('total_count', ascending=False)

# 샘플 월별 추이 생성
def create_sample_monthly_trend(region_id=None, car_type_id=None, months=12):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30*months)
    
    data = []
    current_date = start_date
    
    while current_date <= end_date:
        month_str = current_date.strftime('%Y-%m')
        count = np.random.randint(5000, 20000)
        data.append({
            'month': month_str,
            'total_count': count
        })
        current_date = current_date + timedelta(days=30)
    
    return pd.DataFrame(data)

# 지역 데이터 로드
@st.cache_data(ttl=3600)
def load_regions():
    connection_successful = check_db_connection()
    if connection_successful:
        regions = Region.get_all()
        return regions, {region['id']: region['name'] for region in regions}
    else:
        regions = create_sample_regions()
        return regions, {region['id']: region['name'] for region in regions}

# 차종 데이터 로드
@st.cache_data(ttl=3600)
def load_car_types():
    connection_successful = check_db_connection()
    if connection_successful:
        car_types = CarType.get_all()
        return car_types, {car_type['id']: car_type['name'] for car_type in car_types}
    else:
        car_types = create_sample_car_types()
        return car_types, {car_type['id']: car_type['name'] for car_type in car_types}

# 등록 데이터 로드
def load_registration_data(region_id=None, car_type_id=None, start_date=None, end_date=None):
    connection_successful = check_db_connection()
    if connection_successful:
        params = []
        where_clauses = []
        
        if region_id:
            where_clauses.append("cr.region_id = %s")
            params.append(region_id)
        
        if car_type_id:
            where_clauses.append("cr.car_type_id = %s")
            params.append(car_type_id)
        
        if start_date:
            where_clauses.append("cr.registration_date >= %s")
            params.append(start_date.strftime('%Y-%m-%d'))
        
        if end_date:
            where_clauses.append("cr.registration_date <= %s")
            params.append(end_date.strftime('%Y-%m-%d'))
        
        where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"
        
        query = f"""
            SELECT 
                cr.id,
                cr.registration_date,
                r.name AS region_name,
                ct.name AS car_type_name,
                cm.name AS car_model_name,
                m.name AS manufacturer_name,
                cr.registration_count
            FROM 
                car_registration cr
            JOIN 
                regions r ON cr.region_id = r.id
            JOIN 
                car_types ct ON cr.car_type_id = ct.id
            JOIN 
                car_models cm ON cr.car_model_id = cm.id
            JOIN 
                manufacturers m ON cm.manufacturer_id = m.id
            WHERE 
                {where_clause}
            ORDER BY 
                cr.registration_date DESC
        """
        
        df = db.query_to_dataframe(query, tuple(params))
        return df
    else:
        return create_sample_registration_data(region_id, car_type_id, start_date, end_date)

# 지역별 통계 로드
def load_region_stats(car_type_id=None, start_date=None, end_date=None):
    connection_successful = check_db_connection()
    if connection_successful:
        params = []
        where_clauses = []
        
        if car_type_id:
            where_clauses.append("cr.car_type_id = %s")
            params.append(car_type_id)
        
        if start_date:
            where_clauses.append("cr.registration_date >= %s")
            params.append(start_date.strftime('%Y-%m-%d'))
        
        if end_date:
            where_clauses.append("cr.registration_date <= %s")
            params.append(end_date.strftime('%Y-%m-%d'))
        
        where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"
        
        query = f"""
            SELECT 
                r.name AS region_name, 
                SUM(cr.registration_count) AS total_count
            FROM 
                car_registration cr
            JOIN 
                regions r ON cr.region_id = r.id
            WHERE 
                {where_clause}
            GROUP BY 
                r.name
            ORDER BY 
                total_count DESC
        """
        
        df = db.query_to_dataframe(query, tuple(params))
        return df
    else:
        return create_sample_region_stats(car_type_id, start_date, end_date)

# 차종별 통계 로드
def load_car_type_stats(region_id=None, start_date=None, end_date=None):
    connection_successful = check_db_connection()
    if connection_successful:
        params = []
        where_clauses = []
        
        if region_id:
            where_clauses.append("cr.region_id = %s")
            params.append(region_id)
        
        if start_date:
            where_clauses.append("cr.registration_date >= %s")
            params.append(start_date.strftime('%Y-%m-%d'))
        
        if end_date:
            where_clauses.append("cr.registration_date <= %s")
            params.append(end_date.strftime('%Y-%m-%d'))
        
        where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"
        
        query = f"""
            SELECT 
                ct.name AS car_type, 
                SUM(cr.registration_count) AS total_count
            FROM 
                car_registration cr
            JOIN 
                car_types ct ON cr.car_type_id = ct.id
            WHERE 
                {where_clause}
            GROUP BY 
                ct.name
            ORDER BY 
                total_count DESC
        """
        
        df = db.query_to_dataframe(query, tuple(params))
        return df
    else:
        return create_sample_car_type_stats(region_id, start_date, end_date)

# 제조사별 통계 로드
def load_manufacturer_stats(region_id=None, car_type_id=None, start_date=None, end_date=None):
    connection_successful = check_db_connection()
    if connection_successful:
        params = []
        where_clauses = []
        
        if region_id:
            where_clauses.append("cr.region_id = %s")
            params.append(region_id)
        
        if car_type_id:
            where_clauses.append("cr.car_type_id = %s")
            params.append(car_type_id)
        
        if start_date:
            where_clauses.append("cr.registration_date >= %s")
            params.append(start_date.strftime('%Y-%m-%d'))
        
        if end_date:
            where_clauses.append("cr.registration_date <= %s")
            params.append(end_date.strftime('%Y-%m-%d'))
        
        where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"
        
        query = f"""
            SELECT 
                m.name AS manufacturer_name, 
                SUM(cr.registration_count) AS total_count
            FROM 
                car_registration cr
            JOIN 
                car_models cm ON cr.car_model_id = cm.id
            JOIN 
                manufacturers m ON cm.manufacturer_id = m.id
            WHERE 
                {where_clause}
            GROUP BY 
                m.name
            ORDER BY 
                total_count DESC
        """
        
        df = db.query_to_dataframe(query, tuple(params))
        return df
    else:
        return create_sample_manufacturer_stats(region_id, car_type_id, start_date, end_date)

# 월별 추이 로드
def load_monthly_trend(region_id=None, car_type_id=None, months=12):
    connection_successful = check_db_connection()
    if connection_successful:
        params = []
        where_clauses = []
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30*months)
        
        where_clauses.append("cr.registration_date BETWEEN %s AND %s")
        params.append(start_date.strftime('%Y-%m-%d'))
        params.append(end_date.strftime('%Y-%m-%d'))
        
        if region_id:
            where_clauses.append("cr.region_id = %s")
            params.append(region_id)
        
        if car_type_id:
            where_clauses.append("cr.car_type_id = %s")
            params.append(car_type_id)
        
        where_clause = " AND ".join(where_clauses)
        
        query = f"""
            SELECT 
                DATE_FORMAT(cr.registration_date, '%Y-%m') AS month,
                SUM(cr.registration_count) AS total_count
            FROM 
                car_registration cr
            WHERE 
                {where_clause}
            GROUP BY 
                DATE_FORMAT(cr.registration_date, '%Y-%m')
            ORDER BY 
                month
        """
        
        df = db.query_to_dataframe(query, tuple(params))
        return df
    else:
        return create_sample_monthly_trend(region_id, car_type_id, months)

# 메인 함수
def main():
    st.markdown('<div class="main-header">자동차 등록 현황 조회</div>', unsafe_allow_html=True)
    
    # 연결 확인
    connection_successful = check_db_connection()
    if not connection_successful:
        st.warning("데이터베이스에 연결할 수 없습니다. 샘플 데이터를 사용합니다.")
        
    # 데이터 로드
    regions, region_dict = load_regions()
    car_types, car_type_dict = load_car_types()
    
    # 필터 섹션
    st.markdown('<div class="sub-header">검색 필터</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 지역 선택
            selected_region = st.selectbox(
                "지역 선택",
                options=[None] + [region['id'] for region in regions],
                format_func=lambda x: "전체 지역" if x is None else region_dict.get(x, "")
            )
            
            # 차종 선택
            selected_car_type = st.selectbox(
                "차종 선택",
                options=[None] + [car_type['id'] for car_type in car_types],
                format_func=lambda x: "전체 차종" if x is None else car_type_dict.get(x, "")
            )
        
        with col2:
            # 날짜 범위 선택
            today = datetime.now()
            one_year_ago = today - timedelta(days=365)
            
            start_date = st.date_input(
                "시작 날짜",
                value=one_year_ago,
                max_value=today
            )
            
            end_date = st.date_input(
                "종료 날짜",
                value=today,
                min_value=start_date,
                max_value=today
            )
        
        # 검색 버튼
        search_button = st.button("검색", type="primary")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 검색 결과 표시
    if search_button:
        st.markdown('<div class="sub-header">검색 결과</div>', unsafe_allow_html=True)
        
        # 등록 현황 데이터 로드
        registration_data = load_registration_data(
            region_id=selected_region,
            car_type_id=selected_car_type,
            start_date=start_date,
            end_date=end_date
        )
        
        if registration_data.empty:
            st.warning("검색 조건에 맞는 데이터가 없습니다.")
        else:
            # 총 등록 대수 표시
            total_count = registration_data['registration_count'].sum()
            st.markdown(f"### 총 등록 대수: {total_count:,}대")
            
            # 탭 생성
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "상세 데이터", "지역별 현황", "차종별 현황", "제조사별 현황", "월별 추이"
            ])
            
            # 탭 1: 상세 데이터
            with tab1:
                # 데이터 표시 전 포맷팅
                display_df = registration_data.copy()
                display_df['registration_date'] = pd.to_datetime(display_df['registration_date']).dt.strftime('%Y-%m-%d')
                display_df = display_df.rename(columns={
                    'registration_date': '등록일',
                    'region_name': '지역',
                    'car_type_name': '차종',
                    'car_model_name': '모델명',
                    'manufacturer_name': '제조사',
                    'registration_count': '등록대수'
                })
                
                st.dataframe(display_df[['등록일', '지역', '차종', '제조사', '모델명', '등록대수']], use_container_width=True)
                
                # CSV 다운로드 버튼
                csv = display_df.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label="CSV 다운로드",
                    data=csv,
                    file_name=f"car_registration_data_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            
            # 탭 2: 지역별 현황
            with tab2:
                region_stats = load_region_stats(
                    car_type_id=selected_car_type,
                    start_date=start_date,
                    end_date=end_date
                )
                
                if not region_stats.empty:
                    # 막대 차트
                    fig = px.bar(
                        region_stats,
                        x='region_name',
                        y='total_count',
                        title='지역별 등록 현황',
                        labels={'region_name': '지역', 'total_count': '등록 대수'},
                        color='total_count',
                        color_continuous_scale='Blues'
                    )
                    fig.update_layout(height=500)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # 데이터 테이블
                    display_df = region_stats.reset_index(drop=True)
                    st.dataframe(display_df, use_container_width=True)
            
            # 탭 3: 차종별 현황
            with tab3:
                car_type_stats = load_car_type_stats(
                    region_id=selected_region,
                    start_date=start_date,
                    end_date=end_date
                )
                
                if not car_type_stats.empty:
                    # 파이 차트
                    fig = px.pie(
                        car_type_stats,
                        values='total_count',
                        names='car_type',
                        title='차종별 등록 현황',
                        hole=0.4
                    )
                    fig.update_layout(height=500)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # 데이터 테이블
                    display_df = car_type_stats.reset_index(drop=True)
                    st.dataframe(display_df, use_container_width=True)
            
            # 탭 4: 제조사별 현황
            with tab4:
                manufacturer_stats = load_manufacturer_stats(
                    region_id=selected_region,
                    car_type_id=selected_car_type,
                    start_date=start_date,
                    end_date=end_date
                )
                
                if not manufacturer_stats.empty:
                    # 막대 차트
                    fig = px.bar(
                        manufacturer_stats.head(10),
                        x='manufacturer_name',
                        y='total_count',
                        title='제조사별 등록 현황 (상위 10개)',
                        labels={'manufacturer_name': '제조사', 'total_count': '등록 대수'},
                        color='total_count',
                        color_continuous_scale='Viridis'
                    )
                    fig.update_layout(height=500)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # 데이터 테이블
                    display_df = manufacturer_stats.reset_index(drop=True)
                    st.dataframe(display_df, use_container_width=True)
            
            # 탭 5: 월별 추이
            with tab5:
                monthly_trend = load_monthly_trend(
                    region_id=selected_region,
                    car_type_id=selected_car_type
                )
                
                if not monthly_trend.empty:
                    # 라인 차트
                    fig = px.line(
                        monthly_trend,
                        x='month',
                        y='total_count',
                        title='월별 자동차 등록 추이',
                        labels={'month': '월', 'total_count': '등록 대수'},
                        markers=True
                    )
                    fig.update_layout(height=500)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # 데이터 테이블
                    display_df = monthly_trend.reset_index(drop=True)
                    st.dataframe(display_df, use_container_width=True)

if __name__ == "__main__":
    main() 