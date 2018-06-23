import VARIABLES
import numpy as np


class Line:
    direction = ""
    last_points = []

    def __init__(self, a, b, startPoint, endPoint, points, times, avg=None):
        self.a = a
        self.b = b
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.points = points
        self.last_points = []
        self.avg = avg
        self.startTime = times[startPoint]
        self.endTime = times[endPoint]
        self.last_points_direction = None
        self.direction = None

        for i in range(endPoint - VARIABLES.NUMBER_OF_POINTS_CHOSEN_FOR_EACH_LINE, endPoint):
            self.last_points.append([points.open[i], points.close[i], points.low[i], points.high[i]])

    def getLowPricesArray(self):
        return self.points.low[self.startPoint: self.endPoint]

    def getHighPricesArray(self):
        return self.points.high[self.startPoint: self.endPoint]

    def getOpenPricesArray(self):
        return self.points.open[self.startPoint: self.endPoint]

    def getClosePricesArray(self):
        return self.points.close[self.startPoint: self.endPoint]

    def getXPoints(self):
        points = []
        for i in range(self.startPoint, self.endPoint):
            points.append(i)
        return points

    def getYPoints(self):
        points = []
        for i in range(self.startPoint, self.endPoint):
            points.append(self.points.low[i])
        return points

    def getLastXPoints(self):
        points = []
        for i in range(self.endPoint - VARIABLES.NUMBER_OF_POINTS_CHOSEN_FOR_EACH_LINE, self.endPoint):
            points.append(i)
        return points

    def getLastYPoints(self):
        points = []
        for i in range(self.endPoint - VARIABLES.NUMBER_OF_POINTS_CHOSEN_FOR_EACH_LINE, self.endPoint):
            points.append(self.points.low[i])
        return points

    def get12Dimenssion(self):
        Ndim = len(self.last_points[0])
        dimenssion12Array = np.zeros(len(self.last_points) * Ndim)
        for i in range(len(self.last_points)):
            for j in range(len(self.last_points[i])):
                dimenssion12Array[i * Ndim + j] = self.last_points[i][j]
        return dimenssion12Array
