from os import listdir
from os.path import isfile, join
import csv

mRow = None

with open('tensorflowData12.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    counter = 0

    for index, row in enumerate(reader):
        for index2, row2 in enumerate(reader):
            if index != index2 and row == row2:
                print '---------------------------'
                print index
                print index2
                print row
                print '---------------------------'
