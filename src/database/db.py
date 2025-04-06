
from database.models import Model
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


db_url = "sqlite+aiosqlite:///./sql_app.db"

engine = create_async_engine(db_url)
new_session = async_sessionmaker(engine, expire_on_commit=False)



async def create_tables():
    async with engine.begin() as conn:
       await conn.run_sync(Model.metadata.create_all)
       
async def delete_tables():
   async with engine.begin() as conn:
       await conn.run_sync(Model.metadata.drop_all)