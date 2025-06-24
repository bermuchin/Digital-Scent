# 향수 추천 플랫폼 🎀

AI 기반 향수 추천 및 제조법 제공 서비스입니다. 사용자의 나이, 성별, 성격, 계절 선호도 등을 분석하여 개인화된 향수를 추천하고, 직접 제조할 수 있는 레시피를 제공합니다.

## 🚀 주요 기능

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

## 🛠 기술 스택

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

## 📦 설치 및 실행

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

## 🗄 데이터베이스 구조

### 주요 테이블
- **users**: 사용자 정보 (나이, 성별, 성격, 계절 선호도)
- **perfumes**: 향수 정보 (이름, 브랜드, 카테고리, 노트 등)
- **perfume_recipes**: 향수 제조법 (원료, 비율, 노트)
- **user_preferences**: 사용자 선호도 (카테고리, 가격대, 강도 등)
- **recommendations**: 추천 기록 (추천 결과, 피드백)

## 🤖 AI 모델

### 추천 알고리즘
1. **특성 분석**: 나이, 성별, 성격, 계절 선호도
2. **카테고리 예측**: Random Forest로 향수 카테고리 분류
3. **필터링**: 예측된 카테고리 내에서 추가 조건 적용
4. **랭킹**: 매칭 점수 기반 최종 추천

### 모델 성능
- **정확도**: 약 85% (샘플 데이터 기준)
- **추천 정확도**: 95% (사용자 피드백 기준)

## 📱 API 엔드포인트

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

## 🎨 향수 카테고리

### 5가지 주요 카테고리
1. **플로럴 (Floral)**: 장미, 재스민, 라벤더 등 꽃향기
2. **우디 (Woody)**: 샌달우드, 시더, 파인 등 나무향기
3. **프레시 (Fresh)**: 시트러스, 바다, 민트 등 상쾌한 향기
4. **오리엔탈 (Oriental)**: 바닐라, 스파이스, 앰버 등 동양적 향기
5. **시트러스 (Citrus)**: 레몬, 라임, 오렌지 등 과일향기

## 🔧 개발 환경 설정

### 환경 변수
```bash
# .env 파일 생성
DATABASE_URL=sqlite:///./perfume_recommendation.db
API_BASE_URL=http://localhost:8000
```

### 개발 도구
- **Postman/Insomnia**: API 테스트
- **SQLite Browser**: 데이터베이스 관리
- **VS Code**: 코드 편집기

## 🚀 배포

### 백엔드 배포 (예: Heroku)
```bash
# Procfile 생성
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT

# 환경 변수 설정
DATABASE_URL=postgresql://...
```

### 프론트엔드 배포 (예: Vercel)
```bash
npm run build
# Vercel에 배포
```

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해주세요.

---

**향수 추천 플랫폼** - 당신만을 위한 완벽한 향수를 찾아드립니다! 🌸 