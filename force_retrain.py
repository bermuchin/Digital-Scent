#!/usr/bin/env python3
"""
모델 강제 재훈련 스크립트
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def force_retrain():
    try:
        print("랜덤 포레스트(RFC) 모델 강제 재훈련 시작...")
        
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
        note_recommendations = model.recommend_notes_by_confidence(confidence)
        top = note_recommendations['top']
        middle = note_recommendations['middle']
        base = note_recommendations['base']

        # --- 상세 결과 출력 ---
        print(f"\n✅ 예측 테스트 성공: (탑: {top['category']}, 미들: {middle['category']}, 베이스: {base['category']})")
        print("  [상세 신뢰도]")
        print(f"    - Top({top['category']}): {top['confidence']:.3f}")
        print(f"    - Middle({middle['category']}): {middle['confidence']:.3f}")
        print(f"    - Base({base['category']}): {base['confidence']:.3f}")

        selected_categories = {top['category'], middle['category'], base['category']}
        remaining_confidences = {cat: conf for cat, conf in confidence.items() if cat not in selected_categories}
        sorted_remaining = sorted(remaining_confidences.items(), key=lambda item: item[1], reverse=True)
        print("  [기타 노트 신뢰도]")
        for cat, conf in sorted_remaining:
            print(f"    - {cat:<12s}: {conf:.3f}")
        
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