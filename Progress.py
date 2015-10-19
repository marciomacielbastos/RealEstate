__author__ = 'marcio'

import sys

class Progress:
    def __init__(self, size):
        self.size = size

    def progress(self, val):
        sys.stdout.flush()
        sys.stdout.write("\r%d%%" % (int(val)/ int(self.size)))
        sys.stdout.flush()