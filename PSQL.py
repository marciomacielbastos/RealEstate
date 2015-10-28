from ConnectionFactory import ConnectionFactory
import psycopg2
import psycopg2.extensions
from ErrorLog import ErrorLog
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
__author__ = 'marcio'


class PSQL:
    def __init__(self, database):
        self.connection = None
        self.db = database
        self.sgbd = None
        self.dbAtrib = None
        self.settings()
        self.error_log = ErrorLog(self.__class__.__name__)
        self.cursor = self.get_connection().cursor()

    def settings(self):
        try:
            self.db.db_name = "nycgisdb"
            self.db.user = "marcio"
            self.db.host = "localhost"
            self.db.pswrd = "m2a3rcio"
            self.sgbd = psycopg2
            self.dbAtrib = ("dbname='" + self.db.db_name + "' user='" + self.db.user + "' host='"
                            + self.db.host + "' password='" + self.db.pswrd + "'")
        except TypeError as e:
            print e.message

    def select(self, arg):
        self.cursor.execute(arg)
        self.connection.commit()
        return self.cursor.fetchall()

    def get_connection(self):
        try:
            self.connection = self.sgbd.connect(self.dbAtrib)
            return self.connection
        except Exception as e:
            self.error_log.open()
            self.error_log.write(e.message)
            self.error_log.close()
