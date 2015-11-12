# -*- coding: utf-8 -*-
from CsvManager import CsvManager
from Normalizer import Normalizer
from RealEstateSettings import RealEstateSettings

__author__ = 'marcio'

res = RealEstateSettings('/tmp/manhattan_adrs.csv', '/home/marcio/marcio/manhattanLatLong.csv')
res.search_lat_long()

