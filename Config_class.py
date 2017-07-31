import csv

class sim_config:
    def read_config(self, config_file):
        with open(config_file, 'r+') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                try:
                    setattr(self, row[0], int(row[1]))
                except:
                    try:
                        setattr(self, row[0], float(row[1]))
                    except:
                        setattr(self, row[0], str(row[1]))

    def __init__(self, config_file):
        self.read_config(config_file)