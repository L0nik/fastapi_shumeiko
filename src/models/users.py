from src.database import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class UsersModel(BaseModel):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(200))
    hashed_password: Mapped[str] = mapped_column(String(200))
