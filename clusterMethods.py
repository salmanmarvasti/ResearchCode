from time import time
import numpy as np
import matplotlib.pyplot as plt

from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
import VARIABLES
import TestInfos
from sklearn import mixture


def numberOfPointsInTheCircle(dataX, dataY, centerX, centerY, radius):
    sumP = 0
    for i in range(len(dataY)):
        if ((dataY[i] - centerY)**2 + (dataX[i] - centerX)**2)**0.5 <= radius:
            sumP += 1

    return sumP


def findMinMaxDistance(center, data):
    minDistance = float("inf")
    maxDistance = -1 * float("inf")
    for i in range(len(data[:,1])):
        distance = ((data[i, 1] - center[1])**2 + (data[i, 0] - center[0])**2)**0.5
        if distance < minDistance:
            minDistance = distance
        if distance > maxDistance:
            maxDistance = distance

    return minDistance, maxDistance


def clusterKMeans(data, n_digits, wholeDotOrientationGroup):

    afterTwoStocks = []
    afterTwoStarts = []
    afterTwoEnds = []

    pca = PCA(n_components=n_digits).fit(data)

    # #############################################################################
    # Visualize the results on PCA-reduced data

    reduced_data = PCA(n_components=2).fit_transform(data)
    kmeans = KMeans(init='k-means++', n_clusters=n_digits, n_init=10)
    kmeans.fit(reduced_data)

    # Step size of the mesh. Decrease to increase the quality of the VQ.
    h = .02     # point in the mesh [x_min, x_max]x[y_min, y_max].

    # Plot the decision boundary. For that, we will assign a color to each
    x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
    y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    # Obtain labels for each point in mesh. Use last trained model.
    Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure(2)
    plt.clf()
    # plt.imshow(Z, interpolation='nearest',
    #            extent=(xx.min(), xx.max(), yy.min(), yy.max()),
    #            cmap=plt.cm.Paired,
    #            aspect='auto', origin='lower',)

    dataY = reduced_data[:, 1]
    dataX = reduced_data[:, 0]
    upX=[]
    downX=[]

    #finance
    upXFinance=[]
    upYFinance=[]
    downXFinance=[]
    downYFinance=[]
    steadyXFinance=[]
    steadyYFinance=[]

    #healthCare
    upXHealthCare=[]
    upYHealthCare=[]
    downXHealthCare=[]
    downYHealthCare=[]
    steadyXHealthCare=[]
    steadyYHealthCare=[]

    #Technology
    upXTechnology=[]
    upYTechnology=[]
    downXTechnology=[]
    downYTechnology=[]
    steadyXTechnology=[]
    steadyYTechnology=[]

    #Others
    upXOthers=[]
    upYOthers=[]
    downXOthers=[]
    downYOthers=[]
    steadyXOthers=[]
    steadyYOthers=[]


    dataAfterTwo = []

    for i in range(len(dataY)):
        if wholeDotOrientationGroup[i] == 'up':
            upX.append(dataX[i])
            if TestInfos.stockNameArray[i] in VARIABLES.Finance:
                upXFinance.append(dataX[i])
                upYFinance.append(dataY[i])
            elif TestInfos.stockNameArray[i] in VARIABLES.HealthCare:
                upXHealthCare.append(dataX[i])
                upYHealthCare.append(dataY[i])
            elif TestInfos.stockNameArray[i] in VARIABLES.Technology:
                upXTechnology.append(dataX[i])
                upYTechnology.append(dataY[i])
            else:
                upXOthers.append(dataX[i])
                upYOthers.append(dataY[i])
            if dataX[i] >= 2:
                if not (TestInfos.stockNameArray[i] in afterTwoStocks and
                                TestInfos.stockLines[i].startTime in afterTwoStarts and
                                TestInfos.stockLines[i].endTime in afterTwoEnds):
                    afterTwoStocks.append(TestInfos.stockNameArray[i])
                    afterTwoStarts.append(TestInfos.stockLines[i].startTime)
                    afterTwoEnds.append(TestInfos.stockLines[i].endTime)

        elif wholeDotOrientationGroup[i] == 'down':
            downX.append(dataX[i])
            if TestInfos.stockNameArray[i] in VARIABLES.Finance:
                downXFinance.append(dataX[i])
                downYFinance.append(dataY[i])
            elif TestInfos.stockNameArray[i] in VARIABLES.HealthCare:
                downXHealthCare.append(dataX[i])
                downYHealthCare.append(dataY[i])
            elif TestInfos.stockNameArray[i] in VARIABLES.Technology:
                downXTechnology.append(dataX[i])
                downYTechnology.append(dataY[i])
            else:
                downXOthers.append(dataX[i])
                downYOthers.append(dataY[i])

        else:
            if TestInfos.stockNameArray[i] in VARIABLES.Finance:
                steadyXFinance.append(dataX[i])
                steadyYFinance.append(dataY[i])
            elif TestInfos.stockNameArray[i] in VARIABLES.HealthCare:
                steadyXHealthCare.append(dataX[i])
                steadyYHealthCare.append(dataY[i])
            elif TestInfos.stockNameArray[i] in VARIABLES.Technology:
                steadyXTechnology.append(dataX[i])
                steadyYTechnology.append(dataY[i])
            else:
                steadyXOthers.append(dataX[i])
                steadyYOthers.append(dataY[i])

    # plt.plot(steadyXFinance, steadyYFinance, 'gs', label='Finance Line Steady')
    plt.plot(upXFinance, upYFinance, 'g^', label='Finance Line Up')
    plt.plot(downXFinance, downYFinance, 'go', label='Finance Line Down')
    # plt.plot(steadyXHealthCare, steadyYHealthCare, 'rs', label='HealthCare Line Steady')
    plt.plot(upXHealthCare, upYHealthCare, 'r^', label='HealthCare Line Up')
    plt.plot(downXHealthCare, downYHealthCare, 'ro', label='HealthCare Line Down')
    # plt.plot(steadyXTechnology, steadyYTechnology, 'bs', label='Technology Line Steady')
    plt.plot(upXTechnology, upYTechnology, 'b^', label='Technology Line Up')
    plt.plot(downXTechnology, downYTechnology, 'bo', label='Technology Line Down')
    # plt.plot(steadyXOthers, steadyYOthers, 'ks', label='Others Line Steady')
    plt.plot(upXOthers, upYOthers, 'k^', label='Others Line Up')
    plt.plot(downXOthers, downYOthers, 'ko', label='Others Line Down')
    # Plot the centroids as a white X
    centroids = kmeans.cluster_centers_
    plt.scatter(centroids[:, 0], centroids[:, 1],
                marker='x', s=169, linewidths=3,
                color='darkseagreen', zorder=10, label='clustered points')
    plt.title('K-means clustering on the digits dataset (PCA-reduced data)\n'
              'Centroids are marked with white cross\n' +
              str(VARIABLES.START_YEAR) + '/' + str(VARIABLES.START_MONTH) + '/' + str(VARIABLES.START_DAY) +
              ' - ' +
              str(VARIABLES.FINISH_YEAR) + '/' + str(VARIABLES.FINISH_MONTH) + '/' + str(VARIABLES.FINISH_DAY))
    plt.legend()
    # plt.xlim(x_min, x_max)
    # plt.ylim(y_min+1 , y_max-1)
    # plt.show()

    firstCentroidMinDistance, firstCentroidMaxDistance = findMinMaxDistance(centroids[0], reduced_data)
    secondCentroidMinDistance, secondCentroidMaxDistance = findMinMaxDistance(centroids[1], reduced_data)
    print firstCentroidMinDistance
    print firstCentroidMaxDistance
    print secondCentroidMinDistance
    print secondCentroidMaxDistance

    print numberOfPointsInTheCircle(dataX, dataY, centroids[0, 0], centroids[0, 1], VARIABLES.CIRCLE_RADIUS_AROUND_CENTROIDS)

    for i in range(len(afterTwoEnds)):
        print '******************************************'
        print afterTwoStocks[i]
        print afterTwoStarts[i] + ' - ' + afterTwoEnds[i]
        print '******************************************'

