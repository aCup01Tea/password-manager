from fastapi import APIRouter, Depends, HTTPException

from api.schemas import AppAdd, AppSchema
from cors.repositories import AppRepository
from cors.search import search_gg



app_router = APIRouter(
    tags=["Apps"],
)

@app_router.post("")
async def add_app(app: AppAdd = Depends()):
   if not app.link:
      app.link = search_gg(app.name)
   print(app)
   new_app_id = await AppRepository.add_one(app)
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
   if await AppRepository.update_fields(app_id, field):
      return {"message": "App`s name updated"}
   
   raise HTTPException(status_code=404, detail="App not found")
   
   
@app_router.patch("/upd_link/{app_id}")
async def update_app_link(app_id: int, link: str):
   field = {"link": link}
   if await AppRepository.update_fields(app_id, field):
      return {"message": "App`s link updated"}
   
   raise HTTPException(status_code=404, detail="App not found")
   

@app_router.delete("/{id}")
async def delete_app(id: int):
   if await AppRepository.delete(id):
      return {"message": "App deleted"}
   
   raise HTTPException(status_code=404, detail="App not found")
