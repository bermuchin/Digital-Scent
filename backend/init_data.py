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
    
    # 카테고리별 예시 이름 및 탑/미들/베이스 순서 레시피
    CATEGORY_EXAMPLES = {
        "citrus": {
            "name": "Lemon Grove Breeze",
            "recipes": [
                {"ingredient_name": "Bergamot Oil", "percentage": 10.0, "notes": "탑 노트"},
                {"ingredient_name": "Lemon Zest", "percentage": 8.0, "notes": "탑 노트"},
                {"ingredient_name": "Neroli", "percentage": 7.0, "notes": "미들 노트"},
                {"ingredient_name": "Petitgrain", "percentage": 5.0, "notes": "미들 노트"},
                {"ingredient_name": "Musk", "percentage": 5.0, "notes": "베이스 노트"},
                {"ingredient_name": "Alcohol", "percentage": 65.0, "notes": "베이스"}
            ]
        },
        "floral": {
            "name": "Rose Petal Symphony",
            "recipes": [
                {"ingredient_name": "Rose Absolute", "percentage": 10.0, "notes": "탑 노트"},
                {"ingredient_name": "Peony", "percentage": 7.0, "notes": "미들 노트"},
                {"ingredient_name": "Jasmine", "percentage": 7.0, "notes": "미들 노트"},
                {"ingredient_name": "Violet", "percentage": 6.0, "notes": "베이스 노트"},
                {"ingredient_name": "Musk", "percentage": 5.0, "notes": "베이스 노트"},
                {"ingredient_name": "Alcohol", "percentage": 65.0, "notes": "베이스"}
            ]
        },
        "woody": {
            "name": "Cedarwood Essence",
            "recipes": [
                {"ingredient_name": "Cypress", "percentage": 8.0, "notes": "탑 노트"},
                {"ingredient_name": "Pine", "percentage": 7.0, "notes": "미들 노트"},
                {"ingredient_name": "Cedarwood Oil", "percentage": 10.0, "notes": "베이스 노트"},
                {"ingredient_name": "Sandalwood", "percentage": 8.0, "notes": "베이스 노트"},
                {"ingredient_name": "Vetiver", "percentage": 5.0, "notes": "베이스 노트"},
                {"ingredient_name": "Alcohol", "percentage": 62.0, "notes": "베이스"}
            ]
        },
        "oriental": {
            "name": "Mystique of the East",
            "recipes": [
                {"ingredient_name": "Saffron", "percentage": 7.0, "notes": "탑 노트"},
                {"ingredient_name": "Cardamom", "percentage": 6.0, "notes": "미들 노트"},
                {"ingredient_name": "Oud Oil", "percentage": 8.0, "notes": "베이스 노트"},
                {"ingredient_name": "Amber", "percentage": 9.0, "notes": "베이스 노트"},
                {"ingredient_name": "Vanilla", "percentage": 5.0, "notes": "베이스 노트"},
                {"ingredient_name": "Alcohol", "percentage": 65.0, "notes": "베이스"}
            ]
        },
        "musk": {
            "name": "Pure White Musk",
            "recipes": [
                {"ingredient_name": "Aldehydes", "percentage": 6.0, "notes": "탑 노트"},
                {"ingredient_name": "White Flowers", "percentage": 6.0, "notes": "미들 노트"},
                {"ingredient_name": "White Musk", "percentage": 15.0, "notes": "베이스 노트"},
                {"ingredient_name": "Tonka Bean", "percentage": 5.0, "notes": "베이스 노트"},
                {"ingredient_name": "Alcohol", "percentage": 68.0, "notes": "베이스"}
            ]
        },
        "aquatic": {
            "name": "Oceanic Blue Wave",
            "recipes": [
                {"ingredient_name": "Marine Accord", "percentage": 10.0, "notes": "탑 노트"},
                {"ingredient_name": "Sea Spray", "percentage": 7.0, "notes": "미들 노트"},
                {"ingredient_name": "Cucumber", "percentage": 6.0, "notes": "미들 노트"},
                {"ingredient_name": "Driftwood", "percentage": 7.0, "notes": "베이스 노트"},
                {"ingredient_name": "White Musk", "percentage": 5.0, "notes": "베이스 노트"},
                {"ingredient_name": "Alcohol", "percentage": 65.0, "notes": "베이스"}
            ]
        },
        "green": {
            "name": "Spring Meadow",
            "recipes": [
                {"ingredient_name": "Galbanum", "percentage": 8.0, "notes": "탑 노트"},
                {"ingredient_name": "Green Leaves", "percentage": 7.0, "notes": "미들 노트"},
                {"ingredient_name": "Herb Accord", "percentage": 7.0, "notes": "미들 노트"},
                {"ingredient_name": "Oakmoss", "percentage": 8.0, "notes": "베이스 노트"},
                {"ingredient_name": "Cedarwood", "percentage": 5.0, "notes": "베이스 노트"},
                {"ingredient_name": "Alcohol", "percentage": 65.0, "notes": "베이스"}
            ]
        },
        "gourmand": {
            "name": "Vanilla Caramel Dream",
            "recipes": [
                {"ingredient_name": "Orange", "percentage": 7.0, "notes": "탑 노트"},
                {"ingredient_name": "Caramel", "percentage": 8.0, "notes": "미들 노트"},
                {"ingredient_name": "Chocolate", "percentage": 7.0, "notes": "미들 노트"},
                {"ingredient_name": "Vanilla Absolute", "percentage": 10.0, "notes": "베이스 노트"},
                {"ingredient_name": "Tonka Bean", "percentage": 5.0, "notes": "베이스 노트"},
                {"ingredient_name": "Alcohol", "percentage": 63.0, "notes": "베이스"}
            ]
        },
        "powdery": {
            "name": "Soft Powder Veil",
            "recipes": [
                {"ingredient_name": "Aldehydes", "percentage": 7.0, "notes": "탑 노트"},
                {"ingredient_name": "Iris", "percentage": 8.0, "notes": "미들 노트"},
                {"ingredient_name": "Violet", "percentage": 7.0, "notes": "미들 노트"},
                {"ingredient_name": "Musk", "percentage": 8.0, "notes": "베이스 노트"},
                {"ingredient_name": "Sandalwood", "percentage": 5.0, "notes": "베이스 노트"},
                {"ingredient_name": "Alcohol", "percentage": 65.0, "notes": "베이스"}
            ]
        },
        "fruity": {
            "name": "Peach Blossom Bliss",
            "recipes": [
                {"ingredient_name": "Peach", "percentage": 8.0, "notes": "탑 노트"},
                {"ingredient_name": "Apple", "percentage": 7.0, "notes": "탑 노트"},
                {"ingredient_name": "Raspberry", "percentage": 7.0, "notes": "미들 노트"},
                {"ingredient_name": "Jasmine", "percentage": 6.0, "notes": "미들 노트"},
                {"ingredient_name": "Musk", "percentage": 7.0, "notes": "베이스 노트"},
                {"ingredient_name": "Alcohol", "percentage": 65.0, "notes": "베이스"}
            ]
        },
        "aromatic": {
            "name": "Herbal Harmony",
            "recipes": [
                {"ingredient_name": "Lavender", "percentage": 8.0, "notes": "탑 노트"},
                {"ingredient_name": "Rosemary", "percentage": 7.0, "notes": "미들 노트"},
                {"ingredient_name": "Sage", "percentage": 7.0, "notes": "미들 노트"},
                {"ingredient_name": "Thyme", "percentage": 6.0, "notes": "베이스 노트"},
                {"ingredient_name": "Cedarwood", "percentage": 7.0, "notes": "베이스 노트"},
                {"ingredient_name": "Alcohol", "percentage": 65.0, "notes": "베이스"}
            ]
        },
        "chypre": {
            "name": "Mossy Forest Classic",
            "recipes": [
                {"ingredient_name": "Bergamot", "percentage": 8.0, "notes": "탑 노트"},
                {"ingredient_name": "Labdanum", "percentage": 7.0, "notes": "미들 노트"},
                {"ingredient_name": "Oakmoss", "percentage": 10.0, "notes": "베이스 노트"},
                {"ingredient_name": "Patchouli", "percentage": 7.0, "notes": "베이스 노트"},
                {"ingredient_name": "Musk", "percentage": 5.0, "notes": "베이스 노트"},
                {"ingredient_name": "Alcohol", "percentage": 63.0, "notes": "베이스"}
            ]
        },
        "fougere": {
            "name": "Lavender Fern Mist",
            "recipes": [
                {"ingredient_name": "Lavender", "percentage": 8.0, "notes": "탑 노트"},
                {"ingredient_name": "Geranium", "percentage": 7.0, "notes": "미들 노트"},
                {"ingredient_name": "Oakmoss", "percentage": 8.0, "notes": "베이스 노트"},
                {"ingredient_name": "Coumarin", "percentage": 7.0, "notes": "베이스 노트"},
                {"ingredient_name": "Tonka Bean", "percentage": 7.0, "notes": "베이스 노트"},
                {"ingredient_name": "Alcohol", "percentage": 63.0, "notes": "베이스"}
            ]
        },
        "amber": {
            "name": "Golden Amber Night",
            "recipes": [
                {"ingredient_name": "Mandarin", "percentage": 7.0, "notes": "탑 노트"},
                {"ingredient_name": "Benzoin", "percentage": 8.0, "notes": "미들 노트"},
                {"ingredient_name": "Amber", "percentage": 12.0, "notes": "베이스 노트"},
                {"ingredient_name": "Labdanum", "percentage": 7.0, "notes": "베이스 노트"},
                {"ingredient_name": "Vanilla", "percentage": 5.0, "notes": "베이스 노트"},
                {"ingredient_name": "Alcohol", "percentage": 61.0, "notes": "베이스"}
            ]
        },
        "spicy": {
            "name": "Spiced Saffron Touch",
            "recipes": [
                {"ingredient_name": "Pink Pepper", "percentage": 8.0, "notes": "탑 노트"},
                {"ingredient_name": "Saffron", "percentage": 7.0, "notes": "미들 노트"},
                {"ingredient_name": "Cinnamon", "percentage": 8.0, "notes": "미들 노트"},
                {"ingredient_name": "Clove", "percentage": 7.0, "notes": "베이스 노트"},
                {"ingredient_name": "Patchouli", "percentage": 5.0, "notes": "베이스 노트"},
                {"ingredient_name": "Alcohol", "percentage": 65.0, "notes": "베이스"}
            ]
        },
        "light floral": {
            "name": "Light Lily Whisper",
            "recipes": [
                {"ingredient_name": "Lily", "percentage": 8.0, "notes": "탑 노트"},
                {"ingredient_name": "Freesia", "percentage": 7.0, "notes": "미들 노트"},
                {"ingredient_name": "Cyclamen", "percentage": 7.0, "notes": "미들 노트"},
                {"ingredient_name": "Musk", "percentage": 8.0, "notes": "베이스 노트"},
                {"ingredient_name": "Sandalwood", "percentage": 5.0, "notes": "베이스 노트"},
                {"ingredient_name": "Alcohol", "percentage": 65.0, "notes": "베이스"}
            ]
        },
        "white floral": {
            "name": "White Jasmine Aura",
            "recipes": [
                {"ingredient_name": "Jasmine", "percentage": 10.0, "notes": "탑 노트"},
                {"ingredient_name": "Tuberose", "percentage": 8.0, "notes": "미들 노트"},
                {"ingredient_name": "Gardenia", "percentage": 7.0, "notes": "미들 노트"},
                {"ingredient_name": "Musk", "percentage": 8.0, "notes": "베이스 노트"},
                {"ingredient_name": "Sandalwood", "percentage": 5.0, "notes": "베이스 노트"},
                {"ingredient_name": "Alcohol", "percentage": 62.0, "notes": "베이스"}
            ]
        },
        "casual": {
            "name": "Everyday Comfort",
            "recipes": [
                {"ingredient_name": "Mandarin", "percentage": 7.0, "notes": "탑 노트"},
                {"ingredient_name": "Cotton Accord", "percentage": 8.0, "notes": "미들 노트"},
                {"ingredient_name": "Linen", "percentage": 8.0, "notes": "미들 노트"},
                {"ingredient_name": "Musk", "percentage": 7.0, "notes": "베이스 노트"},
                {"ingredient_name": "Cedarwood", "percentage": 5.0, "notes": "베이스 노트"},
                {"ingredient_name": "Alcohol", "percentage": 65.0, "notes": "베이스"}
            ]
        },
        "cozy": {
            "name": "Warm Cashmere Hug",
            "recipes": [
                {"ingredient_name": "Pear", "percentage": 7.0, "notes": "탑 노트"},
                {"ingredient_name": "Cashmere Wood", "percentage": 8.0, "notes": "미들 노트"},
                {"ingredient_name": "Vanilla", "percentage": 8.0, "notes": "미들 노트"},
                {"ingredient_name": "Tonka Bean", "percentage": 7.0, "notes": "베이스 노트"},
                {"ingredient_name": "Musk", "percentage": 5.0, "notes": "베이스 노트"},
                {"ingredient_name": "Alcohol", "percentage": 65.0, "notes": "베이스"}
            ]
        },
    }

    # 공통 기본값
    DEFAULTS = {
        "brand": "예시브랜드",
        "top_notes": "예시 top notes",
        "middle_notes": "예시 middle notes",
        "base_notes": "예시 base notes",
        "description": "카테고리별 예시 향수입니다.",
        "price_range": "mid-range",
        "season_suitability": "all",
        "personality_match": "balanced",
        "age_group": "adult",
        "gender_target": "unisex"
    }

    perfumes_data = []
    for cat, info in CATEGORY_EXAMPLES.items():
        perfumes_data.append({
            "name": info["name"],
            "brand": DEFAULTS["brand"],
            "category": cat,
            "top_notes": DEFAULTS["top_notes"],
            "middle_notes": DEFAULTS["middle_notes"],
            "base_notes": DEFAULTS["base_notes"],
            "description": DEFAULTS["description"],
            "price_range": DEFAULTS["price_range"],
            "season_suitability": DEFAULTS["season_suitability"],
            "personality_match": DEFAULTS["personality_match"],
            "age_group": DEFAULTS["age_group"],
            "gender_target": DEFAULTS["gender_target"],
            "recipes": info["recipes"]
        })

    # DB에 추가
    for perfume_data in perfumes_data:
        recipes = perfume_data.pop("recipes", [])
        perfume = Perfume(**perfume_data)
        db.add(perfume)
        db.commit()
        db.refresh(perfume)
        for recipe in recipes:
            db_recipe = PerfumeRecipe(perfume_id=perfume.id, **recipe)
            db.add(db_recipe)
        db.commit()
    print(f"{len(perfumes_data)}개 예시 향수 샘플 데이터가 추가되었습니다.")

def train_ml_model():
    """머신러닝 추천 모델을 훈련합니다."""
    db = SessionLocal()
    model = PerfumeRecommendationModel()
    model.train(db)
    print("추천 모델 훈련 완료!")

if __name__ == "__main__":
    init_database()
    create_sample_perfumes()
    train_ml_model() 