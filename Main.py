# -*- coding: utf-8 -*-
from CsvManager import CsvManager
from Normalizer import Normalizer
from RealEstateSettings import RealEstateSettings

__author__ = 'marcio'

res = RealEstateSettings('/home/marcio/marcio/boroughs/manhattan.csv', '/home/marcio/marcio/manhattan.csv')
res.search_lat_long()

