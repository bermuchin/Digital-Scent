from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

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

# 추천 요청 스키마 (익명 사용자용)
class RecommendationRequest(BaseModel):
    age: Optional[int] = None
    gender: Optional[str] = None
    personality: Optional[str] = None
    cost: Optional[str] = None
    purpose: Optional[str] = None
    durability: Optional[str] = None
    fashionstyle: Optional[str] = None
    prefercolor: Optional[str] = None

# 추천 응답 스키마 (멀티라벨 지원)
class RecommendationResponse(BaseModel):
    id: int
    perfume: PerfumeDetail
    predicted_categories: List[str]  # 예측된 향수 카테고리들
    confidence_score: float
    reason: str
    match_factors: List[str]

# 추천 피드백 스키마
class RecommendationFeedback(BaseModel):
    is_liked: bool
    feedback_notes: Optional[str] = None 