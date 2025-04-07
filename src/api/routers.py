from fastapi import APIRouter, Depends, HTTPException

from api.schemas import AccountSchema, AccountAdd, AppAdd, AppSchema
from cors.repositories import AccountRepository, AppRepository
from api.schemas import DatasSchema
from cors.search import search_gg


acc_router = APIRouter(
    tags=["Accounts"],
)


@acc_router.post("")
async def add_account(account: AccountAdd = Depends()):
   new_acc_id = await AccountRepository.add_one(account)
   if new_acc_id == 400:
      raise HTTPException(status_code=400, detail="App not exists")
   return {"id": new_acc_id}
      

@acc_router.get("/accs")
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




app_router = APIRouter(
    tags=["Apps"],
)

@app_router.post("")
async def add_app(app: AppAdd = Depends()):
   if not app.link:
      app.link = search_gg(app.name)
   print(app)
   new_app_id = await AppRepository.add_one(app)
   if new_app_id == 400:
      raise HTTPException(status_code=400, detail="App already exists")
   return {"id": new_app_id}

@app_router.get("")
async def get_apps() -> list[AppSchema]:
   apps = await AppRepository.get_all()
   return apps


@app_router.patch("/upd_name/{app_id}")
async def update_app(app_id: int, name: str):
   if await AppRepository.update_name(app_id, name):
      return {"message": "App`s name updated"}
   
   raise HTTPException(status_code=404, detail="App not found")
   
   
@app_router.patch("/upd_link/{app_id}")
async def update_app(app_id: int, link: str):
   if await AppRepository.update_link(app_id, link):
      return {"message": "App`s link updated"}
   
   raise HTTPException(status_code=404, detail="App not found")
   

@app_router.delete("/{app_id}")
async def delete_app(app_id: int):
   if await AppRepository.delete(app_id):
      return {"message": "App deleted"}
   
   raise HTTPException(status_code=404, detail="App not found")
