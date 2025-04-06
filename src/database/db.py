
from database.models import Model
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import event
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


db_url = "sqlite+aiosqlite:///./sql_app.db"

engine = create_async_engine(db_url)
# new_session = async_sessionmaker(engine, expire_on_commit=False)

# add enforcement for foreign keys
@event.listens_for(engine.sync_engine, "connect")
def enable_sqlite_fks(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

new_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def create_tables():
    async with engine.begin() as conn:
       await conn.run_sync(Model.metadata.create_all)
       
async def delete_tables():
   async with engine.begin() as conn:
       await conn.run_sync(Model.metadata.drop_all)