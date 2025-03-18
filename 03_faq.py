import os
import sys
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import re

# 상위 디렉토리 추가하여 database 모듈 import 가능하게 설정
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.db_connector import DatabaseConnector
from database.models import (
    Industry, Company, FAQCategory, CompanyFAQ
)

# 페이지 설정
st.set_page_config(
    page_title="자동차 FAQ",
    page_icon="❓",
    layout="wide"
)

# 스타일 설정
st.markdown("""
<style>
    .main-header {
        font-size: 24px;
        font-weight: bold;
        color: #ffffff;
        background-color: #1E3F66;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
        text-align: center;
    }
    .sub-header {
        font-size: 20px;
        font-weight: bold;
        color: #1E3F66;
        margin-top: 30px;
        margin-bottom: 15px;
        border-bottom: 2px solid #1E3F66;
        padding-bottom: 5px;
    }
    .filter-section {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .faq-card {
        background-color: #f8f9fa;
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    .faq-question {
        background-color: #f0f2f6;
        border-left: 4px solid #1E3F66;
        padding: 10px 15px;
        margin-bottom: 10px;
        border-radius: 0 5px 5px 0;
        cursor: pointer;
        font-weight: bold;
    }
    .faq-question:hover {
        background-color: #e0e2e6;
    }
    .faq-answer {
        padding: 15px;
        background-color: #f9f9f9;
        border-radius: 5px;
        margin-bottom: 20px;
        border-left: 4px solid #4CAF50;
        color: #333333;
        font-size: 16px;
        line-height: 1.6;
    }
    .search-container {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .highlight {
        background-color: yellow;
        padding: 0 2px;
    }
    .company-name {
        font-size: 14px;
        color: #1E3F66;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .company-card {
        background-color: #f9f9f9;
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 20px;
        border-left: 4px solid #1E3F66;
    }
</style>
""", unsafe_allow_html=True)

# 데이터베이스 연결 확인
@st.cache_resource
def check_db_connection():
    try:
        db = DatabaseConnector()
        db.connect()
        return db.is_connected()
    except Exception as e:
        st.warning(f"데이터베이스 연결에 실패했습니다: {e}")
        st.info("샘플 데이터로 실행됩니다. 일부 기능이 제한됩니다.")
        return False

# 샘플 산업 데이터 생성
def create_sample_industries():
    return [
        {'id': 1, 'name': '자동차 제조'},
        {'id': 2, 'name': '자동차 부품'},
        {'id': 3, 'name': '자동차 판매'},
        {'id': 4, 'name': '정비 및 수리'},
        {'id': 5, 'name': '자동차 보험'}
    ]

# 샘플 기업 데이터 생성
def create_sample_companies():
    return [
        {'id': 1, 'name': '현대자동차', 'industry_id': 1},
        {'id': 2, 'name': '기아자동차', 'industry_id': 1},
        {'id': 3, 'name': '삼성SDI', 'industry_id': 2},
        {'id': 4, 'name': 'LG화학', 'industry_id': 2},
        {'id': 5, 'name': '현대모비스', 'industry_id': 2},
        {'id': 6, 'name': '오토허브', 'industry_id': 3},
        {'id': 7, 'name': '카라이프', 'industry_id': 3},
        {'id': 8, 'name': '오토오아시스', 'industry_id': 4},
        {'id': 9, 'name': '스피드메이트', 'industry_id': 4},
        {'id': 10, 'name': '삼성화재', 'industry_id': 5}
    ]

# 샘플 FAQ 카테고리 데이터 생성
def create_sample_faq_categories():
    return [
        {'id': 1, 'name': '제품 정보'},
        {'id': 2, 'name': '구매 및 결제'},
        {'id': 3, 'name': 'A/S 및 수리'},
        {'id': 4, 'name': '보증 및 보험'},
        {'id': 5, 'name': '기타 문의'}
    ]

