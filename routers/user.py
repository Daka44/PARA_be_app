from fastapi import APIRouter, Depends, HTTPException, status
from app.models import User
from app.database import get_db
from app.schemas import UserOut, UserUpdate
from app.auth import get_current_user  # auth.py에서 가져오기

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

# 현재 로그인한 사용자 정보 조회
@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_user), db=Depends(get_db)):
    try:
        user = await db["users"].find_one({"_id": current_user.id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

# 현재 로그인한 사용자 정보 수정
@router.put("/me", response_model=UserOut)
async def update_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    try:
        if not current_user:
            raise HTTPException(status_code=404, detail="User not found")

        updated_user_data = user_update.dict(exclude_unset=True)
        if updated_user_data:
            if "password" in updated_user_data:  # 비밀번호 변경 시 해싱
                updated_user_data["pw"] = get_password_hash(updated_user_data["password"])
                del updated_user_data["password"]
            await db["users"].update_one(
                {"_id": current_user.id}, {"$set": updated_user_data}
            )

        updated_user = await db["users"].find_one({"_id": current_user.id})
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
