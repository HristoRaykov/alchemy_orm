from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

from findata.entity.constants import FINDATA_SCHEMA
from findata.repository.connection import DbEngine

Base = declarative_base()
Base.metadata.schema = FINDATA_SCHEMA

db_engine = DbEngine()


class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    type = Column(String(50))
    
    __mapper_args__ = {
        'polymorphic_identity': 'employee',
        'polymorphic_on': type
    }


class Engineer(Employee):
    __tablename__ = 'engineer'
    id = Column(Integer, ForeignKey('employee.id'), primary_key=True)
    engineer_name = Column(String(30))
    
    __mapper_args__ = {
        'polymorphic_identity': 'engineer',
    }


class Manager(Employee):
    __tablename__ = 'manager'
    id = Column(Integer, ForeignKey('employee.id'), primary_key=True)
    manager_name = Column(String(30))
    
    __mapper_args__ = {
        'polymorphic_identity': 'manager',
    }


eng = Engineer(id=1, engineer_name='Engineer1')

Session = sessionmaker(bind=db_engine)
session = Session()

Base.metadata.create_all(db_engine)

session.add(eng)
session.commit()

# com_stock = session.query(ComStock).get(com_stk_symbol)

# session.delete(com_stock)
# session.delete(com_stock)

# session.commit()

session.close()
