from collections import Iterable

from sqlalchemy import Column, VARCHAR, TIMESTAMP, FLOAT, PrimaryKeyConstraint, Index, ForeignKey, ForeignKeyConstraint, \
    Table
from sqlalchemy.ext.declarative import ConcreteBase, AbstractConcreteBase
from sqlalchemy.orm import declarative_base, declarative_mixin, declared_attr, relationship, backref
from sqlalchemy.orm.collections import attribute_mapped_collection

from findata.entity.constants import SYMBOL_COL, DATE_COL, CLOSE_PRICE_COL, FINDATA_SCHEMA, HIST_PRICES_TABLE, \
    DEBT_SECS_TABLE, COM_STOCKS_TABLE
from utils import generate_hist_price_join_table

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


debt_sec_hist_prices_ass_table = generate_hist_price_join_table(DEBT_SECS_TABLE, SYMBOL_COL, Base.metadata)


class DebtSec(Base):
    __tablename__ = 'debtsec'  # DEBT_SECS_TABLE
    
    symbol = Column(SYMBOL_COL, VARCHAR, primary_key=True)
    hist_prices = relationship(HistPrice,
                               secondary=debt_sec_hist_prices_ass_table,
                               single_parent=True,
                               cascade='all, delete-orphan')


com_stk_hist_prices_ass_table = generate_hist_price_join_table(COM_STOCKS_TABLE, SYMBOL_COL, Base.metadata)


class ComStock(Base):
    __tablename__ = 'comstk'
    
    symbol = Column(SYMBOL_COL, VARCHAR, primary_key=True)
    hist_prices = relationship(HistPrice,
                               secondary=com_stk_hist_prices_ass_table,
                               single_parent=True,
                               # foreign_keys=HistPrice.symbol,
                               cascade='all, delete-orphan')
