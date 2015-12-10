from CsvManager import CsvManager
from ErrorLog import ErrorLog
from Progress import Progress
import pandas as pd
import numpy as np
import datetime
import threading

__author__ = 'marcio'


class Growth:
    def __init__(self, inputdata, outputdata, path, dt, qnt):
        self.error_log = ErrorLog(self.__class__.__name__)
        self.progress = Progress()
        self.path = path
        self.input = CsvManager.read(inputdata)
        self.output = outputdata
        self.dts = self.set_dts(dt, qnt)
        self.ts = []

    def get_bbls(self):
        bbls_temp = CsvManager.read(self.path)
        bbls = []
        for bbl in bbls_temp:
            bbls.append(int(bbl[0]))
        return bbls

    def binary_search(self, bbl, begin, end):
        if bbl < self.input[(end - begin)/2][0]:
            end = (end-begin)/2
            self.binary_search(bbl, begin, end)
        elif bbl > self.input[(end - begin)/2][0]:
            begin = (end - begin)/2
            self.binary_search(bbl, begin, end)
        elif bbl == self.input[(end - begin)/2][0]:
            return self.sequential_search(bbl, (end - begin) / 2)

    def sequential_search(self, bbl, index):
        while bbl == self.input[index][0]:
            index -= 1
        return index+1


    @staticmethod
    def set_dts(dt, qnt):
        dts = {}
        for i in xrange(qnt):
            sigma = i + 1
            sigma *= dt
            dts[sigma] = sigma
        return dts

    def make_time_series(self, bbl, sigma, index):
        ipt = self.input[self.ts[index]]
        while bbl == ipt[0]:
            self.ts[index] += 1

        series = []
        return series

    def mount_table(self, bbls, sigma, index):
        time_series = []
        self.ts[index] = len(self.input)-1
        self.ts[index] = self.binary_search(bbls[len(bbls)-1], 0, self.ts[index])
        while bbls:
            bbl = bbls.pop(0)
            time_series.append([bbl, self.make_time_series(bbl, sigma, index)])
        self.ts[index] = time_series

    def get_avg_ts(self, sigma, kernels):
        bbls = self.get_bbls()
        begin = 0
        end = len(bbls) / kernels
        t = []
        for i in xrange(kernels):
            self.ts.append([])
            bblsk = bbls[begin:end]
            t.append(threading.Thread(target=self.mount_table, args=(bblsk, sigma, i)))
            begin = end
            end += end
        for i in xrange(len(t)):
            t[i].start()
        for i in xrange(len(t)):
            t[i].join()

        time_series = self.ts[0] + self.ts[1] + self.ts[2]
        return time_series

    def growth(self, sigma):
        CsvManager.append(self.get_avg_ts(sigma), self.output)
