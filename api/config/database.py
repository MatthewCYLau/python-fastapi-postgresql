import os
from google.cloud.sql.connector import Connector, IPTypes
import pg8000
import sqlalchemy
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

postgres_username = os.getenv("DB_USER", "db_user")
postgres_password = os.getenv("DB_PASSWORD")
db_address = os.getenv("DB_HOST")
db_port = "5432"
db_name = "python_fastapi"

SQLALCHEMY_DATABASE_URL = f"postgresql://{postgres_username}:{postgres_password}@{db_address}:{db_port}/{db_name}"

SQLALCHEMY_READ_DATABASE_URL = os.getenv(
    "SQLALCHEMY_READ_DATABASE_URL", SQLALCHEMY_DATABASE_URL
)


def connect_with_connector_auto_iam_authn(
    instance_env_var: str,
) -> sqlalchemy.engine.base.Engine:
    instance_connection_name = os.environ[instance_env_var]
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


def get_database_engine(is_read_only: bool = False):
    conn_env = (
        "INSTANCE_CONNECTION_NAME_READ" if is_read_only else "INSTANCE_CONNECTION_NAME"
    )

    if os.getenv(conn_env):
        engine = connect_with_connector_auto_iam_authn(conn_env)
    elif os.getenv("SQLITE_IN_MEMORY_DB"):
        engine = create_engine(
            "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
        )
    else:
        url = SQLALCHEMY_READ_DATABASE_URL if is_read_only else SQLALCHEMY_DATABASE_URL
        engine = create_engine(url)
    return engine


SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=get_database_engine(is_read_only=False)
)
SessionReadOnly = sessionmaker(
    autocommit=False, autoflush=False, bind=get_database_engine(is_read_only=True)
)

Base = declarative_base()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_read_only_session():
    session = SessionReadOnly()
    try:
        yield session
    finally:
        session.close()
