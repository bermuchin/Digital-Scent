from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.database import get_db, Perfume, Recommendation
from backend.app.schemas import RecommendationRequest, RecommendationResponse, RecommendationFeedback
from backend.app.models.recommendation_model import PerfumeRecommendationModel
import random

router = APIRouter()

# ML 모델 인스턴스 생성 및 로드
recommendation_model = PerfumeRecommendationModel()
try:
    recommendation_model.load_model()
    print("기존 멀티라벨 모델을 성공적으로 로드했습니다.")
except Exception as e:
    print(f"모델 로드 실패, 새로 훈련합니다: {e}")
    recommendation_model.train()

@router.post("/", response_model=RecommendationResponse)
def get_recommendation(request: RecommendationRequest, db: Session = Depends(get_db)):
    """사용자 선호도에 따른 향수를 추천합니다 (멀티라벨)."""
    # 입력 데이터 검증 및 기본값 설정
    age = request.age if request.age else 25
    gender = request.gender if request.gender else "남"
    personality = request.personality if request.personality else "ISTJ"
    cost = request.cost if request.cost else "5만 이하"
    purpose = request.purpose if request.purpose else "자기만족"
    durability = request.durability if request.durability else "상관없음"
    fashionstyle = request.fashionstyle if request.fashionstyle else "캐주얼"
    prefercolor = request.prefercolor if request.prefercolor else "흰색"

    # ML 모델로 향수 카테고리들 예측 (멀티라벨)
    predicted_categories, confidence = recommendation_model.predict_categories(
        age=age,
        gender=gender,
        personality=personality,
        cost=cost,
        purpose=purpose,
        durability=durability,
        fashionstyle=fashionstyle,
        prefercolor=prefercolor
    )

    # 예측된 카테고리들 중 하나를 선택하여 향수 추천
    # 가장 높은 신뢰도를 가진 카테고리나 첫 번째 카테고리 사용
    selected_category = predicted_categories[0] if predicted_categories else "citrus"
    
    # 해당 카테고리의 향수들 조회
    query = db.query(Perfume).filter(Perfume.category == selected_category)
    perfumes = query.all()
    
    # 선택된 카테고리에 향수가 없으면 다른 예측 카테고리 시도
    if not perfumes and len(predicted_categories) > 1:
        for category in predicted_categories[1:]:
            perfumes = db.query(Perfume).filter(Perfume.category == category).all()
            if perfumes:
                selected_category = category
                break
    
    # 여전히 향수가 없으면 모든 향수에서 랜덤 선택
    if not perfumes:
        perfumes = db.query(Perfume).all()
        if not perfumes:
            raise HTTPException(status_code=404, detail="적합한 향수를 찾을 수 없습니다")
    
    selected_perfume = random.choice(perfumes)

    # 추천 이유 생성 (멀티라벨 지원)
    reason = recommendation_model.get_recommendation_reason(
        predicted_categories=predicted_categories,
        age=age,
        gender=gender,
        personality=personality,
        season=None  # season은 더 이상 사용하지 않으므로 None 전달
    )

    match_factors = []  # (필요시 feature 기반 매칭 요소 추가)

    db_recommendation = Recommendation(
        perfume_id=selected_perfume.id,
        confidence_score=confidence,
        reason=reason
    )
    db.add(db_recommendation)
    db.commit()
    db.refresh(db_recommendation)

    return RecommendationResponse(
        id=db_recommendation.id,
        perfume=selected_perfume,
        predicted_categories=predicted_categories,  # 멀티라벨 예측 결과
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
    return {"message": "멀티라벨 모델이 피드백을 반영하여 재학습되었습니다."}

@router.get("/model-status")
def get_model_status():
    status = recommendation_model.should_retrain()
    return {"should_retrain": status} 