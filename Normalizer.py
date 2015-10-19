import datetime
import re
import pyproj

__author__ = 'marcio'


class Normalizer:
    epoch = datetime.datetime.utcfromtimestamp(0)

    def __init__(self):
        pass

    @staticmethod
    def flat(list_):
        _list = []
        for val in list_:
            _list.append(val[0])
        return _list

    @staticmethod
    def quantizer(val):
        q = int(val / 100) * 100
        return q

    @staticmethod
    def format_date(string_date):
        if string_date:
            try:
                return datetime.datetime.strptime(string_date, "%Y-%m-%d")
            except ValueError:
                return Normalizer.epoch
        else:
            return Normalizer.epoch

    @staticmethod
    def time_to_secnds_from_epoch(dt):
        return (dt - Normalizer.epoch).total_seconds()

    @staticmethod
    def set_date(str_time):
        dt = Normalizer.format_date(str_time)
        epoch = Normalizer.format_date('1970-01-01')
        if dt < epoch:
            return None
        else:
            return Normalizer.time_to_secnds_from_epoch(dt)

    @staticmethod
    def set_address(address, bbl):
        adrs = Normalizer.format_address(address)
        return Normalizer.add_borough(adrs, bbl)

    @staticmethod
    def format_address(raw_address):
        tokens = Normalizer.tokenize_elements(raw_address)
        if tokens:
            cooked_address = Normalizer.correct_string_elements(raw_address, tokens)
        else:
            cooked_address = raw_address
        return cooked_address

    @staticmethod
    def tokenize_elements(address):
        adrs = re.findall(ur'[0-9]+\-*[0-9]*\s*\w*\s+\d+\s*\w+', address, re.I | re.U)
        if adrs:
            element = re.match(ur'([0-9]+\-*[0-9]*\s*\w*\s+)(\d+\s*)(\w+)', adrs[0], re.I | re.U).groups()
            return element
        else:
            return None

    @staticmethod
    def correct_string_elements(address, inst):
        try:
            dim = {u'RD': u'road', u'ST': u'street', u'th': u'', u'st': u'', u'nd': u'', u'rd': u''}
            if inst[2] in dim.keys() or inst[2].lower() in dim.keys():
                address = re.sub(ur'(' + inst[0] + ur')(' + inst[1] + ur')(' + inst[2] + ur')',
                                inst[0] + inst[1].replace(u' ', u'') + Normalizer.street_order(inst[1]) + dim[inst[2].lower()], address)
            else:
                address = re.sub(ur'(' + inst[0] + ur')(' + inst[1] + ur')(' + inst[2] + ur')',
                                inst[0] + inst[1].replace(u' ', u'') + Normalizer.street_order(inst[1]) + inst[2], address)
            return address.replace(u'  ', u' ')
        except:
            print inst

    @staticmethod
    def street_order(nmbr):
        dic = {1: u'st ', 2: u'nd ', 3: u'rd '}
        n = nmbr.replace(u' ', u'')[-1]
        num = int(n)
        if num in dic.keys():
            return dic[num]
        else:
            return u'th '

    @staticmethod
    def add_borough(address, bbl):
        neighborhood = Normalizer.get_neighborhood(bbl)
        try:
            return address+neighborhood+', NEW YORK, NY'
        except TypeError:
            if type(address) == 'NoneType':
                print neighborhood
            else:
                print address

    @staticmethod
    def get_neighborhood(bbl):
        neighborhood = {1: ' Manhattan', 2: ' Bronx', 3: ' Brooklyn', 4: ' Queens', 5: ' Staten Island'}
        return neighborhood[int(bbl) / 1000000000]

    @staticmethod
    def convert(x, y):
        """
        :param x: int x-axis coordinate of point in New York-Long Island State Plane coordinate system
        :param y: int y-axis coordinate of point in New York-Long Island State Plane coordinate system
        :rtype : tuple (latitude, longitude)
        The datum provided by pluto has x for y and vice-versa...
        NAD 83 / New York Long Island (ft US) (EPSG 2263): The State Plane zone that covers Long Island
        and New York City is used by all NYC agencies that produce GIS data
        """
        state_plane = pyproj.Proj(init='EPSG:2263', preserve_units=True)
        wgs = pyproj.Proj(proj='latlong', datum='NAD83', ellps='WGS84')
        lng, lat = pyproj.transform(state_plane, wgs, x, y)
        return lat, lng

    @staticmethod
    def set_tuple(i, tuple):
        for j in xrange(i):
            tuple.pop(0)
