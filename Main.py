import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import numpy as np
import os
import csv
import LeastSquare
import TestInfos
from PriceCompleteInfo import *
import clusterMethods
import VARIABLES
import matplotlib.pyplot as plt
from math import *
import warnings


# functions


def writeTensorFlow(data=None, direction=None, dimenssion=None, nameIndexArray=None, name=None):
    data = np.ndarray.tolist(data)
    with open(name + str(dimenssion) + '.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow([str(len(data)), str(dimenssion), 'up', 'down', 'steady'])
        for k in range(len(data)):
            if direction[k] == 'up':
                dir = 0
            elif direction[k] == 'down':
                dir = 1
            elif direction[k] == 'steady':
                dir = 2
            tempArr = data[k] + [dir]
            writer.writerow(tempArr)
    if nameIndexArray:
        with open(name + 'Map' + str(dimenssion) + '.csv', 'w') as f:
            writer = csv.writer(f)
            for k in range(len(nameIndexArray)):
                writer.writerow(nameIndexArray[k])


def jumpedAppropriately(array, meanThreshhold, end):
    avg1 = (array[end - 1][0] + array[end][0]) / 2
    avg2 = (array[end + 1][0] + array[end + 2][0]) / 2
    result = abs(array[end] - array[end - 1]) >= meanThreshhold and abs(array[end - 1] - array[end + 1]) >= meanThreshhold \
           and abs(avg1 - avg2) >= (meanThreshhold*0.5)
    # result = abs(array[end] - array[end - 1]) >= meanThreshhold and abs(
    #     array[end - 1] - array[end + 1]) >= meanThreshhold > abs(array[end] - array[end + 1])
    # result = abs(array[end] - array[end - 1]) >= meanThreshhold and abs(
    #     array[end - 1] - array[end + 1]) >= meanThreshhold
    return result


def checkWindowArray(array, mean, end):
    window = []
    start = 0
    updateStart = False
    while True:
        lowLimitCondition = end - start >= 4 + VARIABLES.WINDOW_OVERLAP
        if abs(end - len(array) - 1) < 6:
            window.append([start, len(array) - 1])
            break
        elif jumpedAppropriately(array, mean, end) and lowLimitCondition:
            window.append([start, end])
            end -= VARIABLES.WINDOW_OVERLAP
            updateStart = True
        # elif end - start >= 100:
        #     window.append([start, end])
        #     end -= VARIABLES.WINDOW_OVERLAP
        #     updateStart = True
        end += 1
        if updateStart:
            updateStart = False
            start = end

    return window


def calcReturnizedMeanMultiplier(price):
    std = np.std(price, axis=0)[0]
    mean = np.mean(price)
    deviation = std / mean
    print 'Deviation is:'
    print deviation
    if chooseReturnized == 'ret':
        VARIABLES.STRAIGHT_LINE_TOLERANCE = max(0.04, VARIABLES.STRAIGHT_LINE_TOLERANCE_RETURNIZED * deviation)
    elif chooseReturnized == 'org':
        VARIABLES.STRAIGHT_LINE_TOLERANCE = max(0.04, VARIABLES.STRAIGHT_LINE_TOLERANCE_ORIGINAL * deviation)
    VARIABLES.RETURNIZED_MEAN_MULTIPLIER = abs(
        VARIABLES.MEAN_THRESHHOLD - VARIABLES.MEAN_THRESHHOLD * log10(VARIABLES.AAPL_DEVIATION / deviation))
    print VARIABLES.RETURNIZED_MEAN_MULTIPLIER


def calcReturnized(prices_2d):
    return tsu.returnize0([prices_2d[i][0] / prices_2d[0][0] for i in range(len(prices_2d))])


# starting the main part

file_names = filter(lambda x: x.endswith('.csv'), os.listdir('/home/sepehr/QSTK-0.2.8/QSTK/QSData/Yahoo'))
while True:
    category = raw_input("hi there, type all for not categorizing and filter for filtering\n"
                         "but if need categories, write the following:\n"
                         "Basic Industries\n"
                         "Capital Goods\n"
                         "Consumer Durables\n"
                         "Consumer Non-Durables\n"
                         "Consumer Services\n"
                         "Energy\n"
                         "Finance\n"
                         "Health Care\n"
                         "Miscellaneous\n"
                         "Public Utilities\n"
                         "Technology\n"
                         "Transportation\n")

    categoryArray = []
    if category == 'Basic Industries':
        categoryArray = VARIABLES.BasicIndustries
        break
    elif category == 'Capital Goods':
        categoryArray = VARIABLES.CapitalGoods
        break
    elif category == 'Consumer Durables':
        categoryArray = VARIABLES.ConsumerDurables
        break
    elif category == 'Consumer Non-Durables':
        categoryArray = VARIABLES.ConsumerNonDurables
        break
    elif category == 'Consumer Services':
        categoryArray = VARIABLES.ConsumerServices
        break
    elif category == 'Energy':
        categoryArray = VARIABLES.Energy
        break
    elif category == 'Finance':
        categoryArray = VARIABLES.Finance
        break
    elif category == 'Health Care':
        categoryArray = VARIABLES.HealthCare
        break
    elif category == 'Miscellaneous':
        categoryArray = VARIABLES.Miscellaneous
        break
    elif category == 'Public Utilities':
        categoryArray = VARIABLES.PublicUtilities
        break
    elif category == 'Technology':
        categoryArray = VARIABLES.Technology
        break
    elif category == 'Transportation':
        categoryArray = VARIABLES.Transportation
        break
    elif category == "all" or category == "filter":
        break
    else:
        print "wrong command"
compCounter = 1
justNames = [x[0:len(x) - 4] for x in file_names]

if category == 'all':
    exactName = justNames
elif category == 'filter':
    exactName = []
    for i in justNames:
        if i in VARIABLES.AllCategories:
            exactName.append(i)
else:
    exactName = []
    for i in justNames:
        if i in categoryArray:
            exactName.append(i)

number = raw_input("please enter \"all\" to fetch all data or "
                   "\"some\" for " + str(VARIABLES.NUMBER_OF_STOCKS_PICKED) +
                   " data or s.th else to "
                   "fetch a default parameters: " + str(VARIABLES.EXACT_STOCK))
if number == "all":
    exactName = exactName
elif number == "some":
    exactName2 = []
    i = VARIABLES.START_OF_PICKER
    while len(exactName2) < VARIABLES.NUMBER_OF_STOCKS_PICKED:
        if exactName[i] not in VARIABLES.ARRAY_OF_INVALID_STOCKS:
            exactName2.append(exactName[i])
        i += 1
    exactName = exactName2
else:
    exactName = VARIABLES.EXACT_STOCK

while True:
    chooseReturnized = raw_input("ret or org?\n")
    if chooseReturnized == "ret" or chooseReturnized == "org":
        break
    else:
        print "wrong command"

while True:
    chooseCluster = raw_input("kmeans or gmm?\n")
    if chooseCluster == "kmeans" or chooseCluster == "gmm":
        break
    else:
        print "wrong command"

while True:
    dimenssion = raw_input("dimenssion: 4 or 12?\n")
    if dimenssion == "4" or dimenssion == "12":
        break
    else:
        print "wrong command"

wholeData = []
wholeData12D = []
d_open = []
closes = []
highs = []
lows = []
opens = []
RSISMAs = []
RSIEWMAs = []
times = []
wholeDotOrientationGroup = []
wholeDotOrientationGroup12D = []
nameIndexArray = []

print "you chose " + number + " and the exactName is : " + str(exactName)
print 'number of stocks: ' + str(len(exactName))
warnings.simplefilter("error", RuntimeWarning)
for name in exactName:
    print name
    print compCounter
    compCounter += 1
    nameIndexArray.append([name, len(wholeData)])
    with open('prices.csv') as prices_csv_file:
        with open('mapper.csv') as mapper_csv_file:
            prices = list(csv.DictReader(prices_csv_file))
            mappers = list(csv.DictReader(mapper_csv_file))
            for i in range(len(mappers)):
                if mappers[i]['name'] == name:
                    # print(prices[i]['high'], prices[i]['low'], prices[i]['open'], prices[i]['close'])
                    opens.append([float(prices[i]['open'])])
                    closes.append([float(prices[i]['close'])])
                    highs.append([float(prices[i]['high'])])
                    lows.append([float(prices[i]['low'])])
                    RSISMAs.append([float(prices[i]['RSISMA'])])
                    RSIEWMAs.append([float(prices[i]['RSIEWMA'])])
                    times.append(mappers[i]['date'])

    full_prices_2d = PriceCompleteInfo2D(opens, highs, lows, closes, RSISMA=RSISMAs, RSIEWMA=RSIEWMAs)
    full_prices_1d = PriceCompleteInfo1D(np.squeeze(np.asarray(full_prices_2d.open)),
                                         np.squeeze(np.asarray(full_prices_2d.high)),
                                         np.squeeze(np.asarray(full_prices_2d.low)),
                                         np.squeeze(np.asarray(full_prices_2d.close)),
                                         RSISMA=np.squeeze(np.asarray(full_prices_2d.RSISMA)),
                                         RSIEWMA=np.squeeze(np.asarray(full_prices_2d.RSIEWMA)))
    #
    prices_2d = full_prices_2d.low
    calcReturnizedMeanMultiplier(np.array(prices_2d))
    returnized_2d = PriceCompleteInfo1D(calcReturnized(full_prices_2d.open),
                                        calcReturnized(full_prices_2d.high),
                                        calcReturnized(full_prices_2d.low),
                                        calcReturnized(full_prices_2d.close),
                                        RSISMA=calcReturnized(full_prices_2d.RSISMA),
                                        RSIEWMA=calcReturnized(full_prices_2d.RSIEWMA))
    returnized_1d = PriceCompleteInfo1D(np.squeeze(np.asarray(returnized_2d.open)),
                                        np.squeeze(np.asarray(returnized_2d.high)),
                                        np.squeeze(np.asarray(returnized_2d.low)),
                                        np.squeeze(np.asarray(returnized_2d.close)),
                                        RSISMA=np.squeeze(np.asarray(returnized_2d.RSISMA)),
                                        RSIEWMA=np.squeeze(np.asarray(returnized_2d.RSIEWMA)))
    # print "the prices_2d are: " + str(prices_2d)
    # normalized_prices = prices_2d / prices_2d[0, :]
    # normalized_prices = [prices_2d[i][0]/prices_2d[0][0] for i in range(len(prices_2d))]
    prices_1d = full_prices_1d.low
    # print "the prices_1d are: " + str(prices_1d)
    returnized_prices_2d = calcReturnized(prices_2d)
    # print "returnized_prices_2d is: " + str(returnized_prices_2d)
    windowMean = VARIABLES.RETURNIZED_MEAN_MULTIPLIER * np.mean(abs(returnized_prices_2d))
    window = checkWindowArray(returnized_prices_2d, windowMean, 1)
    # print "the window is : " + str(window)
    # returnized_prices_1d = np.squeeze(np.asarray(returnized_prices_2d))
    # print "returnized_prices_1d is: " + str(returnized_prices_1d)
    if chooseReturnized == "ret":
        specificData, dotOrientationGroup, specificData12D, dotOrientationGroup12D = LeastSquare.gentrends(window, returnized_2d, returnized_1d, name, times,
                                                                  True)
    elif chooseReturnized == "org":
        specificData, dotOrientationGroup, specificData12D, dotOrientationGroup12D = LeastSquare.gentrends(window, full_prices_2d, full_prices_1d, name, times,
                                                                  True)
    else:
        break
    # wholeDotOrientationGroup.append(dotOrientationGroup)
    wholeDotOrientationGroup = wholeDotOrientationGroup + dotOrientationGroup
    wholeDotOrientationGroup12D = wholeDotOrientationGroup12D + dotOrientationGroup12D
    if specificData.any():
        if len(wholeData) != 0:
            # wholeData = wholeData + specificData
            wholeData = np.concatenate((wholeData, specificData), axis=0)
            wholeData12D = np.concatenate((wholeData12D, specificData12D), axis=0)
        else:
            wholeData = specificData
            wholeData12D = specificData12D
            # np.concatenate((wholeData, specificData), axis=0)
        if dimenssion == '12':
            writeTensorFlow(data=specificData12D, direction=dotOrientationGroup12D, dimenssion=12,
                            name=name)
        else:
            writeTensorFlow(data=specificData, direction=dotOrientationGroup, dimenssion=4,
                            name=name)
# plt.show()
# print wholeData
# if dimenssion == '12':
#     wholeData = wholeData12D
#     wholeDotOrientationGroup = wholeDotOrientationGroup12D
# if chooseCluster == 'kmeans':
#     clusterMethods.clusterKMeans(wholeData, 2, wholeDotOrientationGroup)
# elif chooseCluster == 'gmm':
#     clusterMethods.gaussianModelClustering(wholeData, wholeDotOrientationGroup, TestInfos.stockNameArray,
#                                            TestInfos.stockLines)
# if dimenssion == '12':
#     writeTensorFlow(data=wholeData12D, direction=wholeDotOrientationGroup12D, dimenssion=12,
#                     nameIndexArray=nameIndexArray)
# else:
#     writeTensorFlow(data=wholeData, direction=wholeDotOrientationGroup, dimenssion=4,
#                     nameIndexArray=nameIndexArray)
print "end of execution"
