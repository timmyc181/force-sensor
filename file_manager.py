import csv
import datetime
import os


class Logger:
    FOLDER_NAME = 'log'

    def __init__(self):
        folder_exists = os.path.exists(self.FOLDER_NAME)
        if not folder_exists:
            # Create a new directory because it does not exist
            os.makedirs(self.FOLDER_NAME)

        date = datetime.datetime.now().strftime("%H:%M:%S.%f--%m-%d-%Y")
        f = open(self.FOLDER_NAME + '/' + date + '.csv', 'x')
        # with open(self.FOLDER_NAME + '/' + date + '.csv', 'x') as f:
        self.writer = csv.writer(f)

    def add_line(self, time, value):
        row = str(time) + ',' + str(value)
        # print('writing row: %s', row)
        self.writer.writerow([time, value])

    def finish(self):
        self.writer.close()

