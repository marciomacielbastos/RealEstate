# -*- coding: utf-8 -*-
from CsvManager import CsvManager
from Normalizer import Normalizer
from RealEstateSettings import RealEstateSettings

__author__ = 'marcio'

res = RealEstateSettings()
res.search_lat_long('/home/marcio/marcio/boroughs/manhattan.csv', '/home/marcio/marcio/manhattan.csv')

