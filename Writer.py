import csv
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import numpy as np
import os, glob
import LeastSquare
from PriceCompleteInfo import *
import VARIABLES
import shutil
import pandas

try:
    shutil.rmtree('/tmp/QSScratch')
except:
    pass
trouble = []

file_names = filter(lambda x: x.endswith('.csv'), os.listdir('/home/sepehr/QSTK-0.2.8/QSTK/QSData/Yahoo'))
number = raw_input("hi there, please enter \"all\" to fetch all data or something else to fetch a default parameter\n")
if number == "all":
    exactName = [x[0:len(x) - 4] for x in file_names]
else:
    exactName = VARIABLES.EXACT_STOCK

try:
    os.remove('prices.csv')
except:
    pass

try:
    os.remove('mapper.csv')
except:
    pass

print "you chose " + number + " and the exactName is : " + str(exactName)
with open('prices.csv', 'a') as csvfile:
    fieldnames = ['high', 'low', 'open', 'close', 'RSISMA', 'RSIEWMA']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for name in exactName:
        print "exploring the stock related to " + name
        ls_symbols = [name]

        # Start and End date of the charts
        dt_start = dt.datetime(VARIABLES.START_YEAR, VARIABLES.START_MONTH, VARIABLES.START_DAY)
        dt_end = dt.datetime(VARIABLES.FINISH_YEAR, VARIABLES.FINISH_MONTH, VARIABLES.FINISH_DAY)

        # We need closing prices so the timestamp should be hours=16.
        dt_timeofday = dt.timedelta(hours=VARIABLES.CLOSE_HOURS)

        # Get a list of trading days between the start and the end.
        ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

        # Creating an object of the dataaccess class with Yahoo as the source.
        c_dataobj = da.DataAccess(sourcein=VARIABLES.DATA_ACCESS_CLASS,
                                  s_datapath=VARIABLES.DATA_ACCESS_PATH,
                                  verbose=VARIABLES.IS_DEBUG)

        # Keys to be read from the data, it is good to read everything in one go.
        ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

        # Reading the data, now d_data is a dictionary with the keys above.
        # Timestamps and symbols are the ones that were specified before.
        try:
            ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys, verbose=VARIABLES.IS_DEBUG)
        except:
            trouble.append(name)
            continue
        d_data = dict(zip(ls_keys, ldf_data))

        # Filling the data for NAN
        for s_key in ls_keys:
            d_data[s_key] = d_data[s_key].fillna(method='ffill')
            d_data[s_key] = d_data[s_key].fillna(method='bfill')
            d_data[s_key] = d_data[s_key].fillna(1.0)

        mHigh = d_data['high']
        mLow = d_data['low']
        mOpen = d_data['open']
        mClose = d_data['actual_close']

        mHigh = mHigh[name]
        mLow= mLow[name]
        mOpen = mOpen[name]
        mClose = mClose[name]

        delta = mClose.diff()
        delta = delta[1:]
        up, down = delta.values.copy(), delta.values.copy()
        up[up < 0] = 0
        down[down > 0] = 0
        roll_up1 = pandas.stats.moments.ewma(up, VARIABLES.windowLength)
        roll_down1 = pandas.stats.moments.ewma(np.abs(down), VARIABLES.windowLength)
        # Calculate the RSI based on EWMA
        RS1 = roll_up1 / roll_down1
        RSI1 = 100.0 - (100.0 / (1.0 + RS1))

        # Calculate the SMA
        roll_up2 = pandas.rolling_mean(up, VARIABLES.windowLength)
        roll_down2 = pandas.rolling_mean(np.abs(down), VARIABLES.windowLength)

        # Calculate the RSI based on SMA
        RS2 = roll_up2 / roll_down2
        RSI2 = 100.0 - (100.0 / (1.0 + RS2))

        for i in range(len(mHigh)):
            myRSISMA = 50
            myRSIEWMA = 50
            if i == 0:
                writer.writerow({'high': mHigh[i], 'low': mLow[i], 'open': mOpen[i], 'close': mClose[i], 'RSISMA': 50,
                                 'RSIEWMA': 50})
            else:
                if np.isnan(RSI1[i-1]) or RSI1[i-1] == 0:
                    RSI1[i - 1] = 50
                if np.isnan(RSI2[i-1]) or RSI2[i-1] == 0:
                    RSI2[i - 1] = 50
                writer.writerow({'high': mHigh[i], 'low': mLow[i], 'open': mOpen[i], 'close': mClose[i], 'RSISMA': RSI2[i-1],
                                 'RSIEWMA': RSI1[i-1]})

with open('mapper.csv', 'a') as csvfile:
    fieldnames = ['name', 'date']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for name in exactName:
        if name not in trouble:
            print "exploring the stock related to " + name
            ls_symbols = [name]

            # Start and End date of the charts
            dt_start = dt.datetime(VARIABLES.START_YEAR, VARIABLES.START_MONTH, VARIABLES.START_DAY)
            dt_end = dt.datetime(VARIABLES.FINISH_YEAR, VARIABLES.FINISH_MONTH, VARIABLES.FINISH_DAY)

            # We need closing prices so the timestamp should be hours=16.
            dt_timeofday = dt.timedelta(hours=VARIABLES.CLOSE_HOURS)

            # Get a list of trading days between the start and the end.
            ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

            # Creating an object of the dataaccess class with Yahoo as the source.
            c_dataobj = da.DataAccess(VARIABLES.DATA_ACCESS_CLASS)

            # Keys to be read from the data, it is good to read everything in one go.
            ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

            # Reading the data, now d_data is a dictionary with the keys above.
            # Timestamps and symbols are the ones that were specified before.
            ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
            d_data = dict(zip(ls_keys, ldf_data))

            # Filling the data for NAN
            for s_key in ls_keys:
                d_data[s_key] = d_data[s_key].fillna(method='ffill')
                d_data[s_key] = d_data[s_key].fillna(method='bfill')
                d_data[s_key] = d_data[s_key].fillna(1.0)

            mHigh = d_data['high']
            mLow = d_data['low']
            mOpen = d_data['open']
            mClose = d_data['actual_close']

            mHigh = mHigh[name]
            mLow= mLow[name]
            mOpen = mOpen[name]
            mClose = mClose[name]
            for i in range(len(mHigh)):
                writer.writerow({'name': name, 'date': mHigh._index[i]._date_repr})

print trouble
