from os import listdir
from os.path import isfile, join
import csv
from VARIABLES import TENSOR_FLOW_DATA_PATH

mDimension = int(raw_input('print the dimension: '))
print TENSOR_FLOW_DATA_PATH + str(mDimension) + '/'

onlyfiles = [f for f in listdir(TENSOR_FLOW_DATA_PATH + '/') if isfile(join(TENSOR_FLOW_DATA_PATH, f))]
print onlyfiles
print len(onlyfiles)

s = 0
dataArray = []
counter = 0
dataIndicator = []

dimension = 0

for i in onlyfiles:
    print 'scanning index: ' + str(onlyfiles.index(i)) + ' out of ' + str(len(onlyfiles))
    with open(TENSOR_FLOW_DATA_PATH + '/' + i, 'r') as csvfile:
        reader = csv.reader(csvfile)
        counter = 0
        for row in reader:
            if counter == 0:
                s1 = s
                s += int(row[0])
                dimension = int(row[1])
                s2 = s
                dataIndicator.append([i, s1+1, s2])
                counter = 1
            else:
                dataArray.append(row)


print 'whole data length: ' + str(len(dataArray))
counter = 0
with open('tensorflowData' + str(mDimension) + '.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow([str(s), str(dimension), 'up', 'down', 'steady'])
    writer.writerows(dataArray)
    # for i in dataArray:
    #     print 'scanning index: ' + str(counter) + ' out of ' + str(len(dataArray))
    #     counter += 1
    #     writer.writerow(dataArray)

with open('tensorflowDataIndicator' + str(mDimension) + '.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(dataIndicator)
