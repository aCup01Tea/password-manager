
from sqlalchemy import select
from database.db import new_session
from api.schemas import AccountSchema, AccountAdd, AppAdd
from database.models import AccountOrm
from api.schemas import AppSchema
from database.models import AppOrm



class AccountRepository:
    
    @classmethod
    async def add_account(cls, acc: AccountAdd) -> int:
        async with new_session() as session:
           data = acc.model_dump()
           new_acc = AccountOrm(**data)
           session.add(new_acc)
           await session.flush()
           await session.commit()
           return new_acc.id

    @classmethod
    async def get_accounts(cls) -> list[AccountSchema]:
        async with new_session() as session:
           query = select(AccountOrm)
           result = await session.execute(query)
           acc_models = result.scalars().all()
           accs = [AccountSchema.model_validate(acc_model) for acc_model in acc_models]
           return accs
       


class AppRepository:

    @classmethod
    async def add_app(cls, serv: AppAdd) -> int:
        async with new_session() as session:
           data = serv.model_dump()
           new_app = AppOrm(**data)
           session.add(new_app)
           await session.flush()
           await session.commit()
           return new_app.id

    @classmethod
    async def get_apps(cls) -> list[AppSchema]:
        async with new_session() as session:
           query = select(AppOrm)
           result = await session.execute(query)
           app_models = result.scalars().all()
           apps = [AppSchema.model_validate(app_model) for app_model in app_models]
           return apps