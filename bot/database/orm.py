from sqlalchemy import *
from database.models import UsersOrm, UsersProfileOrm, UsersRefsOrm, PurchasedCoursesOrm, SupportTicketsOrm
from database.db import Base, engine, async_session, date
from sqlalchemy.orm import joinedload, selectinload

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

    # Получение пользователя по id
    @staticmethod
    async def select_user(user_id: int) -> UsersOrm:
        async with async_session() as session:

            result = await session.get(UsersOrm, user_id)

            return result
        
    # Добавление пользователя в базу данных
    @staticmethod
    async def add_user(user_id: int, username: str, user_reg_date: date, user_geo: str,
        referrer_id: int | None = None) -> bool:

        user = await AsyncORM.select_user(user_id=user_id)

        if not user:
            user = UsersOrm(user_id=user_id, username=username, user_reg_date=user_reg_date, user_geo=user_geo)
            user_profile = UsersProfileOrm(user_id=user_id, status="Ученик",
            completed_courses=[], purchased_courses=[], balance=0)
            user_refInfo = UsersRefsOrm(user_id=user_id, referrer_id=referrer_id, ref_percent=20)
            
            async with async_session() as session:
                session.add(user)
                session.add(user_profile)
                session.add(user_refInfo)

                await session.commit() 
            return True
        else:
            return False
        

    # Получение информации о профиле пользователя по его id
    @staticmethod
    async def get_profile_info(user_id: int) -> UsersProfileOrm:
        async with async_session() as session:

            query = select(UsersProfileOrm).filter_by(user_id=user_id).options(joinedload(UsersProfileOrm.user))
            result = await session.execute(query)
            return result.scalar_one_or_none()
        

    # Получение реферальной информации пользователя по его id
    @staticmethod
    async def get_ref_info(user_id: int) -> UsersRefsOrm:
        async with async_session() as session:

            query = select(UsersRefsOrm).filter_by(user_id=user_id).options(joinedload(UsersRefsOrm.profile))
            result = await session.execute(query)
            return result.scalar_one_or_none()
        

    # Получение всех реферралов пользователя по его id
    @staticmethod
    async def get_user_referrals(user_id: int) -> list[UsersRefsOrm]:
        async with async_session() as session:

            result = await session.execute(
                select(UsersRefsOrm).where(UsersRefsOrm.referrer_id == user_id).options(joinedload(UsersRefsOrm.profile).selectinload(UsersProfileOrm.purchased_courses))
            )

            referrals = result.scalars().all()


            return referrals
        
    
    # Получение всех купленных курсов реферралами пользователя по его id
    @staticmethod
    async def get_referrals_purchased_courses(user_id: int) -> list[PurchasedCoursesOrm]:
        user_referrals = await AsyncORM.get_user_referrals(user_id)
        purchased_courses_arr = []

        for user_referral in user_referrals:
            if (user_referral.profile.purchased_courses):
                purchased_courses_arr.append(*user_referral.profile.purchased_courses)

        return purchased_courses_arr
    

    # Добавление тикета поддержки в базу данных
    @staticmethod
    async def add_supportTicket(user_id: int, text: str) -> bool:

        supportTicket = SupportTicketsOrm(user_id=user_id, support_ticket_text=text)

        async with async_session() as session:
            session.add(supportTicket)

            await session.commit() 
            
        return True
