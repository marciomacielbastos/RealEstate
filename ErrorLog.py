# -*- coding: utf-8 -*-
import datetime

__author__ = 'marcio'


class ErrorLog:
    def __init__(self, name):
        self.name = name
        self.key = False
        self.file = None
        self.order = 1
        self.create_file()

    def create_file(self):
        try:
            self.file = open(self.name+'_log', 'w+')
            self.file.write(str(datetime.datetime.now())+'\n')
            self.key = True
            self.close()
        except IOError as e:
            print e.args

    def open(self):
        try:
            self.file = open(self.name+'_log', 'a+')
            self.file.write(str(datetime.datetime.now())+'\n')
            self.key = True
        except IOError as e:
            print e.args

    def write(self, string):
        try:
            if self.key:
                msg = str(self.order)+u' '+string+'\n'
                self.file.write(msg.encode('utf8'))
                self.order += 1
        except IOError as e:
            print e.args
        except UnicodeDecodeError as e:
            pass

    def close(self):
        try:
            if self.key:
                self.file.close()
                self.key = False
        except IOError as e:
            print e.args