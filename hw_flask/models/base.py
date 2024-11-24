import os

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine: Engine = create_engine(os.getenv('DATABASE_URL'))
Session: sessionmaker = sessionmaker(bind=engine)


class Base(DeclarativeBase):

    @property
    def id_dict(self):
        return {"id": self.id}


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)