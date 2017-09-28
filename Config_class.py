import csv
import numpy as np

class sim_config:
    def read_config(self, config_file):
        with open(config_file, 'r+') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == 'seed':
                    temp = []
                    for item in row[1][1:-2].split(','):
                        temp.append(int(item))
                    setattr(self,row[0], temp)
                elif row[0] == 'start_box_se' or row[0] == 'start_box_nw':
                    temp = []
                    for item in row[1][1:-2].split(','):
                        temp.append(float(item))
                    setattr(self,row[0], temp)
                else:
                    try:
                        setattr(self, row[0], int(row[1]))
                    except:
                        try:
                            setattr(self, row[0], float(row[1]))
                        except:
                            setattr(self, row[0], str(row[1]))

    def __init__(self, config_file):
        self.read_config(config_file)