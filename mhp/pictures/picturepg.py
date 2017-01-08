from sqlalchemy import Column, Integer, BigInteger, String, DateTime

from mhp.pictures.base import Base


class PicturePG(Base):
    __tablename__ = 'pictures'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    imageuniqueid = Column(String, nullable=False, unique=True)
    originalpath = Column(String)
    originalname = Column(String)
    datetimeoriginal = Column(DateTime)
    datetimedigitized = Column(DateTime)
    width = Column(Integer)
    height = Column(Integer)

    datetimecreated = Column(DateTime)
    datetimeaccessed = Column(DateTime)
    datetimemodified = Column(DateTime)

    phash = Column(String)
    phashrot90 = Column(String)
    phashrot180 = Column(String)
    phashrot270 = Column(String)
