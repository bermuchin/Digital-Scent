from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import users, perfumes, recommendations
from app.database import engine, Base

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="향수 추천 API",
    description="사용자 선호도 기반 향수 추천 및 제조법 제공 서비스",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(perfumes.router, prefix="/api/perfumes", tags=["perfumes"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["recommendations"])

@app.get("/")
async def root():
    return {"message": "향수 추천 API에 오신 것을 환영합니다!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 