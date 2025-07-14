from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.database import get_db, Perfume, PerfumeRecipe
from backend.app.schemas import PerfumeCreate, Perfume as PerfumeSchema, PerfumeDetail, PerfumeRecipeCreate, PerfumeRecipe as PerfumeRecipeSchema

router = APIRouter()

@router.post("/", response_model=PerfumeSchema)
def create_perfume(perfume_data: PerfumeCreate, db: Session = Depends(get_db)):
    """새 향수를 등록합니다."""
    # 향수명 중복 확인
    existing_perfume = db.query(Perfume).filter(Perfume.name == perfume_data.name).first()
    if existing_perfume:
        raise HTTPException(status_code=400, detail="이미 등록된 향수명입니다")
    
    db_perfume = Perfume(**perfume_data.dict())
    db.add(db_perfume)
    db.commit()
    db.refresh(db_perfume)
    return db_perfume

@router.get("/", response_model=List[PerfumeSchema])
def get_perfumes(
    skip: int = 0, 
    limit: int = 100, 
    category: str = None,
    brand: str = None,
    price_range: str = None,
    db: Session = Depends(get_db)
):
    """향수 목록을 조회합니다."""
    query = db.query(Perfume)
    
    # 필터링
    if category:
        query = query.filter(Perfume.category == category)
    if brand:
        query = query.filter(Perfume.brand == brand)
    if price_range:
        query = query.filter(Perfume.price_range == price_range)
    
    perfumes = query.offset(skip).limit(limit).all()
    return perfumes

@router.get("/{perfume_id}", response_model=PerfumeDetail)
def get_perfume(perfume_id: int, db: Session = Depends(get_db)):
    """특정 향수 정보를 조회합니다."""
    perfume = db.query(Perfume).filter(Perfume.id == perfume_id).first()
    if perfume is None:
        raise HTTPException(status_code=404, detail="향수를 찾을 수 없습니다")
    return perfume

@router.put("/{perfume_id}", response_model=PerfumeSchema)
def update_perfume(perfume_id: int, perfume_data: PerfumeCreate, db: Session = Depends(get_db)):
    """향수 정보를 업데이트합니다."""
    perfume = db.query(Perfume).filter(Perfume.id == perfume_id).first()
    if perfume is None:
        raise HTTPException(status_code=404, detail="향수를 찾을 수 없습니다")
    
    # 업데이트할 필드들
    for field, value in perfume_data.dict().items():
        setattr(perfume, field, value)
    
    db.commit()
    db.refresh(perfume)
    return perfume

@router.delete("/{perfume_id}")
def delete_perfume(perfume_id: int, db: Session = Depends(get_db)):
    """향수를 삭제합니다."""
    perfume = db.query(Perfume).filter(Perfume.id == perfume_id).first()
    if perfume is None:
        raise HTTPException(status_code=404, detail="향수를 찾을 수 없습니다")
    
    db.delete(perfume)
    db.commit()
    return {"message": "향수가 삭제되었습니다"}

@router.post("/{perfume_id}/recipes", response_model=PerfumeRecipeSchema)
def create_perfume_recipe(perfume_id: int, recipe_data: PerfumeRecipeCreate, db: Session = Depends(get_db)):
    """향수 제조법을 추가합니다."""
    # 향수 존재 확인
    perfume = db.query(Perfume).filter(Perfume.id == perfume_id).first()
    if perfume is None:
        raise HTTPException(status_code=404, detail="향수를 찾을 수 없습니다")
    
    db_recipe = PerfumeRecipe(
        perfume_id=perfume_id,
        **recipe_data.dict()
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

@router.get("/{perfume_id}/recipes", response_model=List[PerfumeRecipeSchema])
def get_perfume_recipes(perfume_id: int, db: Session = Depends(get_db)):
    """향수 제조법을 조회합니다."""
    # 향수 존재 확인
    perfume = db.query(Perfume).filter(Perfume.id == perfume_id).first()
    if perfume is None:
        raise HTTPException(status_code=404, detail="향수를 찾을 수 없습니다")
    
    recipes = db.query(PerfumeRecipe).filter(PerfumeRecipe.perfume_id == perfume_id).all()
    return recipes

@router.get("/categories/list")
def get_perfume_categories():
    """사용 가능한 향수 카테고리를 반환합니다."""
    return {
        "categories": [
            "citrus", "floral", "woody", "oriental", "musk", "aquatic", "green", "gourmand", "powdery", "fruity", "aromatic", "chypre", "fougere", "amber", "spicy", "light floral", "white floral", "casual", "cozy"
        ],
        "price_ranges": [
            "budget", "mid-range", "luxury"
        ],
        "seasons": [
            "spring", "summer", "autumn", "winter", "all"
        ],
        "personalities": [
            "introvert", "extrovert", "balanced"
        ],
        "age_groups": [
            "young", "adult", "mature"
        ],
        "genders": [
            "male", "female", "unisex"
        ]
    } 