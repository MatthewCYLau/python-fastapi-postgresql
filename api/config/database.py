import os
from sqlalchemy import create_engine, engine
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from google.cloud.sql.connector import Connector, IPTypes
import pg8000
from sqlalchemy.orm import sessionmaker

postgres_username = "db_user"
postgres_password = os.getenv("DB_PASSWORD")
db_address = os.getenv("DB_HOST")
db_port = "5432"
db_name = "python_fastapi"

SQLALCHEMY_DATABASE_URL = f"postgresql://{postgres_username}:{postgres_password}@{db_address}:{db_port}/{db_name}"


def connect_with_connector_auto_iam_authn() -> sqlalchemy.engine.base.Engine:
    instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]
    db_iam_user = os.environ["DB_IAM_USER"]
    ip_type = IPTypes.PUBLIC

    connector = Connector(refresh_strategy="LAZY")

    def getconn() -> pg8000.dbapi.Connection:
        conn: pg8000.dbapi.Connection = connector.connect(
            instance_connection_name,
            "pg8000",
            user=db_iam_user,
            db=db_name,
            enable_iam_auth=True,
            ip_type=ip_type,
        )
        return conn

    pool = sqlalchemy.create_engine("postgresql+pg8000://", creator=getconn)
    return pool


if os.getenv("INSTANCE_CONNECTION_NAME"):
    engine = connect_with_connector_auto_iam_authn()
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
