import time
from BingGeocode import BingGeocode
from CsvManager import CsvManager
from DAOPsql import DAOPsql
from ErrorLog import ErrorLog
from GeoSearch import GeoSearch
from GoogleGeocode import GoogleGeocode
from NominatimGeocode import NominatimGeocode
from Normalizer import Normalizer
from OpenCageGeocode import OpenCageGeocode
from Progress import Progress
from TIGERGeocode import TIGERGeocode

__author__ = 'marcio'


class RealEstateSettings:

    def __init__(self):
        dao = DAOPsql('furman')
        self.geo = GeoSearch(dao)
        self.error_log = ErrorLog(self.__class__.__name__)
        self.progress = Progress()

    def fix_acris(self,  path1, path2):
        tuples = CsvManager.read(path1)
        num = CsvManager.get_number_of_rows(path2)
        self.progress.set_size(len(tuples))
        self.progress.update_progress(num)
        real_estates = []
        while tuples:
            try:
                t = tuples.pop(0)
                bbl = Normalizer.set_bbl(t[0], t[1], t[2])
                address = t[3]+" "+t[4]
                address = Normalizer.set_address(address, bbl)
                date = Normalizer.set_str_to_epoch(t[5])
                price = t[6]
                real_estates.append((bbl, address, date, price))
                num += 1
                self.progress.update_progress(num)
            except ValueError:
                self.error_log.open()
                self.error_log.write(t[1]+", "+str(t[0]))
                self.error_log.close()
            except KeyboardInterrupt:
                print ""
                print "Stopped"
                CsvManager.append_geo_codes(real_estates, path2)
        CsvManager.append_geo_codes(real_estates, path2)

    @staticmethod
    def write_progress(num):
        f = open('progress', 'w+')
        f.write(num)
        f.close()

    @staticmethod
    def read_progress():
        try:
            f = open('progress', 'r+')
            num = int(f.read())
            f.close()
            return num
        except IOError:
            return 0

    def preprocess(self, path1, path2):
        tuples = CsvManager.read(path1)
        num = self.read_progress()
        print num
        if num == 0:
            CsvManager.write_geo_codes([], path2)
            self.write_progress(0)
        self.progress.set_size(len(tuples))
        self.progress.update_progress(num)
        Normalizer.set_tuple(num, tuples)
        return tuples

    def build_geocodings(self):
        nominatim = NominatimGeocode(self.progress, self.error_log, self.geo)
        google = GoogleGeocode(self.progress, self.error_log, self.geo)
        opencage = OpenCageGeocode(self.progress, self.error_log, self.geo)
        bing = BingGeocode(self.progress, self.error_log, self.geo)
        tiger = TIGERGeocode(self.progress, self.error_log, self.geo)
        return nominatim, google, opencage, bing, tiger

    def search_lat_long(self, path1, path2):
        tuples = self.preprocess(path1, path2)
        real_estates = []
        count = 1
        nominatim, google, opencage, bing, tiger = self.build_geocodings()
        while tuples:
            t = tuples.pop(0)
            re, num = self.geocode_process(real_estates, t, nominatim)
            if num == -1:
                re, num = self.geocode_process(real_estates, t, bing)
                if num < 0:
                    self.geocode_process(real_estates, t, tiger)
            elif num == -2:
                i = 0
                while i < 3:
                    time.sleep(4000)
                    re, num = self.geocode_process(real_estates, t, nominatim)
                    if num > 0:
                        continue
                    if num == -2:
                        i += 1
                    if num == -3:
                        CsvManager.append_geo_codes(real_estates, path2)
                        return
                if num < 0:
                    CsvManager.append_geo_codes(real_estates, path2)
                    return num
            elif num == -3:
                print re
                CsvManager.append_geo_codes(real_estates, path2)
                return num
            if count % 100 == 0:
                for i in range(3):
                    t = tuples.pop(0)
                    re, num = self.geocode_process(real_estates, t, google)
                    time.sleep(3)
                    if num < 0:
                        self.geocode_process(real_estates, t, opencage)
                        time.sleep(3)
                    else:
                        t = tuples.pop(0)
                        self.geocode_process(real_estates, t, opencage)
                        time.sleep(3)
            count += 1
        CsvManager.append_geo_codes(real_estates, path2)

    def geocode_process(self, real_estates, t, geocode):
        re, num = geocode.get_coordinates(t)
        if num >= 0:
            real_estates.append(re)
        self.progress.update_progress(num)
        return re, num
