from ErrorLog import ErrorLog

__author__ = 'marcio'


class ConnectionFactory:
    def __init__(self, database):
        self.connection = None
        self.db = database
        self.sgbd = None
        self.dbAtrib = None
        self.settings()
        self.error_log = ErrorLog(self.__class__.__name__)
        self.cursor = self.get_connection().cursor()

    def get_connection(self):
        try:
            self.connection = self.sgbd.connect(user=self.db.user, passwd=self.db.pswrd, db=self.db.db_name)
            return self.connection
        except Exception as e:
            self.close()
            self.error_log.open()
            self.error_log.write(e.message)
            self.error_log.close()

    def close(self):
        self.connection.close()

    def settings(self):
        pass
