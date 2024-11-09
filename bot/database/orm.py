from sqlalchemy import *
from database.models import UsersOrm, UsersProfileOrm, UsersRefsOrm, PurchasedCoursesOrm, SupportTicketsOrm, SupportAgentsReviewsOrm
from database.db import Base, engine, async_session, date
from sqlalchemy.orm import joinedload
from utils import const

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
    async def get_user(user_id: int) -> UsersOrm:
        async with async_session() as session:

            result = await session.get(UsersOrm, user_id)

            return result
        
    # Добавление пользователя в базу данных
    @staticmethod
    async def add_user(user_id: int, username: str, user_reg_date: date, user_geo: str,
        referrer_id: int | None = None) -> bool:

        user = await AsyncORM.get_user(user_id=user_id)

        if not user:
            user = UsersOrm(user_id=user_id, username=username, user_reg_date=user_reg_date, user_geo=user_geo)
            user_profile = UsersProfileOrm(user_id=user_id, status=const.supportAgent,
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
        

    # Получение реферрера пользователя по id пользователя
    @staticmethod
    async def get_user_referrer_id(user_id: int) -> int:
        async with async_session() as session:

            result = await session.execute(
                select(UsersRefsOrm.referrer_id).where(UsersRefsOrm.user_id == user_id)
            )

            referrer_id = result.scalar()

            return referrer_id
        
    
    # Получение всех купленных курсов реферралами пользователя по его id
    @staticmethod
    async def get_referrals_purchased_courses(user_id: int) -> list[PurchasedCoursesOrm]:
        user_referrals = await AsyncORM.get_user_referrals(user_id)
        purchased_courses_arr = []

        for user_referral in user_referrals:
            if (user_referral.profile.purchased_courses):
                purchased_courses_arr.append(*user_referral.profile.purchased_courses)

        return purchased_courses_arr
    

    # Получение реферального процента пользователя
    @staticmethod
    async def get_user_ref_percent(user_id: int) -> int:
        async with async_session() as session:

            result = await session.execute(
                select(UsersRefsOrm.ref_percent).where(UsersRefsOrm.user_id == user_id)
            )
            user_ref_percent = result.scalar()

            return user_ref_percent
    

    # Добавление тикета поддержки в базу данных
    @staticmethod
    async def add_supportTicket(user_id: int, text: str) -> bool:

        supportTicket = SupportTicketsOrm(user_id=user_id, text=text, supportAgent_id=None, status="open", messages=[])

        async with async_session() as session:
            session.add(supportTicket)

            await session.commit() 
            
        return True
    

    # Добавление агента поддержки в базу данных при ответе на тикет поддержки
    @staticmethod
    async def add_supportAgent_for_supportTicket(supportTicket_id: int, supportAgent_id: int) -> bool:

        async with async_session() as session:
            result = await session.execute(select(SupportTicketsOrm).where(SupportTicketsOrm.id == supportTicket_id))
            supportTicket: SupportTicketsOrm = result.scalar()

            supportTicket.supportAgent_id = supportAgent_id

            await session.commit()
                
        return True
    

    # Изменение статуса тикета поддержки
    @staticmethod
    async def change_supportTicket_status(supportTicket_id: int, status: str) -> bool:

        async with async_session() as session:
            result = await session.execute(select(SupportTicketsOrm).where(SupportTicketsOrm.id == supportTicket_id))
            supportTicket: SupportTicketsOrm = result.scalar()

            supportTicket.status = status

            await session.commit()
                
        return True


    # Получение всех тикетов поддержки из базы данных
    @staticmethod
    async def get_all_opened_supportTickets() -> bool:
        async with async_session() as session:

            result = await session.execute(
                select(SupportTicketsOrm).where(SupportTicketsOrm.status == "open").options(joinedload(SupportTicketsOrm.user))
            )

            supportTickets = result.scalars().all()

            return supportTickets
    

    # Получение тикета поддержки по его id
    @staticmethod
    async def get_supportTicket(id: int) -> SupportTicketsOrm:
        async with async_session() as session:

            result = await session.execute(
                select(SupportTicketsOrm).where(SupportTicketsOrm.id == id).options(joinedload(SupportTicketsOrm.user), joinedload(SupportTicketsOrm.supportAgent))
            )

            supportTicket = result.scalar()

            return supportTicket
        

    # Получение баланса пользователя
    @staticmethod
    async def get_balance(user_id: int) -> int:
        async with async_session() as session:

            result = await session.execute(
                select(UsersProfileOrm.balance).where(UsersProfileOrm.user_id == user_id)
            )
            user_balance = result.scalar()

            return user_balance
        

    # Изменение баланса пользователя
    @staticmethod
    async def change_user_balance(user_id: int, amount: int) -> bool:
        past_balance = await AsyncORM.get_balance(user_id)

        async with async_session() as session:
            stmt = (update(UsersProfileOrm)
                    .where(UsersProfileOrm.user_id == user_id)
                    .values(balance=past_balance + amount))
            
            await session.execute(stmt)
            await session.commit()
            return True
        

    # Получение статуса пользователя
    @staticmethod
    async def get_user_status(user_id: int) -> int:
        async with async_session() as session:

            result = await session.execute(
                select(UsersProfileOrm.status).where(UsersProfileOrm.user_id == user_id)
            )
            user_status = result.scalar()

            return user_status
        

    # Добавление отзыва об Агенте поддержки
    @staticmethod
    async def add_review_for_supportAgent(supportTicket_id: int, supportAgent_id: int, evaluation: int) -> bool:
        
        supportAgentReview = SupportAgentsReviewsOrm(supportAgent_id=supportAgent_id, supportTicket_id=supportTicket_id, evaluation=evaluation)

        async with async_session() as session:
            session.add(supportAgentReview)

            await session.commit() 
            
        return True
    

    # Добавление сообщения тикета поддержки
    @staticmethod
    async def add_message_for_supportTicket(supportTicket_id: int, message_text: str) -> bool:

        async with async_session() as session:
            result = await session.execute(select(SupportTicketsOrm).where(SupportTicketsOrm.id == supportTicket_id))
            supportTicket: SupportTicketsOrm = result.scalar()

            supportTicket.messages.append(message_text)

            await session.commit()
                
        return True