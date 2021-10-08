from sqlalchemy import Column, VARCHAR, TIMESTAMP, FLOAT, PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.orm import declarative_base, relationship, declared_attr

from findata.entity.constants import SYMBOL_COL, DATE_COL, CLOSE_PRICE_COL, FINDATA_SCHEMA, HIST_PRICES_TABLE, \
    EQUITIES_TABLE, TYPE_COL, COM_STOCKS_TABLE, CEFS_TABLE, SECURITIES_TABLE
from utils import get_sql_str

Base = declarative_base()
Base.metadata.schema = FINDATA_SCHEMA


# class Identifiable:
#
#     @declared_attr.cascading
#     def symbol(cls):
#         return Column(SYMBOL_COL, VARCHAR)
#
#
# class Dated:
#     date = Column(DATE_COL, TIMESTAMP)
#
#
# class HistPriceId(Identifiable, Dated):
#     PrimaryKeyConstraint(SYMBOL_COL, DATE_COL),
#
#
class HistPrice(Base):  # HistPriceId,
    __tablename__ = HIST_PRICES_TABLE
    __table_args__ = (
        PrimaryKeyConstraint(SYMBOL_COL, DATE_COL),
        ForeignKeyConstraint([SYMBOL_COL], [get_sql_str([EQUITIES_TABLE, SYMBOL_COL])], ondelete='CASCADE'),

    )
    symbol = Column(SYMBOL_COL, VARCHAR)
    date = Column(DATE_COL, TIMESTAMP)
    close = Column(CLOSE_PRICE_COL, FLOAT)


class Security(Base):
    __tablename__ = SECURITIES_TABLE
    __table_args__ = (
        PrimaryKeyConstraint(SYMBOL_COL),
    )
    
    symbol = Column(SYMBOL_COL, VARCHAR)
    type = Column(SYMBOL_COL, VARCHAR)
    hist_prices = relationship(HistPrice, cascade='all, delete-orphan')
    
    # __mapper_args__ = {
    #     'polymorphic_identity': '',
    #     'polymorphic_on': type
    # }


class Equity(Security):  # Identifiable,
    __tablename__ = EQUITIES_TABLE
    
    __table_args__ = (
        PrimaryKeyConstraint(SYMBOL_COL),
    )

    symbol = Column(SYMBOL_COL, VARCHAR)
    type = Column(TYPE_COL, VARCHAR)
    hist_prices = relationship(HistPrice, cascade='all, delete-orphan')
    
    __mapper_args__ = {
        'polymorphic_identity': 'equity',
        'polymorphic_on': type
    }


class ComStock(Equity):
    __tablename__ = COM_STOCKS_TABLE
    __table_args__ = (
        PrimaryKeyConstraint(SYMBOL_COL),
        ForeignKeyConstraint([SYMBOL_COL], [get_sql_str([EQUITIES_TABLE, SYMBOL_COL])], ondelete='CASCADE')
    )

    symbol = Column(SYMBOL_COL, VARCHAR)

    __mapper_args__ = {
        'polymorphic_identity': 'com_stk',
    }


class Cef(Equity):
    __tablename__ = CEFS_TABLE
    __table_args__ = (
        PrimaryKeyConstraint(SYMBOL_COL),
        ForeignKeyConstraint([SYMBOL_COL], [get_sql_str([EQUITIES_TABLE, SYMBOL_COL])], ondelete='CASCADE')
    )

    symbol = Column(SYMBOL_COL, VARCHAR)
    
    __mapper_args__ = {
        'polymorphic_identity': 'cef',
    }
