#!/usr/bin/env python3
"""
ML 모델 테스트 스크립트
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_model():
    try:
        print("랜덤 포레스트(RFC) 모델 테스트 시작...")
        
        from backend.app.models.recommendation_model import PerfumeRecommendationModel
        
        # 모델 인스턴스 생성
        model = PerfumeRecommendationModel()
        print("✅ 모델 인스턴스 생성 완료")
        
        # 모델 로드
        model.load_model()
        print("✅ 모델 로드 완료")
        
        # 실제 사용자와 유사한 테스트 입력값
        test_input = {
            'age': 25,
            'gender': '여',
            'mbti': 'ISTJ',
            'purpose': '자기만족',
            'fashionstyle': '캐주얼',
            'prefercolor': '흰색,검정색'
        }
        
        # 예측 테스트 (다중 라벨 분류)
        predicted_categories, confidences = model.predict_categories(**test_input)
        
        # 신뢰도를 기반으로 Top/Middle/Base 노트 추천
        note_recommendations = model.recommend_notes_by_confidence(confidences)
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
        remaining_confidences = {cat: conf for cat, conf in confidences.items() if cat not in selected_categories}
        sorted_remaining = sorted(remaining_confidences.items(), key=lambda item: item[1], reverse=True)
        print("  [기타 노트 신뢰도]")
        for cat, conf in sorted_remaining:
            print(f"    - {cat:<12s}: {conf:.3f}")
        
        # 추천 이유 테스트
        reason = model.get_recommendation_reason(predicted_categories, test_input['age'], test_input['gender'])
        print(f"\n✅ 추천 이유: {reason}")
        
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