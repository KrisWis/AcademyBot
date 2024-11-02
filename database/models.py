from sqlalchemy import *
from sqlalchemy.orm import Mapped, mapped_column
from database.db import Base,date


# Создаём таблицы
class UsersOrm(Base):
    # Задаём имя таблицы
    __tablename__ = "users"
    
    # Объявляем все колонки
    user_id: Mapped[int] = mapped_column(BigInteger(), primary_key=True, autoincrement=False)
    username: Mapped[str] = mapped_column(String())
    user_date: Mapped[date] = mapped_column(nullable=False)
    user_geo: Mapped[str] = mapped_column(String(), nullable=False)
    user_tag: Mapped[str] = mapped_column(unique=True)

    __table_args__ = (
        UniqueConstraint('user_id', name='unique_user'),
    )