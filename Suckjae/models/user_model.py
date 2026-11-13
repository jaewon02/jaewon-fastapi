from db.connection import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, func

class User(Base):
    __tablename__="users"
    id : Mapped[int]=mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    username:Mapped[str] = mapped_column(String(100), unique=True)
    password:Mapped[str] = mapped_column(String(100))
    email:Mapped[str] = mapped_column(String(100), unique=True)
    name:Mapped[str] = mapped_column(String(100))

class file(Base):
    __tablename__="fileinfo"
    id : Mapped[int]=mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    filename:Mapped[str] = mapped_column(String(100), unique=True)
    location:Mapped[str] = mapped_column(String(255))
    uploadtime: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    
def __str__(self):
    return f"객체정보 : {self}"