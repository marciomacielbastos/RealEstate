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
                list_.append((row[0], row[1]))
            except (KeyError, ValueError, IndexError) as e:
                print e.message
                return
        return list_

    @staticmethod
    def get_number_of_rows(path):
        try:
            file_read = csv.reader(open(path, 'rU'))
            row_count = sum(1 for row in file_read)
            return row_count
        except IOError:
            return 0

    @staticmethod
    def append_geo_codes(data, path):
        try:
            with open(path, 'a') as out:
                csv_out = csv.writer(out)
                for row in data:
                    csv_out.writerow(row)
        except UnicodeEncodeError as e:
            print row

    @staticmethod
    def write_progress(num):
        f = open('progress', 'w+')
        f.write(str(num))
        f.close()

    @staticmethod
    def read_progress():
        try:
            f = open('progress', 'r+')
            num = int(f.read())
            f.close()
            return num
        except IOError:
            return 0
        except ValueError:
            print 0