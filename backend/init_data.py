from app.database import engine, Base, SessionLocal, Perfume, PerfumeRecipe
from app.models.recommendation_model import PerfumeRecommendationModel

def init_database():
    """데이터베이스를 초기화합니다."""
    Base.metadata.create_all(bind=engine)
    print("데이터베이스 테이블이 생성되었습니다.")

def create_sample_perfumes():
    """샘플 향수 데이터를 생성합니다."""
    db = SessionLocal()
    
    # 기존 데이터 삭제
    db.query(PerfumeRecipe).delete()
    db.query(Perfume).delete()
    db.commit()
    
    # 향수 데이터
    perfumes_data = [
        {
            "name": "Rose Garden",
            "brand": "Floral Essence",
            "category": "floral",
            "top_notes": "rose, jasmine, bergamot",
            "middle_notes": "lily, peony, violet",
            "base_notes": "musk, vanilla, sandalwood",
            "description": "우아하고 로맨틱한 플로럴 향수로, 신선한 장미와 재스민의 조화가 특징입니다.",
            "price_range": "mid-range",
            "season_suitability": "spring",
            "personality_match": "introvert",
            "age_group": "adult",
            "gender_target": "female",
            "recipes": [
                {"ingredient_name": "Rose Essential Oil", "percentage": 15.0, "notes": "메인 플로럴 노트"},
                {"ingredient_name": "Jasmine Absolute", "percentage": 10.0, "notes": "센추얼 플로럴 노트"},
                {"ingredient_name": "Bergamot Oil", "percentage": 8.0, "notes": "톱 노트"},
                {"ingredient_name": "Lily Oil", "percentage": 12.0, "notes": "미들 노트"},
                {"ingredient_name": "Vanilla Absolute", "percentage": 5.0, "notes": "베이스 노트"},
                {"ingredient_name": "Sandalwood Oil", "percentage": 8.0, "notes": "우디 베이스"},
                {"ingredient_name": "Musk", "percentage": 3.0, "notes": "픽서"},
                {"ingredient_name": "Alcohol", "percentage": 39.0, "notes": "베이스"}
            ]
        },
        {
            "name": "Sandalwood Forest",
            "brand": "Wood & Co",
            "category": "woody",
            "top_notes": "cedar, pine, bergamot",
            "middle_notes": "sandalwood, oakmoss, patchouli",
            "base_notes": "amber, musk, vanilla",
            "description": "깊고 따뜻한 우디 향수로, 상당목과 파인의 신선함이 샌달우드의 부드러움과 조화를 이룹니다.",
            "price_range": "luxury",
            "season_suitability": "autumn",
            "personality_match": "introvert",
            "age_group": "mature",
            "gender_target": "male",
            "recipes": [
                {"ingredient_name": "Sandalwood Oil", "percentage": 20.0, "notes": "메인 우디 노트"},
                {"ingredient_name": "Cedar Oil", "percentage": 12.0, "notes": "톱 우디 노트"},
                {"ingredient_name": "Pine Oil", "percentage": 8.0, "notes": "톱 노트"},
                {"ingredient_name": "Oakmoss", "percentage": 5.0, "notes": "미들 노트"},
                {"ingredient_name": "Patchouli Oil", "percentage": 8.0, "notes": "어스 노트"},
                {"ingredient_name": "Amber", "percentage": 7.0, "notes": "베이스 노트"},
                {"ingredient_name": "Musk", "percentage": 3.0, "notes": "픽서"},
                {"ingredient_name": "Alcohol", "percentage": 37.0, "notes": "베이스"}
            ]
        },
        {
            "name": "Ocean Breeze",
            "brand": "Aqua Scents",
            "category": "fresh",
            "top_notes": "citrus, sea salt, bergamot",
            "middle_notes": "marine, cucumber, mint",
            "base_notes": "musk, white woods, amber",
            "description": "시원하고 상쾌한 프레시 향수로, 바다의 신선함과 시트러스의 활기를 담았습니다.",
            "price_range": "budget",
            "season_suitability": "summer",
            "personality_match": "extrovert",
            "age_group": "young",
            "gender_target": "unisex",
            "recipes": [
                {"ingredient_name": "Bergamot Oil", "percentage": 15.0, "notes": "메인 시트러스 노트"},
                {"ingredient_name": "Lemon Oil", "percentage": 10.0, "notes": "톱 노트"},
                {"ingredient_name": "Marine Accord", "percentage": 12.0, "notes": "아쿠아틱 노트"},
                {"ingredient_name": "Cucumber Extract", "percentage": 8.0, "notes": "프레시 노트"},
                {"ingredient_name": "Mint Oil", "percentage": 5.0, "notes": "쿨링 노트"},
                {"ingredient_name": "White Woods", "percentage": 8.0, "notes": "베이스 노트"},
                {"ingredient_name": "Musk", "percentage": 2.0, "notes": "픽서"},
                {"ingredient_name": "Alcohol", "percentage": 40.0, "notes": "베이스"}
            ]
        },
        {
            "name": "Spice Market",
            "brand": "Exotic",
            "category": "oriental",
            "top_notes": "cardamom, saffron, bergamot",
            "middle_notes": "rose, jasmine, cinnamon",
            "base_notes": "amber, oud, vanilla",
            "description": "매혹적이고 신비로운 오리엔탈 향수로, 동양의 향신료와 꽃의 조화가 특징입니다.",
            "price_range": "luxury",
            "season_suitability": "winter",
            "personality_match": "extrovert",
            "age_group": "mature",
            "gender_target": "female",
            "recipes": [
                {"ingredient_name": "Oud Oil", "percentage": 8.0, "notes": "메인 오리엔탈 노트"},
                {"ingredient_name": "Cardamom Oil", "percentage": 12.0, "notes": "스파이시 톱 노트"},
                {"ingredient_name": "Saffron", "percentage": 5.0, "notes": "프리미엄 스파이스"},
                {"ingredient_name": "Rose Oil", "percentage": 10.0, "notes": "플로럴 미들 노트"},
                {"ingredient_name": "Jasmine Absolute", "percentage": 8.0, "notes": "센추얼 노트"},
                {"ingredient_name": "Cinnamon Oil", "percentage": 6.0, "notes": "스파이시 노트"},
                {"ingredient_name": "Amber", "percentage": 8.0, "notes": "베이스 노트"},
                {"ingredient_name": "Vanilla Absolute", "percentage": 3.0, "notes": "스위트 베이스"},
                {"ingredient_name": "Alcohol", "percentage": 40.0, "notes": "베이스"}
            ]
        },
        {
            "name": "Lemon Zest",
            "brand": "Citrus Fresh",
            "category": "citrus",
            "top_notes": "lemon, lime, grapefruit",
            "middle_notes": "orange, mandarin, neroli",
            "base_notes": "cedar, musk, amber",
            "description": "상쾌하고 활기찬 시트러스 향수로, 레몬과 라임의 신선함이 오렌지의 달콤함과 조화를 이룹니다.",
            "price_range": "budget",
            "season_suitability": "summer",
            "personality_match": "extrovert",
            "age_group": "young",
            "gender_target": "unisex",
            "recipes": [
                {"ingredient_name": "Lemon Oil", "percentage": 18.0, "notes": "메인 시트러스 노트"},
                {"ingredient_name": "Lime Oil", "percentage": 12.0, "notes": "톱 노트"},
                {"ingredient_name": "Grapefruit Oil", "percentage": 10.0, "notes": "톱 노트"},
                {"ingredient_name": "Orange Oil", "percentage": 8.0, "notes": "미들 노트"},
                {"ingredient_name": "Mandarin Oil", "percentage": 6.0, "notes": "미들 노트"},
                {"ingredient_name": "Neroli Oil", "percentage": 4.0, "notes": "플로럴 노트"},
                {"ingredient_name": "Cedar Oil", "percentage": 8.0, "notes": "베이스 노트"},
                {"ingredient_name": "Musk", "percentage": 2.0, "notes": "픽서"},
                {"ingredient_name": "Alcohol", "percentage": 32.0, "notes": "베이스"}
            ]
        },
        {
            "name": "Lavender Dreams",
            "brand": "Nature Scents",
            "category": "floral",
            "top_notes": "lavender, bergamot, lemon",
            "middle_notes": "rose, violet, sage",
            "base_notes": "sandalwood, amber, musk",
            "description": "차분하고 편안한 라벤더 향수로, 스트레스 해소와 휴식을 돕는 아로마테라피 효과가 있습니다.",
            "price_range": "budget",
            "season_suitability": "spring",
            "personality_match": "introvert",
            "age_group": "young",
            "gender_target": "unisex",
            "recipes": [
                {"ingredient_name": "Lavender Oil", "percentage": 20.0, "notes": "메인 플로럴 노트"},
                {"ingredient_name": "Bergamot Oil", "percentage": 10.0, "notes": "톱 노트"},
                {"ingredient_name": "Lemon Oil", "percentage": 8.0, "notes": "톱 노트"},
                {"ingredient_name": "Rose Oil", "percentage": 8.0, "notes": "미들 노트"},
                {"ingredient_name": "Violet Leaf", "percentage": 5.0, "notes": "미들 노트"},
                {"ingredient_name": "Sage Oil", "percentage": 4.0, "notes": "허브 노트"},
                {"ingredient_name": "Sandalwood Oil", "percentage": 8.0, "notes": "베이스 노트"},
                {"ingredient_name": "Amber", "percentage": 5.0, "notes": "베이스 노트"},
                {"ingredient_name": "Musk", "percentage": 2.0, "notes": "픽서"},
                {"ingredient_name": "Alcohol", "percentage": 30.0, "notes": "베이스"}
            ]
        },
        {
            "name": "Vanilla Dreams",
            "brand": "Sweet Scents",
            "category": "oriental",
            "top_notes": "vanilla, tonka bean, bergamot",
            "middle_notes": "cinnamon, clove, jasmine",
            "base_notes": "musk, sandalwood, amber",
            "description": "달콤하고 따뜻한 바닐라 향수로, 로맨틱하고 여성스러운 매력을 표현합니다.",
            "price_range": "mid-range",
            "season_suitability": "winter",
            "personality_match": "introvert",
            "age_group": "adult",
            "gender_target": "female",
            "recipes": [
                {"ingredient_name": "Vanilla Absolute", "percentage": 15.0, "notes": "메인 스위트 노트"},
                {"ingredient_name": "Tonka Bean", "percentage": 8.0, "notes": "톱 노트"},
                {"ingredient_name": "Bergamot Oil", "percentage": 6.0, "notes": "톱 노트"},
                {"ingredient_name": "Cinnamon Oil", "percentage": 8.0, "notes": "스파이시 노트"},
                {"ingredient_name": "Clove Oil", "percentage": 4.0, "notes": "스파이시 노트"},
                {"ingredient_name": "Jasmine Absolute", "percentage": 6.0, "notes": "플로럴 노트"},
                {"ingredient_name": "Sandalwood Oil", "percentage": 8.0, "notes": "베이스 노트"},
                {"ingredient_name": "Amber", "percentage": 6.0, "notes": "베이스 노트"},
                {"ingredient_name": "Musk", "percentage": 3.0, "notes": "픽서"},
                {"ingredient_name": "Alcohol", "percentage": 36.0, "notes": "베이스"}
            ]
        }
    ]
    
    # 향수 데이터 생성
    for perfume_data in perfumes_data:
        recipes = perfume_data.pop("recipes")
        
        db_perfume = Perfume(**perfume_data)
        db.add(db_perfume)
        db.commit()
        db.refresh(db_perfume)
        
        # 제조법 데이터 생성
        for recipe_data in recipes:
            db_recipe = PerfumeRecipe(
                perfume_id=db_perfume.id,
                **recipe_data
            )
            db.add(db_recipe)
        
        db.commit()
        print(f"향수 '{db_perfume.name}' 생성 완료")
    
    db.close()
    print("샘플 향수 데이터 생성이 완료되었습니다.")

def train_ml_model():
    """ML 모델을 훈련합니다."""
    model = PerfumeRecommendationModel()
    model.train()
    print("ML 모델 훈련이 완료되었습니다.")

if __name__ == "__main__":
    print("향수 추천 시스템 초기화를 시작합니다...")
    
    # 데이터베이스 초기화
    init_database()
    
    # 샘플 데이터 생성
    create_sample_perfumes()
    
    # ML 모델 훈련
    train_ml_model()
    
    print("초기화가 완료되었습니다!") 