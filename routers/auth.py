from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from typing import Annotated
import os
from pymongo import MongoClient
from bson.json_util import dumps
from passlib.context import CryptContext

app = FastAPI()

load_dotenv()  # .env 파일 로드
MONGODB_URI = os.getenv("MONGODB_URI")
# MongoDB 연결
client = MongoClient(MONGODB_URI)
db = client["para7"]
print("Database connected!")



# public 폴더를 static으로
app.mount("/public", StaticFiles(directory="public"), name="public")

# index.html 반환
@app.get("/", response_class=HTMLResponse)
def read_root():
    return FileResponse("./public/index.html")



# 비밀번호 해싱 함수
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


"""
/signup
method: POST
header: {
    id: str,
    pw: str
}
response: {
    status: int,
    message: str
}
"""


@app.post("/signup")
def signup(id: str = Header(None), pw: str = Header(None)):
    print(f"Received id: {id}, pw: {pw}")
    if id is None or pw is None:
        raise HTTPException(status_code=400, detail="id나 pw가 없음")

    if db['users'].find_one({"id": id}):
        raise HTTPException(status_code=400, detail="이미 있는 id")

    hashed_password = get_password_hash(pw)
    db['users'].insert_one({"id": id, "pw": hashed_password})

    return {'status': 200, 'message': 'success'}


"""
/signin
method: POST
header: {
    id: str,
    pw: str
}
response: {
    status: int,
    message: str
}
"""


@app.post("/signin")
def signin(id: str = Header(None), pw: str = Header(None)):
    if id is None or pw is None:
        raise HTTPException(status_code=400, detail="id 또는 pw 가 틀림")

    user = db['users'].find_one({"id": id})
    if not user or not verify_password(pw, user["pw"]):
        raise HTTPException(status_code=400, detail="id 또는 pw 가 틀림")

    return {"status": 200, "message": "success"}


"""
/delete/{user_id}
method: DELETE
header: {
    id: str,
    pw: str
}
response: {
    status: int,
    message: str
}
"""


@app.delete("/delete/{user_id}")
def delete_user(user_id: str, id: str = Header(None), pw: str = Header(None)):
    try:
        if id is None or pw is None:
            raise HTTPException(status_code=400, detail="id와 pw를 모두 입력해주세요.")

        user = db["users"].find_one({"id": id})
        if not user or not verify_password(pw, user["pw"]):
            raise HTTPException(status_code=400, detail="id 또는 pw가 일치하지 않습니다.")

        if user_id != id:
            raise HTTPException(status_code=403, detail="삭제 권한이 없습니다.")

        db["users"].delete_one({"id": user_id})
        return {"status": 200, "message": "회원 탈퇴 성공"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
