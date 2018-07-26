import VARIABLES
from Main import calcReturnizedMeanMultiplier, calcReturnized
import numpy as np


def eventDetectorTester(prices):
    calcReturnizedMeanMultiplier(np.array(prices))
    returnized_prices = calcReturnized(prices)
    selectedData = abs(returnized_prices[len(returnized_prices) - VARIABLES.DAYS_CHECKED:len(returnized_prices) - 1])
    differenceArray = []
    for i in (1, range(len(selectedData))):
        differenceArray.append(selectedData[i] - selectedData[i-1])
    windowMean = VARIABLES.RETURNIZED_MEAN_MULTIPLIER * np.mean(np.array(differenceArray))
    todayData = selectedData[len(selectedData)-1]
    yesterdayData = selectedData[len(selectedData)-2]
    if abs(todayData - yesterdayData) >= windowMean:
        return True
    else:
        return False

