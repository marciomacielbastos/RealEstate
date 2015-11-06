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
    def set_str_to_epoch(str_time):
        dt = Normalizer.format_date(str_time)
        epoch = Normalizer.format_date('1970-01-01')
        if dt < epoch:
            return None
        else:
            return Normalizer.time_to_secnds_from_epoch(dt)

    @staticmethod
    def set_address(address, bbl=None):
        adrs = Normalizer.format_address(address)
        if bbl:
            return Normalizer.add_borough(adrs, bbl)
        else:
            return Normalizer.add_city(adrs)

    @staticmethod
    def format_address(raw_address):
        tokens, raw_address = Normalizer.tokenize_elements(raw_address)
        if tokens:
            cooked_address = Normalizer.correct_string_elements(raw_address, tokens)
        else:
            cooked_address = raw_address
        return cooked_address

    @staticmethod
    def first_replaces(address):
        d = {'FIRST': '1ST', 'SECOND': '2ND', 'THIRD': '3RD',
             'FOUTH': '4TH', 'FIFTH': '5TH', 'SIXTH': '6TH',
             'SEVENTH': '7TH', 'EIGHTH': '8TH', 'NINTH': '9TH',
             'TENTH': '10TH', 'ELEVENTH': '11TH'}
        address = address.replace(u'.', u' ')
        for i in d.keys():
            if i in address:
                address = address.replace(i, d[i])
        return address
    @staticmethod
    def tokenize_elements(address):
        address = Normalizer.first_replaces(address)
        address = re.sub(u'\s\s+', u' ', address)
        adrs = re.findall(ur'[0-9]+\-*[0-9]*\s*\w*\s+\d+\s*\w+\s*\w*', address, re.I | re.U)
        if adrs:
            element = re.match(ur'([0-9]+\-*[0-9]*\s*\w*\s+)(\d+\s*)(\w+)(\s*\w*)', adrs[0], re.I | re.U).groups()
            if element[3] == u'':
                element = (element[0], element[1], element[2])
            return element, address
        else:
            adrs = re.findall(ur'[0-9]+\-*[0-9]*\s*\w*\s+\w+\s*\w+', address, re.I | re.U)
            if adrs:
                element = re.match(ur'([0-9]+\-*[0-9]*\s*\w*\s+)(\w+\s*)(\w*)', adrs[0], re.I | re.U).groups()
                if element[2] == u'':
                    element = (element[0], element[1])
                return element, address
            else:
                return None, address

    @staticmethod
    def correct_string_elements(address, inst):
        try:
            dim = {u'AV': u' AVENUE', u'AVE': u' AVENUE', u'RD': u' ROAD', u'ST': u' STREET', u'th': u'',
                   u'st': u'', u'nd': u'', u'rd': u''}
            if len(inst) > 2:
                if inst[2] in dim.keys() or inst[2].lower() in dim.keys():
                    if len(inst) == 4:
                        if inst[3] in dim.keys():
                            address = re.sub(ur'(' + inst[0] + ur')(' + inst[1] + ur')'
                                             ur'(' + inst[2] + ur')(' + inst[3] + ur')',
                                             inst[0] + inst[1].replace(u' ', u'') +
                                             Normalizer.street_order(inst[1]) + dim[inst[2].lower()] +
                                             dim[inst[3].replace(u' ', u'')], address)
                    else:
                        if inst[2] in dim.keys():
                            address = re.sub(ur'(' + inst[0] + ur')(' + inst[1] + ur')(' + inst[2] + ur')',
                                             inst[0] + inst[1].replace(u' ', u'') + Normalizer.street_order(inst[1]) +
                                             dim[inst[2]], address)
                else:
                    address = re.sub(ur'(' + inst[0] + ur')(' + inst[1] + ur')(' + inst[2] + ur')',
                                     inst[0] + inst[1].replace(u' ', u'') +
                                     Normalizer.street_order(inst[1]) + inst[2], address)
            elif inst[1] in dim.keys() or inst[1].lower() in dim.keys():
                address = re.sub(ur'(' + inst[0] + ur')(' + inst[1] + ur')',
                                 inst[0] + dim[inst[1]], address)
            address += u","
            address = re.sub(u'\s\s+', u' ', address)
            address = re.sub(u' ,', u',', address)
            return address
        except RuntimeError:
            print inst

    @staticmethod
    def street_order(nmbr):
        try:
            dic = {1: u'st ', 2: u'nd ', 3: u'rd '}
            n = nmbr.replace(u' ', u'')[-1]
            num = int(n)
            if num in dic.keys():
                return dic[num]
            else:
                return u'th '
        except ValueError:
            return u''

    @staticmethod
    def add_borough(address, bbl):
        neighborhood = Normalizer.get_neighborhood(bbl)
        try:
            return Normalizer.add_city(address + neighborhood)
        except TypeError:
            if type(address) == 'NoneType':
                print neighborhood
            else:
                print address

    @staticmethod
    def add_city(address):
        return address + ' NEW YORK, NY'

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
    def set_tuple(i, tuple_):
        for j in xrange(i):
            tuple_.pop(0)

    @staticmethod
    def select_zipcode_class(borough):
        zip_codes = [[100, 101, 102], [104], [112], [110, 111, 113, 114, 116], [103]]
        return zip_codes.pop(int(borough))

    @staticmethod
    def set_bbl(bourough, block, lot):
        return int(bourough) * 1000000000 + int(block) * 10000 + int(lot)

    @staticmethod
    def epoch_to_datetime(epoch):
        return datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S')