from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

DATABASE_URE=("mysql+pymysql://root:mysql@localhost:3306/fastapi")
engine=create_engine(DATABASE_URE, echo=True)

class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(autoflush=False, bind=engine)

def get_db():
    print("db 연결 시작")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        print("DB 종료")