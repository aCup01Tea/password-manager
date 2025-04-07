import datetime
from fastapi import APIRouter, Depends, HTTPException

from api.schemas import AccountSchema, AccountAdd
from cors.repositories import AccountRepository, AppRepository
from api.schemas import DatasSchema



acc_router = APIRouter(
    tags=["Accounts"],
)


@acc_router.post("")
async def add_account(account: AccountAdd = Depends()):
   data = account.model_dump()
   new_acc_id = await AccountRepository.add_one(data)
   if new_acc_id == "fk":
      raise HTTPException(status_code=400, detail="App not exists")
   return {"id": new_acc_id}
      

@acc_router.get("/only")
async def get_accounts() -> list[AccountSchema]:
   accs = await AccountRepository.get_all()
   return accs

@acc_router.get("")
async def get_all_accounts() -> list[DatasSchema]:
   accs = await AccountRepository.get_all()
   apps = await AppRepository.get_all()
   datas = []
   for app in apps:
      data = DatasSchema(id=app.id, name=app.name, link=app.link, accounts=[acc for acc in accs if acc.app_id == app.id])
      datas.append(data)

   return datas


@acc_router.patch("/upd_login/{account_id}")
async def update_app_login(account_id: int, login: str):
   fields = {"login": login, "date_edit": datetime.datetime.now()}
   if await AccountRepository.update_fields(account_id, fields):
      return {"message": "Account`s login updated"}
   
   raise HTTPException(status_code=404, detail="Account not found")
   
   
@acc_router.patch("/upd_password/{account_id}")
async def update_app_password(account_id: int, password: str):
   fields = {"password": password, "date_edit": datetime.datetime.now()}
   if await AccountRepository.update_fields(account_id, fields):
      return {"message": "Account`s password updated"}
   
   raise HTTPException(status_code=404, detail="Account not found")

@acc_router.patch("/upd_description/{account_id}")
async def update_app_password(account_id: int, description: str):
   field = {"description": description}
   if await AccountRepository.update_fields(account_id, field):
      return {"message": "Account`s description updated"}
   
   raise HTTPException(status_code=404, detail="Account not found")


@acc_router.delete("/{id}")
async def delete_app(id: int):
   if await AccountRepository.delete_one(id):
      return {"message": "Account deleted"}
   
   raise HTTPException(status_code=404, detail="Account not found")

