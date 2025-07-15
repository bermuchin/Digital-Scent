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

class PerfumeRecommendationModel:
    def __init__(self):
        self.model = OneVsRestClassifier(RandomForestClassifier(n_estimators=100, random_state=42))
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
        # 엑셀 데이터 로드
        excel_df = self.load_excel_data()
        if excel_df is not None and not excel_df.empty:
            excel_df['weight'] = 1.0  # 엑셀 데이터는 기본 가중치
            excel_df['source'] = 'excel'
            print(f"엑셀 데이터 로드: {len(excel_df)}개")
        else:
            # 엑셀 데이터가 없으면 빈 데이터프레임 반환
            print("엑셀 데이터가 없으므로 빈 데이터프레임 반환")
            return pd.DataFrame(), pd.Series(dtype=object), np.array([])
        
        # 피드백 데이터 (가능한 경우)
        feedback_df = pd.DataFrame()
        if db_session:
            try:
                feedback_df = self.prepare_feedback_data(db_session)
            except Exception as e:
                print(f"피드백 데이터 로드 실패: {e}")
        
        # 데이터 결합
        if not feedback_df.empty:
            combined_df = pd.concat([excel_df, feedback_df], ignore_index=True)
            print(f"훈련 데이터: 엑셀 {len(excel_df)}개, 피드백 {len(feedback_df)}개")
        else:
            combined_df = excel_df
            print(f"훈련 데이터: 엑셀 {len(excel_df)}개")
        
        # 특성과 타겟 분리
        features = ['age', 'gender', 'personality', 'cost', 'purpose', 'durability', 'fashionstyle', 'prefercolor']
        X = combined_df[features]
        y = combined_df['perfume_category']
        weights = combined_df['weight'].values
        
        return X, y, weights
    
    def load_excel_data(self) -> pd.DataFrame:
        """엑셀 데이터를 로드하고 전처리합니다."""
        try:
            # 엑셀 파일 경로 설정
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
            excel_filepath = os.path.join(project_root, "excel_data", "perfume.preferred_cleansed.xlsx")
            
            if not os.path.exists(excel_filepath):
                print(f"엑셀 파일을 찾을 수 없습니다: {excel_filepath}")
                return None
            
            # 엑셀 데이터 로드
            df = pd.read_excel(excel_filepath)
            print(f"엑셀 데이터 로드 완료: {len(df)}행, {len(df.columns)}열")
            
            # 컬럼명 매핑
            column_mapping = {
                'user_id': 'user_id',
                'age_group': 'age_group',
                'gender': 'gender',
                'style': 'fashionstyle',
                'color': 'prefercolor',
                'purpose': 'purpose',
                'price_range': 'cost',
                'durability': 'durability',
                'mbti': 'personality',
                'preferred_Note': 'perfume_category'
            }
            df = df.rename(columns=column_mapping)
            
            # age_group을 정수형 age로 변환
            def age_group_to_int(age_group):
                if isinstance(age_group, str) and age_group.endswith('s'):
                    try:
                        return int(age_group[:-1]) + 5
                    except:
                        return None
                return None
            
            df['age'] = df['age_group'].apply(age_group_to_int)
            
            # 향수 카테고리를 멀티라벨로 변환
            df['perfume_category'] = df['perfume_category'].apply(self.simplify_perfume_category_list)
            
            # 필요한 컬럼만 선택
            required_columns = ['age', 'gender', 'personality', 'cost', 'purpose', 'durability', 'fashionstyle', 'prefercolor', 'perfume_category']
            df = df[required_columns]
            
            # 결측값 처리
            df['age'] = pd.to_numeric(df['age'], errors='coerce')
            df = df.dropna()
            
            # 1개 이상 라벨만 남김
            df = df[df['perfume_category'].apply(lambda x: len(x) > 0)]
            
            print(f"전처리 완료: {len(df)}행")
            return df
            
        except Exception as e:
            print(f"엑셀 데이터 로드 실패: {e}")
            return None
    
    def simplify_perfume_category_list(self, category_text):
        """
        복합 향수 카테고리를 리스트로 변환하고, 각 항목을 19개 표준 카테고리(영문)로 강력하게 매핑합니다.
        괄호, 설명, 띄어쓰기, 오타, 유사 표현 등도 모두 표준 카테고리로 매핑. 매핑 실패시 'other'.
        """
        if pd.isna(category_text):
            return []

        # 표준 카테고리(영문)
        std_categories = [
            'citrus', 'floral', 'woody', 'oriental', 'musk', 'aquatic', 'green', 'gourmand', 'powdery', 'fruity',
            'aromatic', 'chypre', 'fougere', 'amber', 'spicy', 'light floral', 'white floral', 'casual', 'cozy'
        ]
        # 매핑표: 키워드/한글/설명/유사표현 → 표준 카테고리
        mapping = {
            # citrus
            '시트러스': 'citrus', '레몬': 'citrus', '자몽': 'citrus', '상큼': 'citrus', 'citrus': 'citrus',
            # floral
            '플로럴': 'floral', '꽃': 'floral', '장미': 'floral', '백합': 'floral', 'rose': 'floral', 'lily': 'floral', 'floral': 'floral',
            # woody
            '우디': 'woody', '나무': 'woody', '숲': 'woody', 'cedar': 'woody', 'wood': 'woody', 'woody': 'woody',
            # oriental
            '오리엔탈': 'oriental', '신비': 'oriental', 'oriental': 'oriental',
            # musk
            '머스크': 'musk', '포근': 'musk', '따뜻': 'musk', 'musk': 'musk',
            # aquatic
            '아쿠아틱': 'aquatic', '바다': 'aquatic', '비누': 'aquatic', 'aquatic': 'aquatic',
            # green
            '그린': 'green', '풀': 'green', '허브': 'green', '자연': 'green', 'green': 'green',
            # gourmand
            '구르망': 'gourmand', '바닐라': 'gourmand', '초콜릿': 'gourmand', '달콤': 'gourmand', 'gourmand': 'gourmand',
            # powdery
            '파우더리': 'powdery', '파우더': 'powdery', '부드럽': 'powdery', 'powdery': 'powdery',
            # fruity
            '프루티': 'fruity', '과일': 'fruity', '사과': 'fruity', '복숭아': 'fruity', '베리': 'fruity', 'fruity': 'fruity',
            # aromatic
            '아로마틱': 'aromatic', '라벤더': 'aromatic', '로즈마리': 'aromatic', '바질': 'aromatic', 'aromatic': 'aromatic',
            # chypre
            '시프레': 'chypre', '오크모스': 'chypre', '베르가못': 'chypre', '패츌리': 'chypre', 'chypre': 'chypre',
            # fougere
            '푸제르': 'fougere', 'ferny': 'fougere', 'fougere': 'fougere',
            # amber
            '앰버': 'amber', 'amber': 'amber',
            # spicy
            '스파이시': 'spicy', '계피': 'spicy', '정향': 'spicy', '후추': 'spicy', 'spicy': 'spicy',
            # light floral
            '라이트 플로럴': 'light floral', '작은 꽃': 'light floral', '미모사': 'light floral', '은방울꽃': 'light floral', 'light floral': 'light floral',
            # white floral
            '화이트 플로럴': 'white floral', '튜베로즈': 'white floral', '가드니아': 'white floral', '오렌지 블라썸': 'white floral', 'white floral': 'white floral',
            # casual
            '캐쥬얼': 'casual', '린넨': 'casual', '면': 'casual', '일상': 'casual', 'casual': 'casual',
            # cozy
            '코지': 'cozy', '커피': 'cozy', '우드': 'cozy', '포근하고 푹신': 'cozy', 'cozy': 'cozy',
        }
        # 괄호/설명/공백/특수문자 제거 및 소문자화
        def clean_label(label):
            label = str(label)
            label = re.sub(r'\([^)]*\)', '', label)  # 괄호 및 괄호 안 설명 제거
            label = re.sub(r'[^\w가-힣 ]', '', label)  # 특수문자 제거
            label = label.strip().lower()
            return label

        # 쉼표/슬래시/공백 등으로 분리
        raw_cats = re.split(r'[,/]|\n|\t', str(category_text))
        result = set()
        for raw in raw_cats:
            cleaned = clean_label(raw)
            found = None
            for key, std in mapping.items():
                if key in cleaned:
                    found = std
                    break
            if found:
                result.add(found)
            else:
                # 표준 카테고리명 직접 포함시 그대로 사용
                for std in std_categories:
                    if std in cleaned:
                        result.add(std)
                        break
                else:
                    if cleaned:
                        result.add('other')
        return list(result)
    
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
    
    def preprocess_input(self, input_dict):
        """
        입력값의 라벨을 일관성 있게 정규화(한글/영문/표기 변형/unknown 처리)
        """
        # gender
        gender_map = {'여': 'F', '여성': 'F', '남': 'M', '남성': 'M', 'F': 'F', 'M': 'M', 'female': 'F', 'male': 'M', 'unisex': 'unisex'}
        # cost 예시 (실제 데이터에 맞게 확장 필요)
        cost_map = {
            '5만 이하': 'under_50k', '50k_to_100k': '50k_to_100k', '100k_to_200k': '100k_to_200k',
            '200k 이상': 'over_200k', 'mid-range': '50k_to_100k', 'budget': 'under_50k', 'luxury': 'over_200k'
        }
        # purpose 예시
        purpose_map = {
            '자기만족': 'self_satisfaction', 'good_impression': 'good_impression', 'special_event': 'special_event',
            'date_or_social': 'date_or_social', 'formal_occasion': 'formal_occasion'
        }
        # durability 예시
        durability_map = {
            '상관없음': 'any', '2_4_hours': '2_4_hours', '4_6_hours': '4_6_hours', 'over_6_hours': 'over_6_hours'
        }
        # fashionstyle 예시
        fashionstyle_map = {
            '캐주얼': 'casual', 'casual': 'casual', 'minimal': 'minimal', 'simple': 'simple',
            'street': 'street', 'modern': 'modern', 'chic': 'chic', 'sports': 'sports'
        }
        # prefercolor 예시 (공백/쉼표 제거)
        def normalize_color(val):
            if not isinstance(val, str):
                return 'unknown'
            return ','.join([c.strip().lower() for c in val.split(',')])

        # personality (그대로 사용)
        # age (그대로 사용)

        norm = dict(input_dict)
        norm['gender'] = gender_map.get(str(norm.get('gender', '')).strip(), 'F')
        norm['cost'] = cost_map.get(str(norm.get('cost', '')).strip(), '50k_to_100k')
        norm['purpose'] = purpose_map.get(str(norm.get('purpose', '')).strip(), 'good_impression')
        norm['durability'] = durability_map.get(str(norm.get('durability', '')).strip(), 'any')
        norm['fashionstyle'] = fashionstyle_map.get(str(norm.get('fashionstyle', '')).strip(), 'casual')
        norm['prefercolor'] = normalize_color(norm.get('prefercolor', 'unknown'))
        return norm

    def _expand_multilabel_columns(self, df, multilabel_cols, prefix_sep='_'):
        """
        멀티라벨 컬럼(콤마로 구분된 값)을 개별 컬럼(One-hot)으로 확장
        예: 'purpose' 컬럼에 'a,b' → purpose_a=1, purpose_b=1
        """
        for col in multilabel_cols:
            # 모든 유니크 값 추출
            all_labels = set()
            df[col] = df[col].fillna('')
            for items in df[col]:
                all_labels.update([i.strip() for i in str(items).split(',') if i.strip()])
            for label in sorted(all_labels):
                new_col = f"{col}{prefix_sep}{label}"
                df[new_col] = df[col].apply(lambda x: int(label in [i.strip() for i in str(x).split(',')]))
        df = df.drop(columns=multilabel_cols)
        return df

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

        # 범주형 변수 인코딩 (LabelEncoder)
        self.label_encoders = {}
        for column in X.select_dtypes(include=['object']).columns:
            le = LabelEncoder()
            X[column] = X[column].fillna('')
            X[column] = le.fit_transform(X[column])
            self.label_encoders[column] = le
        self.onehot_columns = None  # 사용하지 않음

        # 수치형 변수 스케일링
        X_scaled = self.scaler.fit_transform(X)

        # 멀티라벨 바이너리 인코딩
        y_bin = self.mlb.fit_transform(y)

        # 훈련/테스트 분할 (가중치 고려)
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test, w_train, w_test = train_test_split(
            X_scaled, y_bin, weights, test_size=0.2, random_state=42, stratify=None
        )
        
        # 멀티라벨 분류에 적합한 모델 설정
        from sklearn.ensemble import RandomForestClassifier
        base_classifier = RandomForestClassifier(
            n_estimators=200,  # 트리 개수 증가
            max_depth=10,      # 깊이 제한으로 과적합 방지
            min_samples_split=5,
            min_samples_leaf=2,
            class_weight='balanced',  # 클래스 불균형 처리
            random_state=42
        )
        self.model = OneVsRestClassifier(base_classifier)
        
        # 피드백 데이터가 있을 때만 가중치 적용
        if np.any(weights != 1.0):
            print(f"[DEBUG] 피드백 데이터(가중치!=1.0)가 있으므로 가중치 적용 훈련")
            print(f"[DEBUG] w_train type: {type(w_train)}, shape: {w_train.shape}, dtype: {w_train.dtype}")
            print(f"[DEBUG] w_train min: {w_train.min()}, max: {w_train.max()}, mean: {w_train.mean():.3f}")
            try:
                self.model.fit(X_train, y_train, sample_weight=w_train)
                print("[DEBUG] 가중치 적용하여 모델 훈련 성공!")
            except ValueError as e:
                print(f"[DEBUG] sample_weight 적용 실패: {e}")
                print("가중치 없이 모델 훈련")
                self.model.fit(X_train, y_train)
        else:
            print(f"[DEBUG] 피드백 데이터가 없으므로 가중치 없이 훈련")
            print(f"[DEBUG] X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")
            self.model.fit(X_train, y_train)
        
        # 모델 평가 - 멀티라벨 분류에 적합한 지표들
        y_pred = self.model.predict(X_test)
        
        # 1. Exact Match Accuracy (기존 accuracy)
        from sklearn.metrics import accuracy_score
        exact_accuracy = accuracy_score(y_test, y_pred)
        print(f"Exact Match Accuracy: {exact_accuracy:.3f}")
        
        # 2. Hamming Loss (멀티라벨 분류에 적합)
        from sklearn.metrics import hamming_loss
        hamming_loss_score = hamming_loss(y_test, y_pred)
        print(f"Hamming Loss: {hamming_loss_score:.3f} (낮을수록 좋음)")
        
        # 3. Micro-averaged F1 Score
        from sklearn.metrics import f1_score
        micro_f1 = f1_score(y_test, y_pred, average='micro', zero_division=0)
        print(f"Micro-averaged F1 Score: {micro_f1:.3f}")
        
        # 4. Macro-averaged F1 Score
        macro_f1 = f1_score(y_test, y_pred, average='macro', zero_division=0)
        print(f"Macro-averaged F1 Score: {macro_f1:.3f}")
        
        # 5. Subset Accuracy (Exact Match)
        from sklearn.metrics import jaccard_score
        subset_accuracy = jaccard_score(y_test, y_pred, average='samples', zero_division=0)
        print(f"Subset Accuracy (Jaccard): {subset_accuracy:.3f}")

        # Classification Report
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=self.mlb.classes_, zero_division=0))

        # Multilabel Confusion Matrix
        print("\nMultilabel Confusion Matrix:")
        print(multilabel_confusion_matrix(y_test, y_pred))
        
        # 각 라벨별 예측 성능 분석
        print("\n라벨별 예측 성능 분석:")
        for i, label in enumerate(self.mlb.classes_):
            true_count = np.sum(y_test[:, i])
            pred_count = np.sum(y_pred[:, i])
            correct_count = np.sum((y_test[:, i] == 1) & (y_pred[:, i] == 1))
            print(f"{label:15s}: 실제 {true_count:3d}개, 예측 {pred_count:3d}개, 정확 {correct_count:3d}개")
        
        self.is_trained = True
        self.last_retrain_date = datetime.utcnow()
        
        # 모델 저장
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
    
    def predict_categories(self, age: int, gender: str, personality: str, cost: str, purpose: str, durability: str, fashionstyle: str, prefercolor: str) -> tuple:
        """사용자 특성에 따른 향수 카테고리들을 예측합니다."""
        if not self.is_trained:
            raise ValueError("모델이 훈련되지 않았습니다. 먼저 train()을 호출하세요.")
        # 입력값 정규화
        input_dict = {
            'age': age,
            'gender': gender,
            'personality': personality,
            'cost': cost,
            'purpose': purpose,
            'durability': durability,
            'fashionstyle': fashionstyle,
            'prefercolor': prefercolor
        }
        input_dict = self.preprocess_input(input_dict)
        input_data = pd.DataFrame([input_dict])
        # 범주형 변수 인코딩 (LabelEncoder)
        for column in input_data.select_dtypes(include=['object']).columns:
            if column in self.label_encoders:
                le = self.label_encoders[column]
                values = input_data[column].values
                unknown_mask = ~input_data[column].isin(le.classes_)
                if unknown_mask.any():
                    replacement_label = le.classes_[0]
                    input_data.loc[unknown_mask, column] = replacement_label
                    print(f"Warning: Unknown label '{values[unknown_mask][0]}' in column '{column}' replaced with '{replacement_label}'")
                input_data[column] = le.transform(input_data[column])
        # 스케일링
        input_scaled = self.scaler.transform(input_data)
        # 예측
        y_pred_bin = self.model.predict(input_scaled)
        # 바이너리 결과를 라벨 리스트로 변환
        predicted_categories = self.mlb.inverse_transform(y_pred_bin)[0]
        # 신뢰도 계산 (예측된 라벨들의 평균 확률)
        y_pred_proba = self.model.predict_proba(input_scaled)
        confidence = np.mean([np.max(proba) for proba in y_pred_proba])
        return predicted_categories, confidence
    
    def get_recommendation_reason(self, predicted_categories: List[str], age: int, 
                                 gender: str, personality: str, season: str) -> str:
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