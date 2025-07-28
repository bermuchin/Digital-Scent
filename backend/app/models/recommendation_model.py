import sklearn
sklearn.set_config(enable_metadata_routing=True)

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler, MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, multilabel_confusion_matrix, hamming_loss, f1_score, jaccard_score
from sklearn.multiclass import OneVsRestClassifier
import joblib
import os
from typing import List, Dict, Tuple
from datetime import datetime, timedelta
import re

from sklearn.multioutput import ClassifierChain

class PerfumeRecommendationModel:
    def __init__(self):
        # 모델은 train() 메서드에서 GridSearchCV를 통해 최적화된 후 최종적으로 ClassifierChain으로 정의됩니다.
        self.model = ClassifierChain(RandomForestClassifier(n_estimators=100, random_state=42))
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.mlb = MultiLabelBinarizer()  # 멀티라벨 바이너리 인코더
        self.is_trained = False
        self.last_retrain_date = None
        self.onehot_columns = None  # One-hot 인코딩 컬럼 순서 저장
        
        # 모델 파일 경로 설정 (루트 디렉토리 기준)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # backend/app/models -> backend/app -> backend -> 루트
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        self.model_filepath = os.path.join(project_root, "ml_models", "perfume_recommendation_multilabel.pkl")
        
    def get_feedback_weight(self, is_liked: bool, days_old: int) -> float:
        """피드백의 가중치를 계산합니다."""
        base_weight = 2.0 if is_liked else 1.0  # 좋아요는 더 높은 가중치
        
        # 시간에 따른 가중치 감소 (최신 피드백이 더 중요)
        time_decay = max(0.1, 1.0 - (days_old / 365))  # 1년 후 10%까지 감소
        
        return base_weight * time_decay
    
    def prepare_feedback_data(self, db_session) -> pd.DataFrame:
        """실제 사용자 피드백 데이터를 준비합니다."""
        from backend.app.database import Recommendation, Perfume
        
        # 피드백이 있는 추천 기록 조회
        feedback_records = db_session.query(Recommendation).filter(
            Recommendation.is_liked.isnot(None)
        ).all()
        
        feedback_data = []
        
        for record in feedback_records:
            # 향수 정보 조회
            perfume = db_session.query(Perfume).filter(Perfume.id == record.perfume_id).first()
            if not perfume:
                continue
            
            # 익명 사용자는 기본값 사용
            age = 30
            gender = "other"
            personality = "balanced"
            season_preference = "spring"
            
            # 피드백 가중치 계산
            days_old = (datetime.utcnow() - record.created_at).days
            weight = self.get_feedback_weight(record.is_liked, days_old)
            
            # 좋아요인 경우만 훈련 데이터에 포함 (싫어요는 다른 카테고리 학습에 활용)
            if record.is_liked:
                feedback_data.append({
                    'age': age,
                    'gender': gender,
                    'personality': personality,
                    'season_preference': season_preference,
                    'perfume_category': [perfume.category],  # 리스트로 변경
                    'weight': weight,
                    'source': 'feedback'
                })
        
        return pd.DataFrame(feedback_data)
    
    def prepare_enhanced_training_data(self, db_session=None) -> Tuple[pd.DataFrame, pd.Series, np.ndarray]:
        """향상된 훈련 데이터를 준비합니다 (엑셀 데이터 + 피드백 데이터)."""
        excel_df = self.load_excel_data()
        if excel_df is not None and not excel_df.empty:
            excel_df['weight'] = 1.0
            excel_df['source'] = 'excel'
            print(f"엑셀 데이터 로드: {len(excel_df)}개")
        else:
            print("엑셀 데이터가 없으므로 빈 데이터프레임 반환")
            return pd.DataFrame(), pd.Series(dtype=object), np.array([])
        feedback_df = pd.DataFrame()
        if db_session:
            try:
                feedback_df = self.prepare_feedback_data(db_session)
            except Exception as e:
                print(f"피드백 데이터 로드 실패: {e}")
        if not feedback_df.empty:
            combined_df = pd.concat([excel_df, feedback_df], ignore_index=True)
            print(f"훈련 데이터: 엑셀 {len(excel_df)}개, 피드백 {len(feedback_df)}개")
        else:
            combined_df = excel_df
            print(f"훈련 데이터: 엑셀 {len(excel_df)}개")
        features = ['age', 'gender', 'mbti', 'purpose', 'fashionstyle', 'prefercolor']
        X = combined_df[features]
        y = combined_df['perfume_category']
        weights = combined_df['weight'].values
        return X, y, weights

    def load_excel_data(self) -> pd.DataFrame:
        """엑셀 데이터를 로드하고 전처리합니다."""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
            excel_filepath = os.path.join(project_root, "excel_data", "merged_pickple_remember.xlsx")
            if not os.path.exists(excel_filepath):
                print(f"엑셀 파일을 찾을 수 없습니다: {excel_filepath}")
                return None
            df = pd.read_excel(excel_filepath)
            print(f"엑셀 데이터 로드 완료: {len(df)}행, {len(df.columns)}열")
            column_mapping = {
                'user_id': 'user_id',
                'age_group': 'age_group',
                'gender': 'gender',
                'style': 'fashionstyle',
                'color': 'prefercolor',
                'purpose': 'purpose',
                'mbti': 'mbti',
                'preferred_Note': 'perfume_category',
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
            df['perfume_category'] = df['perfume_category'].apply(self.simplify_perfume_category_list)
            required_columns = ['age', 'gender', 'mbti', 'purpose', 'fashionstyle', 'prefercolor', 'perfume_category']
            df = df[required_columns]
            df['age'] = pd.to_numeric(df['age'], errors='coerce')
            # mbti 결측치는 'unknown'으로 채움
            df['mbti'] = df['mbti'].fillna('unknown')
            df['mbti'] = df['mbti'].replace('', 'unknown')
            # mbti를 제외한 나머지 필드는 결측치 제거
            non_mbti_cols = [col for col in required_columns if col != 'mbti']
            df = df.dropna(subset=non_mbti_cols)
            print(f"전처리 완료: {len(df)}행")
            return df
        except Exception as e:
            print(f"엑셀 데이터 로드 실패: {e}")
            return None
    def preprocess_input(self, input_dict):
        gender_map = {'여': 'F', '여성': 'F', '남': 'M', '남성': 'M', 'F': 'F', 'M': 'M', 'female': 'F', 'male': 'M', 'unisex': 'unisex'}
        purpose_map = {
            '자기만족': 'self_satisfaction', 'good_impression': 'good_impression', 'special_event': 'special_event',
            'date_or_social': 'date_or_social', 'formal_occasion': 'formal_occasion'
        }
        fashionstyle_map = {
            '캐주얼': 'casual', 'casual': 'casual', 'minimal': 'minimal', 'simple': 'simple',
            'street': 'street', 'modern': 'modern', 'chic': 'chic', 'sports': 'sports'
        }
        color_map = {
        '흰색': 'white', '검정': 'black', '파랑': 'blue', '노랑': 'yellow', '초록': 'green',
        '분홍': 'pink', '보라': 'purple', '빨강': 'red', '주황': 'orange', '민트': 'mint',
        '베이지': 'beige', '갈색': 'brown', '그레이': 'gray', '코랄': 'coral'
    }
        def normalize_color(val):
            if not isinstance(val, str):
                return 'unknown'
            colors = [color_map.get(c.strip(), c.strip().lower()) for c in val.split(',')]
            return ','.join(colors)
            
        norm = dict(input_dict)
        norm['gender'] = gender_map.get(str(norm.get('gender', '')).strip(), 'F')
        norm['purpose'] = purpose_map.get(str(norm.get('purpose', '')).strip(), 'good_impression')
        norm['fashionstyle'] = fashionstyle_map.get(str(norm.get('fashionstyle', '')).strip(), 'casual')
        norm['prefercolor'] = normalize_color(norm.get('prefercolor', 'unknown'))
        return norm
    
    def _calculate_match_score(self, perfume: Dict, age: int, gender: str, 
                              personality: str, season: str) -> float:
        """향수와 사용자 선호도의 매칭 점수를 계산합니다."""
        score = 0.0
        
        # 나이 그룹 매칭
        if perfume['age_group'] == 'young' and age < 30:
            score += 0.2
        elif perfume['age_group'] == 'adult' and 30 <= age <= 50:
            score += 0.2
        elif perfume['age_group'] == 'mature' and age > 50:
            score += 0.2
        
        # 성별 매칭
        if perfume['gender_target'] == gender or perfume['gender_target'] == 'unisex':
            score += 0.2
        
        # 성격 매칭
        if perfume['personality_match'] == personality:
            score += 0.2
        
        # 계절 매칭
        if perfume['season_suitability'] == season or perfume['season_suitability'] == 'all':
            score += 0.2
        
        # 카테고리 선호도 (랜덤하게 추가)
        if np.random.random() > 0.5:
            score += 0.1
        
        return min(score, 1.0)
    
    def train(self, db_session=None, force_retrain=False):
        """모델을 훈련합니다."""
        # 재훈련 필요성 확인
        if not force_retrain and self.should_retrain():
            print("재훈련이 필요하지 않습니다.")
            return
        X, y, weights = self.prepare_enhanced_training_data(db_session)
        print("[DEBUG] X shape:", X.shape)
        print("[DEBUG] X columns:", X.columns.tolist())
        print("[DEBUG] y shape:", y.shape)
        print("[DEBUG] X head:\n", X.head())

        # --- 피처 엔지니어링 및 전처리 (다중 선택 피처 처리 포함) ---
        X_processed = X.copy()

        # 1. 수치형 변수 스케일링
        numeric_features = X.select_dtypes(include=np.number).columns.tolist()
        if numeric_features:
            self.scaler.fit(X_processed[numeric_features])
            X_processed[numeric_features] = self.scaler.transform(X_processed[numeric_features])

        # 2. 다중 선택 가능 피처 처리 (Multi-label Binarization)
        multilabel_cols = ['purpose', 'prefercolor', 'fashionstyle']
        for col in multilabel_cols:
            # 콤마로 구분된 문자열을 개별 컬럼으로 분리 (예: 'casual,street' -> casual=1, street=1)
            dummies = X_processed[col].str.get_dummies(sep=',')
            # 컬럼 이름에 접두사 추가 (예: fashionstyle_casual)
            dummies.columns = [f"{col}_{c.strip()}" for c in dummies.columns]
            X_processed = pd.concat([X_processed, dummies], axis=1)
        
        # 3. 단일 선택 피처 처리 (One-Hot Encoding) 및 원본 컬럼 삭제
        single_label_cols = ['gender', 'mbti']
        X_processed = pd.get_dummies(X_processed, columns=single_label_cols, dummy_na=False)
        X_processed = X_processed.drop(columns=multilabel_cols)

        # 예측 시 사용하기 위해 최종 컬럼 순서 저장
        self.onehot_columns = X_processed.columns.tolist()
        self.label_encoders = {}

        # 멀티라벨 바이너리 인코딩
        y_bin = self.mlb.fit_transform(y)
        # 훈련/테스트 분할 (가중치 고려)
        # 다중 라벨 데이터에서는 일반적인 train_test_split보다 IterativeStratification이 더 안정적인 분할을 보장합니다.
        from skmultilearn.model_selection import IterativeStratification

        # 80/20 분할을 위해 n_splits=5로 설정 (1/5이 테스트 세트가 됨)
        stratifier = IterativeStratification(n_splits=5, order=1)
        train_indices, test_indices = next(stratifier.split(X_processed, y_bin))

        X_train, X_test = X_processed.astype(float).iloc[train_indices], X_processed.astype(float).iloc[test_indices]
        y_train, y_test = y_bin[train_indices], y_bin[test_indices]
        w_train, w_test = weights[train_indices], weights[test_indices]
        # RandomForest 파라미터 튜닝 (GridSearchCV)
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import GridSearchCV
        param_grid = {
            'n_estimators': [100, 200],
            'max_depth': [8, 10, 12],
            'min_samples_split': [2, 5],
            'min_samples_leaf': [1, 2],
            'class_weight': ['balanced']
        }
        base_rf = RandomForestClassifier(random_state=42)
        base_rf.set_fit_request(sample_weight=True)  # sample_weight metadata routing 명시
        grid_search = GridSearchCV(base_rf, param_grid, cv=3, scoring='f1_micro', n_jobs=-1)
        try:
            grid_search.fit(X_train, y_train, sample_weight=w_train)
        except Exception as e:
            print(f"GridSearchCV에서 sample_weight 적용 실패: {e}, 가중치 없이 튜닝")
            grid_search.fit(X_train, y_train)
        best_rf = grid_search.best_estimator_
        best_rf.set_fit_request(sample_weight=True)  # 최적 모델에도 metadata routing 명시
        print(f"[DEBUG] GridSearch 최적 파라미터: {grid_search.best_params_}")
        # 기존: self.model = OneVsRestClassifier(best_rf)
        # 변경: ClassifierChain 적용
        from sklearn.multioutput import ClassifierChain
        self.model = ClassifierChain(best_rf)
        self.model.fit(X_train, y_train, sample_weight=w_train)
        # 모델 평가 - 멀티라벨 분류에 적합한 지표들
        y_pred = self.model.predict(X_test)
        from sklearn.metrics import accuracy_score, hamming_loss, f1_score, jaccard_score, classification_report, multilabel_confusion_matrix
        exact_accuracy = accuracy_score(y_test, y_pred)
        print(f"Exact Match Accuracy: {exact_accuracy:.3f}")
        hamming_loss_score = hamming_loss(y_test, y_pred)
        print(f"Hamming Loss: {hamming_loss_score:.3f} (낮을수록 좋음)")
        micro_f1 = f1_score(y_test, y_pred, average='micro', zero_division=0)
        print(f"Micro-averaged F1 Score: {micro_f1:.3f}")
        macro_f1 = f1_score(y_test, y_pred, average='macro', zero_division=0)
        print(f"Macro-averaged F1 Score: {macro_f1:.3f}")
        subset_accuracy = jaccard_score(y_test, y_pred, average='samples', zero_division=0)
        print(f"Subset Accuracy (Jaccard): {subset_accuracy:.3f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=self.mlb.classes_, zero_division=0))
        print("\nMultilabel Confusion Matrix:")
        print(multilabel_confusion_matrix(y_test, y_pred))
        self.is_trained = True
        self.last_retrain_date = datetime.utcnow()
        self.save_model()
    
    def should_retrain(self) -> bool:
        """재훈련이 필요한지 확인합니다."""
        if not self.is_trained:
            return True
        
        if not self.last_retrain_date:
            return True
        
        # 마지막 훈련 후 7일이 지났으면 재훈련
        days_since_last_train = (datetime.utcnow() - self.last_retrain_date).days
        return days_since_last_train >= 7
    
    def retrain_with_feedback(self, db_session):
        """피드백 데이터를 사용하여 모델을 재훈련합니다."""
        print("피드백 데이터로 모델을 재훈련합니다...")
        self.train(db_session, force_retrain=True)
        print("피드백 기반 재훈련 완료!")
    
    def predict_categories(self, age: int, gender: str, mbti: str, purpose: str, fashionstyle: str, prefercolor: str) -> tuple:
        """사용자 특성에 따른 향수 카테고리들을 예측합니다."""
        if not self.is_trained:
            raise ValueError("모델이 훈련되지 않았습니다. 먼저 train()을 호출하세요.")
        # 입력값 정규화
        input_dict = {
            'age': age,
            'gender': gender,
            'mbti': mbti,
            'purpose': purpose,
            'fashionstyle': fashionstyle,
            'prefercolor': prefercolor
        }
        print(f"[DEBUG] raw input_dict: {input_dict}")
        input_dict = self.preprocess_input(input_dict)
        print(f"[DEBUG] preprocessed input_dict: {input_dict}")
        
        # --- 훈련 시점과 동일한 구조의 입력 데이터 생성 ---
        # 1. 훈련된 컬럼 목록을 기반으로 빈 데이터프레임 생성
        input_processed = pd.DataFrame(columns=self.onehot_columns)
        input_processed.loc[0] = 0.0

        # 2. 수치형 데이터 변환 및 채우기
        numeric_features = [col for col in self.scaler.feature_names_in_ if col in input_dict]
        if numeric_features:
            numeric_df = pd.DataFrame([input_dict])[numeric_features]
            scaled_numeric = self.scaler.transform(numeric_df)
            for i, col in enumerate(numeric_features):
                input_processed.loc[0, col] = scaled_numeric[0, i]

        # 3. 다중 선택 피처 변환 및 채우기
        multilabel_cols = ['purpose', 'prefercolor', 'fashionstyle']
        for col in multilabel_cols:
            if col in input_dict and input_dict[col]:
                values = str(input_dict[col]).split(',')
                for val in values:
                    dummy_col_name = f"{col}_{val.strip()}"
                    if dummy_col_name in input_processed.columns:
                        input_processed.loc[0, dummy_col_name] = 1

        # 4. 단일 선택 피처 변환 및 채우기
        single_label_cols = ['gender', 'mbti']
        for col in single_label_cols:
            if col in input_dict and input_dict[col]:
                dummy_col_name = f"{col}_{input_dict[col]}"
                if dummy_col_name in input_processed.columns:
                    input_processed.loc[0, dummy_col_name] = 1

        # 예측
        y_pred_bin = self.model.predict(input_processed)
        # 바이너리 결과를 라벨 리스트로 변환
        predicted_categories = self.mlb.inverse_transform(y_pred_bin)[0]
        # 모든 카테고리에 대해 confidence 반환
        y_pred_proba = self.model.predict_proba(input_processed)
        confidences = {self.mlb.classes_[i]: y_pred_proba[0][i] for i in range(len(self.mlb.classes_))}
        return predicted_categories, confidences
    
    def get_recommendation_reason(self, predicted_categories: List[str], age: int, 
                                 gender: str, mbti: str, season: str) -> str:
        """추천 이유를 생성합니다."""
        reasons = []
        # 나이 기반 이유
        if age < 25:
            reasons.append("젊은 층에게 인기 있는")
        elif age < 40:
            reasons.append("성인층에게 선호되는")
        else:
            reasons.append("성숙한 분위기의")
        # 성별 기반 이유
        if gender == "남":
            reasons.append("남성에게 적합한")
        elif gender == "여":
            reasons.append("여성에게 어울리는")
        else:
            reasons.append("모든 성별에게 매력적인")
        # 카테고리 기반 이유
        category_reasons = {
            "citrus": "상큼하고 경쾌한",
            "floral": "우아하고 로맨틱한",
            "woody": "깊고 안정감 있는",
            "oriental": "신비롭고 매혹적인",
            "musk": "포근하고 따뜻한",
            "aquatic": "시원하고 깨끗한",
            "green": "자연스럽고 상쾌한",
            "gourmand": "달콤하고 매력적인",
            "powdery": "부드럽고 우아한",
            "fruity": "달콤하고 생기있는",
            "aromatic": "허브향이 풍부한",
            "chypre": "고급스럽고 세련된",
            "fougere": "클래식하고 남성적인",
            "amber": "따뜻하고 달콤한",
            "spicy": "강렬하고 매혹적인"
        }
        for category in predicted_categories:
            if category in category_reasons:
                reasons.append(category_reasons[category])
                break
        if not reasons:
            reasons.append("개성 있는")
        return " ".join(reasons) + " 향수입니다."
    
    def save_model(self):
        """모델을 저장합니다."""
        try:
            os.makedirs(os.path.dirname(self.model_filepath), exist_ok=True)
            model_data = {
                'model': self.model,
                'label_encoders': self.label_encoders,
                'scaler': self.scaler,
                'mlb': self.mlb,  # MultiLabelBinarizer 추가
                'is_trained': self.is_trained,
                'last_retrain_date': self.last_retrain_date,
                'onehot_columns': self.onehot_columns # One-hot 컬럼 순서 저장
            }
            joblib.dump(model_data, self.model_filepath)
            print(f"[DEBUG] 모델 저장 시도: {self.model_filepath}")
            print(f"Model saved to {self.model_filepath}")
        except Exception as e:
            print(f"모델 저장 실패: {e}")
    
    def load_model(self):
        """저장된 모델을 로드합니다."""
        try:
            if os.path.exists(self.model_filepath):
                model_data = joblib.load(self.model_filepath)
                self.model = model_data['model']
                self.label_encoders = model_data['label_encoders']
                self.scaler = model_data['scaler']
                self.mlb = model_data['mlb']  # MultiLabelBinarizer 로드
                self.is_trained = model_data['is_trained']
                self.last_retrain_date = model_data['last_retrain_date']
                self.onehot_columns = model_data['onehot_columns'] # One-hot 컬럼 순서 로드
                print("모델 로드 완료!")
            else:
                print("저장된 모델 파일이 없습니다. 새로 훈련합니다.")
                self.train()
        except Exception as e:
            print(f"모델 로드 실패: {e}")
            print("새로 훈련합니다.")
            self.train() 

    def simplify_perfume_category_list(self, category_text: str) -> List[str]:
        """
        복합 향수 카테고리를 리스트로 변환하고, 각 항목을 표준 카테고리(영문)로 강력하게 매핑합니다.
        유사 카테고리를 통합하여 데이터 품질과 모델 성능을 향상시킵니다.
        """
        import re
        if pd.isna(category_text):
            return []
        
        # 명확성과 유지보수성을 위해 재구성된 매핑 규칙
        # 유사 카테고리를 통합하고, 긴 키워드를 우선적으로 매칭합니다.
        mapping = {
            # Floral 계열 (통합)
            '화이트 플로럴': 'floral', '라이트 플로럴': 'floral', '플로럴': 'floral', 'white floral': 'floral', 'light floral': 'floral',
            '장미': 'floral', 'rose': 'floral', '자스민': 'floral', '백합': 'floral', '꽃': 'floral',
            # Woody 계열 (통합)
            '우디': 'woody', '우드': 'woody', '나무': 'woody', '샌달우드': 'woody', '시더우드': 'woody', '숲': 'woody', '오리엔탈': 'woody', '신비': 'woody',
            # Citrus 계열
            '시트러스': 'citrus', '상큼': 'citrus', '레몬': 'citrus', '자몽': 'citrus', '베르가못': 'citrus',
            # 기타 주요 카테고리 (한글/영문/유사어 포함)
            '머스크': 'musk', '포근': 'musk',
            '아쿠아틱': 'aquatic', '바다': 'aquatic', '비누': 'aquatic',
            '그린': 'green', '풀': 'green', '허브': 'green', '스파이시': 'green', '후추': 'green',
            '아로마틱': 'aromatic', '라벤더': 'aromatic',
            '프루티': 'fruity', '과일': 'fruity',
            '구르망': 'gourmand', '달콤': 'gourmand', '바닐라': 'gourmand',
            '파우더리': 'powdery', '파우더': 'powdery',
            '시프레': 'chypre', '푸제르': 'fougere', '앰버': 'amber',
            '캐쥬얼': 'casual', '일상': 'casual',
            '코지': 'cozy', '커피': 'cozy',
        }
        # 긴 키워드가 먼저 매칭되도록 정렬 (e.g., '화이트 플로럴'이 '플로럴'보다 먼저)
        sorted_keys = sorted(mapping.keys(), key=len, reverse=True)

        def clean_label(label):
            label = str(label)
            label = re.sub(r'\([^)]*\)', '', label)  # 괄호와 내용 제거
            label = re.sub(r'[^\w가-힣 ]', '', label)  # 특수문자 제거
            label = label.strip().lower()
            return label
        raw_cats = re.split(r'[,/]', str(category_text))
        result = set()
        for raw in raw_cats:
            cleaned = clean_label(raw)
            if not cleaned:
                continue
            # 정렬된 키로 매칭하여 가장 구체적인 키워드를 먼저 찾음
            for key in sorted_keys:
                if key in cleaned:
                    result.add(mapping[key])
                    break
        return list(result) 

    NOTE_CATEGORY_MAP = {
        "top": ["citrus", "fruity", "aquatic", "green"],
        "middle": ["floral", "powdery", "aromatic", "fougere"],
        "base": ["amber", "chypre", "gourmand", "cozy", "musk", "woody"]
    }

    def recommend_notes_by_confidence(self, confidence_dict):
        """
        confidence_dict: {카테고리명: 확률, ...}
        각 노트별로 NOTE_CATEGORY_MAP에 해당하는 카테고리 중 confidence가 가장 높은 향조를 추천
        """
        result = {}
        for note, categories in self.NOTE_CATEGORY_MAP.items():
            best_cat = None
            best_conf = -1
            for cat in categories:
                conf = confidence_dict.get(cat, 0)
                if conf > best_conf:
                    best_cat = cat
                    best_conf = conf
            result[note] = {"category": best_cat, "confidence": best_conf}
        return result