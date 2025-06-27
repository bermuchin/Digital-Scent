import asyncio
import schedule
import time
from datetime import datetime
from app.database import SessionLocal
from app.models.recommendation_model import PerfumeRecommendationModel

class ModelRetrainScheduler:
    def __init__(self):
        self.recommendation_model = PerfumeRecommendationModel()
        self.is_running = False
    
    def retrain_job(self):
        """정기적인 모델 재훈련 작업"""
        print(f"[{datetime.now()}] 모델 재훈련 작업 시작...")
        
        try:
            db = SessionLocal()
            self.recommendation_model.retrain_with_feedback(db)
            db.close()
            print(f"[{datetime.now()}] 모델 재훈련 완료")
        except Exception as e:
            print(f"[{datetime.now()}] 모델 재훈련 실패: {e}")
    
    def start_scheduler(self):
        """스케줄러를 시작합니다."""
        if self.is_running:
            print("스케줄러가 이미 실행 중입니다.")
            return
        
        # 매일 새벽 2시에 재훈련
        schedule.every().day.at("02:00").do(self.retrain_job)
        
        # 피드백 데이터가 100개 이상 쌓이면 즉시 재훈련
        schedule.every().hour.do(self.check_feedback_threshold)
        
        self.is_running = True
        print("모델 재훈련 스케줄러가 시작되었습니다.")
        
        while self.is_running:
            schedule.run_pending()
            time.sleep(60)  # 1분마다 체크
    
    def check_feedback_threshold(self):
        """피드백 데이터 임계값을 확인합니다."""
        try:
            db = SessionLocal()
            from app.database import Recommendation
            
            # 새로운 피드백 개수 확인 (마지막 재훈련 이후)
            if self.recommendation_model.last_retrain_date:
                new_feedback_count = db.query(Recommendation).filter(
                    Recommendation.is_liked.isnot(None),
                    Recommendation.created_at > self.recommendation_model.last_retrain_date
                ).count()
                
                if new_feedback_count >= 50:  # 50개 이상의 새 피드백이 있으면 재훈련
                    print(f"새로운 피드백 {new_feedback_count}개 발견. 즉시 재훈련 시작...")
                    self.retrain_job()
            
            db.close()
        except Exception as e:
            print(f"피드백 임계값 확인 실패: {e}")
    
    def stop_scheduler(self):
        """스케줄러를 중지합니다."""
        self.is_running = False
        print("모델 재훈련 스케줄러가 중지되었습니다.")

# 전역 스케줄러 인스턴스
scheduler = ModelRetrainScheduler()

def start_model_scheduler():
    """백그라운드에서 스케줄러를 시작합니다."""
    import threading
    
    def run_scheduler():
        scheduler.start_scheduler()
    
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    return scheduler_thread 