from sqlalchemy import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.db import Base
from sqlalchemy.dialects.postgresql import ARRAY


# Создаём таблицы

# Таблица с общими данными пользователей
class UsersOrm(Base):
    __tablename__ = "users"
    
    user_id: Mapped[int] = mapped_column(BigInteger(), primary_key=True, autoincrement=False)
    username: Mapped[str] = mapped_column(String())
    user_reg_date: Mapped[str] = mapped_column(nullable=False)
    user_geo: Mapped[str] = mapped_column(String(), nullable=False)

    profile: Mapped["UsersProfileOrm"] = relationship("UsersProfileOrm", back_populates="user")

    __table_args__ = (
        UniqueConstraint('user_id', name='unique_user'),
    )


# Таблица с данными о профилях пользователей
class UsersProfileOrm(Base):
    __tablename__ = 'usersProfiles'

    user_id: Mapped[int] = mapped_column(BigInteger(), ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)

    status: Mapped[str] = mapped_column(String())

    completed_courses: Mapped[list[str]] = mapped_column(ARRAY(String))

    purchased_courses: Mapped[list["PurchasedCoursesOrm"]] = relationship("PurchasedCoursesOrm", back_populates="user_profile")
    
    balance: Mapped[int] = mapped_column(Integer())

    user: Mapped["UsersOrm"] = relationship("UsersOrm", back_populates="profile")

    refInfo: Mapped["UsersRefsOrm"] = relationship("UsersRefsOrm", back_populates="profile")
    

# Таблица с данными о реф.системе пользователей
class UsersRefsOrm(Base):
    __tablename__ = 'usersRefs'

    user_id: Mapped[int] = mapped_column(BigInteger(), ForeignKey('usersProfiles.user_id', ondelete='CASCADE'), primary_key=True)

    referrer_id: Mapped[int | None] = mapped_column(BigInteger(), ForeignKey('users.user_id', ondelete='CASCADE'))
    referrer: Mapped["UsersOrm"] = relationship("UsersOrm", foreign_keys=[referrer_id])

    ref_percent: Mapped[int] = mapped_column(Integer())

    profile: Mapped["UsersProfileOrm"] = relationship("UsersProfileOrm", back_populates="refInfo")
    

# Таблица с данными о купленных курсах
class PurchasedCoursesOrm(Base):
    __tablename__ = 'purchasedCourses'

    user_id: Mapped[int] = mapped_column(BigInteger(), ForeignKey('usersProfiles.user_id', ondelete='CASCADE'), primary_key=True)

    user_profile: Mapped[UsersProfileOrm] = relationship("UsersProfileOrm", back_populates="purchased_courses")

    purchased_course_name: Mapped[str] = mapped_column(String())

    purchase_date: Mapped[str] = mapped_column(nullable=False)
    
    price: Mapped[int] = mapped_column(Integer())

# Таблица с тикетами поддержки
class SupportTicketsOrm(Base):
    __tablename__ = 'supportTickets'

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(BigInteger(), ForeignKey('users.user_id', ondelete='CASCADE'))

    user: Mapped["UsersOrm"] = relationship("UsersOrm", foreign_keys=[user_id])

    support_ticket_text: Mapped[str] = mapped_column(String())