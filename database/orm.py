from sqlalchemy import *
from database.models import UsersOrm, UserProfileOrm
from database.db import Base, engine, async_session, date
from sqlalchemy.orm import joinedload

# Создаём класс для ORM
class AsyncORM:
    # Метод для создания таблиц
    @staticmethod
    async def create_tables():

        async with engine.begin() as conn:
            engine.echo = False

            assert engine.url.database == 'test', 'Дропать прод запрещено'

            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            engine.echo = True

    @staticmethod
    async def select_user(user_id: int) -> UsersOrm:
        async with async_session() as session:

            result = await session.get(UsersOrm, user_id)

            return result
        
    @staticmethod
    async def user_exists(user_id: int) -> bool:
        async with async_session() as session:

            result = await session.get(UsersOrm, user_id)

            return bool(result)
        
    @staticmethod
    async def add_user(user_id: int, username: str, user_reg_time: date, user_geo: str, user_tag: str,
    user_status: str, completed_courses: list[str], balance: int) -> bool:

        user = await AsyncORM.select_user(user_id=user_id)

        # И если пользователя нету в бд
        if not user:
            user = UsersOrm(user_id=user_id, username=username, user_reg_time=user_reg_time, user_geo=user_geo, user_tag=user_tag)
            user_profile = UserProfileOrm(user_id=user_id, status=user_status,
            completed_courses=completed_courses, balance=balance)
            
            async with async_session() as session:
                session.add(user)
                session.add(user_profile)

                await session.commit() 
            return True
        else:
            return False
        

    @staticmethod
    async def get_profile_info(user_id: int) -> UserProfileOrm:
        async with async_session() as session:

            query = select(UserProfileOrm).filter_by(user_id=user_id).options(joinedload(UserProfileOrm.user))
            result = await session.execute(query)
            return result.scalar_one_or_none()