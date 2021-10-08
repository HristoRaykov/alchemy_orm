from collections import Iterable

from sqlalchemy import Column, VARCHAR, TIMESTAMP, FLOAT, PrimaryKeyConstraint, Index, ForeignKey, ForeignKeyConstraint
from sqlalchemy.ext.declarative import ConcreteBase, AbstractConcreteBase
from sqlalchemy.orm import declarative_base, declarative_mixin, declared_attr, relationship, backref
from sqlalchemy.orm.collections import attribute_mapped_collection

from findata.entity.constants import SYMBOL_COL, DATE_COL, CLOSE_PRICE_COL, FINDATA_SCHEMA, HIST_PRICES_TABLE, \
    DEBT_SECS_TABLE

Base = declarative_base()
Base.metadata.schema = FINDATA_SCHEMA


def get_sql_str(names: list):
    sql_str = '.'.join(names)
    
    return sql_str


class HistPrice(Base):
    __tablename__ = 'histprice'
    
    symbol = Column(SYMBOL_COL, VARCHAR, primary_key=True)
    date = Column(DATE_COL, TIMESTAMP, primary_key=True)
    close = Column(CLOSE_PRICE_COL, FLOAT)


class DebtSec(Base):
    __tablename__ = 'debtsec'  # DEBT_SECS_TABLE
    
    symbol = Column(SYMBOL_COL, VARCHAR, primary_key=True)
    hist_prices = relationship(HistPrice,
                               # back_populates=HistPrice,
                               # backref='histprice',
                               foreign_keys=HistPrice.symbol,
                               primaryjoin=lambda: DebtSec.symbol == HistPrice.symbol,
                               cascade='all, delete-orphan')


class ComStock(Base):
    __tablename__ = 'comstk'  # DEBT_SECS_TABLE
    
    symbol = Column(SYMBOL_COL, VARCHAR, primary_key=True)
    hist_prices = relationship(HistPrice,
                               # back_populates=HistPrice,
                               # backref='histprice',
                               foreign_keys=HistPrice.symbol,
                               primaryjoin=lambda: ComStock.symbol == HistPrice.symbol,
                               cascade='all, delete-orphan')
