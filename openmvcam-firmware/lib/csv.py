class writer:
    def __init__(self, file):
        self.file = file

    def writerow(self, row):
        self.file.write(','.join(row) + '\n')
