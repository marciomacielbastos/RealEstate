import time
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import sys
from CsvManager import CsvManager
# from DAO import DAO
from ErrorLog import ErrorLog
from GeoSearch import GeoSearch
from Normalizer import Normalizer
from Progress import Progress

__author__ = 'marcio'


class RealEstateSettings:
    def __init__(self):
        # self.dao = DAO('furman')
        self.geo = GeoSearch()
        self.error_log = ErrorLog(self.__class__.__name__)
        self.progress = Progress()

    # def get_coordinates_db(self):
    #     tuples = self.dao.picky_select_to_geocode()
    #     real_estates = []
    #     i = 0
    #     for t in tuples:
    #         try:
    #             bbl = t[0]
    #             address = Normalizer.set_address(t[1], bbl)
    #             lat, lon, full_address = self.geo.search(address)
    #             if lat is None:
    #                 raise ValueError
    #             real_estates.append((bbl, t[1], full_address, lat, lon))
    #             time.sleep(1)
    #         except ValueError:
    #             self.error_log.open()
    #             self.error_log.write(t[1]+", "+str(t[0]))
    #             self.error_log.close()
    #     CsvManager.store_geo_codes(real_estates)

    def get_coordinates_csv(self, path1, path2, i=0):
        if i > 3:
            raise GeocoderTimedOut
        tuples = CsvManager.read(path1)
        num = CsvManager.get_number_of_rows(path2)
        print num
        if num == 0:
            CsvManager.write_geo_codes([], path2)
        self.progress.set_size(len(tuples))
        self.progress.set_progress(num)
        Normalizer.set_tuple(num, tuples)
        real_estates = []
        while tuples:
            try:
                t = tuples.pop(0)
                bbl = t[0]
                address = Normalizer.set_address(t[1], bbl)
                lat, lon, full_address = self.geo.search(address)
                if lat is None:
                    raise ValueError
                real_estates.append((bbl, t[1], full_address, lat, lon))
                num += 1
                self.progress.set_progress(num)
                time.sleep(1.2)
            except ValueError:
                self.error_log.open()
                self.error_log.write(t[1]+", "+str(t[0]))
                self.error_log.close()
            except (GeocoderTimedOut,GeocoderServiceError) as e:
                CsvManager.append_geo_codes(real_estates, path2)
                self.error_log.open()
                self.error_log.write(e.message)
                self.error_log.close()
                if '[Errno 111]' in e.message:
                    time.sleep(1800)
                i += 1
                RealEstateSettings.get_coordinates_csv(self, path1, path2, i)
            except KeyboardInterrupt:
                print ""
                print "Stopped"
                CsvManager.append_geo_codes(real_estates, path2)
            i = 0
        CsvManager.append_geo_codes(real_estates, path2)
