import logging

import pandas as pd
from sqlalchemy.orm import sessionmaker

from findata.entity.entities import Base, ComStock, HistPrice, Cef
from findata.repository.connection import DbEngine

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

db_engine = DbEngine()

Session = sessionmaker(bind=db_engine)
session = Session()

# debt_sec_symbol = 'bac-pp'
# debt_sec = DebtSec(symbol=debt_sec_symbol, type='debt_sec')
# debt_sec_hist_price1 = HistPrice(symbol=debt_sec_symbol, date=pd.to_datetime('2021-10-4'), close=25.55)
# debt_sec_hist_price2 = HistPrice(symbol=debt_sec_symbol, date=pd.to_datetime('2021-10-1'), close=25.56)
# debt_sec.hist_prices = [debt_sec_hist_price1, debt_sec_hist_price2]

com_stk_symbol = 'BAC'
com_stk = ComStock(symbol=com_stk_symbol, type='com_stk')
hist_price_com_stk1 = HistPrice(symbol=com_stk_symbol, date=pd.to_datetime('2021-10-4'), close=45.55)
hist_price_com_stk2 = HistPrice(symbol=com_stk_symbol, date=pd.to_datetime('2021-10-1'), close=43.56)
com_stk.hist_prices = [hist_price_com_stk1, hist_price_com_stk2]

cef_symbol = 'BST'
cef = Cef(symbol=cef_symbol, type='cef')
cef_hist_price1 = HistPrice(symbol=cef_symbol, date=pd.to_datetime('2021-10-4'), close=49.55)
cef_hist_price2 = HistPrice(symbol=cef_symbol, date=pd.to_datetime('2021-10-1'), close=48.56)
cef.hist_prices = [cef_hist_price1, cef_hist_price2]

Base.metadata.create_all(db_engine)

# session.add(debt_sec)
session.add(com_stk)
session.add(cef)
session.commit()


# debt_sec = session.query(DebtSec).get(debt_sec)
com_stk = session.query(ComStock).get(com_stk_symbol)
cef = session.query(Cef).get(cef)

# session.delete(debt_sec)
# session.delete(com_stock)

session.commit()

session.close()
