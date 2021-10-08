from findata.entity.constants import SYMBOL_COL, DATE_COL, CLOSE_PRICE_COL, FINDATA_SCHEMA
from sqlalchemy import Column, VARCHAR, TIMESTAMP, FLOAT, PrimaryKeyConstraint, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import declarative_base, declarative_mixin, declared_attr, relationship

Base = declarative_base()
Base.metadata.schema = FINDATA_SCHEMA


def get_sql_str(names: list):
    sql_str = '.'.join(names)
    
    return sql_str


@declarative_mixin
class IdentifiableMixin(object):
    
    @declared_attr.cascading
    def __tablename__(cls):
        return cls.__tablename__
    
    __mapper_args__ = {'always_refresh': True}
    
    # symbol = Column(SYMBOL_COL, VARCHAR)
    @declared_attr.cascading
    def symbol(cls):
        return Column(SYMBOL_COL, VARCHAR)
    
    # __mapper_args__ = {'polymorphic_identity': 'engineer'}
    
    # @declared_attr
    # def __mapper_args__(cls):
    #     if cls.__name__ == 'Employee':
    #         return {
    #             "polymorphic_on":cls.type,
    #             "polymorphic_identity":"Employee"
    #         }
    #     else:
    #         return {"polymorphic_identity":cls.__name__}


@declarative_mixin
class DatedMixin(object):
    
    @declared_attr.cascading
    def __tablename__(cls):
        return cls.__tablename__
    
    __mapper_args__ = {'always_refresh': True}
    
    # date = Column(DATE_COL, TIMESTAMP)
    @declared_attr.cascading
    def date(cls):
        return Column(DATE_COL, TIMESTAMP)


@declarative_mixin
class HistPriceMixin(IdentifiableMixin, DatedMixin):
    
    @declared_attr
    def __tablename__(cls):
        return cls.__tablename__
    
    # close = Column(CLOSE_PRICE_COL, FLOAT)
    @declared_attr.cascading
    def close(cls):
        return Column(CLOSE_PRICE_COL, FLOAT)


# , IdentifiableMixin, DatedMixin
class HistPrice(Base, HistPriceMixin):
    __tablename__ = 'histprice'
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
    
    symbol = Column(SYMBOL_COL, VARCHAR, ForeignKey('tradable.symbol'), primary_key=True)
    date = Column(DATE_COL, TIMESTAMP, primary_key=True)
    # high = None
    # low = None
    # open = None
    # volume = None
    # div_cash = None
    # split_factor = None
    # @declared_attr
    # def __table_args__(cls):
    #     return (PrimaryKeyConstraint(SYMBOL_COL, DATE_COL),
    #             ForeignKeyConstraint([SYMBOL_COL], [get_sql_str([cls.__tablename__, SYMBOL_COL])], ondelete='CASCADE'),
    #             {})
    __table_args__ = (
        PrimaryKeyConstraint(SYMBOL_COL, DATE_COL),
        ForeignKeyConstraint(['symbol'], ['tradable.symbol'], ondelete='CASCADE')
    )


# @declarative_mixin
class Tradable(Base): #, IdentifiableMixin
    __tablename__ = 'tradable'
    # __table_args__ = (
    #     PrimaryKeyConstraint(SYMBOL_COL),
    # )
    
    # @declared_attr
    # def __tablename__(cls):
    #     return cls.__tablename__
    
    # __table_args__ = (
    #     PrimaryKeyConstraint(IdentifiableMixin.symbol),
    # )
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
    symbol = Column(SYMBOL_COL, VARCHAR, primary_key=True)
    hist_prices = relationship(HistPrice,  cascade='all, delete-orphan') # backref='histprice',
    # @declared_attr.cascading
    # def hist_prices(cls):
    #     return relationship(HistPrice,
    #                         # backref=HistPrice,
    #                         # collection_class=attribute_mapped_collection('symbol'),
    #                         # secondary=followers,
    #                         # primaryjoin=lambda: HistPrice.symbol == cls.symbol,
    #                         # cascade='all, delete-orphan'
    #                         )
    
    # @declared_attr.cascading
    # def __table_args__(cls):
    #     return (PrimaryKeyConstraint(SYMBOL_COL), {})
    # __mapper_args__ = {
    #     'polymorphic_identity': 'tradable',
    #     'polymorphic_on': 'symbol'
    # }


# class DebtSecHistPrices(Base):
#     __tablename__ = 'debtsechistprices'
#     debt_sec = Column(ForeignKey('debtsec.symbol'), primary_key=True)
#     hist_price_debt_sec_symbol = Column(ForeignKey('histprice.symbol'), primary_key=True)
#     hist_price_debt_sec_date = Column(ForeignKey('histprice.date'), primary_key=True)
#     debt_sec_hist_price = relationship('debtsec', back="association")


# class DebtSec(Tradable):
#     __tablename__ = 'debtsec'  # DEBT_SECS_TABLE
#
#     # def __init__(self, **kwargs) -> None:
#     #     super().__init__(**kwargs)
#
#     __table_args__ = (
#         PrimaryKeyConstraint(SYMBOL_COL),
#     )
    # @declared_attr
    # def __table_args__(cls):
    #     args = dict()
    #     x = Tradable.__table_args__
    #     args.update(Tradable.__table_args__)
    #     return args
    
    # __mapper_args__ = {
    #     'polymorphic_identity': 'debtsec',
    #     "concrete": True
    # }

# https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#association-pattern
