import os

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


class DbEngine(Engine):
    PORT = os.environ["PSQL_PORT"]
    _USERNAME = os.environ["PSQL_USER"]
    _PASSWORD = os.environ["PSQL_PASS"]
    IP_ADDRESS = "localhost"  # os.environ["SERVER_IP"]
    DBNAME = 'findata'  # todo os.environ["FINDATA_DB"]
    
    CONN_STR = 'postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}?gssencmode=disable'.format(
        username=_USERNAME,
        password=_PASSWORD,
        ipaddress=IP_ADDRESS,
        port=PORT,
        dbname=DBNAME)
    
    def __init__(self):
        engine = create_engine(DbEngine.CONN_STR, echo=True, future=True)
        super().__init__(engine.pool, engine.dialect, engine.url)
