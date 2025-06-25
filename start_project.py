#!/usr/bin/env python3
"""
향수 추천 플랫폼 전체 프로젝트 실행 스크립트
"""

import os
import sys
import subprocess
import threading
import time
from pathlib import Path

def print_banner():
    """프로젝트 배너를 출력합니다."""
    print("🎀" * 50)
    print("🎀           향수 추천 플랫폼           🎀")
    print("🎀     AI 기반 향수 추천 및 제조법     🎀")
    print("🎀" * 50)
    print()

def check_requirements():
    """필요한 도구들이 설치되어 있는지 확인합니다."""
    print("🔍 시스템 요구사항을 확인합니다...")
    
    # Python 버전 확인
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 이상이 필요합니다.")
        return False
    print(f"✅ Python 버전: {sys.version.split()[0]}")
    
    # Node.js 확인
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js 버전: {result.stdout.strip()}")
        else:
            print("❌ Node.js가 설치되어 있지 않습니다.")
            return False
    except FileNotFoundError:
        print("❌ Node.js가 설치되어 있지 않습니다.")
        print("📥 Node.js를 설치해주세요: https://nodejs.org/")
        return False
    
    # npm 확인
    try:
        # 먼저 일반적인 npm 경로 시도
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm 버전: {result.stdout.strip()}")
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        # npm 전체 경로 시도
        npm_paths = [
            r"C:\Program Files\nodejs\npm.cmd",
            r"C:\Program Files\nodejs\npm.ps1",
            r"C:\Program Files (x86)\nodejs\npm.cmd",
            r"C:\Program Files (x86)\nodejs\npm.ps1"
        ]
        
        npm_found = False
        for npm_path in npm_paths:
            if os.path.exists(npm_path):
                try:
                    result = subprocess.run([npm_path, "--version"], capture_output=True, text=True)
                    if result.returncode == 0:
                        print(f"✅ npm 버전: {result.stdout.strip()}")
                        npm_found = True
                        break
                except Exception:
                    continue
        
        if not npm_found:
            print("❌ npm이 설치되어 있지 않습니다.")
            return False
    
    return True

def setup_backend():
    """백엔드를 설정합니다."""
    print("\n🔧 백엔드 설정을 시작합니다...")
    
    # requirements.txt 확인
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt 파일을 찾을 수 없습니다.")
        return False
    
    # 패키지 설치
    print("📦 Python 패키지를 설치합니다...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ 패키지 설치 완료")
    except subprocess.CalledProcessError:
        print("❌ 패키지 설치에 실패했습니다.")
        return False
    
    # 데이터베이스 초기화
    print("🗄 데이터베이스를 초기화합니다...")
    try:
        subprocess.run([sys.executable, "backend/init_data.py"], check=True)
        print("✅ 데이터베이스 초기화 완료")
    except subprocess.CalledProcessError:
        print("❌ 데이터베이스 초기화에 실패했습니다.")
        return False
    
    return True

def setup_frontend():
    """프론트엔드를 설정합니다."""
    print("\n🔧 프론트엔드 설정을 시작합니다...")
    
    # frontend 디렉토리 확인
    if not Path("frontend").exists():
        print("❌ frontend 디렉토리를 찾을 수 없습니다.")
        return False
    
    # package.json 확인
    if not Path("frontend/package.json").exists():
        print("❌ package.json 파일을 찾을 수 없습니다.")
        return False
    
    # npm 경로 찾기
    npm_cmd = "npm"
    npm_paths = [
        r"C:\Program Files\nodejs\npm.cmd",
        r"C:\Program Files\nodejs\npm.ps1",
        r"C:\Program Files (x86)\nodejs\npm.cmd",
        r"C:\Program Files (x86)\nodejs\npm.ps1"
    ]
    
    for npm_path in npm_paths:
        if os.path.exists(npm_path):
            npm_cmd = npm_path
            break
    
    # 의존성 설치
    print("📦 React 의존성을 설치합니다...")
    try:
        os.chdir("frontend")
        subprocess.run([npm_cmd, "install"], check=True)
        os.chdir("..")
        print("✅ 의존성 설치 완료")
    except subprocess.CalledProcessError:
        print("❌ 의존성 설치에 실패했습니다.")
        return False
    
    return True

def run_backend():
    """백엔드 서버를 실행합니다."""
    print("\n🚀 백엔드 서버를 시작합니다...")
    print("📍 서버 주소: http://localhost:8000")
    print("📚 API 문서: http://localhost:8000/docs")
    
    try:
        os.chdir("backend")
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "app.main:app",
            "--reload",
            "--host", "0.0.0.0",
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n👋 백엔드 서버가 중지되었습니다.")
    finally:
        os.chdir("..")

def run_frontend():
    """프론트엔드 서버를 실행합니다."""
    print("\n🚀 프론트엔드 서버를 시작합니다...")
    print("📍 서버 주소: http://localhost:3000")
    
    # npm 경로 찾기
    npm_cmd = "npm"
    npm_paths = [
        r"C:\Program Files\nodejs\npm.cmd",
        r"C:\Program Files\nodejs\npm.ps1",
        r"C:\Program Files (x86)\nodejs\npm.cmd",
        r"C:\Program Files (x86)\nodejs\npm.ps1"
    ]
    
    for npm_path in npm_paths:
        if os.path.exists(npm_path):
            npm_cmd = npm_path
            break
    
    try:
        os.chdir("frontend")
        subprocess.run([npm_cmd, "start"], shell=True)
    except KeyboardInterrupt:
        print("\n👋 프론트엔드 서버가 중지되었습니다.")
    finally:
        os.chdir("..")

def main():
    """메인 함수"""
    print_banner()
    
    # 시스템 요구사항 확인
    if not check_requirements():
        print("\n❌ 시스템 요구사항을 충족하지 못했습니다.")
        sys.exit(1)
    
    # 백엔드 설정
    if not setup_backend():
        print("\n❌ 백엔드 설정에 실패했습니다.")
        sys.exit(1)
    
    # 프론트엔드 설정
    if not setup_frontend():
        print("\n❌ 프론트엔드 설정에 실패했습니다.")
        sys.exit(1)
    
    print("\n🎉 모든 설정이 완료되었습니다!")
    print("=" * 50)
    print("🌐 웹사이트: http://localhost:3000")
    print("🔗 API 문서: http://localhost:8000/docs")
    print("🔄 서버를 중지하려면 Ctrl+C를 누르세요.")
    print("=" * 50)
    
    # 백엔드와 프론트엔드를 별도 스레드에서 실행
    backend_thread = threading.Thread(target=run_backend)
    frontend_thread = threading.Thread(target=run_frontend)
    
    try:
        backend_thread.start()
        time.sleep(3)  # 백엔드가 시작될 시간을 줍니다
        frontend_thread.start()
        
        # 메인 스레드에서 대기
        backend_thread.join()
        frontend_thread.join()
        
    except KeyboardInterrupt:
        print("\n👋 프로젝트가 중지되었습니다.")
        sys.exit(0)

if __name__ == "__main__":
    main() 