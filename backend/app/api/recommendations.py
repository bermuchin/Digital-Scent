from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db, Perfume, Recommendation
from app.schemas import RecommendationRequest, RecommendationResponse, RecommendationFeedback
from app.models.recommendation_model import PerfumeRecommendationModel
import random

router = APIRouter()

# ML 모델 인스턴스 생성 및 로드
recommendation_model = PerfumeRecommendationModel()
try:
    recommendation_model.load_model()
    print("기존 모델을 성공적으로 로드했습니다.")
except Exception as e:
    print(f"모델 로드 실패, 새로 훈련합니다: {e}")
    recommendation_model.train()

@router.post("/", response_model=RecommendationResponse)
def get_recommendation(request: RecommendationRequest, db: Session = Depends(get_db)):
    """사용자 선호도에 따른 향수를 추천합니다."""
    # 입력 데이터 검증 및 기본값 설정
    age = request.age if request.age else 25
    gender = request.gender if request.gender and request.gender.strip() else "other"
    personality = request.personality if request.personality and request.personality.strip() else "balanced"
    season_preference = request.season_preference if request.season_preference and request.season_preference.strip() else "spring"
    
    # ML 모델로 향수 카테고리 예측
    predicted_category, confidence = recommendation_model.predict_category(
        age=age,
        gender=gender,
        personality=personality,
        season=season_preference
    )
    
    # 해당 카테고리의 향수들 조회
    query = db.query(Perfume).filter(Perfume.category == predicted_category)
    
    # 추가 필터링
    if age < 30:
        query = query.filter(Perfume.age_group == "young")
    elif age > 50:
        query = query.filter(Perfume.age_group == "mature")
    else:
        query = query.filter(Perfume.age_group == "adult")
    
    if gender != "other":
        query = query.filter(
            (Perfume.gender_target == gender) | 
            (Perfume.gender_target == "unisex")
        )
    
    if season_preference:
        query = query.filter(
            (Perfume.season_suitability == season_preference) |
            (Perfume.season_suitability == "all")
        )
    
    if personality:
        query = query.filter(Perfume.personality_match == personality)
    
    if request.price_preference:
        query = query.filter(Perfume.price_range == request.price_preference)
    
    # 결과가 없으면 필터를 완화
    perfumes = query.all()
    if not perfumes:
        # 카테고리만으로 다시 검색
        perfumes = db.query(Perfume).filter(Perfume.category == predicted_category).all()
    
    if not perfumes:
        raise HTTPException(status_code=404, detail="적합한 향수를 찾을 수 없습니다")
    
    # 랜덤하게 하나 선택 (실제로는 더 정교한 랭킹 알고리즘 사용)
    selected_perfume = random.choice(perfumes)
    
    # 추천 이유 생성
    reason = recommendation_model.get_recommendation_reason(
        predicted_category=predicted_category,
        age=age,
        gender=gender,
        personality=personality,
        season=season_preference
    )
    
    # 매칭 요소들
    match_factors = []
    if selected_perfume.personality_match == personality:
        match_factors.append("성격 매칭")
    if selected_perfume.season_suitability == season_preference:
        match_factors.append("계절 매칭")
    if selected_perfume.age_group in ["young", "adult", "mature"]:
        if (age < 30 and selected_perfume.age_group == "young") or \
           (30 <= age <= 50 and selected_perfume.age_group == "adult") or \
           (age > 50 and selected_perfume.age_group == "mature"):
            match_factors.append("연령대 매칭")
    
    # 추천 기록을 데이터베이스에 저장 (익명 사용자용)
    db_recommendation = Recommendation(
        perfume_id=selected_perfume.id,
        confidence_score=confidence,
        reason=reason
    )
    db.add(db_recommendation)
    db.commit()
    db.refresh(db_recommendation)
    
    return RecommendationResponse(
        id=db_recommendation.id,  # 추천 ID 추가
        perfume=selected_perfume,
        confidence_score=confidence,
        reason=reason,
        match_factors=match_factors
    )

@router.post("/feedback/{recommendation_id}")
def submit_recommendation_feedback(
    recommendation_id: int, 
    feedback: RecommendationFeedback, 
    db: Session = Depends(get_db)
):
    """추천에 대한 피드백을 제출합니다."""
    # 추천 기록 조회
    recommendation = db.query(Recommendation).filter(
        Recommendation.id == recommendation_id
    ).first()
    
    if recommendation is None:
        raise HTTPException(status_code=404, detail="추천 기록을 찾을 수 없습니다")
    
    # 피드백 업데이트
    recommendation.is_liked = feedback.is_liked
    db.commit()
    
    return {"message": "피드백이 저장되었습니다"}

@router.get("/categories/{category}", response_model=List[dict])
def get_perfumes_by_category(category: str, db: Session = Depends(get_db)):
    perfumes = db.query(Perfume).filter(Perfume.category == category).all()
    result = []
    for perfume in perfumes:
        result.append({
            "id": perfume.id,
            "name": perfume.name,
            "brand": perfume.brand,
            "category": perfume.category,
            "description": perfume.description
        })
    return result

@router.get("/popular", response_model=List[dict])
def get_popular_perfumes(db: Session = Depends(get_db)):
    perfumes = db.query(Perfume).all()
    # 예시: 단순히 랜덤 5개 반환
    return random.sample(perfumes, min(5, len(perfumes)))

@router.post("/retrain-model")
def retrain_model_with_feedback(db: Session = Depends(get_db)):
    recommendation_model.retrain_with_feedback(db)
    return {"message": "모델이 피드백을 반영하여 재학습되었습니다."}

@router.get("/model-status")
def get_model_status():
    status = recommendation_model.should_retrain()
    return {"should_retrain": status} 