# 샘플 FAQ 데이터 생성
def create_sample_faqs(company_id=None, category_id=None, keyword=None):
    all_faqs = [
        {'id': 1, 'company_id': 1, 'company_name': '현대자동차', 'question': '차량의 기본 사양은 어떻게 되나요?', 'answer': '당사 차량의 기본 사양은 모델별로 상이하며, 공식 웹사이트에서 확인하실 수 있습니다. 기본적으로 에어백, ABS, 후방 카메라 등이 기본 장착됩니다.'},
        {'id': 2, 'company_id': 1, 'company_name': '현대자동차', 'question': '할부 구매 시 이자율은 어떻게 되나요?', 'answer': '할부 이자율은 고객님의 신용도와 할부 기간에 따라 다르게 책정됩니다. 현재 기본 할부 이자율은 연 4.5%~8.9%입니다.'},
        {'id': 3, 'company_id': 1, 'company_name': '현대자동차', 'question': '정기점검은 얼마나 자주 받아야 하나요?', 'answer': '정기점검은 1년에 1회 또는 주행거리 15,000km마다 받으시는 것을 권장합니다. 엔진오일은 6개월 또는 5,000km마다 교체하는 것이 좋습니다.'},
        {'id': 4, 'company_id': 1, 'company_name': '현대자동차', 'question': '신차 보증기간은 어떻게 되나요?', 'answer': '일반 승용차의 경우 기본 보증기간은 3년 또는 60,000km이며, 파워트레인은 5년 또는 100,000km입니다. 하이브리드 모델의 경우 하이브리드 시스템은 8년 또는 160,000km입니다.'},
        {'id': 5, 'company_id': 2, 'company_name': '기아자동차', 'question': '전기차 주행거리는 얼마나 되나요?', 'answer': '전기차의 주행거리는 모델에 따라 다르며, 당사의 최신 전기차 모델은 1회 충전 시 최대 450km까지 주행 가능합니다. 단, 주행 환경과 운전 습관에 따라 달라질 수 있습니다.'},
        {'id': 6, 'company_id': 2, 'company_name': '기아자동차', 'question': '차량 구매 시 필요한 서류는 무엇인가요?', 'answer': '차량 구매 시 필요한 서류는 신분증, 자동차 등록에 필요한 주민등록등본, 자동차세 납부를 위한 통장 사본 등이 필요합니다. 할부 구매 시에는 추가 서류가 필요할 수 있습니다.'},
        {'id': 7, 'company_id': 2, 'company_name': '기아자동차', 'question': '차량 고장 시 무상 견인 서비스를 받을 수 있나요?', 'answer': '네, 당사에서 구매한 차량은 보증기간 내에 차량 고장 시 전국 어디서나 무상 견인 서비스를 제공받으실 수 있습니다. 견인 서비스는 고객센터로 연락하시면 안내받으실 수 있습니다.'},
        {'id': 8, 'company_id': 3, 'company_name': '제네시스', 'question': '배터리 수명은 얼마나 되나요?', 'answer': '당사의 자동차 배터리는 일반적으로 3-5년의 수명을 가지고 있습니다. 전기차 배터리의 경우 8-10년 또는 160,000km까지 보증이 제공됩니다.'},
        {'id': 9, 'company_id': 3, 'company_name': '제네시스', 'question': '배터리 충전 시간은 얼마나 소요되나요?', 'answer': '급속 충전기 사용 시 약 30-40분 내에 80%까지 충전 가능하며, 완속 충전의 경우 약 6-8시간이 소요됩니다. 충전 시간은 배터리 잔량과 환경에 따라 달라질 수 있습니다.'},
        {'id': 10, 'company_id': 4, 'company_name': 'BMW', 'question': '부품 가격은 어디서 확인할 수 있나요?', 'answer': '부품 가격은 당사 공식 웹사이트 또는 가까운 대리점에서 확인하실 수 있습니다. 또한 고객센터로 문의하시면 정확한 부품 가격을 안내받으실 수 있습니다.'}
    ]
    
    filtered_faqs = all_faqs
    
    # 기업 ID로 필터링
    if company_id is not None:
        filtered_faqs = [faq for faq in filtered_faqs if faq['company_id'] == company_id]
    
    # 키워드로 필터링
    if keyword is not None and keyword.strip():
        keyword = keyword.lower()
        filtered_faqs = [faq for faq in filtered_faqs if keyword in faq['question'].lower() or keyword in faq['answer'].lower()]
    
    return pd.DataFrame(filtered_faqs)

# 샘플 산업별 FAQ 통계 생성
def create_sample_industry_faq_stats():
    industries = create_sample_industries()
    data = []
    
    for industry in industries:
        count = np.random.randint(20, 200)
        data.append({
            'industry_name': industry['name'],
            'faq_count': count
        })
    
    return pd.DataFrame(data).sort_values('faq_count', ascending=False)

