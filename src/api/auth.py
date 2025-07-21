from fastapi import APIRouter

from passlib.context import CryptContext

from src.database import async_session_maker
from src.repo.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
async def register_user(
        user_data: UserRequestAdd
):
    hashed_password = pwd_context.hash(user_data.password)
    new_user_data = UserAdd(email=user_data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        user = await UsersRepository(session).add(new_user_data)
        await session.commit()

    if user:
        return {"status": "OK"}
    else:
        return {"status": "ERROR"}