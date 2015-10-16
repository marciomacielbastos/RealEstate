from _mysql import MySQLError
import MySQLdb
from ConnectionFactory import ConnectionFactory

__author__ = 'marcio'


class MySql(ConnectionFactory):
    def settings(self):
        try:
            self.db.user = "marcio"
            self.db.pswrd = "PUT YOUR PSWRD"
            self.sgbd = MySQLdb

        except TypeError as e:
            print e.message

    def select(self, arg):
        self.cursor.execute(arg)
        self.connection.commit()
        return self.cursor.fetchall()

    def insert(self, arg, arg2):
        self.cursor.execute(arg, arg2)
        self.connection.commit()

    def insert_many(self, arg, arg2):
        self.cursor.executemany(arg, arg2)
        self.connection.commit()
