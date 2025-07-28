#!/usr/bin/env python3
"""
엑셀 데이터 처리 및 ML 모델 재훈련 스크립트
"""

import sys
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, multilabel_confusion_matrix
from sklearn.multiclass import OneVsRestClassifier
import joblib
from datetime import datetime

# 프로젝트 루트 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.models.recommendation_model import PerfumeRecommendationModel

def load_excel_data():
    """엑셀 데이터를 로드합니다."""
    file_path = "excel_data/merged_pickple_remember.xlsx"
    print("=" * 60)
    print("엑셀 데이터 로드")
    print("=" * 60)
    try:
        # 엑셀 파일 읽기
        df = pd.read_excel(file_path)
        print(f"데이터 로드 완료: {len(df)}행, {len(df.columns)}열")
        print(f"컬럼명: {list(df.columns)}")
        print(f"\n데이터 샘플:")
        print(df.head())
        print(f"\n데이터 정보:")
        print(df.info())
        return df
    except Exception as e:
        print(f"엑셀 파일 로드 실패: {e}")
        return None

def simplify_perfume_category_list(category_text):
    """복합 향수 카테고리를 리스트로 변환하고, 각 항목을 영어로 매핑합니다."""
    if pd.isna(category_text):
        return []
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
        '코지': 'cozy
    }
    categories = [cat.strip() for cat in str(category_text).split(',')]
    result = []
    for cat in categories:
        for korean, english in category_mapping.items():
            if korean in cat:
                result.append(english)
                break
        else:
            result.append('other')
    return list(set(result))  # 중복 제거

def preprocess_data_multilabel(df):
    """멀티라벨 데이터 전처리"""
    column_mapping = {
        'user_id': 'user_id',
        'age_group': 'age_group',
        'gender': 'gender',
        'mbti': 'personality',
        'purpose': 'purpose',
        'fashionstyle': 'fashionstyle',
        'prefercolor': 'prefercolor',
        'perfume_category': 'perfume_category'
    }
    df = df.rename(columns=column_mapping)
    def age_group_to_int(age_group):
        if isinstance(age_group, str) and age_group.endswith('s'):
            try:
                return int(age_group[:-1]) + 5
            except:
                return None
        return None
    df['age'] = df['age_group'].apply(age_group_to_int)
    # 멀티라벨 변환
    df['perfume_category'] = df['perfume_category'].apply(simplify_perfume_category_list)
    required_columns = ['age', 'gender', 'personality', 'purpose', 'fashionstyle', 'prefercolor', 'perfume_category']
    df = df[required_columns]
    df['age'] = pd.to_numeric(df['age'], errors='coerce')
    df = df.dropna()
    # 1개 이상 라벨만 남김
    df = df[df['perfume_category'].apply(lambda x: len(x) > 0)]
    return df

def train_multilabel_model(df):
    features = ['age', 'gender', 'personality', 'purpose', 'fashionstyle', 'prefercolor']
    X = df[features]
    y = df['perfume_category']
    # 범주형 인코딩
    label_encoders = {}
    for col in X.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        label_encoders[col] = le
    # 멀티라벨 바이너리 인코딩
    mlb = MultiLabelBinarizer()
    y_bin = mlb.fit_transform(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y_bin, test_size=0.5, random_state=42)
    model = OneVsRestClassifier(RandomForestClassifier(n_estimators=100, random_state=42))
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"정확도(샘플 단위): {accuracy_score(y_test, y_pred):.3f}")
    print(classification_report(y_test, y_pred, target_names=mlb.classes_))
    print("혼동 행렬:")
    print(multilabel_confusion_matrix(y_test, y_pred))
    return model, label_encoders, mlb

def save_multilabel_model(model, label_encoders, mlb, path='ml_models/perfume_recommendation_multilabel.pkl'):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump({'model': model, 'label_encoders': label_encoders, 'mlb': mlb}, path)
    print(f"모델 저장 완료: {path}")

def load_multilabel_model(path='ml_models/perfume_recommendation_multilabel.pkl'):
    return joblib.load(path)

def main():
    print("엑셀 데이터 처리 및 멀티라벨 모델 재훈련을 시작합니다...")
    df = load_excel_data()
    if df is None:
        return
    df_processed = preprocess_data_multilabel(df)
    model, encoders, mlb = train_multilabel_model(df_processed)
    save_multilabel_model(model, encoders, mlb)
    print("✅ 멀티라벨 모델 훈련 및 저장 완료!")

if __name__ == "__main__":
    main() 