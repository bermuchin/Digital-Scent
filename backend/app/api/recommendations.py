from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db, Perfume, Recommendation, User
from app.schemas import RecommendationRequest, RecommendationResponse, RecommendationFeedback
from app.models.recommendation_model import PerfumeRecommendationModel
import random

router = APIRouter()

# ML 모델 인스턴스 생성
recommendation_model = PerfumeRecommendationModel()

@router.post("/", response_model=RecommendationResponse)
def get_recommendation(request: RecommendationRequest, db: Session = Depends(get_db)):
    """사용자 선호도에 따른 향수를 추천합니다."""
    # ML 모델로 향수 카테고리 예측
    predicted_category, confidence = recommendation_model.predict_category(
        age=request.age,
        gender=request.gender,
        personality=request.personality,
        season=request.season_preference
    )
    
    # 해당 카테고리의 향수들 조회
    query = db.query(Perfume).filter(Perfume.category == predicted_category)
    
    # 추가 필터링
    if request.age < 30:
        query = query.filter(Perfume.age_group == "young")
    elif request.age > 50:
        query = query.filter(Perfume.age_group == "mature")
    else:
        query = query.filter(Perfume.age_group == "adult")
    
    if request.gender != "other":
        query = query.filter(
            (Perfume.gender_target == request.gender) | 
            (Perfume.gender_target == "unisex")
        )
    
    if request.season_preference:
        query = query.filter(
            (Perfume.season_suitability == request.season_preference) |
            (Perfume.season_suitability == "all")
        )
    
    if request.personality:
        query = query.filter(Perfume.personality_match == request.personality)
    
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
        age=request.age,
        gender=request.gender,
        personality=request.personality,
        season=request.season_preference
    )
    
    # 매칭 요소들
    match_factors = []
    if selected_perfume.personality_match == request.personality:
        match_factors.append("성격 매칭")
    if selected_perfume.season_suitability == request.season_preference:
        match_factors.append("계절 매칭")
    if selected_perfume.age_group in ["young", "adult", "mature"]:
        if (request.age < 30 and selected_perfume.age_group == "young") or \
           (30 <= request.age <= 50 and selected_perfume.age_group == "adult") or \
           (request.age > 50 and selected_perfume.age_group == "mature"):
            match_factors.append("연령대 매칭")
    
    return RecommendationResponse(
        perfume=selected_perfume,
        confidence_score=confidence,
        reason=reason,
        match_factors=match_factors
    )

@router.post("/user/{user_id}", response_model=RecommendationResponse)
def get_user_recommendation(user_id: int, db: Session = Depends(get_db)):
    """등록된 사용자에 대한 향수를 추천합니다."""
    # 사용자 정보 조회
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    # 추천 요청 생성
    request = RecommendationRequest(
        age=user.age,
        gender=user.gender,
        personality=user.personality,
        season_preference=user.season_preference
    )
    
    # 추천 실행
    recommendation = get_recommendation(request, db)
    
    # 추천 기록 저장
    db_recommendation = Recommendation(
        user_id=user_id,
        perfume_id=recommendation.perfume.id,
        confidence_score=recommendation.confidence_score,
        reason=recommendation.reason
    )
    db.add(db_recommendation)
    db.commit()
    
    return recommendation

@router.get("/user/{user_id}/history", response_model=List[dict])
def get_user_recommendation_history(user_id: int, db: Session = Depends(get_db)):
    """사용자의 추천 기록을 조회합니다."""
    # 사용자 존재 확인
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    # 추천 기록 조회
    recommendations = db.query(Recommendation).filter(
        Recommendation.user_id == user_id
    ).order_by(Recommendation.created_at.desc()).all()
    
    history = []
    for rec in recommendations:
        perfume = db.query(Perfume).filter(Perfume.id == rec.perfume_id).first()
        if perfume:
            history.append({
                "id": rec.id,
                "perfume_name": perfume.name,
                "perfume_brand": perfume.brand,
                "confidence_score": rec.confidence_score,
                "reason": rec.reason,
                "created_at": rec.created_at,
                "is_liked": rec.is_liked
            })
    
    return history

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
    """특정 카테고리의 향수들을 조회합니다."""
    perfumes = db.query(Perfume).filter(Perfume.category == category).all()
    
    return [
        {
            "id": perfume.id,
            "name": perfume.name,
            "brand": perfume.brand,
            "description": perfume.description,
            "price_range": perfume.price_range
        }
        for perfume in perfumes
    ]

@router.get("/popular", response_model=List[dict])
def get_popular_perfumes(db: Session = Depends(get_db)):
    """인기 향수들을 조회합니다 (좋아요가 많은 순)."""
    # 좋아요가 많은 추천들을 기반으로 인기 향수 계산
    popular_recommendations = db.query(
        Recommendation.perfume_id,
        db.func.count(Recommendation.id).label('recommendation_count'),
        db.func.sum(db.case((Recommendation.is_liked == True, 1), else_=0)).label('like_count')
    ).group_by(Recommendation.perfume_id).order_by(
        db.func.sum(db.case((Recommendation.is_liked == True, 1), else_=0)).desc()
    ).limit(10).all()
    
    popular_perfumes = []
    for rec in popular_recommendations:
        perfume = db.query(Perfume).filter(Perfume.id == rec.perfume_id).first()
        if perfume:
            popular_perfumes.append({
                "id": perfume.id,
                "name": perfume.name,
                "brand": perfume.brand,
                "category": perfume.category,
                "description": perfume.description,
                "recommendation_count": rec.recommendation_count,
                "like_count": rec.like_count
            })
    
    return popular_perfumes 