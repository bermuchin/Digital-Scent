from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db, User, UserPreference
from app.schemas import UserCreate, User as UserSchema, UserPreferenceCreate, UserPreference as UserPreferenceSchema, UserRegistration
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=UserSchema)
def create_user(user_data: UserRegistration, db: Session = Depends(get_db)):
    """새 사용자를 등록합니다."""
    # 이메일 중복 확인
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다")
    
    # 사용자명 중복 확인
    existing_username = db.query(User).filter(User.username == user_data.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="이미 사용 중인 사용자명입니다")
    
    # 사용자 생성
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        age=user_data.age,
        gender=user_data.gender,
        personality=user_data.personality,
        season_preference=user_data.season_preference
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # 선호도 정보가 있으면 저장
    if user_data.preferences:
        db_preference = UserPreference(
            user_id=db_user.id,
            category_preference=user_data.preferences.category_preference,
            price_preference=user_data.preferences.price_preference,
            intensity_preference=user_data.preferences.intensity_preference,
            longevity_preference=user_data.preferences.longevity_preference
        )
        db.add(db_preference)
        db.commit()
    
    return db_user

@router.get("/", response_model=List[UserSchema])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """모든 사용자 목록을 조회합니다."""
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=UserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """특정 사용자 정보를 조회합니다."""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    return user

@router.put("/{user_id}", response_model=UserSchema)
def update_user(user_id: int, user_data: UserCreate, db: Session = Depends(get_db)):
    """사용자 정보를 업데이트합니다."""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    # 업데이트할 필드들
    for field, value in user_data.dict().items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """사용자를 삭제합니다."""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    db.delete(user)
    db.commit()
    return {"message": "사용자가 삭제되었습니다"}

@router.post("/{user_id}/preferences", response_model=UserPreferenceSchema)
def create_user_preference(user_id: int, preference_data: UserPreferenceCreate, db: Session = Depends(get_db)):
    """사용자 선호도를 생성합니다."""
    # 사용자 존재 확인
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    # 기존 선호도가 있으면 업데이트, 없으면 생성
    existing_preference = db.query(UserPreference).filter(UserPreference.user_id == user_id).first()
    
    if existing_preference:
        for field, value in preference_data.dict().items():
            setattr(existing_preference, field, value)
        db.commit()
        db.refresh(existing_preference)
        return existing_preference
    else:
        db_preference = UserPreference(
            user_id=user_id,
            **preference_data.dict()
        )
        db.add(db_preference)
        db.commit()
        db.refresh(db_preference)
        return db_preference

@router.get("/{user_id}/preferences", response_model=UserPreferenceSchema)
def get_user_preference(user_id: int, db: Session = Depends(get_db)):
    """사용자 선호도를 조회합니다."""
    preference = db.query(UserPreference).filter(UserPreference.user_id == user_id).first()
    if preference is None:
        raise HTTPException(status_code=404, detail="선호도 정보를 찾을 수 없습니다")
    return preference 