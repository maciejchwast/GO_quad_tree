import random
import math
import numpy as np
import matplotlib.pyplot as plt
import sys
from PIL import Image, ImageDraw

class Point:

    def __init__(self, px, py):
        self.x = px
        self.y = py

    def print(self):
        return "X = " + str(round(self.x, 2)) + ", Y = " + str(round(self.y, 2))

    def toInt(self):
        self.x = int(self.x)
        self.y = int(self.y)

    def half(self):
        return Point(self.x/2, self.y/2)

    def invX(self):
        return Point(-self.x, self.y)

    def invY(self):
        return Point(self.x, -self.y)

class Straight:

    def print(self):
        return "y = " + str(round(self.a, 2)) + "X + " + str(round(self.b, 2))

    def __init__(self, p1: Point, p2: Point):
        self.a = (p1.y - p2.y) / (p1.x - p2.x)
        self.b = p1.y - self.a * p1.x


class Line:
    head: Point
    tail: Point

    def print(self):
        return "head point: " + self.head.print() + " tail point: " + self.tail.print()

    def __init__(self, p1: Point, p2: Point):
        self.head = p1
        self.tail = p2
        self.belongs_to_straight = Straight(p1, p2)


class Plot:
    plot = plt

    def __init__(self):
        self.plot.xlim(-1000, 1000)
        self.plot.ylim(-1000, 1000)


class pointCloud:
    points = []

    def __init__(self, center: Point, spread):
        self.points.clear()
        self.centerPoint = center
        self.spread = spread
        for i in range(random.randrange(5, 10)):
            newPoint = randomPointWithinDistance(self.spread, self.centerPoint)
            self.points.append(newPoint)
        self.pointCount = len(self.points)

    def draw(self, plot: plt, _color):

        for pt in self.points:
            plot.plot.plot(pt.x, pt.y, '.', color=_color)

    def printPoints(self):
        for pt in self.points:
            print("Point ",pt.x,", ", pt.y)


def randomPoint():
    a = random.randrange(-1000, 1000)
    b = random.randrange(-1000, 1000)
    return Point(a, b)


def pointDistance(p1: Point, p2: Point):
    return math.sqrt((p2.x * p2.x - p1.x * p1.x) - (p2.y * p2.y - p1.y * p1.y))


def randomPointExcludeArea(p1: Point, range):
    result = randomPoint()
    while pointDistance(result, p1) < range:
        result = randomPoint()
    return result


def randomPointWithinDistance(dist, p1: Point):
    result = Point(random.randrange(p1.x - dist, p1.x + dist), random.randrange(p1.y - dist, p1.y + dist))
    return result


def pointsAngle(p1: Point, p2: Point):
    p3 = Point(p2.x-p1.x, p2.y-p1.y)
    return math.degrees(math.acos(p3.x/math.sqrt(p3.x*p3.x + p3.y*p3.y)))


def getSlope(p1: Point, p2: Point):
    if p1.x == p2.x:
        return float('inf')
    else:
        return 1.0*(p1.y-p2.y)/(p1.x-p2.x)


def getCrossProduct(p1: Point, p2: Point, p3: Point):
    return ((p2.x - p1.x)*(p3.y - p1.y)) - ((p2.y - p1.y)*(p3.x - p1.x))


def graham(cld: pointCloud):
    _hull = []
    _hull.clear()
    _sortedPoints = sorted(cld.points, key=lambda p: [p.x, p.y])
    startPoint = _sortedPoints.pop(0)
    _hull.append(startPoint)
    _sortedPoints.sort(key=lambda p: (getSlope(p, startPoint), -p.y, p.x))
    for _pt in _sortedPoints:
        _hull.append(_pt)
        while len(_hull) > 2 and getCrossProduct(_hull[-3], _hull[-2], _hull[-1]) < 0:
            _hull.pop(-2)
    return _hull


def pointsToValueArray(points):
    px = []
    py = []
    px.clear()
    py.clear()
    for ppt in points:
        px.append(ppt.x)
        py.append(ppt.y)
    return px, py

