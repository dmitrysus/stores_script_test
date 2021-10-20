"""
StoreCSVWizard

Interface around csv library
provides basic instruments to read/write csv files with data from stores
"""
import csv
import datetime


class StoreCSVWizard:
    """Class to read/write csv files"""
    def __init__(self, path, n=5):
        self.n = n
        self.path = path
        self.file = self.get_file()
        self.header = self.get_header()
        self.writer = self.get_writer()
        self.writer.writerow(self.header)

    def get_header(self):
        """Get a header for a file"""
        header = ['url', 'email', 'facebook', 'twitter'] + [
            f'{t} {i}' for i in range(1, self.n + 1) for t in ['title', 'image']]
        return header

    @staticmethod
    def get_file():
        f = open(f'output-{datetime.datetime.now().timestamp()}.csv', 'w')
        return f

    def get_writer(self):
        writer = csv.writer(self.file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        return writer

    def load_data(self):
        with open(self.path) as csvfile:
            data = csv.DictReader(csvfile)
            for row in data:
                yield row

    def write_data(self, data):
        """Write data to a file"""
        for row in data:
            r = [row.get(key) for key in self.header]
            self.writer.writerow(r)
        self.file.close()
