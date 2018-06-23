import math
import numpy as np

import CandleStickChartTest
import VARIABLES
from Line import Line
import matplotlib.pyplot as plt
import TestInfos


def findTheCrrosings(line):
    arrayX = []
    arrayY = []
    for i in range(len(line.getYPoints()) - 1):
        if (line.a * (line.getXPoints()[i]) + line.b - line.getYPoints()[i]) * (
                            line.a * (line.getXPoints()[i + 1]) + line.b - line.getYPoints()[i + 1]) < 0:
            a1 = line.getYPoints()[i + 1] - line.getYPoints()[i]
            b1 = line.getYPoints()[i] - a1 * line.getXPoints()[i]
            ourX = (b1 - line.b) / (line.a - a1)
            ourY = a1 * ourX + b1
            arrayX.append(ourX)
            arrayY.append(ourY)
    return arrayX, arrayY


def normalizeDataStatic(data, window, full_prices_1d):
    result = []
    lowest_highest_scale = []
    for i in range(len(window)):
        lows = full_prices_1d.low[window[i][0]:window[i][1]]
        highs = full_prices_1d.high[window[i][0]:window[i][1]]
        lowest = min(lows)
        highest = max(highs)
        scale = highest - lowest
        for j in range(VARIABLES.NUMBER_OF_POINTS_CHOSEN_FOR_EACH_LINE):
            lowest_highest_scale.append([lowest, highest, scale])
    for i in range(len(data)):
        mdata = data[i]
        open = mdata[0]
        close = mdata[1]
        low = mdata[2]
        high = mdata[3]
        # dynamic OHLC
        lowest = lowest_highest_scale[i][0]
        scale = lowest_highest_scale[i][2]
        dyno = ((open - lowest) / scale) * VARIABLES.NORMALIZE_SCALE
        dync = ((close - lowest) / scale) * VARIABLES.NORMALIZE_SCALE
        dynl = ((low - lowest) / scale) * VARIABLES.NORMALIZE_SCALE
        dynh = ((high - lowest) / scale) * VARIABLES.NORMALIZE_SCALE
        result.append([dyno, dync, dynl, dynh])
    return result


def normalizeDataDynamic(data, window, full_prices_1d):
    mdatas = []
    result = []
    lowest_highest_scale = []
    for i in range(len(data)):
        mdata = data[i]
        windowNum = int(i/VARIABLES.NUMBER_OF_POINTS_CHOSEN_FOR_EACH_LINE)
        endIndex = window[windowNum][1]
        firstChosenDataIndex = endIndex - VARIABLES.NUMBER_OF_POINTS_CHOSEN_FOR_EACH_LINE
        dataIndex = 0
        for j in range(firstChosenDataIndex, endIndex):
            open = mdata[0]
            close = mdata[1]
            low = mdata[2]
            high = mdata[3]
            if open == full_prices_1d.open[j] and close == full_prices_1d.close[j] and low == full_prices_1d.low[j] and high == full_prices_1d.high[j]:
                dataIndex = j
                break
        if dataIndex >= 14:
            mdatas.append(mdata)
            lows = full_prices_1d.low[dataIndex-13:dataIndex+1]
            highs = full_prices_1d.high[dataIndex-13:dataIndex+1]
            lowest = min(lows)
            highest = max(highs)
            scale = highest - lowest
            lowest_highest_scale.append([lowest, highest, scale])
    for i in range(len(mdatas)):
        mdata = mdatas[i]
        open = mdata[0]
        close = mdata[1]
        low = mdata[2]
        high = mdata[3]
        # dynamic OHLC
        lowest = lowest_highest_scale[i][0]
        scale = lowest_highest_scale[i][2]
        if scale == 0:
            continue
        dyno = ((open - lowest) / scale) * VARIABLES.NORMALIZE_SCALE
        dync = ((close - lowest) / scale) * VARIABLES.NORMALIZE_SCALE
        dynl = ((low - lowest) / scale) * VARIABLES.NORMALIZE_SCALE
        dynh = ((high - lowest) / scale) * VARIABLES.NORMALIZE_SCALE
        result.append([dyno, dync, dynl, dynh])
    return result


def getAverage(full_price_1d):
    avg = 0
    for i in range(len(full_price_1d.high)):
        avg += (full_price_1d.high[i] + full_price_1d.low[i] + full_price_1d.close[i] + full_price_1d.open[i]) / 4
    avg /= len(full_price_1d.high)
    return avg


