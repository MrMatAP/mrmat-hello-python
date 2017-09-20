from sqlalchemy import Column, BigInteger, Integer, String
from sqlalchemy.orm import relationship

from mhpython.orm.sqlorm.sqlorm_base import Base


class SQLORMBloodType(Base):
    """
    An ORM blood type representation

    Note how the id column must be an Integer for SQLite's auto-increment to work
    """
    __tablename__ = 'bloodtype'

    id = Column(BigInteger().with_variant(Integer, 'sqlite'), primary_key=True)
    name = Column(String, unique=True)

    people_rel = relationship("SQLORMPerson", back_populates="bloodtype_rel")

    def __init__(self, name):
        self.name = name
