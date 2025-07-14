#!/usr/bin/env python3
"""
향수 추천 플랫폼 백엔드 서버 실행 스크립트
멀티라벨 분류 기반 AI 추천 시스템
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Python 버전을 확인합니다."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 이상이 필요합니다.")
        print(f"현재 버전: {sys.version}")
        sys.exit(1)
    print(f"✅ Python 버전 확인: {sys.version.split()[0]}")

def install_requirements():
    """필요한 패키지를 설치합니다."""
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("❌ requirements.txt 파일을 찾을 수 없습니다.")
        sys.exit(1)
    
    print("📦 필요한 패키지를 설치합니다...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ 패키지 설치 완료")
    except subprocess.CalledProcessError:
        print("❌ 패키지 설치에 실패했습니다.")
        sys.exit(1)

def init_database():
    """데이터베이스를 초기화합니다."""
    print("🗄 데이터베이스를 초기화합니다...")
    try:
        subprocess.run([sys.executable, "backend/init_data.py"], check=True)
        print("✅ 데이터베이스 초기화 완료")
    except subprocess.CalledProcessError:
        print("❌ 데이터베이스 초기화에 실패했습니다.")
        sys.exit(1)

def run_server():
    """FastAPI 서버를 실행합니다."""
    print("🚀 멀티라벨 향수 추천 서버를 시작합니다...")
    print("📍 서버 주소: http://localhost:8000")
    print("📚 API 문서: http://localhost:8000/docs")
    print("🎯 멀티라벨 분류: 여러 향수 카테고리 동시 추천")
    print("📊 엑셀 데이터 기반: 719개 실제 사용자 데이터")
    print("🔄 서버를 중지하려면 Ctrl+C를 누르세요.")
    print("-" * 50)
    
    try:
        # uvicorn 서버 실행 (루트에서 backend.app.main:app으로 실행)
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "backend.app.main:app",
            "--reload",
            "--host", "0.0.0.0",
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n👋 서버가 중지되었습니다.")
    except Exception as e:
        print(f"❌ 서버 실행 중 오류가 발생했습니다: {e}")
        sys.exit(1)

def main():
    """메인 함수"""
    print("🎀 향수 추천 플랫폼 백엔드 서버")
    print("🤖 멀티라벨 AI 추천 시스템")
    print("=" * 50)
    
    # Python 버전 확인
    check_python_version()
    
    # 패키지 설치
    install_requirements()
    
    # 데이터베이스 초기화
    init_database()
    
    # 서버 실행
    run_server()

if __name__ == "__main__":
    main() 