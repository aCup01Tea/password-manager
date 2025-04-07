from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from api.api import api_router
from database.db import create_tables, delete_tables



@asynccontextmanager
async def lifespan(app: FastAPI):
   
    if not os.path.exists("sql_app.db"):
        await create_tables()
    # await create_tables()
    print("База готова")
    yield
    # await delete_tables()
    # print("База очищена")


app = FastAPI(
    lifespan=lifespan,
    title="My Pass",
)


origins = [ "http://localhost:3000", ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello, Demidos!"}


app.include_router(api_router)



if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8080,
        reload=True,
    )
