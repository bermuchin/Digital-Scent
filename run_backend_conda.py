#!/usr/bin/env python3
"""
향수 추천 플랫폼 백엔드 서버 (Conda 환경용)
"""

import sys
import os
import uvicorn

# 백엔드 디렉토리를 Python 경로에 추가
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

def main():
    print("🎀 향수 추천 플랫폼 백엔드 서버")
    print("=" * 50)
    print("✅ Conda 환경에서 실행 중...")
    
    # 서버 실행
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main() 