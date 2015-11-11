# -*- coding: utf-8 -*-
from CsvManager import CsvManager
from Normalizer import Normalizer
from RealEstateSettings import RealEstateSettings

__author__ = 'marcio'

res = RealEstateSettings('/tmp/acris_outfile.csv', '/home/marcio/marcio/acris_fixed.csv')
res.fix_acris()

