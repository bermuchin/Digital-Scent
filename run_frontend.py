#!/usr/bin/env python3
"""
향수 추천 플랫폼 프론트엔드 실행 스크립트
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_node_installed():
    """Node.js가 설치되어 있는지 확인합니다."""
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js 버전 확인: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Node.js가 설치되어 있지 않습니다.")
    print("📥 Node.js를 설치해주세요: https://nodejs.org/")
    return False

def check_npm_installed():
    """npm이 설치되어 있는지 확인합니다."""
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm 버전 확인: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ npm이 설치되어 있지 않습니다.")
    return False

def install_dependencies():
    """프론트엔드 의존성을 설치합니다."""
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ frontend 디렉토리를 찾을 수 없습니다.")
        return False
    
    package_json = frontend_dir / "package.json"
    if not package_json.exists():
        print("❌ package.json 파일을 찾을 수 없습니다.")
        return False
    
    print("📦 프론트엔드 의존성을 설치합니다...")
    try:
        os.chdir(frontend_dir)
        subprocess.run(["npm", "install"], check=True)
        print("✅ 의존성 설치 완료")
        return True
    except subprocess.CalledProcessError:
        print("❌ 의존성 설치에 실패했습니다.")
        return False

def run_frontend():
    """React 개발 서버를 실행합니다."""
    print("🚀 프론트엔드 서버를 시작합니다...")
    print("📍 서버 주소: http://localhost:3000")
    print("🔄 서버를 중지하려면 Ctrl+C를 누르세요.")
    print("-" * 50)
    
    try:
        # frontend 디렉토리로 이동
        os.chdir("frontend")
        
        # npm start 실행
        subprocess.run(["npm", "start"])
    except KeyboardInterrupt:
        print("\n👋 프론트엔드 서버가 중지되었습니다.")
    except Exception as e:
        print(f"❌ 프론트엔드 서버 실행 중 오류가 발생했습니다: {e}")
        sys.exit(1)

def main():
    """메인 함수"""
    print("🎀 향수 추천 플랫폼 프론트엔드")
    print("=" * 50)
    
    # Node.js 확인
    if not check_node_installed():
        sys.exit(1)
    
    # npm 확인
    if not check_npm_installed():
        sys.exit(1)
    
    # 의존성 설치
    if not install_dependencies():
        sys.exit(1)
    
    # 프론트엔드 서버 실행
    run_frontend()

if __name__ == "__main__":
    main() 