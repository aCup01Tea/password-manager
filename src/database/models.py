
import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Model(DeclarativeBase):
   id: Mapped[int] = mapped_column(primary_key=True)
   pass



class AccountOrm(Model):
   __tablename__ = "accounts"
   app_id: Mapped[int] = mapped_column(ForeignKey("apps.id"))
   login: Mapped[str | None]
   password: Mapped[str]
   date_edit: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now())
   description: Mapped[str | None]
   link: Mapped[str | None]
   

class AppOrm(Model):
   __tablename__ = "apps"
   name: Mapped[str]
   link: Mapped[str | None]