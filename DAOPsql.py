from DataBase import DataBase
from PSQL import PSQL

__author__ = 'marcio'


class DAOPsql:
    att = ("(id SERIAL PRIMARY KEY, "
           "bbl bigint(20), "
           "price FLOAT, qprice INTEGER, "
           "start_date TIME NULL, end_date TIME NULL, "
           "address TEXT)")

    def __init__(self, db_name):
        db = DataBase(db_name)
        self.sql = PSQL(db)

    def do(self, arg):
        return self.sql.select(arg)

