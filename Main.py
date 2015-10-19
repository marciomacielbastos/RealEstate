# -*- coding: utf-8 -*-
from CsvManager import CsvManager
from Normalizer import Normalizer
from RealEstateSettings import RealEstateSettings

__author__ = 'marcio'

# res = RealEstateSettings()
# res.get_coordinates_csv()
a = [1, 2, 3]
Normalizer.set_tuple(0, a)
print a
print CsvManager.get_number_of_rows('/home/marcio/marcio/boroughs/brooklyn.csv')