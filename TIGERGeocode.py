import sys
import time
from CsvManager import CsvManager
from Normalizer import Normalizer

__author__ = 'marcio'


class TIGERGeocode:
    def __init__(self, progress, error_log, geo):
        self.error_log = error_log
        self.progress = progress
        self.geo = geo

    def get_coordinates(self, t):
        try:
            # bbl = t[0]
            address = t[1]# Normalizer.set_address(t[1], bbl)
            lon, lat, full_address = self.geo.search_dao(address, t[0])
            if lat is None:
                raise ValueError
            TIGERGeocode.print_status(" TIGER")
            num = CsvManager.read_progress()+1
            CsvManager.write_progress(num)
            return (bbl, t[1], full_address, lon, lat, 4), num
        except ValueError:
            self.error_log.open()
            self.error_log.write(t[1]+", "+str(t[0]))
            self.error_log.close()
            TIGERGeocode.print_status(" Lat, Long not found ")
            return -1, False

        except KeyboardInterrupt:
            TIGERGeocode.print_status(" Stopped ")
            return -3, False

    @staticmethod
    def get_num():
        return 5

    @staticmethod
    def print_status(string):
        sys.stdout.flush()
        sys.stdout.write(string)
        time.sleep(1)
        sys.stdout.flush()
