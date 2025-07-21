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
        print("[DEBUG] 모델 인스턴스 생성 완료")
        
        # 강제 재훈련
        model.train(force_retrain=True)
        print("[DEBUG] 모델 강제 재훈련 완료!")
        
        # 테스트
        predicted_categories, confidence = model.predict_categories(
            age=25,
            gender='여',
            mbti='ISTJ',
            purpose='자기만족',
            fashionstyle='캐주얼',
            prefercolor='흰색'
        )
        # 탑/미들/베이스 노트별 추천
        notes = model.recommend_notes_by_confidence(confidence)
        print(f"✅ 예측 테스트 성공: (탑: {notes['top']['category']}, 미들: {notes['middle']['category']}, 베이스: {notes['base']['category']})")
        print("  [상세 신뢰도]")
        for note in ['top', 'middle', 'base']:
            cat = notes[note]['category']
            conf = notes[note]['confidence']
            print(f"    - {note.capitalize()}({cat}): {conf:.3f}")
        print("[DEBUG] 예측 테스트 완료!")
        
        return True
        
    except Exception as e:
        import traceback
        print(f"❌ 에러 발생: {e}")
        traceback.print_exc()
        sys.stdout.flush()
        sys.stderr.flush()
        return False

if __name__ == "__main__":
    success = force_retrain()
    if success:
        print("\n🎉 모델 재훈련 성공!")
    else:
        print("\n💥 모델 재훈련 실패!") 