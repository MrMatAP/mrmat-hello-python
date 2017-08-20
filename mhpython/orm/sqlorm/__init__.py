from .sqlorm_base import Base
from .sqlorm_bloodtype import SQLORMBloodType
from .sqlorm_cctype import SQLORMCCType
from .sqlorm_city import SQLORMCity
from .sqlorm_company import SQLORMCompany
from .sqlorm_country import SQLORMCountry
from .sqlorm_gender import SQLORMGender
from .sqlorm_occupation import SQLORMOccupation
from .sqlorm_person import SQLORMPerson
from .sqlorm_title import SQLORMTitle

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class SQLORMDao:
    engine = None
    session = None

    def __init__(self, conn_string):
        self.engine = create_engine(conn_string)
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)
