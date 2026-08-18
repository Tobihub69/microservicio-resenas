import os
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./db/reviews.db"
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})


def create_db_and_tables():
    os.makedirs("db", exist_ok=True)
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
