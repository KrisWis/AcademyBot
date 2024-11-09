from sqlalchemy import *
from database.models import UsersOrm, UsersProfileOrm, UsersRefsOrm, PurchasedCoursesOrm, SupportTicketsOrm, SupportAgentsReviewsOrm, UsersReplenishBalanceOrm, UsersWithdrawBalanceOrm
from database.db import Base, engine, async_session, date
from sqlalchemy.orm import joinedload
from utils import const
from datetime import datetime, timedelta
import os

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
        

    # Получение пользователей по параметрам
    @staticmethod
    async def get_users(period: str = None, geo: str = None) -> list[UsersOrm] | str:
        
        now = datetime.now()
        date = now - timedelta(weeks=100000)

        if period == 'day':
            date = now - timedelta(hours=1)

        if period == 'week':
            week = now - timedelta(weeks=1)
            date = week

        if period == 'month':
            month = now - timedelta(days=30)
            date = month
        
        async with async_session() as session:

            if geo:
                result = await session.execute(
                    select(UsersProfileOrm)
                )
                users = result.scalars().all()

                stmt = select(UsersOrm.user_geo, func.count(UsersOrm.user_id)) \
                    .select_from(UsersOrm) \
                    .where(UsersOrm.user_reg_date >= date) \
                    .group_by(UsersOrm.user_geo) \
                    .order_by(func.count(UsersOrm.user_id).desc()) \
                    .limit(10) \
                    .distinct()

                result = await session.execute(stmt)
                name = result.all()

                count_geo = {}
                for country in name:
                    count_geo[country[0]] = int(country[1])

                msg = ''
                for i in count_geo:
                    msg += f'{i}: {count_geo[i]} ' \
                        f'({round(count_geo[i] / len(await AsyncORM.get_users(period=period)) * 100, 2)}%)\n'

                return msg if msg else 'Не обнаружено'

            else:
                result = await session.execute(
                    select(UsersOrm).where(UsersOrm.user_reg_date >= date).options(joinedload(UsersOrm.profile).selectinload(UsersProfileOrm.purchased_courses)))
                users = result.scalars().all()
                
                return users
            

    # Получение информации о купленных курсов по параметрам
    @staticmethod
    async def get_purchased_courses(period: str = None) -> list[PurchasedCoursesOrm] | str:
        
        now = datetime.now()
        date = now - timedelta(weeks=100000)

        if period == 'day':
            date = now - timedelta(hours=1)

        if period == 'week':
            week = now - timedelta(weeks=1)
            date = week

        if period == 'month':
            month = now - timedelta(days=30)
            date = month
        
        async with async_session() as session:

            result = await session.execute(
                select(PurchasedCoursesOrm).where(PurchasedCoursesOrm.purchase_date >= date))
            users = result.scalars().all()
            
            return users
        

    # Получение общей суммы пополнения баланса пользователями за определённый период
    @staticmethod
    async def get_replenishBalances_sum(period: str = None) -> int:
        
        now = datetime.now()
        date = now - timedelta(weeks=100000)

        if period == 'day':
            date = now - timedelta(hours=1)

        if period == 'week':
            week = now - timedelta(weeks=1)
            date = week

        if period == 'month':
            month = now - timedelta(days=30)
            date = month
        
        async with async_session() as session:

            result = await session.execute(
                select(UsersReplenishBalanceOrm.replenish_sum).where(UsersReplenishBalanceOrm.replenish_date >= date))
            users = result.scalars().all()
            
            return sum(users)
        

    # Получение общей суммы вывода с баланса пользователями за определённый период
    @staticmethod
    async def get_withdrawBalances_sum(period: str = None) -> int:
        
        now = datetime.now()
        date = now - timedelta(weeks=100000)

        if period == 'day':
            date = now - timedelta(hours=1)

        if period == 'week':
            week = now - timedelta(weeks=1)
            date = week

        if period == 'month':
            month = now - timedelta(days=30)
            date = month
        
        async with async_session() as session:

            result = await session.execute(
                select(UsersWithdrawBalanceOrm.withdraw_sum).where(UsersWithdrawBalanceOrm.withdraw_date >= date))
            users = result.scalars().all()
            
            return sum(users)
            
        
    # Добавление пользователя в базу данных
    @staticmethod
    async def add_user(user_id: int, username: str, user_reg_date: date, user_geo: str,
        referrer_id: int | None = None) -> bool:

        user = await AsyncORM.get_user(user_id=user_id)

        user_default_status = const.student

        if user_id == int(os.getenv("leader_id")):
            user_default_status = const.leader

        if not user:
            user = UsersOrm(user_id=user_id, username=username, user_reg_date=user_reg_date, user_geo=user_geo)
            user_profile = UsersProfileOrm(user_id=user_id, status=user_default_status,
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
    

    # Добавление тикета поддержки
    @staticmethod
    async def add_supportTicket(user_id: int, text: str) -> bool:

        supportTicket = SupportTicketsOrm(user_id=user_id, text=text, supportAgent_id=None, status="open", messages=[])

        async with async_session() as session:
            session.add(supportTicket)

            await session.commit() 
            
        return True
    

    # Добавление информации о пополнении баланса
    @staticmethod
    async def add_replenishBalance_info(user_id: int, sum: int, date: Date) -> bool:

        replenishBalance_info = UsersReplenishBalanceOrm(user_id=user_id, replenish_sum=sum, replenish_date=date)

        async with async_session() as session:
            session.add(replenishBalance_info)

            await session.commit() 
            
        return True
    

    # Добавление информации о выводе с баланса
    @staticmethod
    async def add_withdrawBalance_info(user_id: int, sum: int, date: Date) -> bool:

        withdrawBalance_info = UsersWithdrawBalanceOrm(user_id=user_id, withdraw_sum=sum, withdraw_date=date)

        async with async_session() as session:
            session.add(withdrawBalance_info)

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