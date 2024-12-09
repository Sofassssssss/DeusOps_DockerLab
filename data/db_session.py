from os import getenv

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
from sqlalchemy import MetaData
import sqlalchemy.ext.declarative as dec

meta = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
      })
SqlAlchemyBase = dec.declarative_base(metadata=meta)

__factory = None


def global_init():
    global __factory

    if __factory:
        return

    db_url = getenv("DB_URL")
    if db_url is None:
        raise Exception("DB_URL env var is not set. Popa ezha")

    print(f"Подключение к базе данных по адресу {db_url}")

    engine = sa.create_engine(db_url, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
