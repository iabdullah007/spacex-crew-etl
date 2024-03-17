from enum import Enum as PythonEnum
from typing import List, Optional

from pydantic import BaseModel, Field
from sqlalchemy import ARRAY, Column, create_engine, Enum, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class CrewStatus(PythonEnum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    RETIRED = 'retired'
    UNKNOWN = 'unknown'


class CrewSqlalchemyOrm(Base):
    """
    sqlalchemy model of Crew document
    """

    __tablename__ = 'crew'

    id = Column(String, nullable=False, primary_key=True)
    name = Column(String, nullable=True)
    status = Column(Enum(CrewStatus), nullable=False)
    agency = Column(String, nullable=True)
    wikipedia = Column(String, nullable=True)
    launches = Column(ARRAY(String), nullable=False)


class CrewModel(BaseModel):
    """
    Pydantic model of a crew for data validation
    """

    id: str = Field(description='The id of the crew member')
    name: Optional[str] = Field(description='The name of the crew member')
    status: CrewStatus = Field(description='Status of the crew')
    agency: Optional[str] = Field(description='Affiliated agency name', default=None)
    wikipedia: Optional[str] = Field(description='Wikipedia link to the crew bio', default=None)
    launches: List[str] = Field(description='List of launches the crew involved in')


def create_tables(connection_url: str):
    """
    Creates the DB tables corresponding to the ORM model.

    Args:
        connection_url: the URL to an SQL database.
    """
    engine = create_engine(connection_url, echo=True)
    Base.metadata.create_all(engine)
