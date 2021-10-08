from sqlalchemy import Table, Column, ForeignKeyConstraint, TIMESTAMP, VARCHAR

from constants import *


def get_sql_str(names: list):
    sql_str = '.'.join(names)
    
    return sql_str


def get_join_col_name(ref_table, ref_key):
    name = '{}_{}'.format(ref_table[:-1], ref_key)
    return name


def generate_hist_price_join_table(ref_table, ref_key, meta):
    join_tbl_name = '{}_{}_ass'.format(ref_table[:-1], HIST_PRICES_TABLE)
    ref_table_col = get_join_col_name(ref_table, ref_key)
    hist_price_symbol_col = get_join_col_name(HIST_PRICES_TABLE, SYMBOL_COL)
    hist_price_date_col = get_join_col_name(HIST_PRICES_TABLE, DATE_COL)
    join_tbl = Table(join_tbl_name, meta,
                     Column(ref_table_col, VARCHAR, primary_key=True),
                     Column(hist_price_symbol_col, VARCHAR, primary_key=True),
                     Column(hist_price_date_col, TIMESTAMP, primary_key=True),
                     ForeignKeyConstraint([ref_table_col], [get_sql_str([ref_table, SYMBOL_COL])]),
                     ForeignKeyConstraint([hist_price_symbol_col, hist_price_date_col],
                                          [get_sql_str([HIST_PRICES_TABLE, SYMBOL_COL]),
                                           get_sql_str([HIST_PRICES_TABLE, DATE_COL])])
                     )
    return join_tbl