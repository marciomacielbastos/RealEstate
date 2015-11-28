from CsvManager import CsvManager
from ErrorLog import ErrorLog
from Progress import Progress
import pandas as pd
import numpy as np
import datetime
import calendar as cd
import threading

__author__ = 'marcio'


class Growth:
    def __init__(self, inputdata, outputdata, path, dt, qnt):
        self.error_log = ErrorLog(self.__class__.__name__)
        self.progress = Progress()
        self.path = path
        self.input = self.cast_intput(inputdata)
        self.output = outputdata
        self.dts = self.set_dts(dt, qnt)
        self.datestart = datetime.datetime.strptime('1901-01-01', "%Y-%m-%d").date()
        self.datefinal = datetime.datetime.strptime('2014-12-31', "%Y-%m-%d").date()
        self.ts = [[], []]

    def cast_intput(self, inputdata):
        cols = ['bb', 'price', 'date']
        input_ = pd.read_csv(inputdata, quotechar='"', sep=',', index_col=False, names=cols)
        bbs = self.get_bbs()
        input_['bb'] = input_['bb'].astype(int)
        input_['price'] = input_['price'].astype(float)
        input_['date'] = pd.to_datetime(input_['date'], format="%Y-%m-%d")
        temp1 = input_[['bb', 'price', 'date']][input_['bb'] < bbs[len(bbs)/2]]
        temp2 = input_[['bb', 'price', 'date']][input_['bb'] >= bbs[len(bbs)/2]]
        return temp1, temp2

    def get_bbs(self):
        bbs_temp = CsvManager.read(self.path)
        bbs = []
        for bb in bbs_temp:
            bbs.append(int(bb[0]))
        return bbs

    @staticmethod
    def set_dts(dt, qnt):
        dts = {}
        for i in xrange(qnt):
            sigma = i + 1
            sigma *= dt
            dts[sigma] = sigma
        return dts

    @staticmethod
    def add_months(date_, sigma):
        month = date_.month - 1 + sigma
        year = int(date_.year + month / 12)
        month = month % 12 + 1
        day = min(date_.day, cd.monthrange(year, month)[1])
        return datetime.date(year, month, day)

    def period_avg(self, bb, date_, dt, index):
        try:
            date1 = date_
            date2 = self.add_months(date_, dt)
            table = self.input[index][['price']][(self.input[index]['bb'] == bb) & (
                    self.input[index]['date'] >= date1) & (self.input[index]['date'] <= date2)].values
            if len(table):
                return np.average(table)
            else:
                return 0
        except ValueError:
            pass

    def make_time_series(self, bb, sigma, index):
        series = []
        date_ = self.datestart
        dt = self.dts[sigma]
        i = 1
        while date_ < self.datefinal:
            avg = self.period_avg(bb, date_, dt, index)
            if avg > 0:
                series.append([i, avg])
            date_ = self.add_months(date_, dt)
            i += 1
        return series

    def mount_table(self, bbs, sigma, index):
        time_series = []
        while bbs:
            bb = bbs.pop(0)
            time_series.append([bb, self.make_time_series(bb, sigma, index)])
        self.ts[index] = time_series

    def get_avg_ts(self, sigma):
        bbs = self.get_bbs()
        bbs1 = bbs[:len(bbs)/2]
        bbs2 = bbs[len(bbs)/2:]
        bbs = None
        t1 = threading.Thread(target=self.mount_table, args=(bbs1, sigma, 0))
        t2 = threading.Thread(target=self.mount_table, args=(bbs2, sigma, 1))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        time_series = self.ts[0]+self.ts[1]
        return time_series

    def growth(self, sigma):
        CsvManager.append(self.get_avg_ts(sigma), self.output)
