__author__ = 'marcio'


class DataBase:
    def __init__(self, name):
        self.db_name = name
        self.pswrd = None
        self.user = None
        self.host = None

    def set_user(self, user):
        self.user = user

    def set_host(self, host):
        self.host = host

    def set_pass(self, password):
        self.pswrd = password
