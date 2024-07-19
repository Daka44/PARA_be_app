from fastapi import APIRouter, Depends, HTTPException, status, Header
from app.database import get_db
from app.utils import get_password_hash, verify_password

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

# 현재 로그인한 사용자 정보 조회
@router.get("/me")
async def read_users_me(id: str = Header(None), db=Depends(get_db)):
    if id is None:
        raise HTTPException(status_code=400, detail="아이디를 입력해주세요.")
    try:
        user = await db["users"].find_one({"id": id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        # 비밀번호 제외하고 반환
        del user["pw"]
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


# 현재 로그인한 사용자 정보 수정
@router.put("/me")
async def update_user(
    id: str = Header(None),
    username: str = Header(None),
    email: str = Header(None),
    password: str = Header(None),
    db=Depends(get_db),
):
    try:
        if id is None:
            raise HTTPException(status_code=400, detail="아이디를 입력해주세요.")
        user = await db["users"].find_one({"id": id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        updated_user_data = {}
        if username:
            updated_user_data["username"] = username
        if email:
            updated_user_data["email"] = email
        if password:
            updated_user_data["pw"] = get_password_hash(password)

        if updated_user_data:
            await db["users"].update_one(
                {"id": id}, {"$set": updated_user_data}
            )

        updated_user = await db["users"].find_one({"id": id})
        del updated_user["pw"]
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
