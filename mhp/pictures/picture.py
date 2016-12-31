from sqlalchemy import Column, BigInteger, String, DateTime

from mhp.pictures.base import Base


class Picture(Base):
    __tablename__ = 'pictures'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    imageuniqueid = Column(String, nullable=False, unique=True)
    originalpath = Column(String)
    originalname = Column(String)
    datetimeoriginal = Column(DateTime)
    datetimedigitized = Column(DateTime)
