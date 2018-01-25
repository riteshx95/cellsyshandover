#
#   EE 764
#   Wireless & Mobile Communication
#   Simulation Assignment 1
#
#   Hexagonal geometry functions
#
#   Author: Ritesh
#   RollNo: 163079001
#
# # # # # # # # # # # # # # # # # # # # #

import numpy as np
import math
import random

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

def ss(theta):
        return np.sin(theta)
def cc(theta):
        return np.cos(theta)

class geom(object):
    def __init__(self, radius):
        self.radius = radius
        self.redge = radius * cc(np.pi / 6)
        ta = np.pi / 3
        verts = [ (      1,       0),
                  ( cc(ta),  ss(ta)),
                  (-cc(ta),  ss(ta)),
                  (     -1,       0),
                  (-cc(ta), -ss(ta)),
                  ( cc(ta), -ss(ta)) ]
        self.basis = np.asarray([np.asarray(item) for item in verts])
        self.basis *= radius

    # Checks if point p(i, j) is a reuse cell or not
    # for reuse factor 3
    def check3(self, p):
        if((p[1] - p[0]) % 3 == 0):
            return 1
        else:
            return 0

    # It checks if the p(i, j) is a reuse cell or not
    # if n is the reuse factor
    def checkReuse(self, p, rf):
        if(rf == 3):
            return self.check3(p)
        k = math.floor(math.sqrt((rf - 1) / 3))
        # basis found (k, k + 1)
        if(((k * p[1]) - ((k + 1) * p[0])) % rf == 0):
            return 1
        else:
            return 0

    def checkReuseSectored(self, p):
        i = p[0]
        j = p[1]
        ch = (2 * j) + i
        if(ch < 0):
            j += int(abs(ch))
        if(j % 2 == 0):
            if(i > (-1 * int(abs(j) / 2))):
                return 0
        else:
            if(i >= (-1 * int(abs(j) / 2))):
                return 0
        return 1

    # Gets the list of all reuse cells for the given
    # reuse factor 'rf' upto specified no. of tiers 'ntiers'
    def reuseCells(self, ntiers, rf):
        thelist = []
        p = -1 * ntiers
        q = 0
        r = ntiers
        while(q < ntiers):
            for i in range(p, q + 1):
                if(self.checkReuse((i, r), rf)):
                    thelist.append((i, r))
            r -= 1
            q += 1
        while(p <= 0):
            for i in range(p, q + 1):
                if(self.checkReuse((i, r), rf)):
                    thelist.append((i, r))
            r -= 1
            p += 1
        return thelist

    # Gets the list of all reuse cells for the given
    # reuse factor 'rf' upto specified no. of tiers 'ntiers'
    def reuseCellsSectored(self, ntiers):
        thelist = []
        p = -1 * ntiers
        q = 0
        r = ntiers
        while(q < ntiers):
            for i in range(p, q + 1):
                if(self.checkReuseSectored((i, r))):
                    thelist.append((i, r))
            r -= 1
            q += 1
        while(p <= 0):
            for i in range(p, q + 1):
                if(self.checkReuseSectored((i, r))):
                    thelist.append((i, r))
            r -= 1
            p += 1
        return thelist

    def isContainedInHex(self, center, pt):
        x = center[0] * np.cos(np.pi / 6)
        y = center[1] + (center[0] * np.sin(np.pi / 6))
        center = np.asarray([2 * self.redge * x, 2 * self.redge * y])
        vertices = [(center + z) for z in self.basis]
        theHexagon = Polygon(vertices)
        pp = Point(pt[0], pt[1])
        if(theHexagon.contains(pp)):
            return 1
        else:
            return 0

    def getRandomPointInHex(self):
        precision = 3
        pr = np.sqrt(self.radius * self.radius * random.randint(0, 10 ** precision) / float(10 ** precision))
        theta = 2 * np.pi * random.random()
        thePoint = (pr * np.cos(theta), pr * np.sin(theta))
        while((pr < 10) or (not self.isContainedInHex((0, 0), thePoint))):
            pr = np.sqrt(self.radius * self.radius * random.randint(0, 10 ** precision) / float(10 ** precision))
            theta = 2 * np.pi * random.random()
            thePoint = (pr * np.cos(theta), pr * np.sin(theta))
        return thePoint

    def getRandomPointInSector(self):
        precision = 3
        pr = np.sqrt(self.radius * self.radius * random.randint(0, 10 ** precision) / float(10 ** precision))
        theta = (2 * (np.pi / 3) * random.random()) - (np.pi / 3)
        thePoint = (pr * np.cos(theta), pr * np.sin(theta))
        while((pr < 10) or (not self.isContainedInHex((0, 0), thePoint))):
            pr = np.sqrt(self.radius * self.radius * random.randint(0, 10 ** precision) / float(10 ** precision))
            theta = (2 * (np.pi / 3) * random.random()) - (np.pi / 3)
            thePoint = (pr * np.cos(theta), pr * np.sin(theta))
        return thePoint