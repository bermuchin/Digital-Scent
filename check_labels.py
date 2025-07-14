#!/usr/bin/env python3
"""
DB와 엑셀 데이터의 향수 카테고리 분포 분석 (엑셀 라벨도 모델의 정규화 함수로 집계)
"""

from collections import Counter
from backend.app.database import Perfume, get_db
from sqlalchemy.orm import Session
import pandas as pd
from backend.app.models.recommendation_model import PerfumeRecommendationModel

# 1. DB 기준 분포
if __name__ == "__main__":
    db: Session = next(get_db())
    categories = [p.category for p in db.query(Perfume).all()]
    counter = Counter(categories)
    total = sum(counter.values())
    print("[DB] 향수 계열별 분포 (개수/비율):")
    for cat, count in counter.most_common():
        print(f"{cat}: {count}개 ({count/total:.2%})")
    print(f"총 향수 개수: {total}\n")

    # 2. 엑셀 기준 분포 (정규화 적용)
    try:
        model = PerfumeRecommendationModel()
        df = pd.read_excel('excel_data/perfume.preferred_cleansed.xlsx')
        all_cats = []
        for cats in df['preferred_Note'].dropna():
            all_cats.extend(model.simplify_perfume_category_list(cats))
        excel_counter = Counter(all_cats)
        excel_total = sum(excel_counter.values())
        unique_labels = set(all_cats)
        print("[엑셀] (정규화) 향수 계열별 분포 (개수/비율):")
        for cat, count in excel_counter.most_common():
            print(f"{cat}: {count}개 ({count/excel_total:.2%})")
        print(f"총 라벨 등장 횟수: {excel_total}")
        print(f"라벨 종류(유니크): {sorted(unique_labels)}")
        print(f"라벨 종류 개수: {len(unique_labels)}")
    except Exception as e:
        print(f"엑셀 데이터 분석 실패: {e}") 