def onclick(event, Xs, Ys, names, lines):
    # print ('button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
    #     event.button, event.x, event.y, event.xdata, event.ydata))
    clickedX = event.xdata
    clickedY = event.ydata
    minDistance = 10000000
    minName = ''
    minLine = None
    for i in range(len(Xs)):
        if ((Xs[i]-clickedX)**2 + (Ys[i]-clickedY)**2)**0.5 < minDistance:
            minDistance = ((Xs[i]-clickedX)**2 + (Ys[i]-clickedY)**2)**0.5
            minName = names[i]
            minLine = lines[i]

    # print minName
    print '%s\t%s' % (minLine.startTime, minLine.endTime)


def gaussianModelClustering(wholeData, wholeDotOrientationGroup, names, lines):
    wholeData[0] = [0, 0, 0, 0, 0]
    wholeData = PCA(n_components=2).fit_transform(wholeData)

    dataY = wholeData[:, 1]
    dataX = wholeData[:, 0]

    justUpDownWholeData = []

    for i in range(len(dataY)):
        if wholeDotOrientationGroup[i] == 'up' or wholeDotOrientationGroup[i] == 'down':
            justUpDownWholeData.append(wholeData[i])

    wholeData = np.array(justUpDownWholeData)
    dataY = wholeData[:, 1]
    dataX = wholeData[:, 0]

    gmm = mixture.GMM(n_components=2)
    gmm.fit(wholeData)
    colors = ['r' if i == 0 else 'g' for i in gmm.predict(wholeData)]
    markers = ['^' if wholeDotOrientationGroup[i] == 'up' else 'o' for i in range(len(wholeData))]
    labels = ['up' if wholeDotOrientationGroup[i] == 'up' else 'down' for i in range(len(wholeData))]

    labelList = []

    fig, ax = plt.subplots()

    for x, y, i in zip(wholeData[:, 0], wholeData[:, 1], range(len(colors))):
        if labels[i] not in labelList:
            ax.scatter([x], [y], c=colors[i], marker=markers[i], label=labels[i])
            labelList.append(labels[i])
        else:
            ax.scatter([x], [y], c=colors[i], marker=markers[i])

    # plt.scatter(dataX, dataY, c=colors, marker=markers, label=labels)
    plt.title('GMM clustering on the digits dataset (PCA-reduced data)\n' +
              str(VARIABLES.START_YEAR) + '/' + str(VARIABLES.START_MONTH) + '/' + str(VARIABLES.START_DAY) +
              ' - ' +
              str(VARIABLES.FINISH_YEAR) + '/' + str(VARIABLES.FINISH_MONTH) + '/' + str(VARIABLES.FINISH_DAY))

    cid = fig.canvas.mpl_connect('button_press_event', lambda event: onclick(event, wholeData[:, 0], wholeData[:, 1], names, lines))

    plt.legend()
    # plt.show()
