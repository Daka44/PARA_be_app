from fastapi import FastAPI

from app.routers import auth, user, f1  # 라우터 import

app = FastAPI()

app.include_router(auth.router)  # auth 라우터 포함
app.include_router(user.router)  # user 라우터 포함
app.include_router(f1.router)  # f1 라우터 포함