# 샘플 카테고리별 FAQ 통계 생성
def create_sample_category_faq_stats():
    categories = create_sample_faq_categories()
    data = []
    
    for category in categories:
        count = np.random.randint(30, 150)
        data.append({
            'category_name': category['name'],
            'faq_count': count
        })
    
    return pd.DataFrame(data).sort_values('faq_count', ascending=False)

# 샘플 인기 FAQ 생성
def create_sample_popular_faqs(limit=10):
    all_faqs = create_sample_faqs()
    return all_faqs.sort_values('view_count', ascending=False).head(limit)

# 샘플 최근 FAQ 생성
def create_sample_recent_faqs(limit=10):
    all_faqs = create_sample_faqs()
    all_faqs['created_at'] = pd.to_datetime(all_faqs['created_at'])
    return all_faqs.sort_values('created_at', ascending=False).head(limit)

# 기업 데이터 로드
@st.cache_data(ttl=3600)
def load_companies():
    connection_successful = check_db_connection()
    if connection_successful:
        companies = Company.get_all()
        return companies, {company['id']: company['name'] for company in companies}
    else:
        companies = create_sample_companies()
        return companies, {company['id']: company['name'] for company in companies}

# 산업 데이터 로드
@st.cache_data(ttl=3600)
def load_industries():
    connection_successful = check_db_connection()
    if connection_successful:
        industries = Industry.get_all()
        return industries, {industry['id']: industry['name'] for industry in industries}
    else:
        industries = create_sample_industries()
        return industries, {industry['id']: industry['name'] for industry in industries}

# FAQ 카테고리 데이터 로드
@st.cache_data(ttl=3600)
def load_faq_categories():
    connection_successful = check_db_connection()
    if connection_successful:
        categories = FAQCategory.get_all()
        return categories, {category['id']: category['name'] for category in categories}
    else:
        categories = create_sample_faq_categories()
        return categories, {category['id']: category['name'] for category in categories}

# 기업 FAQ 데이터 로드
def load_company_faqs(company_id=None, category_id=None, keyword=None):
    connection_successful = check_db_connection()
    if connection_successful:
        params = []
        where_clauses = []
        
        if company_id:
            where_clauses.append("cf.company_id = %s")
            params.append(company_id)
        
        if category_id:
            where_clauses.append("cf.category_id = %s")
            params.append(category_id)
        
        if keyword and keyword.strip():
            where_clauses.append("(cf.question LIKE %s OR cf.answer LIKE %s)")
            keyword_param = f"%{keyword}%"
            params.append(keyword_param)
            params.append(keyword_param)
        
        where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"
        
        query = f"""
            SELECT 
                cf.id,
                cf.question,
                cf.answer,
                cf.view_count,
                cf.created_at,
                c.name AS company_name,
                fc.name AS category_name
            FROM 
                company_faqs cf
            JOIN 
                companies c ON cf.company_id = c.id
            JOIN 
                faq_categories fc ON cf.category_id = fc.id
            WHERE 
                {where_clause}
            ORDER BY 
                cf.view_count DESC
        """
        
        df = DatabaseConnector().query_to_dataframe(query, tuple(params))
        return df
    else:
        return create_sample_faqs(company_id, category_id, keyword)

# 산업별 FAQ 통계 데이터 로드
@st.cache_data(ttl=3600)
def load_industry_faq_stats():
    connection_successful = check_db_connection()
    if connection_successful:
        query = """
            SELECT 
                i.name AS industry_name,
                COUNT(cf.id) AS faq_count
            FROM 
                industries i
            JOIN 
                companies c ON i.id = c.industry_id
            JOIN 
                company_faqs cf ON c.id = cf.company_id
            GROUP BY 
                i.name
            ORDER BY 
                faq_count DESC
        """
        
        df = DatabaseConnector().query_to_dataframe(query)
        return df
    else:
        return create_sample_industry_faq_stats()

# 카테고리별 FAQ 통계 데이터 로드
@st.cache_data(ttl=3600)
def load_category_faq_stats():
    connection_successful = check_db_connection()
    if connection_successful:
        query = """
            SELECT 
                fc.name AS category_name,
                COUNT(cf.id) AS faq_count
            FROM 
                faq_categories fc
            JOIN 
                company_faqs cf ON fc.id = cf.category_id
            GROUP BY 
                fc.name
            ORDER BY 
                faq_count DESC
        """
        
        df = DatabaseConnector().query_to_dataframe(query)
        return df
    else:
        return create_sample_category_faq_stats()

