#!/usr/bin/env python3
"""
ML 모델 테스트 스크립트
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_model():
    try:
        print("ML 모델 테스트 시작...")
        
        from backend.app.models.recommendation_model import PerfumeRecommendationModel
        
        # 모델 인스턴스 생성
        model = PerfumeRecommendationModel()
        print("✅ 모델 인스턴스 생성 완료")
        
        # 모델 로드
        model.load_model()
        print("✅ 모델 로드 완료")
        
        # 예측 테스트
        prediction, confidence = model.predict_category(25, 'female', 'introvert', 'spring')
        print(f"✅ 예측 성공: {prediction}, 신뢰도: {confidence}")
        
        return True
        
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_model()
    if success:
        print("\n🎉 ML 모델 테스트 성공!")
    else:
        print("\n💥 ML 모델 테스트 실패!") 