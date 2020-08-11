from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from app.settings import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False))

Base = declarative_base()


@contextmanager
def db_session():
    """
    Context manager which provides transaction management for the nested
    block. A transaction is started when the block is entered, and then either
    committed if the block exits without incident, or rolled back if an error
    is raised.
    https://docs.sqlalchemy.org/en/13/orm/session_basics.html
    :return: a scoped session
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
