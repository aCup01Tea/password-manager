
from fastapi import APIRouter
from api.App import app_router
from api.Account import acc_router


api_router = APIRouter(
    prefix="/api"
)


api_router.include_router(acc_router, prefix="/accounts")
api_router.include_router(app_router, prefix="/apps")