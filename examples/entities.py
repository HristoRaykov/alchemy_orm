from sqlalchemy import Column, VARCHAR, TIMESTAMP, FLOAT, PrimaryKeyConstraint, ForeignKeyConstraint, ForeignKey, \
    Integer, Table
from sqlalchemy.orm import declarative_base, relationship, declared_attr, declarative_mixin

from constants import *
from utils import get_sql_str

Base = declarative_base()
Base.metadata.schema = FINDATA_SCHEMA


# class Identifiable:
#     symbol = Column(SYMBOL_COL, VARCHAR)
#     type = Column(SYMBOL_COL, VARCHAR)
#
#
# class Dated:
#     date = Column(DATE_COL, TIMESTAMP)
#
#
# class HistPriceId(Identifiable, Dated):
#     PrimaryKeyConstraint(SYMBOL_COL, DATE_COL),


class HistPrice(Base):
    __tablename__ = HIST_PRICES_TABLE
    __table_args__ = (
        PrimaryKeyConstraint(SYMBOL_COL, DATE_COL),
    )
    
    symbol = Column(SYMBOL_COL, VARCHAR)
    date = Column(DATE_COL, TIMESTAMP)
    close = Column(CLOSE_PRICE_COL, FLOAT)
    
    # @declared_attr
    # def __table_args__(cls):
    #     args = dict()
    #     args.update(MySQLSettings.__table_args__)
    #     args.update(MyOtherMixin.__table_args__)
    #     return args


class HasHistPrices(object):
    
    @declared_attr
    def hist_prices(cls):
        hist_price_association = Table(
            '%s_%s' % (cls.__tablename__[:-1], HistPrice.__tablename__),
            cls.metadata,
            Column('%s_%s'% (HistPrice.__tablename__[:-1], SYMBOL_COL), ForeignKey("address.id"), primary_key=True), # todo
            Column(
                "%s_symbol" % cls.__tablename__,
                ForeignKey("%s.symbol" % cls.__tablename__),
                primary_key=True,
            ),
        )
        return relationship(Address, secondary=address_association)

"%s_%s" % ('hist_price', 'symbol')

class Security(Base):
    # __abstract__ = True
    __tablename__ = SECURITIES_TABLE
    
    @declared_attr.cascading
    def symbol(cls):
        return Column(SYMBOL_COL, VARCHAR, primary_key=True)
    
    @declared_attr  # .cascading
    def type(cls):
        return Column(TYPE_COL, VARCHAR)


class Equity(Security):
    # __tablename__ = EQUITIES_TABLE
    __abstract__ = True
    
    @declared_attr
    def symbol(cls):
        return Column(SYMBOL_COL, VARCHAR, primary_key=True)
    
    # @declared_attr
    # def hist_prices(cls):
    #     return relationship(HistPrice, cascade='all, delete-orphan')
    
    @declared_attr
    def __mapper_args__(cls):
        return {
            'polymorphic_identity': 'security',
            'polymorphic_on': 'type'
        }


class ComStock(Equity):
    __tablename__ = COM_STOCKS_TABLE
    __table_args__ = (
        # PrimaryKeyConstraint(SYMBOL_COL),
        # ForeignKeyConstraint([SYMBOL_COL], [get_sql_str([SECURITIES_TABLE, SYMBOL_COL])], ondelete='CASCADE'),
    )
    
    # symbol = Column(SYMBOL_COL, VARCHAR, primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'com_stk',
    }


class Cef(Equity):
    __tablename__ = CEFS_TABLE
    __table_args__ = (
        # PrimaryKeyConstraint(SYMBOL_COL),
        ForeignKeyConstraint([SYMBOL_COL], [get_sql_str([SECURITIES_TABLE, SYMBOL_COL])], ondelete='CASCADE'),
    )
    
    # symbol = Column(SYMBOL_COL, VARCHAR, primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'cef',
    }

# class FixedIncome(Security):
#     __tablename__ = 'fixed_income'
#     __table_args__ = (
#         PrimaryKeyConstraint(SYMBOL_COL),
#         ForeignKeyConstraint([SYMBOL_COL], [get_sql_str([SECURITIES_TABLE, SYMBOL_COL])], ondelete='CASCADE')
#     )
#     __mapper_args__ = {
#         'polymorphic_identity': 'fixed_income',
#     }
# issuer = None


# class DebtSec(FixedIncome):
#     __tablename__ = DEBT_SECS_TABLE
#     __table_args__ = (
#         PrimaryKeyConstraint(SYMBOL_COL),
#         # ForeignKeyConstraint([SYMBOL_COL], [get_sql_str([EQUITIES_TABLE, SYMBOL_COL])], ondelete='CASCADE')
#     )


# class Bond(FixedIncome):
#     pass
