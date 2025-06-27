import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
from typing import List, Dict, Tuple
from datetime import datetime, timedelta

class PerfumeRecommendationModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.is_trained = False
        self.last_retrain_date = None
        
        # 모델 파일 경로 설정 (루트 디렉토리 기준)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # backend/app/models -> backend/app -> backend -> 루트
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        self.model_filepath = os.path.join(project_root, "ml_models", "perfume_recommendation_model.pkl")
        
    def get_feedback_weight(self, is_liked: bool, days_old: int) -> float:
        """피드백의 가중치를 계산합니다."""
        base_weight = 2.0 if is_liked else 1.0  # 좋아요는 더 높은 가중치
        
        # 시간에 따른 가중치 감소 (최신 피드백이 더 중요)
        time_decay = max(0.1, 1.0 - (days_old / 365))  # 1년 후 10%까지 감소
        
        return base_weight * time_decay
    
    def prepare_feedback_data(self, db_session) -> pd.DataFrame:
        """실제 사용자 피드백 데이터를 준비합니다."""
        from app.database import Recommendation, Perfume, User
        
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
            
            # 사용자 정보 조회 (익명 사용자는 기본값 사용)
            if record.user_id:
                user = db_session.query(User).filter(User.id == record.user_id).first()
                if user:
                    age = user.age
                    gender = user.gender
                    personality = user.personality
                    season_preference = user.season_preference
                else:
                    continue
            else:
                # 익명 사용자는 기본값 사용 (실제로는 더 정교한 방법 필요)
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
                    'perfume_category': perfume.category,
                    'weight': weight,
                    'source': 'feedback'
                })
        
        return pd.DataFrame(feedback_data)
    
    def prepare_enhanced_training_data(self, db_session=None) -> Tuple[pd.DataFrame, pd.Series, np.ndarray]:
        """향상된 훈련 데이터를 준비합니다 (샘플 데이터 + 피드백 데이터)."""
        # 기본 샘플 데이터
        sample_df = self.prepare_sample_data()
        sample_df['weight'] = 1.0  # 샘플 데이터는 기본 가중치
        sample_df['source'] = 'sample'
        
        # 피드백 데이터 (가능한 경우)
        feedback_df = pd.DataFrame()
        if db_session:
            try:
                feedback_df = self.prepare_feedback_data(db_session)
            except Exception as e:
                print(f"피드백 데이터 로드 실패: {e}")
        
        # 데이터 결합
        if not feedback_df.empty:
            combined_df = pd.concat([sample_df, feedback_df], ignore_index=True)
            print(f"훈련 데이터: 샘플 {len(sample_df)}개, 피드백 {len(feedback_df)}개")
        else:
            combined_df = sample_df
            print(f"훈련 데이터: 샘플 {len(sample_df)}개")
        
        # 특성과 타겟 분리
        features = ['age', 'gender', 'personality', 'season_preference']
        X = combined_df[features]
        y = combined_df['perfume_category']
        weights = combined_df['weight'].values
        
        return X, y, weights
    
    def prepare_sample_data(self) -> pd.DataFrame:
        """샘플 향수 데이터를 생성합니다."""
        np.random.seed(42)
        
        # 향수 카테고리별 샘플 데이터
        perfumes_data = []
        
        # 플로럴 향수들
        floral_perfumes = [
            {"name": "Rose Garden", "brand": "Floral Essence", "category": "floral", 
             "top_notes": "rose, jasmine", "middle_notes": "lily, peony", "base_notes": "musk, vanilla",
             "price_range": "mid-range", "season_suitability": "spring", "personality_match": "introvert",
             "age_group": "adult", "gender_target": "female"},
            {"name": "Lavender Dreams", "brand": "Nature Scents", "category": "floral",
             "top_notes": "lavender, bergamot", "middle_notes": "rose, violet", "base_notes": "sandalwood, amber",
             "price_range": "budget", "season_suitability": "spring", "personality_match": "introvert",
             "age_group": "young", "gender_target": "unisex"},
        ]
        
        # 우디 향수들
        woody_perfumes = [
            {"name": "Sandalwood Forest", "brand": "Wood & Co", "category": "woody",
             "top_notes": "cedar, pine", "middle_notes": "sandalwood, oakmoss", "base_notes": "amber, musk",
             "price_range": "luxury", "season_suitability": "autumn", "personality_match": "introvert",
             "age_group": "mature", "gender_target": "male"},
            {"name": "Oak & Leather", "brand": "Heritage", "category": "woody",
             "top_notes": "leather, tobacco", "middle_notes": "oak, cedar", "base_notes": "vanilla, patchouli",
             "price_range": "mid-range", "season_suitability": "autumn", "personality_match": "extrovert",
             "age_group": "adult", "gender_target": "male"},
        ]
        
        # 프레시 향수들
        fresh_perfumes = [
            {"name": "Ocean Breeze", "brand": "Aqua Scents", "category": "fresh",
             "top_notes": "citrus, sea salt", "middle_notes": "marine, cucumber", "base_notes": "musk, white woods",
             "price_range": "budget", "season_suitability": "summer", "personality_match": "extrovert",
             "age_group": "young", "gender_target": "unisex"},
            {"name": "Mountain Air", "brand": "Alpine", "category": "fresh",
             "top_notes": "pine, mint", "middle_notes": "eucalyptus, sage", "base_notes": "cedar, amber",
             "price_range": "mid-range", "season_suitability": "summer", "personality_match": "balanced",
             "age_group": "adult", "gender_target": "unisex"},
        ]
        
        # 오리엔탈 향수들
        oriental_perfumes = [
            {"name": "Spice Market", "brand": "Exotic", "category": "oriental",
             "top_notes": "cardamom, saffron", "middle_notes": "rose, jasmine", "base_notes": "amber, oud",
             "price_range": "luxury", "season_suitability": "winter", "personality_match": "extrovert",
             "age_group": "mature", "gender_target": "female"},
            {"name": "Vanilla Dreams", "brand": "Sweet Scents", "category": "oriental",
             "top_notes": "vanilla, tonka bean", "middle_notes": "cinnamon, clove", "base_notes": "musk, sandalwood",
             "price_range": "mid-range", "season_suitability": "winter", "personality_match": "introvert",
             "age_group": "adult", "gender_target": "female"},
        ]
        
        # 시트러스 향수들
        citrus_perfumes = [
            {"name": "Lemon Zest", "brand": "Citrus Fresh", "category": "citrus",
             "top_notes": "lemon, lime", "middle_notes": "grapefruit, orange", "base_notes": "cedar, musk",
             "price_range": "budget", "season_suitability": "summer", "personality_match": "extrovert",
             "age_group": "young", "gender_target": "unisex"},
            {"name": "Bergamot Bliss", "brand": "Italian Scents", "category": "citrus",
             "top_notes": "bergamot, mandarin", "middle_notes": "neroli, petitgrain", "base_notes": "oakmoss, amber",
             "price_range": "mid-range", "season_suitability": "spring", "personality_match": "balanced",
             "age_group": "adult", "gender_target": "unisex"},
        ]
        
        all_perfumes = floral_perfumes + woody_perfumes + fresh_perfumes + oriental_perfumes + citrus_perfumes
        
        # 사용자 선호도와 매칭되는 향수 데이터 생성
        for perfume in all_perfumes:
            for age in [20, 25, 30, 35, 40, 45, 50]:
                for gender in ["male", "female", "other"]:
                    for personality in ["introvert", "extrovert", "balanced"]:
                        for season in ["spring", "summer", "autumn", "winter"]:
                            # 매칭 점수 계산
                            match_score = self._calculate_match_score(
                                perfume, age, gender, personality, season
                            )
                            
                            # 매칭 점수가 높은 경우만 데이터에 포함
                            if match_score > 0.6:
                                perfumes_data.append({
                                    'age': age,
                                    'gender': gender,
                                    'personality': personality,
                                    'season_preference': season,
                                    'perfume_category': perfume['category'],
                                    'price_range': perfume['price_range'],
                                    'season_suitability': perfume['season_suitability'],
                                    'personality_match': perfume['personality_match'],
                                    'age_group': perfume['age_group'],
                                    'gender_target': perfume['gender_target'],
                                    'match_score': match_score
                                })
        
        return pd.DataFrame(perfumes_data)
    
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
    
    def prepare_training_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        """훈련 데이터를 준비합니다."""
        df = self.prepare_sample_data()
        
        # 특성과 타겟 분리
        features = ['age', 'gender', 'personality', 'season_preference']
        X = df[features]
        y = df['perfume_category']
        
        return X, y
    
    def train(self, db_session=None, force_retrain=False):
        """모델을 훈련합니다."""
        # 재훈련 필요성 확인
        if not force_retrain and self.should_retrain():
            print("재훈련이 필요하지 않습니다.")
            return
        
        X, y, weights = self.prepare_enhanced_training_data(db_session)
        
        # 범주형 변수 인코딩
        for column in X.select_dtypes(include=['object']).columns:
            le = LabelEncoder()
            X[column] = le.fit_transform(X[column])
            self.label_encoders[column] = le
        
        # 수치형 변수 스케일링
        X_scaled = self.scaler.fit_transform(X)
        
        # 훈련/테스트 분할 (가중치 고려)
        X_train, X_test, y_train, y_test, w_train, w_test = train_test_split(
            X_scaled, y, weights, test_size=0.2, random_state=42, stratify=y
        )
        
        # 가중치 기반 모델 훈련
        self.model.fit(X_train, y_train, sample_weight=w_train)
        
        # 모델 평가
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model accuracy: {accuracy:.3f}")
        
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
        """피드백 데이터를 포함하여 모델을 재훈련합니다."""
        print("피드백 데이터를 포함한 모델 재훈련을 시작합니다...")
        self.train(db_session, force_retrain=True)
        print("모델 재훈련이 완료되었습니다.")
    
    def predict_category(self, age: int, gender: str, personality: str, 
                        season: str) -> Tuple[str, float]:
        """사용자 특성에 따른 향수 카테고리를 예측합니다."""
        if not self.is_trained:
            self.train()
        
        # 입력 데이터 검증 및 기본값 설정
        if not gender or gender.strip() == "":
            gender = "other"
        if not personality or personality.strip() == "":
            personality = "balanced"
        if not season or season.strip() == "":
            season = "spring"
        
        # 입력 데이터 준비
        input_data = pd.DataFrame([{
            'age': age,
            'gender': gender,
            'personality': personality,
            'season_preference': season
        }])
        
        # 범주형 변수 인코딩
        for column in input_data.select_dtypes(include=['object']).columns:
            if column in self.label_encoders:
                # 빈 값이나 None 값을 기본값으로 대체
                input_data[column] = input_data[column].fillna('other' if column == 'gender' else 'balanced' if column == 'personality' else 'spring')
                input_data[column] = self.label_encoders[column].transform(input_data[column])
        
        # 스케일링
        input_scaled = self.scaler.transform(input_data)
        
        # 예측
        prediction = self.model.predict(input_scaled)[0]
        confidence = max(self.model.predict_proba(input_scaled)[0])
        
        return prediction, confidence
    
    def get_recommendation_reason(self, predicted_category: str, age: int, 
                                 gender: str, personality: str, season: str) -> str:
        """추천 이유를 생성합니다."""
        reasons = []
        
        if predicted_category == "floral":
            if gender == "female":
                reasons.append("여성스러운 플로럴 향이 당신의 우아함을 강조합니다")
            if season == "spring":
                reasons.append("봄철에 어울리는 신선한 꽃향기입니다")
        elif predicted_category == "woody":
            if personality == "introvert":
                reasons.append("차분한 우디 향이 당신의 내면의 깊이를 표현합니다")
            if season == "autumn":
                reasons.append("가을철에 완벽한 따뜻한 우디 향입니다")
        elif predicted_category == "fresh":
            if personality == "extrovert":
                reasons.append("활기찬 프레시 향이 당신의 에너지를 돋보이게 합니다")
            if season == "summer":
                reasons.append("여름철에 시원한 프레시 향입니다")
        elif predicted_category == "oriental":
            if age > 40:
                reasons.append("성숙한 오리엔탈 향이 당신의 매력을 극대화합니다")
            if season == "winter":
                reasons.append("겨울철에 따뜻한 오리엔탈 향입니다")
        elif predicted_category == "citrus":
            if age < 30:
                reasons.append("젊은 시트러스 향이 당신의 활력을 표현합니다")
            if season in ["spring", "summer"]:
                reasons.append("봄/여름철에 상쾌한 시트러스 향입니다")
        
        if not reasons:
            reasons.append(f"당신의 선호도와 잘 맞는 {predicted_category} 향입니다")
        
        return " ".join(reasons)
    
    def save_model(self):
        """모델을 저장합니다."""
        os.makedirs(os.path.dirname(self.model_filepath), exist_ok=True)
        
        model_data = {
            'model': self.model,
            'label_encoders': self.label_encoders,
            'scaler': self.scaler,
            'is_trained': self.is_trained,
            'last_retrain_date': self.last_retrain_date
        }
        
        joblib.dump(model_data, self.model_filepath)
        print(f"Model saved to {self.model_filepath}")
    
    def load_model(self):
        """모델을 로드합니다."""
        if os.path.exists(self.model_filepath):
            model_data = joblib.load(self.model_filepath)
            self.model = model_data['model']
            self.label_encoders = model_data['label_encoders']
            self.scaler = model_data['scaler']
            self.is_trained = model_data['is_trained']
            self.last_retrain_date = model_data.get('last_retrain_date', None)
            print(f"Model loaded from {self.model_filepath}")
        else:
            print("Model file not found. Training new model...")
            self.train() 