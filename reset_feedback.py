#!/usr/bin/env python3
"""
사용자 피드백 데이터 초기화 스크립트
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.database import SessionLocal, Recommendation
from datetime import datetime

def reset_feedback_data():
    """사용자 피드백 데이터를 초기화합니다."""
    db = SessionLocal()
    
    try:
        print("=" * 60)
        print("피드백 데이터 초기화")
        print("=" * 60)
        
        # 현재 피드백 데이터 확인
        feedback_count = db.query(Recommendation).filter(
            Recommendation.is_liked.isnot(None)
        ).count()
        
        print(f"현재 피드백 데이터: {feedback_count}개")
        
        if feedback_count == 0:
            print("초기화할 피드백 데이터가 없습니다.")
            return
        
        # 사용자 확인
        confirm = input(f"\n정말로 {feedback_count}개의 피드백 데이터를 모두 삭제하시겠습니까? (y/N): ")
        
        if confirm.lower() != 'y':
            print("초기화가 취소되었습니다.")
            return
        
        # 피드백 데이터 삭제
        deleted_count = db.query(Recommendation).filter(
            Recommendation.is_liked.isnot(None)
        ).delete()
        
        db.commit()
        
        print(f"✅ {deleted_count}개의 피드백 데이터가 성공적으로 삭제되었습니다.")
        print("샘플 데이터는 그대로 유지됩니다.")
        
        # 삭제 후 상태 확인
        remaining_feedback = db.query(Recommendation).filter(
            Recommendation.is_liked.isnot(None)
        ).count()
        
        print(f"남은 피드백 데이터: {remaining_feedback}개")
        
    except Exception as e:
        print(f"피드백 초기화 중 오류 발생: {e}")
        db.rollback()
    finally:
        db.close()

def reset_feedback_with_backup():
    """피드백 데이터를 백업 후 초기화합니다."""
    db = SessionLocal()
    
    try:
        print("=" * 60)
        print("피드백 데이터 백업 후 초기화")
        print("=" * 60)
        
        # 현재 피드백 데이터 확인
        feedback_records = db.query(Recommendation).filter(
            Recommendation.is_liked.isnot(None)
        ).all()
        
        if not feedback_records:
            print("백업할 피드백 데이터가 없습니다.")
            return
        
        # 백업 파일 생성
        backup_filename = f"feedback_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(backup_filename, 'w', encoding='utf-8') as f:
            f.write("피드백 데이터 백업\n")
            f.write("=" * 50 + "\n")
            f.write(f"백업 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"총 피드백 수: {len(feedback_records)}\n\n")
            
            for i, record in enumerate(feedback_records, 1):
                f.write(f"{i}. 추천 ID: {record.id}\n")
                f.write(f"   향수 ID: {record.perfume_id}\n")
                f.write(f"   사용자 ID: {record.user_id}\n")
                f.write(f"   피드백: {'좋아요' if record.is_liked else '싫어요'}\n")
                f.write(f"   신뢰도: {record.confidence_score}\n")
                f.write(f"   생성일: {record.created_at}\n")
                f.write(f"   이유: {record.reason}\n")
                f.write("-" * 30 + "\n")
        
        print(f"백업 파일이 생성되었습니다: {backup_filename}")
        
        # 사용자 확인
        confirm = input(f"\n정말로 {len(feedback_records)}개의 피드백 데이터를 모두 삭제하시겠습니까? (y/N): ")
        
        if confirm.lower() != 'y':
            print("초기화가 취소되었습니다.")
            return
        
        # 피드백 데이터 삭제
        deleted_count = db.query(Recommendation).filter(
            Recommendation.is_liked.isnot(None)
        ).delete()
        
        db.commit()
        
        print(f"✅ {deleted_count}개의 피드백 데이터가 성공적으로 삭제되었습니다.")
        print(f"백업 파일: {backup_filename}")
        
    except Exception as e:
        print(f"피드백 백업 및 초기화 중 오류 발생: {e}")
        db.rollback()
    finally:
        db.close()

def reset_feedback_by_date():
    """특정 날짜 이후의 피드백 데이터만 초기화합니다."""
    db = SessionLocal()
    
    try:
        print("=" * 60)
        print("날짜별 피드백 데이터 초기화")
        print("=" * 60)
        
        # 날짜 입력 받기
        date_str = input("초기화할 날짜를 입력하세요 (YYYY-MM-DD 형식): ")
        
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            print("올바른 날짜 형식을 입력해주세요 (예: 2024-01-15)")
            return
        
        # 해당 날짜 이후의 피드백 데이터 확인
        feedback_records = db.query(Recommendation).filter(
            Recommendation.is_liked.isnot(None),
            Recommendation.created_at >= target_date
        ).all()
        
        if not feedback_records:
            print(f"{date_str} 이후의 피드백 데이터가 없습니다.")
            return
        
        print(f"{date_str} 이후의 피드백 데이터: {len(feedback_records)}개")
        
        # 사용자 확인
        confirm = input(f"\n정말로 {len(feedback_records)}개의 피드백 데이터를 삭제하시겠습니까? (y/N): ")
        
        if confirm.lower() != 'y':
            print("초기화가 취소되었습니다.")
            return
        
        # 피드백 데이터 삭제
        deleted_count = db.query(Recommendation).filter(
            Recommendation.is_liked.isnot(None),
            Recommendation.created_at >= target_date
        ).delete()
        
        db.commit()
        
        print(f"✅ {deleted_count}개의 피드백 데이터가 성공적으로 삭제되었습니다.")
        
    except Exception as e:
        print(f"날짜별 피드백 초기화 중 오류 발생: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("피드백 데이터 초기화 옵션:")
    print("1. 모든 피드백 데이터 초기화")
    print("2. 백업 후 모든 피드백 데이터 초기화")
    print("3. 특정 날짜 이후 피드백 데이터 초기화")
    
    choice = input("\n옵션을 선택하세요 (1-3): ")
    
    if choice == "1":
        reset_feedback_data()
    elif choice == "2":
        reset_feedback_with_backup()
    elif choice == "3":
        reset_feedback_by_date()
    else:
        print("잘못된 옵션입니다.") 