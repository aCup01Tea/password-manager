from fastapi import APIRouter, Depends, HTTPException

from api.schemas import AppAdd, AppSchema
from cors.repositories import AccountRepository, AppRepository
from cors.search import search_gg



app_router = APIRouter(
    tags=["Apps"],
)

@app_router.post("")
async def add_app(app: AppAdd = Depends()):
   if not app.link:
      app.link = search_gg(app.name)
   data = app.model_dump()
   new_app_id = await AppRepository.add_one(data)
   if new_app_id == "uq":
      raise HTTPException(status_code=400, detail="App already exists")
   return {"id": new_app_id}

@app_router.get("")
async def get_apps() -> list[AppSchema]:
   apps = await AppRepository.get_all()
   return apps


@app_router.patch("/upd_name/{app_id}")
async def update_app_name(app_id: int, name: str):
    field = {"name": name}
    res = await AppRepository.update_fields(app_id, field)
    if not res:
        raise HTTPException(status_code=404, detail="App not found")
    if res == "uq":
      raise HTTPException(status_code=400, detail="App already exists")
    
    return {"message": "App`s name updated"}
   
   
   
@app_router.patch("/upd_link/{app_id}")
async def update_app_link(app_id: int, link: str):
    field = {"link": link}
    res = await AppRepository.update_fields(app_id, field)
    if not res:
        raise HTTPException(status_code=404, detail="App not found")
   
    return {"message": "App`s link updated"}


@app_router.delete("/{id}")
async def delete_app(id: int):

    # Альтернативный вариант - разрешить пользователю удалить сразу всё, пройдясь сначала по аккаунтам
    # accs = await AccountRepository.get_by_app_id(id)
    # if accs:
    #     for acc in accs:
    #         await AccountRepository.delete_one(acc.id)

    res = await AppRepository.delete_one(id)
    if not res:
        raise HTTPException(status_code=404, detail="App not found")
    if res == "fk":
       raise HTTPException(status_code=400, detail="You can't delete an app while it has accounts.")
    
    return {"message": "App deleted"}

@app_router.delete("")
async def delete_multiple_apps(ids: list[int]):
    not_empty_apps = []
    empty_apps = []
    for id in ids:
       accs = await AccountRepository.get_by_app_id(id)
       if accs:
          not_empty_apps.append(id)
       else:
          empty_apps.append(id)
          
    if empty_apps == []:
       raise HTTPException(status_code=400, detail="You can't delete apps while they have accounts.")
    
    res = await AppRepository.delete_multiple(empty_apps)
    if not res:
        raise HTTPException(status_code=404, detail=f"Apps with ids {empty_apps} not found")
    if res == "fk":
       raise HTTPException(status_code=400, detail="You can't delete apps while they have accounts.")
    

    return {"message": "Apps deleted", "Deleted app ids": empty_apps, "Not deleted app ids": not_empty_apps}
    
