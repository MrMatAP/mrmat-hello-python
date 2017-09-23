from sqlalchemy import Column, ForeignKey, BigInteger, Integer, String, Date, REAL
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound

from mhpython.orm.sqlorm import Base, SQLORMGender, SQLORMBloodType, SQLORMCCType, SQLORMCity, SQLORMCompany, \
    SQLORMOccupation
from .sqlorm_title import SQLORMTitle


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
    gender_rel = relationship("SQLORMGender", back_populates="people_rel")

    def gender(self, session, name):
        if name is None:
            return None if self.gender_rel is None else self.gender_rel.name
        try:
            self.gender_rel = session.query(SQLORMGender).filter(SQLORMGender.name.is_(name)).one()
        except NoResultFound:
            self.gender_rel = SQLORMGender(name)

    bloodtype_id = Column(BigInteger().with_variant(Integer, 'sqlite'), ForeignKey('bloodtype.id'))
    bloodtype_rel = relationship("SQLORMBloodType", back_populates="people_rel")

    def bloodtype(self, session, name):
        if name is None:
            return None if self.bloodtype_rel is None else self.bloodtype_rel.name
        try:
            self.bloodtype_rel = session.query(SQLORMBloodType).filter(SQLORMBloodType.name.is_(name)).one()
        except NoResultFound:
            self.bloodtype_rel = SQLORMBloodType(name)

    title_id = Column(BigInteger().with_variant(Integer, 'sqlite'), ForeignKey('title.id'))
    title_rel = relationship("SQLORMTitle", back_populates="people_rel")

    def title(self, session, name):
        if name is None:
            return None if self.title_rel is None else self.title_rel.name
        try:
            self.title_rel = session.query(SQLORMTitle).filter(SQLORMTitle.name.is_(name)).one()
        except NoResultFound:
            self.title_rel = SQLORMTitle(name)

    cctype_id = Column(BigInteger().with_variant(Integer, 'sqlite'), ForeignKey('cctype.id'))
    cctype_rel = relationship("SQLORMCCType", back_populates="people_rel")

    def cctype(self, session, name):
        if name is None:
            return None if self.cctype_rel is None else self.cctype_rel.name
        try:
            self.cctype_rel = session.query(SQLORMCCType).filter(SQLORMCCType.name.is_(name)).one()
        except NoResultFound:
            self.cctype_rel = SQLORMCCType(name)

    city_id = Column(BigInteger().with_variant(Integer, 'sqlite'), ForeignKey('city.id'))
    city_rel = relationship("SQLORMCity", back_populates="people")

    def city(self, session, name, state, country, code):
        if name is None:
            return None if self.city_rel is None else self.city_rel.name
        try:
            self.city_rel = session.query(SQLORMCity).filter(SQLORMCity.name.is_(name)).one()
        except NoResultFound:
            self.city_rel = SQLORMCity(session, name, state, country, code)

    company_id = Column(BigInteger().with_variant(Integer, 'sqlite'), ForeignKey('company.id'))
    company_rel = relationship("SQLORMCompany", back_populates="people_rel")

    def company(self, session, name):
        if name is None:
            return None if self.company_rel is None else self.company_rel.name
        try:
            self.company_rel = session.query(SQLORMCompany).filter(SQLORMCompany.name.is_(name)).one()
        except NoResultFound:
            self.company_rel = SQLORMCompany(name)

    occupation_id = Column(BigInteger().with_variant(Integer, 'sqlite'), ForeignKey('occupation.id'))
    occupation_rel = relationship("SQLORMOccupation", back_populates="people_rel")

    def occupation(self, session, name):
        if name is None:
            return None if self.occupation_rel is None else self.occupation_rel.name
        try:
            self.occupation_rel = session.query(SQLORMOccupation).filter(SQLORMOccupation.name.is_(name)).one()
        except NoResultFound:
            self.occupation_rel = SQLORMOccupation(name)

    def __repr__(self):
        return "<SQLPerson(givenname='%s', middleinitial='%s', surname='%s')>" % \
               (self.givenname, self.middleinitial, self.surname)
