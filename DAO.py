from DataBase import DataBase
from MySql import MySql

__author__ = 'marcio'


class DAO:
    att = ("(id SERIAL PRIMARY KEY, "
           "bbl bigint(20), "
           "price FLOAT, qprice INTEGER, "
           "start_date TIME NULL, end_date TIME NULL, "
           "address TEXT)")

    def __init__(self, db_name):
        db = DataBase(db_name)
        self.sql = MySql(db)

    def do(self, arg):
        return self.sql.select(arg)

    def insert_many(self, values):
        ins = ('''INSERT INTO acris_a2k (bbl, price, qprice, start_date, end_date)
               VALUES ('%s', '%s', '%s', '%s', '%s')''')
        self.sql.insert_many(ins, values)

    def insert_many_gambiarra(self, table, list_):
        for t in list_:
            self.sql.select("INSERT INTO " + table +
                            "(bbl, price, qprice, start_date, end_date, address) "
                            "VALUES ('" + str(t[0]) + "', '" + str(t[1]) + "', '" + str(t[2]) + "',"
                            " '" + str(t[3]) + "', '" + str(t[4]) + "', '" + t[5] + "')")

    def insert(self, values):
        ins = "INSERT INTO acris_a2k (bbl, price, qprice, start_date, end_date) VALUES (%s, %s, %s, %s, %s)"
        self.sql.insert(ins, values)

    def insert2(self, values):
        ins = ("INSERT INTO acris_b2k (bbl, price, qprice, start_date, end_date) VALUES ("
               "'" + str(values[0]) + "', '" + str(values[1]) + "', '" + str(values[2]) + ""
               "', '" + str(values[3]) + "', '" + str(values[4]) + "')")
        self.sql.select(ins)

    def picky_select(self):
        tuples = self.do("SELECT bbl, price, start_date, end_date, address"
                         " FROM acris WHERE price >= 200000;")
        return tuples

    def picky_select_to_geocode(self):
        tuples = self.do("SELECT DISTINCT(bbl), address"
                         " FROM acris WHERE price >= 200000 "
                         "AND bbl LIKE '4_________';")
        return tuples
