import sys

__author__ = 'marcio'


class Progress:
    def __init__(self):
        self.size = 0

    def set_progress(self, val):
        sys.stdout.flush()
        sys.stdout.write("\r%d%%" % (int(val) / int(self.size)))
        sys.stdout.flush()

    def set_size(self, num):
        self.size = num

    @staticmethod
    def flush():
        sys.stdout.flush()
