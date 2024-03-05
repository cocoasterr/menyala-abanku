from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, MetaData
from app.config import settings
from sqlalchemy.ext.declarative import declarative_base
from fastapi import HTTPException, status
from typing import Generator



class databaseSession:
    def __init__(self):
        self.psql_engine = None
        self.psql_session = None

    def init(self):
        self.psql_engine = create_engine(settings.DB_CONFIG)
        self.psql_session = sessionmaker(
            autocommit=False, autoflush=False, bind=self.psql_engine
        )
        print(f"Connected to Postgres")

    async def conn(self):
        try:
            conn = self.psql_engine.connect()
            return conn
        except Exception as e:
            print("Unable to connect to the Postgres server.")


Base = declarative_base()
meta = MetaData()

db = databaseSession()


def commit_rollback(session):
    try:
        session.commit()
        session.flush()
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Data rollback!"
        )


def get_db() -> Generator[Session, None, None]:
    """
    Function to generate db session
    :return: Session
    """
    try:
        data = db.psql_session()
        yield data
    finally:
        data.close()
