from CsvManager import CsvManager
from ErrorLog import ErrorLog
from Progress import Progress
import numpy as np
import datetime
import threading

__author__ = 'marcio'


class Growth:
    def __init__(self, inputdata, outputdata, path):
        self.path = path
        self.input = CsvManager.read(inputdata)
        self.output = outputdata
        self.ts = []
        self.kernels = 1

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

    def make_time_series(self, bbl, index):
        ipt = self.input[self.ts[index]]
        dst = {}
        while bbl == ipt[0]:
            self.ts[index] += 1
            su = ipt[1].strip().lower()
            if su in dst.keys():
                dst[su].append((ipt[2], ipt[3]))
            else:
                dst[su] = [(ipt[2], ipt[3])]
        series = [[key, dst[key]] for key in dst.keys()]
        return series

    @staticmethod
    def fix(val, index):
        if index == 0:
            return int(val)
        if index == 3:
            return float(val)

    def preprocess(self, index):
        period = len(self.input) / self.kernels
        offset = len(self.input) % self.kernels

        pass

    def mount_table(self, bbls, index):
        time_series = []
        self.ts[index] = len(self.input)-1
        self.ts[index] = self.binary_search(bbls[len(bbls)-1], 0, self.ts[index])
        while bbls:
            bbl = bbls.pop(0)
            time_series.append([bbl, self.make_time_series(bbl, index)])
        self.ts[index] = time_series

    def get_avg_ts(self):
        bbls = self.get_bbls()
        offset = len(bbls) % self.kernels
        if offset:
            period = (len(bbls) / self.kernels)
        else:
            period = len(bbls) / self.kernels
        end = 0
        t = []
        for i in xrange(self.kernels):
            self.ts.append([])
            begin = end
            end += period
            if offset:
                end += 1
                offset -= 1
            bblsk = bbls[begin:end]
            t.append(threading.Thread(target=self.mount_table, args=(bblsk, i)))
            if end > len(bbls):
                end = len(bbls)
        for i in xrange(len(t)):
            t[i].start()
        for i in xrange(len(t)):
            t[i].join()
        time_series = []
        for ts in self.ts:
            time_series += ts
        return time_series

    def growth(self, kernels=1):
        self.kernels = kernels
        CsvManager.append(self.get_avg_ts(), self.output)
