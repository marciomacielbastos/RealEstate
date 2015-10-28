import time
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import sys
from CsvManager import CsvManager
# from DAO import DAO
from DAOPsql import DAOPsql
from ErrorLog import ErrorLog
from GeoSearch import GeoSearch
from Normalizer import Normalizer
from Progress import Progress

__author__ = 'marcio'


class RealEstateSettings:
    def __init__(self):
        # dao = DAOPsql('furman')
        # self.geo = GeoSearch(dao)
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

    def get_coordinates_nominatim(self, path1, path2, i=0):
        if i > 3:
            raise GeocoderTimedOut
        tuples = CsvManager.read(path1)
        num = CsvManager.get_number_of_rows(path2)
        print num
        if num == 0:
            CsvManager.write_geo_codes([], path2)
        self.progress.set_size(len(tuples))
        self.progress.update_progress(num)
        Normalizer.set_tuple(num, tuples)
        real_estates = []
        while tuples:
            try:
                t = tuples.pop(0)
                bbl = t[0]
                address = Normalizer.set_address(t[1], bbl)
                lat, lon, full_address = self.geo.search_nominatim(address)
                if lat is None:
                    raise ValueError
                real_estates.append((bbl, t[1], full_address, lat, lon))
                num += 1
                self.progress.update_progress(num)
                time.sleep(1.2)
            except ValueError:
                self.error_log.open()
                self.error_log.write(t[1]+", "+str(t[0]))
                self.error_log.close()
            except (GeocoderTimedOut, GeocoderServiceError) as e:
                CsvManager.append_geo_codes(real_estates, path2)
                self.error_log.open()
                self.error_log.write(e.message)
                self.error_log.close()
                if '[Errno 111]' in e.message:
                    time.sleep(4000)
                i += 1
                RealEstateSettings.get_coordinates_nominatim(self, path1, path2, i)
            except KeyboardInterrupt:
                print ""
                print "Stopped"
                CsvManager.append_geo_codes(real_estates, path2)
            i = 0
        CsvManager.append_geo_codes(real_estates, path2)

    def get_coordinates_openmapquest(self, path1, path2, i=0):
        if i > 3:
            raise GeocoderTimedOut
        tuples = CsvManager.read(path1)
        num = CsvManager.get_number_of_rows(path2)
        print num
        if num == 0:
            CsvManager.write_geo_codes([], path2)
        self.progress.set_size(len(tuples))
        self.progress.update_progress(num)
        Normalizer.set_tuple(num, tuples)
        real_estates = []
        while tuples:
            t = tuples.pop(0)
            bbl = t[0]
            address = Normalizer.set_address(t[1], bbl)
            try:
                lat, lon, full_address = self.geo.search_openmapquest(address)
                if lat is None:
                    raise ValueError
                real_estates.append((bbl, t[1], full_address, lat, lon))
                num += 1
                self.progress.update_progress(num)
                time.sleep(1.2)
            except ValueError:
                self.error_log.open()
                self.error_log.write(t[1]+", "+str(t[0]))
                self.error_log.close()
                lat, lon, full_address = self.geo.search_nominatim(address)
                if lat is None:
                    pass

            except (GeocoderTimedOut, GeocoderServiceError) as e:
                CsvManager.append_geo_codes(real_estates, path2)
                self.error_log.open()
                self.error_log.write(e.message)
                self.error_log.close()
                if '[Errno 111]' in e.message:
                    time.sleep(4000)
                i += 1
                RealEstateSettings.get_coordinates_nominatim(self, path1, path2, i)
            except KeyboardInterrupt:
                print ""
                print "Stopped"
                CsvManager.append_geo_codes(real_estates, path2)
            i = 0
        CsvManager.append_geo_codes(real_estates, path2)

    def get_coordinates_TIGER(self, path1, path2):
        tuples = CsvManager.read(path1)
        num = CsvManager.get_number_of_rows(path2)
        print num
        if num == 0:
            CsvManager.write_geo_codes([], path2)
        self.progress.set_size(len(tuples))
        self.progress.update_progress(num)
        Normalizer.set_tuple(num, tuples)
        real_estates = []
        while tuples:
            try:
                t = tuples.pop(0)
                bbl = Normalizer.set_bbl(t[0], t[1], t[2])
                address = t[3]+" "+t[4]
                address = Normalizer.set_address(address)
                lon, lat = self.geo.search_dao(address, t[0])
                print lon, lat
                date = Normalizer.set_str_to_epoch(t[6])
                price = t[7]
                if lat is None:
                    raise ValueError
                real_estates.append((bbl, lon, lat, date, price))
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