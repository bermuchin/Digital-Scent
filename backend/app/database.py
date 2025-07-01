from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# 데이터베이스 URL (개발용 SQLite 사용)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'perfume_recommendation.db')}")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 데이터베이스 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 향수 모델
class Perfume(Base):
    __tablename__ = "perfumes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    brand = Column(String(100))
    category = Column(String(50))  # "floral", "woody", "fresh", "oriental", "citrus"
    top_notes = Column(Text)
    middle_notes = Column(Text)
    base_notes = Column(Text)
    description = Column(Text)
    price_range = Column(String(20))  # "budget", "mid-range", "luxury"
    season_suitability = Column(String(50))  # "spring", "summer", "autumn", "winter", "all"
    personality_match = Column(String(50))  # "introvert", "extrovert", "balanced"
    age_group = Column(String(20))  # "young", "adult", "mature"
    gender_target = Column(String(20))  # "male", "female", "unisex"
    
    # 관계
    recipes = relationship("PerfumeRecipe", back_populates="perfume")

# 향수 제조법 모델
class PerfumeRecipe(Base):
    __tablename__ = "perfume_recipes"
    
    id = Column(Integer, primary_key=True, index=True)
    perfume_id = Column(Integer, ForeignKey("perfumes.id"))
    ingredient_name = Column(String(100))
    percentage = Column(Float)
    notes = Column(Text)
    
    # 관계
    perfume = relationship("Perfume", back_populates="recipes")

# 추천 기록 모델 (익명 사용자만)
class Recommendation(Base):
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    perfume_id = Column(Integer, ForeignKey("perfumes.id"))
    confidence_score = Column(Float)
    reason = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_liked = Column(Boolean, nullable=True)  # 사용자 피드백 