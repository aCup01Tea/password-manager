
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError

from database.db import new_session
from database.models import AccountOrm
from database.models import AppOrm

import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)




class SQLAlchemyRepository:
    model = None
    
    @classmethod
    async def add_one(cls, data: dict) -> int:
        async with new_session() as session:
            new_item = cls.model(**data)
            try:
                session.add(new_item)
                await session.flush()
                await session.commit()
                return new_item.id
            except IntegrityError as e:
                await session.rollback()
                if "FOREIGN KEY constraint failed" in str(e.orig):
                    return "fk"
                if "UNIQUE constraint failed" in str(e.orig):
                    return "uq"
                raise e
            except Exception as e:
                await session.rollback()
                raise e

    @classmethod
    async def get_all(cls) -> list[dict]:
        async with new_session() as session:
           query = select(cls.model)
           result = await session.execute(query)
           item_models = result.scalars().all()
           # accs = [AccountSchema.model_validate(acc_model) for acc_model in acc_models]
           # items = [item_model.model_dump() for item_model in item_models]
           return item_models
    

    @classmethod
    async def delete_one(cls, item_id: int):
        async with new_session() as session:
            try:
                stmt = delete(cls.model).filter(cls.model.id == item_id)
                res = await session.execute(stmt)
                if res.rowcount == 0:
                    return False
                await session.commit()
                return True
            except IntegrityError as e:
                await session.rollback()
                if "FOREIGN KEY constraint failed" in str(e.orig):
                    return "fk"
                raise e
            except Exception as e:
                await session.rollback()
                raise e

    @classmethod
    async def delete_multiple(cls, item_ids: list[int]):
        async with new_session() as session:
            try:
                stmt = delete(cls.model).filter(cls.model.id.in_(item_ids))
                res = await session.execute(stmt)
                if res.rowcount == 0:
                    return False
                await session.commit()
                return True
            except IntegrityError as e:
                await session.rollback()
                if "UNIQUE constraint failed" in str(e.orig):
                    return "uq"
                raise e
            except Exception as e:
                await session.rollback()
                raise e
    
    @classmethod
    async def update_fields(cls, item_id: int, field: dict):
        async with new_session() as session:
            try:
                stmt = update(cls.model).where(cls.model.id == item_id).values(field)
                res = await session.execute(stmt)
                if res.rowcount == 0:
                    return False
                await session.commit()
                return True
            except IntegrityError as e:
                await session.rollback()
                if "UNIQUE constraint failed" in str(e.orig):
                    return "uq"
                raise e
            except Exception as e:
                await session.rollback()
                raise e



class AccountRepository(SQLAlchemyRepository):
    model = AccountOrm

    @classmethod
    async def get_by_app_id(cls, app_id: int) -> list[dict]:
        async with new_session() as session:
           query = select(cls.model).where(cls.model.app_id == app_id)
           result = await session.execute(query)
           item_models = result.scalars().all()
           return item_models
    


class AppRepository(SQLAlchemyRepository):
    model = AppOrm
    