# 인기 FAQ 데이터 로드
@st.cache_data(ttl=3600)
def load_popular_faqs(limit=10):
    connection_successful = check_db_connection()
    if connection_successful:
        query = f"""
            SELECT 
                cf.id,
                cf.question,
                cf.answer,
                cf.view_count,
                cf.created_at,
                c.name AS company_name,
                fc.name AS category_name
            FROM 
                company_faqs cf
            JOIN 
                companies c ON cf.company_id = c.id
            JOIN 
                faq_categories fc ON cf.category_id = fc.id
            ORDER BY 
                cf.view_count DESC
            LIMIT {limit}
        """
        
        df = DatabaseConnector().query_to_dataframe(query)
        return df
    else:
        return create_sample_popular_faqs(limit)

# 최근 FAQ 데이터 로드
@st.cache_data(ttl=3600)
def load_recent_faqs(limit=10):
    connection_successful = check_db_connection()
    if connection_successful:
        query = f"""
            SELECT 
                cf.id,
                cf.question,
                cf.answer,
                cf.view_count,
                cf.created_at,
                c.name AS company_name,
                fc.name AS category_name
            FROM 
                company_faqs cf
            JOIN 
                companies c ON cf.company_id = c.id
            JOIN 
                faq_categories fc ON cf.category_id = fc.id
            ORDER BY 
                cf.created_at DESC
            LIMIT {limit}
        """
        
        df = DatabaseConnector().query_to_dataframe(query)
        return df
    else:
        return create_sample_recent_faqs(limit)

# 텍스트 하이라이트 함수
def highlight_text(text, search_term):
    if not search_term or not text:
        return text
    
    pattern = re.compile(f"({re.escape(search_term)})", re.IGNORECASE)
    highlighted = pattern.sub(r'<span class="highlight">\1</span>', text)
    return highlighted

