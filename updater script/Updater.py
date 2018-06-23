import os
import subprocess
import urllib2

from VARIABLES import ADDRESS_TO_FILES, ADDRESS_TO_SHELL_SCRIPT
import csv
import os


def wait_for_internet_connection(name):
    while True:
        print 'waiting for internet receiving ' + name
        try:
            response = urllib2.urlopen('http://ce.sharif.edu/', timeout=1)
            return
        except:
            print 'internet connection failure'
            pass


def reverseCSV(name):
    mDate = []
    mOpen = []
    mHigh = []
    mLow = []
    mClose = []
    mAdjClose = []
    mVolume = []

    with open(name, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mDate.append(row['Date'])
            mOpen.append(row['Open'])
            mHigh.append(row['High'])
            mLow.append(row['Low'])
            mClose.append(row['Close'])
            mAdjClose.append(row['Adj Close'])
            mVolume.append(row['Volume'])

    date2 = mDate[::-1]
    open2 = mOpen[::-1]
    high2 = mHigh[::-1]
    low2 = mLow[::-1]
    close2 = mClose[::-1]
    adjClose2 = mAdjClose[::-1]
    volume2 = mVolume[::-1]

    try:
        os.remove(name)
    except OSError:
        pass

    with open(name, 'w') as csvfile:
        fieldnames = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in range(len(open2)):
            writer.writerow({'Date': date2[i], 'Open': open2[i], 'High': high2[i], 'Low': low2[i], 'Close': close2[i], 'Volume': volume2[i], 'Adj Close': adjClose2[i]})


nameList = os.listdir(ADDRESS_TO_FILES)
names = []

for i in nameList:
    if i[len(i)-3: len(i)] == 'csv':
        names.append(i[0: len(i)-4])

# try:
#     os.remove('errors.txt')
# except OSError:
#     pass


print names
# f = open('errors.txt', 'w')
# f.write('[')
i = 0
errorCount = 0
while i < len(names):
    print i
    if errorCount == 0:
        print names[i]
        print ADDRESS_TO_SHELL_SCRIPT + ' ' + '\'' + names[i] + '\''
    try:
        wait_for_internet_connection(names[i])
    except:
        pass
    try:
        output = subprocess.check_output(ADDRESS_TO_SHELL_SCRIPT + ' ' + '\'' + names[i] + '\'', shell=True)
        outputSplit = output.split('\n')
        mOutput = outputSplit[len(outputSplit) - 2]
        if 'Error' in mOutput:
            print 'Error' + str(errorCount)
            errorCount += 1
            if errorCount == 40:
                errorCount = 0
                # f.write(names[i] + ', ')
                i += 1
        else:
            print output
            errorCount = 0
            reverseCSV(names[i]+'.csv')
            i += 1
    except:
        print 'Except Error' + str(errorCount)
        errorCount += 1
        if errorCount == 40:
            errorCount = 0
            # f.write(names[i] + ', ')
            i += 1
#
# f.write(']')
# f.close()
