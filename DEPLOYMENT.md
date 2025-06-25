# 🌐 향수 추천 플랫폼 배포 가이드

## 🚀 배포 옵션

### 1. **Vercel + Railway (추천)**

#### 프론트엔드 배포 (Vercel)
1. [Vercel](https://vercel.com)에 가입
2. GitHub 저장소 연결
3. 프로젝트 설정:
   - Framework Preset: `Create React App`
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `build`
4. 환경변수 설정:
   - `REACT_APP_API_URL`: 백엔드 URL (예: `https://your-app.railway.app`)

#### 백엔드 배포 (Railway)
1. [Railway](https://railway.app)에 가입
2. GitHub 저장소 연결
3. 프로젝트 설정:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. 환경변수 설정:
   - `DATABASE_URL`: PostgreSQL 데이터베이스 URL

### 2. **Netlify + Render**

#### 프론트엔드 배포 (Netlify)
1. [Netlify](https://netlify.com)에 가입
2. GitHub 저장소 연결
3. 빌드 설정:
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `build`

#### 백엔드 배포 (Render)
1. [Render](https://render.com)에 가입
2. GitHub 저장소 연결
3. 서비스 설정:
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 3. **Heroku (전체 스택)**

1. [Heroku](https://heroku.com)에 가입
2. Heroku CLI 설치
3. 명령어 실행:
```bash
heroku create your-app-name
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

## 📋 배포 전 체크리스트

### 프론트엔드
- [ ] `package.json`에 build 스크립트 확인
- [ ] 환경변수 `REACT_APP_API_URL` 설정
- [ ] API 호출 URL이 올바른지 확인

### 백엔드
- [ ] `requirements.txt` 파일 존재
- [ ] `Procfile` 파일 생성
- [ ] CORS 설정 확인
- [ ] 데이터베이스 연결 설정

### 데이터베이스
- [ ] PostgreSQL 데이터베이스 생성
- [ ] 환경변수 `DATABASE_URL` 설정
- [ ] 초기 데이터 마이그레이션

## 🔧 환경변수 설정

### 프론트엔드 (Vercel/Netlify)
```
REACT_APP_API_URL=https://your-backend-url.railway.app
```

### 백엔드 (Railway/Render)
```
DATABASE_URL=postgresql://username:password@host:port/database
PORT=8000
```

## 🐛 문제 해결

### 일반적인 문제들
1. **CORS 오류**: 백엔드 CORS 설정 확인
2. **API 연결 실패**: 환경변수 URL 확인
3. **빌드 실패**: 의존성 설치 확인
4. **데이터베이스 연결 실패**: DATABASE_URL 확인

### 로그 확인
- Vercel: Dashboard > Functions > Logs
- Railway: Deployments > Logs
- Render: Services > Logs

## 📞 지원

문제가 발생하면 다음을 확인하세요:
1. 브라우저 개발자 도구의 콘솔 로그
2. 서버 로그
3. 네트워크 탭에서 API 요청/응답 