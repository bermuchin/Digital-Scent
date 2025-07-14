#!/usr/bin/env python3
"""
엑셀 데이터의 향수 카테고리 라벨 분석
"""

import pandas as pd

category_mapping = {
    '시트러스': 'citrus',
    '플로럴': 'floral',
    '우디': 'woody',
    '머스크': 'musk',
    '아쿠아틱': 'aquatic',
    '그린': 'green',
    '아로마틱': 'aromatic',
    '오리엔탈': 'oriental',
    '푸제르': 'fougere',
    '시프레': 'chypre',
    '앰버': 'amber',
    '스파이시': 'spicy',
    '파우더리': 'powdery',
    '프루티': 'fruity',
    '구르망': 'gourmand',
    '캐쥬얼': 'casual',
    '코지': 'cozy',
    '라이트 플로럴': 'light_floral',
    '화이트 플로럴': 'white_floral'
}

def simplify(cat):
    mapped = [category_mapping[k] for k in category_mapping if k in str(cat)]
    return mapped if mapped else ['other']

df = pd.read_excel('excel_data/perfume.preferred_cleansed.xlsx')
df['perfume_category'] = df['preferred_Note'].apply(simplify)
cats = set()
for x in df['perfume_category']:
    cats.update(x)
print('실제 라벨 목록:', sorted(cats))
print('실제 라벨 개수:', len(cats))

# 매핑되지 않은 값(즉, 'other'로 분류된 원본 preferred_Note) 출력
unmapped = df[df['perfume_category'].apply(lambda x: 'other' in x)]['preferred_Note'].unique()
print('\n매핑되지 않은 preferred_Note 값:')
for val in unmapped:
    print('-', val) 