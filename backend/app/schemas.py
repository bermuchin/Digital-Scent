from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# 사용자 관련 스키마
class UserBase(BaseModel):
    username: str
    email: EmailStr
    age: int
    gender: str
    personality: str
    season_preference: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# 향수 관련 스키마
class PerfumeBase(BaseModel):
    name: str
    brand: str
    category: str
    top_notes: str
    middle_notes: str
    base_notes: str
    description: str
    price_range: str
    season_suitability: str
    personality_match: str
    age_group: str
    gender_target: str

class PerfumeCreate(PerfumeBase):
    pass

class Perfume(PerfumeBase):
    id: int
    
    class Config:
        from_attributes = True

# 향수 제조법 스키마
class PerfumeRecipeBase(BaseModel):
    ingredient_name: str
    percentage: float
    notes: Optional[str] = None

class PerfumeRecipeCreate(PerfumeRecipeBase):
    pass

class PerfumeRecipe(PerfumeRecipeBase):
    id: int
    perfume_id: int
    
    class Config:
        from_attributes = True

# 향수 상세 정보 (제조법 포함)
class PerfumeDetail(Perfume):
    recipes: List[PerfumeRecipe] = []

# 사용자 선호도 스키마
class UserPreferenceBase(BaseModel):
    category_preference: str
    price_preference: str
    intensity_preference: str
    longevity_preference: str

class UserPreferenceCreate(UserPreferenceBase):
    pass

class UserPreference(UserPreferenceBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True

# 추천 요청 스키마
class RecommendationRequest(BaseModel):
    age: int
    gender: str
    personality: str
    season_preference: str
    category_preference: Optional[str] = None
    price_preference: Optional[str] = None
    intensity_preference: Optional[str] = None
    longevity_preference: Optional[str] = None

# 추천 응답 스키마
class RecommendationResponse(BaseModel):
    id: int
    perfume: PerfumeDetail
    confidence_score: float
    reason: str
    match_factors: List[str]

# 추천 피드백 스키마
class RecommendationFeedback(BaseModel):
    is_liked: bool
    feedback_notes: Optional[str] = None

# 사용자 등록 스키마
class UserRegistration(BaseModel):
    username: str
    email: EmailStr
    age: int
    gender: str
    personality: str
    season_preference: str
    preferences: Optional[UserPreferenceCreate] = None 