import os

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker

from hw_flask.models.base import Base

engine: Engine = create_engine(os.getenv('DATABASE_URL'))
Session: sessionmaker = sessionmaker(bind=engine)


def prepare_db():
    Base.metadata.create_all(engine)