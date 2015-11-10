from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import sys
import time
from CsvManager import CsvManager
from Normalizer import Normalizer

__author__ = 'marcio'


class GoogleGeocode:
    def __init__(self, progress, error_log, geo):
        self.error_log = error_log
        self.progress = progress
        self.geo = geo

    def get_coordinates(self, t):
        try:
            bbl = t[0]
            address = Normalizer.set_address(t[1], bbl)
            lat, lon, full_address = self.geo.search_nominatim(address)
            GoogleGeocode.print_status(" Google")
            time.sleep(1)
            if lat is None:
                raise ValueError
            num = CsvManager.read_progress()+1
            CsvManager.write_progress(num)
            return (bbl, t[1], full_address, lon, lat, 1), num
        except ValueError:
            self.error_log.open()
            self.error_log.write(t[1]+", "+str(t[0]))
            self.error_log.close()
            GoogleGeocode.print_status(" Lat, Long not found ")
            time.sleep(1)
            return -1, False
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            self.error_log.open()
            self.error_log.write(e.message)
            self.error_log.close()
            GoogleGeocode.print_status(e.message)
            time.sleep(1)
            return -2, False
        except KeyboardInterrupt:
            GoogleGeocode.print_status(" Stopped ")
            time.sleep(1)
            return -3, False

    @staticmethod
    def get_num():
        return 2

    @staticmethod
    def print_status(string):
        sys.stdout.flush()
        sys.stdout.write(string)
        sys.stdout.flush()
