import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

postgres_username = "db_user"
postgres_password = os.getenv("DB_PASSWORD", "localhost")
db_address = os.getenv("DB_HOST", "localhost")
db_port = "5432"
db_name = "python_fastapi"

SQLALCHEMY_DATABASE_URL = f"postgresql://{postgres_username}:{postgres_password}@{db_address}:{db_port}/{db_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
