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
    
    # 향수 데이터 (멀티라벨 분류에 맞는 현대적인 향수들)
    perfumes_data = [
        {
            "name": "Citrus Wood Harmony",
            "brand": "Modern Scents",
            "category": "citrus",
            "top_notes": "bergamot, lemon, grapefruit",
            "middle_notes": "cedar, sandalwood, vetiver",
            "base_notes": "musk, amber, vanilla",
            "description": "상큼한 시트러스와 따뜻한 우디 노트의 완벽한 조화. 현대적이고 세련된 향수입니다.",
            "price_range": "mid-range",
            "season_suitability": "all",
            "personality_match": "extrovert",
            "age_group": "adult",
            "gender_target": "unisex",
            "recipes": [
                {"ingredient_name": "Bergamot Oil", "percentage": 15.0, "notes": "메인 시트러스 노트"},
                {"ingredient_name": "Lemon Oil", "percentage": 10.0, "notes": "톱 노트"},
                {"ingredient_name": "Cedar Oil", "percentage": 12.0, "notes": "우디 미들 노트"},
                {"ingredient_name": "Sandalwood Oil", "percentage": 8.0, "notes": "우디 베이스"},
                {"ingredient_name": "Vetiver Oil", "percentage": 5.0, "notes": "어스 노트"},
                {"ingredient_name": "Musk", "percentage": 3.0, "notes": "픽서"},
                {"ingredient_name": "Alcohol", "percentage": 47.0, "notes": "베이스"}
            ]
        },
        {
            "name": "Floral Musk Elegance",
            "brand": "Luxury Scents",
            "category": "floral",
            "top_notes": "rose, jasmine, peony",
            "middle_notes": "lily, violet, iris",
            "base_notes": "musk, amber, sandalwood",
            "description": "우아한 플로럴과 센추얼한 머스크의 조화. 여성스럽고 세련된 향수입니다.",
            "price_range": "luxury",
            "season_suitability": "spring",
            "personality_match": "introvert",
            "age_group": "adult",
            "gender_target": "female",
            "recipes": [
                {"ingredient_name": "Rose Absolute", "percentage": 12.0, "notes": "메인 플로럴 노트"},
                {"ingredient_name": "Jasmine Absolute", "percentage": 10.0, "notes": "센추얼 플로럴"},
                {"ingredient_name": "Peony Oil", "percentage": 8.0, "notes": "미들 플로럴"},
                {"ingredient_name": "Lily Oil", "percentage": 6.0, "notes": "미들 노트"},
                {"ingredient_name": "Musk", "percentage": 8.0, "notes": "베이스 노트"},
                {"ingredient_name": "Amber", "percentage": 6.0, "notes": "베이스 노트"},
                {"ingredient_name": "Alcohol", "percentage": 50.0, "notes": "베이스"}
            ]
        },
        {
            "name": "Aquatic Citrus Fresh",
            "brand": "Ocean Scents",
            "category": "aquatic",
            "top_notes": "marine, bergamot, lemon",
            "middle_notes": "sea salt, cucumber, mint",
            "base_notes": "white musk, amber, driftwood",
            "description": "바다의 신선함과 시트러스의 활기를 담은 상쾌한 향수입니다.",
            "price_range": "budget",
            "season_suitability": "summer",
            "personality_match": "extrovert",
            "age_group": "young",
            "gender_target": "unisex",
            "recipes": [
                {"ingredient_name": "Marine Accord", "percentage": 15.0, "notes": "메인 아쿠아틱 노트"},
                {"ingredient_name": "Bergamot Oil", "percentage": 12.0, "notes": "시트러스 톱 노트"},
                {"ingredient_name": "Sea Salt", "percentage": 8.0, "notes": "미네랄 노트"},
                {"ingredient_name": "Cucumber Extract", "percentage": 6.0, "notes": "프레시 노트"},
                {"ingredient_name": "White Musk", "percentage": 5.0, "notes": "베이스 노트"},
                {"ingredient_name": "Alcohol", "percentage": 54.0, "notes": "베이스"}
            ]
        },
        {
            "name": "Oriental Woody Mystique",
            "brand": "Exotic Scents",
            "category": "oriental",
            "top_notes": "saffron, cardamom, bergamot",
            "middle_notes": "rose, oud, sandalwood",
            "base_notes": "amber, vanilla, musk",
            "description": "신비로운 오리엔탈과 깊은 우디 노트의 조화. 매혹적이고 고급스러운 향수입니다.",
            "price_range": "luxury",
            "season_suitability": "winter",
            "personality_match": "extrovert",
            "age_group": "mature",
            "gender_target": "unisex",
            "recipes": [
                {"ingredient_name": "Oud Oil", "percentage": 8.0, "notes": "메인 오리엔탈 노트"},
                {"ingredient_name": "Saffron", "percentage": 5.0, "notes": "프리미엄 스파이스"},
                {"ingredient_name": "Cardamom Oil", "percentage": 10.0, "notes": "스파이시 노트"},
                {"ingredient_name": "Rose Oil", "percentage": 8.0, "notes": "플로럴 노트"},
                {"ingredient_name": "Sandalwood Oil", "percentage": 12.0, "notes": "우디 베이스"},
                {"ingredient_name": "Amber", "percentage": 8.0, "notes": "베이스 노트"},
                {"ingredient_name": "Alcohol", "percentage": 49.0, "notes": "베이스"}
            ]
        },
        {
            "name": "Green Aromatic Nature",
            "brand": "Nature Scents",
            "category": "green",
            "top_notes": "grass, leaves, bergamot",
            "middle_notes": "sage, rosemary, thyme",
            "base_notes": "moss, cedar, musk",
            "description": "자연의 신선함과 허브의 상쾌함을 담은 그린 향수입니다.",
            "price_range": "mid-range",
            "season_suitability": "spring",
            "personality_match": "introvert",
            "age_group": "adult",
            "gender_target": "unisex",
            "recipes": [
                {"ingredient_name": "Grass Extract", "percentage": 12.0, "notes": "메인 그린 노트"},
                {"ingredient_name": "Sage Oil", "percentage": 8.0, "notes": "허브 노트"},
                {"ingredient_name": "Rosemary Oil", "percentage": 6.0, "notes": "허브 노트"},
                {"ingredient_name": "Moss", "percentage": 5.0, "notes": "어스 노트"},
                {"ingredient_name": "Cedar Oil", "percentage": 8.0, "notes": "우디 베이스"},
                {"ingredient_name": "Musk", "percentage": 3.0, "notes": "픽서"},
                {"ingredient_name": "Alcohol", "percentage": 58.0, "notes": "베이스"}
            ]
        },
        {
            "name": "Gourmand Vanilla Delight",
            "brand": "Sweet Scents",
            "category": "gourmand",
            "top_notes": "vanilla, caramel, bergamot",
            "middle_notes": "chocolate, coffee, cinnamon",
            "base_notes": "musk, amber, sandalwood",
            "description": "달콤하고 따뜻한 구르망 향수로, 로맨틱한 분위기를 연출합니다.",
            "price_range": "mid-range",
            "season_suitability": "winter",
            "personality_match": "introvert",
            "age_group": "adult",
            "gender_target": "female",
            "recipes": [
                {"ingredient_name": "Vanilla Absolute", "percentage": 15.0, "notes": "메인 스위트 노트"},
                {"ingredient_name": "Caramel", "percentage": 8.0, "notes": "스위트 노트"},
                {"ingredient_name": "Chocolate", "percentage": 6.0, "notes": "구르망 노트"},
                {"ingredient_name": "Coffee", "percentage": 4.0, "notes": "구르망 노트"},
                {"ingredient_name": "Cinnamon Oil", "percentage": 5.0, "notes": "스파이시 노트"},
                {"ingredient_name": "Amber", "percentage": 6.0, "notes": "베이스 노트"},
                {"ingredient_name": "Alcohol", "percentage": 56.0, "notes": "베이스"}
            ]
        },
        {
            "name": "Powdery Floral Grace",
            "brand": "Elegant Scents",
            "category": "powdery",
            "top_notes": "iris, violet, bergamot",
            "middle_notes": "rose, peony, lily",
            "base_notes": "musk, amber, vanilla",
            "description": "부드럽고 우아한 파우더리 향수로, 클래식하고 세련된 매력을 표현합니다.",
            "price_range": "luxury",
            "season_suitability": "spring",
            "personality_match": "introvert",
            "age_group": "mature",
            "gender_target": "female",
            "recipes": [
                {"ingredient_name": "Iris Root", "percentage": 10.0, "notes": "메인 파우더리 노트"},
                {"ingredient_name": "Violet Leaf", "percentage": 8.0, "notes": "파우더리 노트"},
                {"ingredient_name": "Rose Oil", "percentage": 8.0, "notes": "플로럴 노트"},
                {"ingredient_name": "Peony Oil", "percentage": 6.0, "notes": "플로럴 노트"},
                {"ingredient_name": "Musk", "percentage": 8.0, "notes": "베이스 노트"},
                {"ingredient_name": "Amber", "percentage": 6.0, "notes": "베이스 노트"},
                {"ingredient_name": "Alcohol", "percentage": 54.0, "notes": "베이스"}
            ]
        },
        {
            "name": "Fruity Floral Joy",
            "brand": "Fresh Scents",
            "category": "fruity",
            "top_notes": "peach, apple, bergamot",
            "middle_notes": "rose, jasmine, peony",
            "base_notes": "musk, amber, vanilla",
            "description": "달콤하고 생기있는 프루티 향수로, 젊고 활기찬 매력을 표현합니다.",
            "price_range": "budget",
            "season_suitability": "summer",
            "personality_match": "extrovert",
            "age_group": "young",
            "gender_target": "female",
            "recipes": [
                {"ingredient_name": "Peach Extract", "percentage": 12.0, "notes": "메인 프루티 노트"},
                {"ingredient_name": "Apple Extract", "percentage": 8.0, "notes": "프루티 노트"},
                {"ingredient_name": "Rose Oil", "percentage": 6.0, "notes": "플로럴 노트"},
                {"ingredient_name": "Jasmine Absolute", "percentage": 5.0, "notes": "플로럴 노트"},
                {"ingredient_name": "Musk", "percentage": 4.0, "notes": "베이스 노트"},
                {"ingredient_name": "Alcohol", "percentage": 65.0, "notes": "베이스"}
            ]
        },
        {
            "name": "Aromatic Herbal Fresh",
            "brand": "Herbal Scents",
            "category": "aromatic",
            "top_notes": "lavender, rosemary, bergamot",
            "middle_notes": "sage, thyme, mint",
            "base_notes": "cedar, amber, musk",
            "description": "상쾌한 허브와 아로마틱 노트의 조화로 스트레스 해소에 도움을 줍니다.",
            "price_range": "budget",
            "season_suitability": "all",
            "personality_match": "introvert",
            "age_group": "adult",
            "gender_target": "unisex",
            "recipes": [
                {"ingredient_name": "Lavender Oil", "percentage": 15.0, "notes": "메인 아로마틱 노트"},
                {"ingredient_name": "Rosemary Oil", "percentage": 10.0, "notes": "허브 노트"},
                {"ingredient_name": "Sage Oil", "percentage": 6.0, "notes": "허브 노트"},
                {"ingredient_name": "Thyme Oil", "percentage": 4.0, "notes": "허브 노트"},
                {"ingredient_name": "Cedar Oil", "percentage": 8.0, "notes": "우디 베이스"},
                {"ingredient_name": "Musk", "percentage": 3.0, "notes": "픽서"},
                {"ingredient_name": "Alcohol", "percentage": 54.0, "notes": "베이스"}
            ]
        },
        {
            "name": "Chypre Oakmoss Classic",
            "brand": "Classic Scents",
            "category": "chypre",
            "top_notes": "bergamot, lemon, oakmoss",
            "middle_notes": "rose, jasmine, patchouli",
            "base_notes": "musk, amber, sandalwood",
            "description": "클래식한 시프레 향수로, 우아하고 세련된 고전적 매력을 표현합니다.",
            "price_range": "luxury",
            "season_suitability": "autumn",
            "personality_match": "introvert",
            "age_group": "mature",
            "gender_target": "unisex",
            "recipes": [
                {"ingredient_name": "Oakmoss", "percentage": 8.0, "notes": "메인 시프레 노트"},
                {"ingredient_name": "Bergamot Oil", "percentage": 12.0, "notes": "시트러스 톱 노트"},
                {"ingredient_name": "Rose Oil", "percentage": 8.0, "notes": "플로럴 노트"},
                {"ingredient_name": "Jasmine Absolute", "percentage": 6.0, "notes": "플로럴 노트"},
                {"ingredient_name": "Patchouli Oil", "percentage": 8.0, "notes": "어스 노트"},
                {"ingredient_name": "Sandalwood Oil", "percentage": 8.0, "notes": "우디 베이스"},
                {"ingredient_name": "Alcohol", "percentage": 50.0, "notes": "베이스"}
            ]
        },
        {
            "name": "Fougere Lavender Modern",
            "brand": "Modern Scents",
            "category": "fougere",
            "top_notes": "lavender, bergamot, lemon",
            "middle_notes": "geranium, oakmoss, coumarin",
            "base_notes": "musk, amber, sandalwood",
            "description": "현대적인 푸제르 향수로, 클래식하면서도 세련된 남성적 매력을 표현합니다.",
            "price_range": "mid-range",
            "season_suitability": "all",
            "personality_match": "extrovert",
            "age_group": "adult",
            "gender_target": "male",
            "recipes": [
                {"ingredient_name": "Lavender Oil", "percentage": 15.0, "notes": "메인 아로마틱 노트"},
                {"ingredient_name": "Bergamot Oil", "percentage": 10.0, "notes": "시트러스 노트"},
                {"ingredient_name": "Geranium Oil", "percentage": 8.0, "notes": "플로럴 노트"},
                {"ingredient_name": "Oakmoss", "percentage": 6.0, "notes": "어스 노트"},
                {"ingredient_name": "Coumarin", "percentage": 4.0, "notes": "헤이 노트"},
                {"ingredient_name": "Sandalwood Oil", "percentage": 8.0, "notes": "우디 베이스"},
                {"ingredient_name": "Alcohol", "percentage": 49.0, "notes": "베이스"}
            ]
        },
        {
            "name": "Amber Vanilla Warmth",
            "brand": "Warm Scents",
            "category": "amber",
            "top_notes": "vanilla, tonka bean, bergamot",
            "middle_notes": "amber, benzoin, labdanum",
            "base_notes": "musk, sandalwood, vanilla",
            "description": "따뜻하고 달콤한 앰버 향수로, 로맨틱하고 포근한 분위기를 연출합니다.",
            "price_range": "mid-range",
            "season_suitability": "winter",
            "personality_match": "introvert",
            "age_group": "adult",
            "gender_target": "female",
            "recipes": [
                {"ingredient_name": "Vanilla Absolute", "percentage": 12.0, "notes": "메인 스위트 노트"},
                {"ingredient_name": "Tonka Bean", "percentage": 8.0, "notes": "스위트 노트"},
                {"ingredient_name": "Amber", "percentage": 15.0, "notes": "메인 앰버 노트"},
                {"ingredient_name": "Benzoin", "percentage": 6.0, "notes": "레진 노트"},
                {"ingredient_name": "Labdanum", "percentage": 5.0, "notes": "레진 노트"},
                {"ingredient_name": "Sandalwood Oil", "percentage": 8.0, "notes": "우디 베이스"},
                {"ingredient_name": "Alcohol", "percentage": 46.0, "notes": "베이스"}
            ]
        },
        {
            "name": "Spicy Oriental Heat",
            "brand": "Exotic Scents",
            "category": "spicy",
            "top_notes": "cardamom, saffron, bergamot",
            "middle_notes": "cinnamon, clove, rose",
            "base_notes": "amber, oud, musk",
            "description": "강렬하고 매혹적인 스파이시 향수로, 동양의 신비로운 매력을 표현합니다.",
            "price_range": "luxury",
            "season_suitability": "winter",
            "personality_match": "extrovert",
            "age_group": "mature",
            "gender_target": "unisex",
            "recipes": [
                {"ingredient_name": "Cardamom Oil", "percentage": 12.0, "notes": "메인 스파이시 노트"},
                {"ingredient_name": "Saffron", "percentage": 5.0, "notes": "프리미엄 스파이스"},
                {"ingredient_name": "Cinnamon Oil", "percentage": 8.0, "notes": "스파이시 노트"},
                {"ingredient_name": "Clove Oil", "percentage": 6.0, "notes": "스파이시 노트"},
                {"ingredient_name": "Rose Oil", "percentage": 6.0, "notes": "플로럴 노트"},
                {"ingredient_name": "Oud Oil", "percentage": 8.0, "notes": "오리엔탈 노트"},
                {"ingredient_name": "Alcohol", "percentage": 55.0, "notes": "베이스"}
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