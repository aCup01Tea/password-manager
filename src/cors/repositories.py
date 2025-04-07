
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError

from database.db import new_session
from api.schemas import AccountSchema, AccountAdd, AppAdd
from database.models import AccountOrm
from api.schemas import AppSchema
from database.models import AppOrm

import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)



class AccountRepository:
    model = AccountOrm
    
    @classmethod
    async def add_one(cls, acc: AccountAdd) -> int:
        async with new_session() as session:
            data = acc.model_dump()
            new_acc = AccountOrm(**data)
            try:
                session.add(new_acc)
                await session.flush()
                await session.commit()
                return new_acc.id
            except IntegrityError as e:
                await session.rollback()
                if "FOREIGN KEY constraint failed" in str(e.orig):
                    return 400
                raise e
            except Exception as e:
                await session.rollback()
                raise e
              

    @classmethod
    async def get_all(cls) -> list[AccountSchema]:
        async with new_session() as session:
           query = select(AccountOrm)
           result = await session.execute(query)
           acc_models = result.scalars().all()
           accs = [AccountSchema.model_validate(acc_model) for acc_model in acc_models]
           return accs
       


class AppRepository:
    model = AppOrm

    @classmethod
    async def add_one(cls, app: AppAdd) -> int:
        async with new_session() as session:
            data = app.model_dump()
            new_app = AppOrm(**data)
            try:
                session.add(new_app)
                await session.flush()
                await session.commit()
                return new_app.id
            except IntegrityError as e:
                await session.rollback()
                if "UNIQUE constraint failed" in str(e.orig):
                    return 400
                raise e
            except Exception as e:
                await session.rollback()
                raise e
            

    @classmethod
    async def get_all(cls) -> list[AppSchema]:
        async with new_session() as session:
           query = select(AppOrm)
           result = await session.execute(query)
           app_models = result.scalars().all()
           apps = [AppSchema.model_validate(app_model) for app_model in app_models]
           return apps
        

    @classmethod
    async def delete(cls, app_id: int):
        async with new_session() as session:
            stmt = delete(cls.model).filter(cls.model.id == app_id)
            res = await session.execute(stmt)
            if res.rowcount == 0:
                return False
            await session.commit()
            return True
        
    @classmethod
    async def update_name(cls, app_id: int, name: str):
        async with new_session() as session:
            stmt = update(cls.model).where(cls.model.id == app_id).values(name=name)
            res = await session.execute(stmt)
            if res.rowcount == 0:
                return False
            await session.commit()
            return True
    
    @classmethod
    async def update_link(cls, app_id: int, link: str):
        async with new_session() as session:
            stmt = update(cls.model).where(cls.model.id == app_id).values(link=link)
            res = await session.execute(stmt)
            if res.rowcount == 0:
                return False
            await session.commit()
            return True