from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import UserIdDep, DBDep
from src.database import async_session_maker
from src.repo.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

@router.post("/login")
async def login_user(
        db: DBDep,
        user_data: UserRequestAdd,
        response: Response
):
    user = await db.users.get_user_with_hashed_password(email=user_data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
    if not AuthService().verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Пароль неверный")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}

@router.post("/register")
async def register_user(
        db: DBDep,
        user_data: UserRequestAdd
):
    hashed_password = AuthService().hash_password(user_data.password)
    new_user_data = UserAdd(email=user_data.email, hashed_password=hashed_password)
    user = await db.users.add(new_user_data)
    await db.commit()

    if user:
        return {"status": "OK"}
    else:
        return {"status": "ERROR"}

@router.get("/me")
async def get_me(
        db: DBDep,
        user_id: UserIdDep
):
    user = await db.users.get_one_or_none(id=user_id)
    return {"status": "OK", "data": user}

@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}