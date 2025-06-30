#!/usr/bin/env python3
"""
모델 강제 재훈련 스크립트
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def force_retrain():
    try:
        print("모델 강제 재훈련 시작...")
        
        from backend.app.models.recommendation_model import PerfumeRecommendationModel
        
        # 모델 인스턴스 생성
        model = PerfumeRecommendationModel()
        
        # 강제 재훈련
        model.train(force_retrain=True)
        
        print("✅ 모델 강제 재훈련 완료!")
        
        # 테스트
        prediction, confidence = model.predict_category(25, 'female', 'introvert', 'spring')
        print(f"✅ 예측 테스트 성공: {prediction}, 신뢰도: {confidence}")
        
        return True
        
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = force_retrain()
    if success:
        print("\n🎉 모델 재훈련 성공!")
    else:
        print("\n💥 모델 재훈련 실패!") 