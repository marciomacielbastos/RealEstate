import csv

__author__ = 'marcio'


class CsvManager:
    def __init__(self):
        pass

    @staticmethod
    def store(data):
        with open('acris2.csv', 'w') as out:
            csv_out = csv.writer(out)
            csv_out.writerow(['lat', 'long', 'start_date', 'end_date', 'price'])
            for row in data:
                csv_out.writerow(row)

    @staticmethod
    def store_geo_codes(data):
        with open('coordinates.csv', 'w') as out:
            csv_out = csv.writer(out)
            csv_out.writerow(['bbl', 'raw_address', 'full_address', 'lat', 'long'])
            for row in data:
                csv_out.writerow(row)

    @staticmethod
    def read():
        list_ = []
        reader = csv.reader(open('/tmp/brooklyn.csv'))
        for row in reader:
            try:
                bbl = row[0]
                address = row[1]
                list_.append((bbl, address))
            except (KeyError, ValueError) as e:
                print e.message

        return list_
