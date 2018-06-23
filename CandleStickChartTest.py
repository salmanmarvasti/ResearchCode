import matplotlib.pyplot as plt
from matplotlib.finance import candlestick2_ochl
import numpy as np

def showCandle(opens, closes, lows, highs):
    fig, ax = plt.subplots()
    # plt.ylim((-0.1, 1.1))
    # plt.xlim((-1, 50))
    candlestick2_ochl(ax, opens, highs, lows, closes, width=1, colorup='k', colordown='r',
                                         alpha=0.75)
    # print "the candles data are open: " + str(opens)
    # print "the candles data are close: " + str(closes)
    # print "the candles data are high: " + str(highs)
    # print "the candles data are low: " + str(lows)

    # plt.show()
