from fastapi import FastAPI
from app.routers import auth, user  # 라우터 import

app = FastAPI()

app.include_router(auth.router)  # auth 라우터 포함
app.include_router(user.router)  # user 라우터 포함
app.include_router(f1.router)
# 추가 설정 (CORS, 미들웨어 등)
# ...

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # 개발 서버 실행 (선택 사항)
