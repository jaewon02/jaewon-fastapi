import uvicorn
from fastapi import FastAPI
from routers.users_router import user_router
from db.connection import Base, engine
from models import user_model

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("---서버 시작시 설정 내용---")
    # print(Base.metadata.tables)
    Base.metadata.create_all(bind=engine)
    yield
    print("---서버 종료시 설정 내용---")

app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

app.include_router(router=user_router, prefix="/users")