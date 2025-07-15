# 향수 추천 플랫폼 

AI 기반 향수 추천 및 제조법 제공 서비스입니다. 사용자의 나이, 성별, 성격, 계절 선호도 등을 분석하여 개인화된 향수를 추천하고, 직접 제조할 수 있는 레시피를 제공합니다.

## 주요 실행/관리 스크립트

- `start_project.py` : 전체 개발환경 자동 세팅 및 서버 실행 통합 스크립트
- `run_backend.py` : 백엔드(FastAPI) 서버 실행 (의존성 설치, DB 초기화 포함)
- `run_backend_conda.py` : Conda 환경에서 백엔드 서버 실행
- `run_frontend.py` : 프론트엔드(React) 개발 서버 실행
- `train_model.py` : 전체 데이터로 추천 모델 훈련 및 저장
- `force_retrain.py` : 최신 데이터로 추천 모델 강제 재훈련
- `test_model.py` : 저장된 추천 모델의 예측/추천 이유 테스트
- `process_excel_data.py` : 엑셀 데이터 전처리 및 멀티라벨 모델 훈련/저장
- `check_feedback.py` : 피드백 데이터 통계, 분포, 모델 재훈련 필요성 등 분석
- `check_labels.py` : DB/엑셀의 향수 카테고리 분포 비교 분석
- `reset_feedback.py` : 피드백 데이터 전체/일부 초기화, 백업, 날짜별 초기화 등


## 주요 기능

### 백엔드 (FastAPI)
- **사용자 관리**: 회원가입, 프로필 관리, 선호도 설정
- **향수 데이터베이스**: 다양한 향수 정보 및 제조법 저장
- **AI 추천 시스템**: 머신러닝 기반 개인화 추천
- **REST API**: 프론트엔드와 통신하는 API 엔드포인트

### 프론트엔드 (React)
- **반응형 웹 디자인**: 모바일/데스크톱 최적화
- **향수 추천 플로우**: 단계별 질문을 통한 추천
- **향수 상세 정보**: 향수 정보 및 제조법 표시
- **사용자 피드백**: 추천 결과에 대한 평가 시스템

### AI/ML
- **Random Forest 모델**: 사용자 특성 기반 향수 카테고리 예측
- **개인화 알고리즘**: 나이, 성별, 성격, 계절 매칭
- **피드백 학습**: 사용자 평가를 통한 모델 개선

## 기술 스택

### 백엔드
- **Python 3.8+**
- **FastAPI**: 고성능 웹 프레임워크
- **SQLAlchemy**: ORM
- **SQLite**: 개발용 데이터베이스 (MySQL/PostgreSQL 지원)
- **Scikit-learn**: 머신러닝 라이브러리
- **Pydantic**: 데이터 검증

### 프론트엔드
- **React 18**
- **Tailwind CSS**: 스타일링
- **React Router**: 라우팅
- **Axios**: HTTP 클라이언트
- **Lucide React**: 아이콘
- **Framer Motion**: 애니메이션

## AI/ML 주요 라이브러리(툴)

- **scikit-learn** : 머신러닝 모델(랜덤포레스트, 멀티라벨 분류, 전처리, 평가 등)
- **pandas** : 데이터프레임 기반 데이터 처리/분석
- **numpy** : 수치 연산 및 배열 처리
- **joblib** : 모델 및 전처리 객체 직렬화/저장/로드

## 설치 및 실행

### 1. 저장소 클론
```bash
git clone <repository-url>
cd perfume-recommendation
```

### 2. 백엔드 설정
```bash
# Python 가상환경 생성 (선택사항)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 데이터베이스 초기화 및 샘플 데이터 생성
cd backend
python init_data.py

# 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 프론트엔드 설정
```bash
# 새 터미널에서
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm start
```

### 4. 접속
- **백엔드 API**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs
- **프론트엔드**: http://localhost:3000

## 데이터베이스 구조

### 주요 테이블
- **users**: 사용자 정보 (나이, 성별, 성격, 계절 선호도)
- **perfumes**: 향수 정보 (이름, 브랜드, 카테고리, 노트 등)
- **perfume_recipes**: 향수 제조법 (원료, 비율, 노트)
- **user_preferences**: 사용자 선호도 (카테고리, 가격대, 강도 등)
- **recommendations**: 추천 기록 (추천 결과, 피드백)

## AI 모델

### 추천 알고리즘
1. **특성 분석**: 나이, 성별, 성격, 계절 선호도
2. **카테고리 예측**: Random Forest로 향수 카테고리 분류
3. **필터링**: 예측된 카테고리 내에서 추가 조건 적용
4. **랭킹**: 매칭 점수 기반 최종 추천

## API 엔드포인트

### 사용자 관리
- `POST /api/users/` - 사용자 등록
- `GET /api/users/` - 사용자 목록
- `GET /api/users/{id}` - 사용자 정보
- `PUT /api/users/{id}` - 사용자 정보 수정

### 향수 관리
- `GET /api/perfumes/` - 향수 목록
- `GET /api/perfumes/{id}` - 향수 상세 정보
- `GET /api/perfumes/{id}/recipes` - 향수 제조법

### 추천 시스템
- `POST /api/recommendations/` - 향수 추천
- `POST /api/recommendations/user/{id}` - 사용자별 추천
- `GET /api/recommendations/user/{id}/history` - 추천 기록
- `POST /api/recommendations/feedback/{id}` - 피드백 제출


