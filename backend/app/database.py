from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# 데이터베이스 URL (개발용 SQLite 사용)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./perfume_recommendation.db")

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

# 사용자 모델
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    age = Column(Integer)
    gender = Column(String(10))  # "male", "female", "other"
    personality = Column(String(50))  # "introvert", "extrovert", "balanced"
    season_preference = Column(String(20))  # "spring", "summer", "autumn", "winter"
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 관계
    preferences = relationship("UserPreference", back_populates="user")
    recommendations = relationship("Recommendation", back_populates="user")

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

# 사용자 선호도 모델
class UserPreference(Base):
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category_preference = Column(String(50))
    price_preference = Column(String(20))
    intensity_preference = Column(String(20))  # "light", "medium", "strong"
    longevity_preference = Column(String(20))  # "short", "medium", "long"
    
    # 관계
    user = relationship("User", back_populates="preferences")

# 추천 기록 모델
class Recommendation(Base):
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    perfume_id = Column(Integer, ForeignKey("perfumes.id"))
    confidence_score = Column(Float)
    reason = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_liked = Column(Boolean, nullable=True)  # 사용자 피드백
    
    # 관계
    user = relationship("User", back_populates="recommendations") 