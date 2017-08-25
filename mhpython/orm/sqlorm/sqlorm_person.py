from sqlalchemy import Column, ForeignKey, BigInteger, Integer, String, Date, REAL
from sqlalchemy.orm import relationship

from mhpython.orm.sqlorm import Base


class SQLORMPerson(Base):
    """
    An ORM person representation

    Note how the id column must be an Integer for SQLite's auto-increment to work
    """
    __tablename__ = "people"

    id = Column(BigInteger().with_variant(Integer, 'sqlite'), primary_key=True)
    givenname = Column(String)
    middleinitial = Column(String)
    surname = Column(String)
    streetaddress = Column(String)
    zipcode = Column(String)
    emailaddress = Column(String)
    username = Column(String)
    password = Column(String)
    telephonenumber = Column(String)
    maidenname = Column(String)
    birthday = Column(Date)
    ccnumber = Column(String)
    cvv2 = Column(String)
    ccexpires = Column(String)
    nationalid = Column(String)
    upstracking = Column(String)
    vehicle = Column(String)
    domain = Column(String)
    kilograms = Column(String)
    centimeters = Column(String)
    latitude = Column(REAL)
    longitude = Column(REAL)
    guid = Column(String)

    gender_id = Column(BigInteger().with_variant(Integer, 'sqlite'), ForeignKey('gender.id'))
    gender = relationship("SQLORMGender", back_populates="people")

    bloodtype_id = Column(BigInteger().with_variant(Integer, 'sqlite'), ForeignKey('bloodtype.id'))
    bloodtype = relationship("SQLORMBloodType", back_populates="people")

    title_id = Column(BigInteger().with_variant(Integer, 'sqlite'), ForeignKey('titles.id'))
    title = relationship("SQLORMTitle", back_populates="people")

    cctype_id = Column(BigInteger().with_variant(Integer, 'sqlite'), ForeignKey('cctype.id'))
    cctype = relationship("SQLORMCCType", back_populates="people")

    city_id = Column(BigInteger().with_variant(Integer, 'sqlite'), ForeignKey('city.id'))
    city = relationship("SQLORMCity", back_populates="people")

    company_id = Column(BigInteger().with_variant(Integer, 'sqlite'), ForeignKey('company.id'))
    company = relationship("SQLORMCompany", back_populates="people")

    occupation_id = Column(BigInteger().with_variant(Integer, 'sqlite'), ForeignKey('occupation.id'))
    occupation = relationship("SQLORMOccupation", back_populates="people")

    def __repr__(self):
        return "<SQLPerson(givenname='%s', middleinitial='%s', surname='%s')>" % \
               (self.givenname, self.middleinitial, self.surname)
