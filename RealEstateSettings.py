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

    def __init__(self, inputdata, outputdata):
        dao = DAOPsql('furman')
        self.geo = GeoSearch(dao)
        self.error_log = ErrorLog(self.__class__.__name__)
        self.progress = Progress()
        self.input = inputdata
        self.output = outputdata

    def fix_acris(self):
        tuples = CsvManager.read(self.input)
        num = CsvManager.get_number_of_rows(self.output)
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
                CsvManager.append_geo_codes(real_estates, self.output)
        CsvManager.append_geo_codes(real_estates, self.output)

    def preprocess(self):
        tuples = CsvManager.read(self.input)
        num = CsvManager.read_progress()
        print num
        if num == 0:
            CsvManager.write_geo_codes([], self.output)
            CsvManager.write_progress('0')
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

    def search_lat_long(self):
        tuples = self.preprocess()
        count = 1
        nominatim, google, opencage, bing, tiger = self.build_geocodings()
        while tuples:
            t = tuples.pop(0)
            status, found = self.geocode_process(t, tiger)
            if not found:
                if status == -1:
                    status, found = self.geocode_process(t, bing)
                    if not found and status == -1:
                        self.geocode_process(t, tiger)
                elif status == -2:
                    i = 1
                    while i < 3:
                        print "Waiting 45' for the "+Normalizer.set_order(str(i))+" time"
                        time.sleep(2700)
                        status, found = self.geocode_process(t, nominatim)
                        if found:
                            continue
                        elif status == -2:
                            i += 1
                        elif status == -3:
                            return
                if count % 100 == 0:
                    for i in range(3):
                        t = tuples.pop(0)
                        status, found = self.geocode_process(t, google)
                        time.sleep(3)
                        if not found:
                            self.geocode_process(t, opencage)
                            time.sleep(3)
                        else:
                            t = tuples.pop(0)
                            self.geocode_process(t, opencage)
                            time.sleep(3)
            count += 1

    def geocode_process(self, t, geocode):
        re, num = geocode.get_coordinates(t)
        if num:
            CsvManager.append_geo_codes([re], self.output)
            self.progress.update_progress(num)
        return re, num
