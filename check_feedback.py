#!/usr/bin/env python3
"""
피드백 데이터 확인 및 분석 스크립트
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.database import SessionLocal, Recommendation, Perfume, User
from datetime import datetime, timedelta
import pandas as pd

def check_feedback_data():
    """피드백 데이터를 확인하고 분석합니다."""
    db = SessionLocal()
    
    try:
        print("=" * 60)
        print("피드백 데이터 분석")
        print("=" * 60)
        
        # 1. 전체 추천 기록 수
        total_recommendations = db.query(Recommendation).count()
        print(f"전체 추천 기록: {total_recommendations}개")
        
        # 2. 피드백이 있는 추천 기록 수
        feedback_recommendations = db.query(Recommendation).filter(
            Recommendation.is_liked.isnot(None)
        ).count()
        print(f"피드백이 있는 추천 기록: {feedback_recommendations}개")
        
        # 3. 피드백 비율
        if total_recommendations > 0:
            feedback_rate = (feedback_recommendations / total_recommendations) * 100
            print(f"피드백 비율: {feedback_rate:.1f}%")
        
        # 4. 좋아요/싫어요 분포
        liked_count = db.query(Recommendation).filter(
            Recommendation.is_liked == True
        ).count()
        
        disliked_count = db.query(Recommendation).filter(
            Recommendation.is_liked == False
        ).count()
        
        print(f"좋아요: {liked_count}개")
        print(f"싫어요: {disliked_count}개")
        
        if feedback_recommendations > 0:
            like_rate = (liked_count / feedback_recommendations) * 100
            print(f"좋아요 비율: {like_rate:.1f}%")
        
        # 5. 최근 피드백 (최근 7일)
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_feedback = db.query(Recommendation).filter(
            Recommendation.is_liked.isnot(None),
            Recommendation.created_at >= week_ago
        ).count()
        print(f"최근 7일 피드백: {recent_feedback}개")
        
        # 6. 상세 피드백 데이터
        print("\n" + "=" * 60)
        print("상세 피드백 데이터")
        print("=" * 60)
        
        feedback_records = db.query(Recommendation).filter(
            Recommendation.is_liked.isnot(None)
        ).order_by(Recommendation.created_at.desc()).limit(10).all()
        
        for i, record in enumerate(feedback_records, 1):
            perfume = db.query(Perfume).filter(Perfume.id == record.perfume_id).first()
            user_info = "익명" if record.user_id is None else f"사용자 {record.user_id}"
            
            print(f"{i}. {perfume.name if perfume else 'Unknown'} ({perfume.brand if perfume else 'Unknown'})")
            print(f"   사용자: {user_info}")
            print(f"   피드백: {'좋아요' if record.is_liked else '싫어요'}")
            print(f"   신뢰도: {record.confidence_score:.2f}")
            print(f"   날짜: {record.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print()
        
        # 7. 카테고리별 피드백 분석
        print("=" * 60)
        print("카테고리별 피드백 분석")
        print("=" * 60)
        
        # 피드백이 있는 추천과 향수 정보를 조인
        feedback_with_perfumes = db.query(Recommendation, Perfume).join(
            Perfume, Recommendation.perfume_id == Perfume.id
        ).filter(
            Recommendation.is_liked.isnot(None)
        ).all()
        
        category_stats = {}
        for rec, perfume in feedback_with_perfumes:
            category = perfume.category
            if category not in category_stats:
                category_stats[category] = {'liked': 0, 'disliked': 0}
            
            if rec.is_liked:
                category_stats[category]['liked'] += 1
            else:
                category_stats[category]['disliked'] += 1
        
        for category, stats in category_stats.items():
            total = stats['liked'] + stats['disliked']
            like_rate = (stats['liked'] / total) * 100 if total > 0 else 0
            print(f"{category}: 좋아요 {stats['liked']}개, 싫어요 {stats['disliked']}개 (좋아요 비율: {like_rate:.1f}%)")
        
        # 8. 재훈련 가능성 확인
        print("\n" + "=" * 60)
        print("재훈련 가능성 분석")
        print("=" * 60)
        
        if feedback_recommendations >= 50:
            print("✅ 충분한 피드백 데이터가 있습니다 (50개 이상)")
            print("   - 모델 재훈련이 가능합니다")
        elif feedback_recommendations >= 20:
            print("⚠️  피드백 데이터가 부족합니다 (20-49개)")
            print("   - 더 많은 피드백이 필요합니다")
        else:
            print("❌ 피드백 데이터가 매우 부족합니다 (20개 미만)")
            print("   - 사용자 참여를 유도해야 합니다")
        
        # 9. 최근 피드백 추세
        print("\n" + "=" * 60)
        print("최근 피드백 추세")
        print("=" * 60)
        
        # 최근 30일간 일별 피드백 수
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        daily_feedback = db.query(Recommendation).filter(
            Recommendation.is_liked.isnot(None),
            Recommendation.created_at >= thirty_days_ago
        ).all()
        
        daily_counts = {}
        for rec in daily_feedback:
            date_str = rec.created_at.strftime('%Y-%m-%d')
            daily_counts[date_str] = daily_counts.get(date_str, 0) + 1
        
        if daily_counts:
            avg_daily = sum(daily_counts.values()) / len(daily_counts)
            print(f"최근 30일 평균 일일 피드백: {avg_daily:.1f}개")
            
            recent_days = sorted(daily_counts.keys())[-7:]  # 최근 7일
            print("최근 7일 피드백:")
            for date in recent_days:
                print(f"  {date}: {daily_counts[date]}개")
        else:
            print("최근 30일간 피드백이 없습니다.")
        
    except Exception as e:
        print(f"데이터 분석 중 오류 발생: {e}")
    finally:
        db.close()

def check_model_retrain_status():
    """모델 재훈련 상태를 확인합니다."""
    print("\n" + "=" * 60)
    print("모델 재훈련 상태 확인")
    print("=" * 60)
    
    try:
        from backend.app.models.recommendation_model import PerfumeRecommendationModel
        
        model = PerfumeRecommendationModel()
        model.load_model()
        
        print(f"모델 훈련 상태: {'훈련됨' if model.is_trained else '미훈련'}")
        
        if model.last_retrain_date:
            print(f"마지막 재훈련: {model.last_retrain_date.strftime('%Y-%m-%d %H:%M:%S')}")
            
            days_since_retrain = (datetime.utcnow() - model.last_retrain_date).days
            print(f"마지막 재훈련 후 경과일: {days_since_retrain}일")
            
            if days_since_retrain >= 7:
                print("✅ 7일이 지나 재훈련이 권장됩니다")
            else:
                print(f"⚠️  재훈련까지 {7 - days_since_retrain}일 남았습니다")
        else:
            print("마지막 재훈련 정보가 없습니다")
            
    except Exception as e:
        print(f"모델 상태 확인 중 오류 발생: {e}")

if __name__ == "__main__":
    check_feedback_data()
    check_model_retrain_status() 