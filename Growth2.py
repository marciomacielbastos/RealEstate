from CsvManager import CsvManager
import threading

__author__ = 'marcio'


class Growth2:
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

    def sequential_search(self, bbl, index):
        while bbl == self.input[index][0]:
            index -= 1
        return index+1

    def binary_search(self, bbl, begin, end):
        cond = len(self.input)
        while cond:
            index = (end - begin)/2 + begin
            val = self.input[index][0]
            if bbl < val:
                end = (end-begin) / 2 + begin
                cond /= 2
            elif bbl > val:
                begin = begin + (end - begin)/2 + 1
                cond /= 2
            elif bbl == val:
                return self.sequential_search(bbl, index)
        return None

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
            if self.ts[index] < len(self.input):
                ipt = self.input[self.ts[index]]
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
        end = 0
        begin = 0
        for i in xrange(index+1):
            begin = end
            end += period
            if offset:
                end += 1
                offset -= 1
        for i in xrange(begin, end):
            self.input[i] = (self.fix(self.input[i][0], 0), self.input[i][1], self.input[i][2], self.fix(self.input[i][3], 3))
            bola= 2


    def mount_table(self, bbls, index):
        self.preprocess(index)
        time_series = []
        self.ts[index] = self.binary_search(bbls[0], 0, len(self.input)-1)
        while bbls:
            bbl = bbls.pop(0)
            time_series.append([bbl, self.make_time_series(bbl, index)])
        self.ts[index] = time_series
        print "terminou ",index

    def get_avg_ts(self):
        bbls = self.get_bbls()
        offset = len(bbls) % self.kernels
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
            print "quase"
            t[i].join()
        time_series = []
        print "quase"
        for ts in self.ts:
            time_series += ts
        return time_series

    def growth(self, kernels=1):
        self.kernels = kernels
        CsvManager.append(self.get_avg_ts(), self.output)
