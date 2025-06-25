#!/usr/bin/env python3
"""
향수 추천 모델을 미리 훈련시키는 스크립트
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.models.recommendation_model import PerfumeRecommendationModel

def main():
    print("향수 추천 모델 훈련을 시작합니다...")
    
    # 모델 인스턴스 생성
    model = PerfumeRecommendationModel()
    
    # 모델 훈련
    model.train()
    
    print("모델 훈련이 완료되었습니다!")
    print(f"모델 파일이 저장되었습니다: ml_models/perfume_recommendation_model.pkl")

if __name__ == "__main__":
    main() 