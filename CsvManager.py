import csv

__author__ = 'marcio'


class CsvManager:
    def __init__(self):
        pass

    @staticmethod
    def store(data, path):
        with open(path, 'w') as out:
            csv_out = csv.writer(out)
            csv_out.writerow(['lat', 'long', 'start_date', 'end_date', 'price'])
            for row in data:
                csv_out.writerow(row)

    @staticmethod
    def write_geo_codes(data, path):
        with open(path, 'w') as out:
            csv_out = csv.writer(out)
            csv_out.writerow(['bbl', 'raw_address', 'full_address', 'lat', 'long'])
            for row in data:
                csv_out.writerow(row)

    @staticmethod
    def read(path):
        list_ = []
        file_read = csv.reader(open(path, 'rU'))
        for row in file_read:
            try:
                list_.append((row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
            except (KeyError, ValueError) as e:
                print e.message
        return list_

    @staticmethod
    def get_number_of_rows(path):
        try:
            file_read = csv.reader(open(path))
            row_count = sum(1 for row in file_read)
            return row_count
        except IOError:
            return 0

    @staticmethod
    def append_geo_codes(data, path):
        with open(path, 'a') as out:
            csv_out = csv.writer(out)
            for row in data:
                csv_out.writerow(row)