def gentrends(window, full_prices_2d, full_prices_1d, name, times, normCandle, charts=True):
    prices_2d = np.array(full_prices_2d.low[:])
    prices_1d = np.array(full_prices_1d.low[:])
    lines = []
    dotOrientationGroup = []
    dotOrientationGroup12D = []
    # stockPriceAverage = getAverage(full_prices_1d)
    sum2 = 0
    for i in range(len(window)):
        crosingsX = []
        crosingsY = []
        xBar = np.average(range(window[i][0], window[i][1], 1))
        yBar = np.average(prices_1d[window[i][0]:window[i][1]])
        sumOne = 0
        sumTwo = 0
        sum1 = 0
        if abs(window[i][0] - window[i][1]) > 1:
            for j in range(window[i][0], window[i][1]):
                sumOne += (j - xBar) * prices_1d[j]
                sumTwo += math.pow((j - xBar), 2)
            a = float(sumOne / sumTwo)
            b = yBar - a * xBar
            line = Line(a, b, window[i][0], window[i][1], full_prices_1d, times)
            if not (math.isnan(line.a) or math.isnan(line.b)):
                for k in range(len(line.getXPoints())):
                    sum1 += math.pow(line.getYPoints()[k] - (line.a * k + line.b), 2)
                sum2 += math.sqrt((sum1 / (line.endPoint - line.startPoint)))

            crossX, crossY = findTheCrrosings(line)

            for k in range(len(crossX)):
                crosingsX.append(crossX[k])
                crosingsY.append(crossY[k])

            # slope = (crosingsY[len(crosingsY) - 1] - crosingsY[0]) / crosingsY[0]
            avg2 = (line.getYPoints()[len(line.getYPoints()) - 1] + line.getYPoints()[len(line.getYPoints()) - 2] +
                    line.getYPoints()[len(line.getYPoints()) - 3])/3
            avg1 = (line.getYPoints()[0] + line.getYPoints()[1] + line.getYPoints()[2]) / 3
            slope = (avg2 - avg1) / avg1

            if slope >= VARIABLES.STRAIGHT_LINE_TOLERANCE:
                line.direction = "up"
            elif slope < -1 * VARIABLES.STRAIGHT_LINE_TOLERANCE:
                line.direction = "down"
            else:
                line.direction = "steady"
                # if line.a >= VARIABLES.STRAIGHT_LINE_TOLERANCE:
                #     line.direction = "up"
                # elif line.a < -1 * VARIABLES.STRAIGHT_LINE_TOLERANCE:
                #     line.direction = "down"
                # else:
                #     line.direction = "steady"

            lines.append(line)

            plt.plot(line.getXPoints(), line.getYPoints())
            plt.plot(line.getXPoints(), [line.a * i + line.b for i in line.getXPoints()])
            plt.title('Stock\'s name: ' + str(VARIABLES.EXACT_STOCK))
            # plt.plot(crosingsX, crosingsY, 'r*')

    data = []
    data12D = []

    for i in range(len(lines)-1):
        lines[i].last_points_direction = lines[i+1].direction
        for j in range(VARIABLES.NUMBER_OF_POINTS_CHOSEN_FOR_EACH_LINE):
            dotOrientationGroup.append(lines[i].last_points_direction)
        dotOrientationGroup12D.append(lines[i].last_points_direction)

    for line in lines:
        if line.last_points_direction == 'up':
            plt.plot(line.getLastXPoints(), line.getLastYPoints(), 'bo')
        elif line.last_points_direction == 'down':
            plt.plot(line.getLastXPoints(), line.getLastYPoints(), 'ko')
        elif line.last_points_direction == 'steady':
            plt.plot(line.getLastXPoints(), line.getLastYPoints(), 'ro')

    # print "the data are: "

    for i in range(len(lines)-1):
        data = data + lines[i].last_points
        for j in range(len(lines[i].last_points)):
            TestInfos.stockNameArray.append(name)
            TestInfos.stockLines.append(lines[i])
    data = np.array(data)
    counter = 0
    tempArr = []
    for i in data:
        for j in i:
            tempArr.append(j)
        counter += 1
        if counter == 3:
            data12D.append(tempArr)
            counter = 0
            tempArr = []
    data12D = np.array(data12D)

    # print str(data)
    # print str(len(data))
    # print str(len(data[0]))

    # normalizedData = np.array(normalizeDataStatic(data, window, full_prices_1d))
    normalizedData = np.array(normalizeDataDynamic(data, window, full_prices_1d))
    normalizedData12D = []
    counter = 0
    tempArr = []
    for i in normalizedData:
        for j in i:
            tempArr.append(j)
        counter += 1
        if counter == 3:
            normalizedData12D.append(tempArr)
            counter = 0
            tempArr = []
    normalizedData12D = np.array(normalizedData12D)
    if normCandle:
        candleInput = normalizedData
    else:
        candleInput = data
    # CandleStickChartTest.showCandle(candleInput[:, 0], candleInput[:, 1], candleInput[:, 2], candleInput[:, 3])
    return normalizedData, dotOrientationGroup, normalizedData12D, dotOrientationGroup12D
