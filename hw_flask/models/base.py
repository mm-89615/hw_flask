from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):

    @property
    def id_dict(self):
        return {"id": self.id}