# FAQ 카드 표시 함수
def display_faq_card(faq, keyword=None):
    question = faq['question']
    answer = faq['answer']
    
    if keyword and keyword.strip():
        question = highlight_text(question, keyword)
        answer = highlight_text(answer, keyword)
    
    st.markdown(f"""
    <div class="faq-card">
        <div class="faq-question">{question}</div>
        <div class="faq-answer">{answer}</div>
        <div class="faq-meta">
            <span>기업: {faq['company_name']}</span> | 
            <span>카테고리: {faq['category_name']}</span> | 
            <span>조회수: {faq['view_count']}</span> | 
            <span>등록일: {pd.to_datetime(faq['created_at']).strftime('%Y-%m-%d')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# FAQ 데이터 로드
@st.cache_data(ttl=3600)
def load_faq_data():
    try:
        db = DatabaseConnector()
        db.connect()
        
        if not db.is_connected():
            st.warning("데이터베이스 연결이 활성화되지 않았습니다. 샘플 데이터를 생성합니다.")
            return create_sample_faqs(), pd.DataFrame(create_sample_companies())
        
        # FAQ 데이터 조회 쿼리
        query = """
            SELECT 
                f.id, f.question, f.answer, 
                c.name as company_name,
                c.id as company_id
            FROM faq_table f
            JOIN car_company_table c ON f.car_company_id = c.id
        """
        
        # 회사 데이터 쿼리
        company_query = """
            SELECT id, name
            FROM car_company_table
            ORDER BY name
        """
        
        faq_df = db.query_to_dataframe(query)
        company_df = db.query_to_dataframe(company_query)
        
        db.disconnect()
        
        if faq_df.empty:
            st.warning("FAQ 데이터를 찾을 수 없습니다.")
            return create_sample_faqs(), pd.DataFrame(create_sample_companies())
        
        return faq_df, company_df
    
    except Exception as e:
        st.error(f"데이터베이스 연결 중 오류가 발생했습니다: {e}")
        return create_sample_faqs(), pd.DataFrame(create_sample_companies())

# 메인 함수
def main():
    st.markdown('<div class="main-header">자동차 FAQ</div>', unsafe_allow_html=True)
    
    # 데이터베이스 연결 체크
    connected = check_db_connection()
    
    try:
        # FAQ 데이터 로드
        faq_data, company_data = load_faq_data()
        
        if faq_data.empty:
            st.warning("FAQ 데이터를 불러올 수 없습니다. 샘플 데이터를 사용합니다.")
            faq_data = create_sample_faqs()
            company_data = pd.DataFrame(create_sample_companies())
    except Exception as e:
        st.error(f"데이터 로드 중 오류가 발생했습니다: {e}")
        faq_data = create_sample_faqs()
        company_data = pd.DataFrame(create_sample_companies())
    
    # 검색 기능
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    search_term = st.text_input("질문 검색:", placeholder="검색어를 입력하세요...")
    
    # 회사 필터 추가
    company_options = ["전체"] + sorted(company_data['name'].unique().tolist())
    selected_company = st.selectbox("회사 선택:", options=company_options)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 필터링된 데이터 준비
    filtered_data = faq_data.copy()
    
    # 회사 필터 적용
    if selected_company != "전체":
        filtered_data = filtered_data[filtered_data['company_name'] == selected_company]
    
    # 검색어가 있으면 검색 결과 표시
    if search_term:
        st.markdown(f'<div class="sub-header">"{search_term}" 검색 결과</div>', unsafe_allow_html=True)
        
        # 질문이나 답변에 검색어가 포함된 FAQ 필터링
        mask = (filtered_data['question'].str.contains(search_term, case=False) | 
                filtered_data['answer'].str.contains(search_term, case=False))
        search_results = filtered_data[mask]
        
        if search_results.empty:
            st.info(f'"{search_term}"에 대한 검색 결과가 없습니다.')
        else:
            st.write(f"총 {len(search_results)}개의 결과를 찾았습니다.")
            
            for _, faq in search_results.iterrows():
                with st.expander(faq['question']):
                    st.markdown(f'<div class="company-name">{faq["company_name"]}</div>', unsafe_allow_html=True)
                    
                    # 검색어 강조 표시
                    highlighted_answer = highlight_text(faq['answer'], search_term)
                    st.markdown(f'<div class="faq-answer">{highlighted_answer}</div>', 
                                unsafe_allow_html=True)
    else:
        # 회사별 FAQ 표시
        companies = filtered_data['company_name'].unique()
        
        for company in companies:
            st.markdown(f'<div class="sub-header">{company}</div>', unsafe_allow_html=True)
            
            # 해당 회사의 FAQ 필터링
            company_faqs = filtered_data[filtered_data['company_name'] == company]
            
            for _, faq in company_faqs.iterrows():
                with st.expander(faq['question']):
                    st.markdown(f'<div class="faq-answer">{faq["answer"]}</div>', unsafe_allow_html=True)
    
    # 회사별 통계
    st.markdown('<div class="sub-header">회사별 FAQ 제공 현황</div>', unsafe_allow_html=True)
    
    # 회사별 질문 수 계산
    company_stats = faq_data.groupby('company_name').size().reset_index(name='FAQ 수')
    company_stats = company_stats.sort_values('FAQ 수', ascending=False)
    
    # 그래프와 데이터 나란히 표시
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # 그래프로 표시
        st.bar_chart(company_stats.set_index('company_name'))
    
    with col2:
        # 테이블 형식으로 표시
        st.dataframe(company_stats.rename(columns={'company_name': '회사명'}), use_container_width=True)

    # FAQ 작성 기능
    st.markdown('<div class="sub-header">새로운 FAQ 만들기</div>', unsafe_allow_html=True)
    st.write("자동차 관련 새로운 FAQ를 작성해보세요!")
    
    # 폼 생성
    with st.form("faq_form"):
        selected_company_id = st.selectbox(
            "회사 선택",
            options=company_data['id'].tolist(),
            format_func=lambda x: company_data[company_data['id'] == x]['name'].iloc[0]
        )
        new_question = st.text_area("질문:", height=100)
        new_answer = st.text_area("답변:", height=200)
        
        submitted = st.form_submit_button("FAQ 저장")
        
        if submitted and new_question and new_answer:
            try:
                db = DatabaseConnector()
                db.connect()
                
                if db.is_connected():
                    # FAQ 추가 쿼리
                    query = """
                        INSERT INTO faq_table 
                        (car_company_id, question, answer) 
                        VALUES (%s, %s, %s)
                    """
                    db.execute_update(query, (selected_company_id, new_question, new_answer))
                    db.disconnect()
                    
                    st.success("FAQ가 성공적으로 추가되었습니다!")
                    st.rerun()  # 페이지 새로고침
            except Exception as e:
                st.error(f"FAQ 추가 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main() 