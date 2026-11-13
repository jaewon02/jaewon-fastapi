from schemas.user_schemas import User
from fastapi import status, Query,  File, UploadFile, Form, Depends
from sqlalchemy.orm import Session
from models import user_model
from typing import Annotated;import os, shutil

users : list[User] = [
    User(username="aaa", password="aaa", email="aaa@aaa.aaa", name="홍길동"),
    User(username="bbb", password="bbb", email="bbb@bbb.bbb", name="김개똥")
]

async def get_users(db:Session) -> list[User]:
    userTable = db.query(user_model.User).all()
    print("user table : ", userTable)
    if len(userTable) == 0:
        return None
    # users= User(**userTable.model_dump())
    users=[User.model_validate(user) for user in userTable]
    '''    
    users=[]
    for user in userTable: #usertable = [객체1, 객체2]
        user.append(user.model_validate(user)) #db모델 -> 스키마 변환
    '''
    return users

async def get_user(email : str, db=Session) -> User | None:
    # print("email 데이터 베이스 연결")
    email_user=db.query(user_model.User).filter(user_model.User.email == email).first()

    # for u in users:
    #     print(u)
    #     if u.email == email:
    #         return u
    return email_user

async def insert(user:User, db :Session) -> User | None:  
    exist_user=db.query(user_model.User).filter(user_model.User.username == user.username).first()
    if exist_user:
        return None
    userTable=user_model.User(**user.model_dump())
    print("저장전 확인 id: ", userTable.id)
    db.add(userTable) #insert
    db.commit()
    db.refresh(userTable)
    print("저장 후 확인 id: ", userTable.id)
    return user

from schemas.user_update_schemas import UserUpdate
async def update(username: str, user:UserUpdate, db:Session):
    user_table=db.query(user_model.User).filter(user_model.User.username == username).first()
    if user_table is None:
        return None
    # user_table.email=user.email
    # user_table.name=user.name
    user_dict=user.model_dump(exclude_unset= True)
    print("user_dict : ", user_dict)
    for k, v in user_dict.items():
        setattr(user_table, k,v)

    db.commit()
    db.refresh(user_table)
    return User.model_validate(user_table)
    # for i, u in enumerate(users):
    #     if u.username == username:
    #         users[i] = user
    #         return u
    # return None

async def delete(username:str):
    for i, u in enumerate(users):
        if u.username == username:
            del_user=users.pop(i)
            return del_user
    return None

async def db_get_one(id:int, db:Session) -> User|None:
    userTable = db.get(user_model.User, id)
    if not userTable:
        return None
    return User.model_validate(userTable)

async def delee_id(del_id, db:Session):
    print("del_id 함수 도착:", del_id, __file__)
    delete_id = db.get(user_model.User, del_id)
    if delete_id is None:
        return None
    result = User.model_validate(delete_id)
    db.delete(delete_id)
    db.commit()
    return result

async def del_email(email:str, db:Session):
    delete_email=db.query(user_model.User).filter(user_model.User.email == email).first()
    if delete_email is None:
        return None
    result = User.model_validate(delete_email)
    db.delete(delete_email)
    db.commit()
    return result



UPLOAD_DIR = "static/files"
async def upload_file(files:UploadFile, db:Session):
    filename=os.path.basename(files.filename)
    upload=db.query(user_model.file).filter(user_model.file.filename == filename).first()
    if upload is not None:
        return None
    
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    save_path = os.path.join(UPLOAD_DIR, filename)
    with open(save_path, "wb") as f:
        shutil.copyfileobj(files.file, f)

    fileTable = user_model.file(filename=filename, location=save_path)
    print("저장전 확인 id: ", fileTable.id)   # 아직 None
    db.add(fileTable)
    db.commit()
    db.refresh(fileTable)
    print("저장 후 확인 id: ", fileTable.id)   # DB가 부여한 번호
    return fileTable

async def get_info(db):
    files = db.query(user_model.file).all()
    return files

async def get_download(filename: str, db:Session):
    fidl=db.query(user_model.file).filter(user_model.file.filename == filename).first()
    return fidl
