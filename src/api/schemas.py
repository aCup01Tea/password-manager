
from datetime import datetime
from pydantic import BaseModel, ConfigDict



class AccountBase(BaseModel):
    app_id: int
    login: str | None = None
    password: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)

class AccountAdd(AccountBase):
    pass


class AccountSchema(AccountBase):
    id: int
    date_edit: datetime = datetime.now()
    




class AppBase(BaseModel):
    name: str
    link: str | None = None

    model_config = ConfigDict(from_attributes=True)

class AppAdd(AppBase):
    pass
    

class AppSchema(AppBase):
    id: int



class DatasSchema(BaseModel):
    id: int
    name: str
    link: str | None = None
    accounts: list[AccountSchema] = []

    model_config = ConfigDict(from_attributes=True)