'''
def beautifyPlot():
    axis[0, 0].set_title("Chmury punktow")
    axis[0, 0].set_xlim(-1000, 1000)
    axis[0, 0].set_ylim(-1000, 1000)
    axis[0, 0].get_xaxis().set_visible(False)
    axis[0, 0].get_yaxis().set_visible(False)

    axis[0, 1].set_title("Otoczki")
    axis[0, 1].set_xlim(-1000, 1000)
    axis[0, 1].set_ylim(-1000, 1000)
    axis[0, 1].get_xaxis().set_visible(False)
    axis[0, 1].get_yaxis().set_visible(False)

    axis[1, 0].set_title("Figury")
    axis[1, 0].set_xlim(-1000, 1000)
    axis[1, 0].set_ylim(-1000, 1000)
    axis[1, 0].get_xaxis().set_visible(False)
    axis[1, 0].get_yaxis().set_visible(False)
'''

def quadtree_plot(img, p1: Point, p2: Point):
    p1.toInt()
    p2.toInt()
    for i in range(p1.x, p2.x, 4):
        for j in range(p1.y, p2.y, 4):
            if abs(p1.x - p2.x) < 10 or abs(p1.y - p2.y) < 10:
                quadtree_plot(img, Point(0, 0), Point(im.width / 2, img.height / 2))
            if black_pixel_inside(img, p1, Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)):
                draw_cross(img, p1, p2)
                quadtree_plot(img, p1, Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2))
            if black_pixel_inside(img, Point(p2.x / 2 + p1.x, p1.y), Point(p2.x, (p2.y + p1.y) / 2)):
                draw_cross(img, p1, p2)
                quadtree_plot(img, Point(p2.x / 2 + p1.x, p1.y), Point(p2.x, (p2.y + p1.y) / 2))
            if black_pixel_inside(img, Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2), p2):
                draw_cross(img, p1, p2)
                quadtree_plot(img, Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2), p2)
            if black_pixel_inside(img, Point(p1.x, (p2.y + p1.y) / 2), Point(p2.x / 2 + p1.x, p2.y)):
                draw_cross(img, p1, p2)
                quadtree_plot(img, Point(p1.x, (p2.y + p1.y) / 2), Point(p2.x / 2 + p1.x, p2.y))


def black_pixel_inside(img, p1: Point, p2: Point):
    p1.toInt()
    p2.toInt()
    px = img.load()
    returnVal = False
    for i in range(p1.x, p2.x, 2):
        for j in range(p1.y, p2.y, 2):
            if px[i, j] == (0, 0, 0, 255):
                if px[i, j] == (255, 0, 0, 255):
                    break
                returnVal = True
        if px[i, j] == (255, 0, 0, 255):
            break
    return returnVal


def draw_cross(img, p1: Point, p2: Point):
    draw = ImageDraw.Draw(img)
    draw.line([(p1.x+p2.x)/2, p1.y, (p1.x+p2.x)/2, p2.y], fill='red')
    draw.line([p1.x, (p1.y+p2.y)/2, p2.x, (p1.y+p2.y)/2], fill='red')
    img.save('result.png')
    print("Punkt ", p1.x, p1.y," i punkt ", p2.x, p2.y)


if __name__ == '__main__':
    #plt.figure(1)
    #clouds = []
    ##figure, axis = plt.subplots(2, 2, constrained_layout=True)
    #for i in range(4):
    #    newCloud = pointCloud(Point((i-2)*450+150, random.randrange(-750, 750)), 240)
    #    clouds.append(newCloud)
    #    col = np.random.rand(3,)
    #    #for pt in clouds[i].points:
    #        #axis[0, 0].plot(pt.x, pt.y, '.', color=col)
    #    hull = graham(clouds[i])
    #
    #    x, y = pointsToValueArray(hull)
    #
    #    #axis[0, 1].fill(x, y, facecolor='none', edgecolor='blue')
    #
    #    plt.fill(x, y, facecolor='black', edgecolor='none')
    #    #hull.clear()
    #    #x.clear()
    #    #y.clear()
    #plt.xlim(-1000, 1000)
    #plt.ylim(-1000, 1000)
    #plt.axis('off')
    #plt.savefig('shapes.png', dpi=80)
    #plt.show()

    sys.setrecursionlimit(5000)
    recursionlvl = 0
    with Image.open('shapes.png') as im:
        quadtree_plot(im, Point(0, 0), Point(im.width, im.height))
        #quadtreePlot(im, Point(0, 0), Point(im.width, im.height))
        #test(im)
    #beautifyPlot()
