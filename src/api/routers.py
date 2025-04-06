from fastapi import APIRouter, Depends, HTTPException

from api.schemas import AccountSchema, AccountAdd, AppAdd, AppSchema
from cors.repositories import AccountRepository, AppRepository
from api.schemas import DatasSchema


acc_router = APIRouter(
    tags=["Accounts"],
)


@acc_router.post("")
async def add_account(account: AccountAdd = Depends()):
   new_acc_id = await AccountRepository.add_account(account)
   if new_acc_id == 400:
      raise HTTPException(status_code=400, detail="App not exists")
   return {"id": new_acc_id}
      

@acc_router.get("/accs")
async def get_accounts() -> list[AccountSchema]:
   accs = await AccountRepository.get_accounts()
   return accs

@acc_router.get("")
async def get_all_accounts() -> list[DatasSchema]:
   accs = await AccountRepository.get_accounts()
   apps = await AppRepository.get_apps()
   datas = []
   for app in apps:
      data = DatasSchema(id=app.id, name=app.name, link=app.link, accounts=[acc for acc in accs if acc.app_id == app.id])
      datas.append(data)

   return datas




app_router = APIRouter(
    tags=["Apps"],
)

@app_router.post("")
async def add_app(app: AppAdd = Depends()):
   new_app_id = await AppRepository.add_app(app)
   if new_app_id == 400:
      raise HTTPException(status_code=400, detail="App already exists")
   return {"id": new_app_id}

@app_router.get("")
async def get_apps() -> list[AppSchema]:
   apps = await AppRepository.get_apps()
   return apps

