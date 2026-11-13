from fastapi import APIRouter, HTTPException, status, Query, File, UploadFile, Form, Depends
from schemas.user_schemas import User
from db import user_db
from sqlalchemy.orm import Session
from db.connection import get_db
import time
from schemas.user_update_schemas import UserUpdate ;import os
from typing import Annotated
from fastapi.responses import FileResponse


user_router=APIRouter(tags=["Users"])

@user_router.get("/test")
async def test() -> dict:
    db=get_db()
    print("db : ", db)
    print("db next : ", next(db))
    time.sleep(3)
    return {"msg":"test"}

@user_router.get("/test2")
async def test2(db: Session = Depends(get_db)) -> dict:
    print("db : ", db)
    time.sleep(3)
    return {"msg":"test"}

@user_router.get("/")
async def get_users(db : Session=Depends(get_db)) -> list[User] | None:
    users=await user_db.get_users(db)
    print(users)
    if not users:
        raise HTTPException(status_code=404, detail="데이터가 없습니다.")
    return users

@user_router.get("/{email}")
async def user(email, db:Session=Depends(get_db)):
    # print("email router 연결")
    user = await user_db.get_user(email, db)
   # print(user)
    if user :
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="존재하는 않는 사용자 입니다."
        )

@user_router.post("/",
                response_model=User,
                status_code=201,
                summary="회원가입입니다.",
                responses={ 409:{"description":"중복id"} }
                  )
async def post_user(user: User, db : Session = Depends(get_db)) -> User:
    result = await user_db.insert(user)
    if not result: 
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="중복된 ID입니다.")
    return result 

@user_router.put("/{username}")
async def update_user(username : str, user:UserUpdate, db:Session=Depends(get_db)):
    # print("라우터 연결")
    # print(username)
    # print(user)
    result = await user_db.update(username, user, db)
    if result:
        return result
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="수정 사용자 id 없음!!!")

@user_router.put("/form/{username}")
async def update_user(username : str, user:UserUpdate=Form(...), db:Session=Depends(get_db)):
    result = await user_db.update(username, user, db)
    if result:
        return result
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="수정 사용자 id 없음!!!")

# @user_router.delete("/{username}")
# async def delete_user(username:str) -> User:
#     result=await user_db.delete(username)
#     if result: 
#         return result
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")


from db.user_db import db_get_one


@user_router.get("/one/{id}")
async def get_user_one(id:int, db:Session = Depends(get_db)):
    result = await db_get_one(id, db)
    if result:
        return result
    raise HTTPException(status_code=404, detail="존재하지않는 사용자")

@user_router.delete("/{del_id}")
async def del_user_id(del_id, db:Session=Depends(get_db)):
    print("라우터 도착:", del_id)
    delete_id = await user_db.delee_id(del_id, db)
    if delete_id:
        return delete_id
    raise HTTPException(status_code=404, detail="User Not Found")

@user_router.delete("/del/{email}")
async def del_email(email:str, db:Session=Depends(get_db)):
    dEmail=await user_db.del_email(email, db)
    if dEmail is None:
        raise HTTPException(status_code=404, detail="User Not Found")
    return dEmail

@user_router.post("/upload")
async def upload(file: UploadFile,  db:Session=Depends(get_db)):
    upload_db = await user_db.upload_file(file, db)
    if upload_db is None:
        raise HTTPException(status_code=409, detail="이미 같은 이름의 파일이 있습니다")
    return {"msg":"파일 업로드 완료!!!"}

@user_router.get("/file/get_info")
async def get_info(db: Session = Depends(get_db)):
    file=await user_db.get_info(db)
    return {"msg":file}

@user_router.get("/file/download")
async def get_download(filename:str ,db:Session=Depends(get_db)):
    file_dl = await user_db.get_download(filename, db)
    if file_dl is None:
        raise HTTPException(status_code=404, detail="파일이 없수")
    if not os.path.exists(file_dl.location):   
        raise HTTPException(status_code=404, detail="거기에 없수")
    return FileResponse(file_dl.location, filename=file_dl.filename)