import logging

import pandas as pd
from sqlalchemy.orm import sessionmaker

from findata.entity.polimorphic import Equity, Base, ComStock, Cef, HistPrice
from findata.repository.connection import DbEngine

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


db_engine = DbEngine()

Session = sessionmaker(bind=db_engine)
session = Session()

# equity_symbol = 'TSLA'
# equity = Equity(symbol=equity_symbol, type='equity')
# hist_price_equity1 = HistPrice(symbol=equity_symbol, date=pd.to_datetime('2021-10-4'), close=684.55)
# hist_price_equity2 = HistPrice(symbol=equity_symbol, date=pd.to_datetime('2021-10-1'), close=668.56)
# equity.hist_prices = [hist_price_equity1, hist_price_equity2]

com_stk_symbol = 'BAC'
com_stk = ComStock(symbol=com_stk_symbol, type='com_stk')
hist_price_com_stk1 = HistPrice(symbol=com_stk_symbol, date=pd.to_datetime('2021-10-4'), close=45.55)
hist_price_com_stk2 = HistPrice(symbol=com_stk_symbol, date=pd.to_datetime('2021-10-1'), close=43.56)
com_stk.hist_prices = [hist_price_com_stk1, hist_price_com_stk2]

cef_symbol = 'BST'
cef = Cef(symbol=cef_symbol, type='cef')
hist_price1 = HistPrice(symbol=cef_symbol, date=pd.to_datetime('2021-10-4'), close=49.55)
hist_price2 = HistPrice(symbol=cef_symbol, date=pd.to_datetime('2021-10-1'), close=48.56)
cef.hist_prices = [hist_price1, hist_price2]


Base.metadata.create_all(db_engine)


session.add(com_stk)
session.add(cef)
session.commit()


equities = session.query(Equity).all()
com_stocks = session.query(ComStock).all()
cefs = session.query(Cef).all()

session.delete(com_stocks[0])
session.delete(cefs[0])


session.commit()

session.close()
