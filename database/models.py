from sqlalchemy import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.db import Base,date
from sqlalchemy.dialects.postgresql import ARRAY


# Создаём таблицы
class UsersOrm(Base):
    # Задаём имя таблицы
    __tablename__ = "users"
    
    # Объявляем все колонки
    user_id: Mapped[int] = mapped_column(BigInteger(), primary_key=True, autoincrement=False)
    username: Mapped[str] = mapped_column(String())
    user_reg_time: Mapped[str] = mapped_column(nullable=False)
    user_geo: Mapped[str] = mapped_column(String(), nullable=False)
    user_tag: Mapped[str] = mapped_column(unique=True)

    profile: Mapped["UserProfileOrm"] = relationship(back_populates="user")

    __table_args__ = (
        UniqueConstraint('user_id', name='unique_user'),
    )

class UserProfileOrm(Base):
    __tablename__ = 'userProfile'

    user_id: Mapped[int] = mapped_column(BigInteger(), ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True, autoincrement=True)

    status: Mapped[str] = mapped_column(String())

    completed_courses: Mapped[list[str]] = mapped_column(ARRAY(String))

    balance: Mapped[int] = mapped_column(Integer())

    user: Mapped["UsersOrm"] = relationship(back_populates="profile")