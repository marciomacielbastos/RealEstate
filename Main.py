# -*- coding: utf-8 -*-
from CsvManager import CsvManager
from Normalizer import Normalizer
from RealEstateSettings import RealEstateSettings

__author__ = 'marcio'

res = RealEstateSettings()
res.fix_acris('/tmp/acris_output.csv', '/home/marcio/marcio/acris.csv')

