from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import sys
import time
from CsvManager import CsvManager
from Normalizer import Normalizer

__author__ = 'marcio'


class OpenCageGeocode:
    def __init__(self, progress, error_log, geo):
        self.error_log = error_log
        self.progress = progress
        self.geo = geo

    def get_coordinates(self, t):
        try:
            bbl = t[0]
            address = t[1]# Normalizer.set_address(t[1], bbl)
            lat, lon, full_address = self.geo.search_opencage(address)
            if lat is None:
                raise ValueError
            OpenCageGeocode.print_status(" OpenCage")
            num = CsvManager.read_progress()+1
            CsvManager.write_progress(num)
            return (bbl, t[1], full_address.encode('utf-8'), lon, lat, 1), num
        except ValueError:
            self.error_log.open()
            self.error_log.write(t[1]+", "+str(t[0]))
            self.error_log.close()
            OpenCageGeocode.print_status(" Lat, Long not found ")
            return -1, False
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            self.error_log.open()
            self.error_log.write(e.message)
            self.error_log.close()
            OpenCageGeocode.print_status(e.message)
            return -2, False
        except KeyboardInterrupt:
            OpenCageGeocode.print_status(" Stopped ")
            return -3, False

    @staticmethod
    def get_num():
        return 3

    @staticmethod
    def print_status(string):
        sys.stdout.flush()
        sys.stdout.write(string)
        time.sleep(1)
        sys.stdout.flush()
