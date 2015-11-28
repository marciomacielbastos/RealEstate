# -*- coding: utf-8 -*-
# from CsvManager import CsvManager
from Growth import Growth
# from Normalizer import Normalizer
# from RealEstateSettings import RealEstateSettings

__author__ = 'marcio'

res = Growth('/tmp/AcrisInPluto.csv', '/home/marcio/Marcio/timeseries.csv', '/tmp/bbs.csv', 3, 6)
res.growth(6)

