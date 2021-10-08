from collections import Iterable

from sqlalchemy import Column, VARCHAR, TIMESTAMP, FLOAT, PrimaryKeyConstraint, Index, ForeignKey, ForeignKeyConstraint, \
    Table
from sqlalchemy.ext.declarative import ConcreteBase, AbstractConcreteBase
from sqlalchemy.orm import declarative_base, declarative_mixin, declared_attr, relationship, backref
from sqlalchemy.orm.collections import attribute_mapped_collection

from findata.entity.constants import SYMBOL_COL, DATE_COL, CLOSE_PRICE_COL, FINDATA_SCHEMA, HIST_PRICES_TABLE, \
    DEBT_SECS_TABLE, COM_STOCKS_TABLE, EQUITIES_TABLE, CEFS_TABLE
from utils import generate_hist_price_join_table

Base = declarative_base()
Base.metadata.schema = FINDATA_SCHEMA


class Identifiable:
    symbol = Column(SYMBOL_COL, VARCHAR)
    type = Column(SYMBOL_COL, VARCHAR)


class Dated:
    date = Column(DATE_COL, TIMESTAMP)


class HistPriceId(Identifiable, Dated):
    PrimaryKeyConstraint(SYMBOL_COL, DATE_COL),


class HistPrice(HistPriceId, Base):
    __tablename__ = HIST_PRICES_TABLE
    __table_args__ = (
        PrimaryKeyConstraint(SYMBOL_COL, DATE_COL),
    )
    
    close = Column(CLOSE_PRICE_COL, FLOAT)


class Security(Identifiable):
    hist_prices = None

debt_sec_hist_prices_ass_table = generate_hist_price_join_table(DEBT_SECS_TABLE, SYMBOL_COL, Base.metadata)


class FixedIncome(Identifiable):
    issuer = None


class DebtSec(FixedIncome, Base):
    __tablename__ = DEBT_SECS_TABLE
    __table_args__ = (
        PrimaryKeyConstraint(SYMBOL_COL),
    )
    
    hist_prices = relationship(HistPrice,
                               secondary=debt_sec_hist_prices_ass_table,
                               single_parent=True,
                               cascade='all, delete-orphan')


class Bond(FixedIncome):
    pass

class Equity(Identifiable, Base):
    __tablename__ = EQUITIES_TABLE
    
    __table_args__ = (
        PrimaryKeyConstraint(SYMBOL_COL),
    )
    
    debt_secs = None
    bonds = None
    # hist_prices = relationship(HistPrice,
    #                            secondary=,
    #                            single_parent=True,
    #                            cascade='all, delete-orphan')


com_stk_hist_prices_ass_table = generate_hist_price_join_table(COM_STOCKS_TABLE, SYMBOL_COL, Base.metadata)


class ComStock(Equity, Base):
    __tablename__ = COM_STOCKS_TABLE
    __table_args__ = (
        PrimaryKeyConstraint(SYMBOL_COL),
    )
    
    hist_prices = relationship(HistPrice,
                               secondary=com_stk_hist_prices_ass_table,
                               single_parent=True,
                               cascade='all, delete-orphan')


class Cef(Equity, Base):
    __tablename__ = CEFS_TABLE
    __table_args__ = (
        PrimaryKeyConstraint(SYMBOL_COL),
    )
    
    # hist_prices = relationship(HistPrice,
    #                            secondary=,
    #                            single_parent=True,
    #                            cascade='all, delete-orphan')


@declarative_mixin
class RefTargetMixin:
    @declared_attr
    def target_id(cls):
        return Column('target_id', ForeignKey('target.id'))
    
    @declared_attr
    def target(cls):
        return relationship("Target")


class Foo(RefTargetMixin, Base):
    __tablename__ = 'foo'
    id = Column(Integer, primary_key=True)
    foo = Column(VARCHAR)


class Bar(RefTargetMixin, Base):
    __tablename__ = 'bar'
    id = Column(Integer, primary_key=True)
    bar = Column(VARCHAR)


class Target(Base):
    __tablename__ = 'target'
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR)