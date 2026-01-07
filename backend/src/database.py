import os
from sqlmodel import create_engine, Session, SQLModel
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    neon_database_url: str
    auth_jwt_secret: str

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

engine = create_engine(settings.neon_database_url)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    # In a real app we'd use Alembic migrations,
    # but for this hackathon we'll just create all if they don't exist.
    # To force update existing tables:
    # SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
