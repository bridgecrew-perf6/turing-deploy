#coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

def new_session_factory(url="", **kwargs):
    if not url:
        raise Exception
    sql_engine = create_engine(url, **kwargs)

    session_factory = sessionmaker(bind=sql_engine)
    return session_factory

