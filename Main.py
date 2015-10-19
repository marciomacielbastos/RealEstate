# -*- coding: utf-8 -*-
from CsvManager import CsvManager
from Normalizer import Normalizer
from RealEstateSettings import RealEstateSettings

__author__ = 'marcio'

res = RealEstateSettings()
res.get_coordinates_csv('/home/marcio/marcio/boroughs/bronx.csv', 'coord_bronx.csv')