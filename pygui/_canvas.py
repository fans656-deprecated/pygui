from PySide.QtCore import *
from PySide.QtGui import *

import _util

__all__ = ['canvas',
           'drawtext',
           'drawellipse',
           'fillellipse',
           'drawrect',
           'fillrect',
           'rect',
           'width',
           'height',
           'setpen',
           'setbrush',
           'setfont',]
__metaclass__ = _util.metaclass

def drawtext(s):
    painter = canvas.painter
    painter.drawText(rect(), Qt.AlignCenter, s)

def drawrect(rc):
    painter = canvas.painter
    painter.drawRect(rc)

def fillrect(rc):
    painter = canvas.painter
    painter.fillRect(rc, painter.brush())

def drawellipse(*args):
    painter = canvas.painter
    painter.drawEllipse(*args)

def fillellipse(rc):
    painter = canvas.painter
    brush = painter.brush()
    brush.setStyle(Qt.SolidPattern)
    painter.setBrush(brush)
    path = QPainterPath()
    path.addEllipse(rc)
    painter.fillPath(path, painter.brush())

def rect():
    return canvas.paintRect

def width():
    return rect().width()

def height():
    return rect().height()

def setpen(color=Qt.black, width=1):
    pen = canvas.painter.pen()
    pen.setColor(color)
    pen.setWidth(width)
    canvas.painter.setPen(pen)

def setbrush(color=Qt.black):
    brush = canvas.painter.brush()
    brush.setStyle(Qt.SolidPattern)
    brush.setColor(color)
    canvas.painter.setBrush(brush)

def setfont(pointsize=11):
    font = canvas.painter.font()
    font.setPointSize(pointsize)
    canvas.painter.setFont(font)

class CanvasManager:

    def __init__(self):
        self.counter = 0
        self.name2canvas = {}
        self.groups = []

    def __call__(self, *args):
        # canvas(drawer)
        if len(args) == 1:
            if hasattr(args[0], '__call__'):
                name = self.genAnonymousName()
                drawer = args[0]
            else:
                raise Exception('{} is not a callable drawer'.format(repr(args[0])))
        # canvas(name, drawer)
        elif len(args) == 2:
            name = args[0]
            drawer = args[1]
        else:
            raise Exception('Wrong arguments')
        # construct a Canvas()
        c = Canvas(name, drawer)
        self.add(c)
        return SingletonCanvasGroup(c)

    def __getitem__(self, name):
        return self.name2canvas[name]

    def postinit(self):
        self.clearLeafGroups()

    def genAnonymousName(self):
        index = self.counter
        self.counter += 1
        return str(index)

    def add(self, canvas):
        name = canvas.name
        if name in self.name2canvas:
            raise Exception('name "{}" already exists'.format(name))
        else:
            self.name2canvas[name] = canvas

    def addGroup(self, g):
        self.groups.append(g)
        return g

    def clearLeafGroups(self):
        self.groups = [g for g in self.groups if not g.parent]

class Canvas:
    def __init__(self, name='', drawer=None):
        self.name = name
        self.drawer = drawer

    def draw(self, rc):
        canvas.paintRect = rc
        canvas.painter.save()
        self.drawer()
        canvas.painter.restore()

    def __repr__(self):
        return self.name

class CanvasGroup:
    def __init__(self, *children):
        self.initBasic(*children)
        self.setChildrenParent()

    def draw(self, rc):
        self.layoutChildren(rc)

    def initBasic(self, *children):
        self.weight = 1
        self.parent = None
        self.children = list(children)
        canvas.addGroup(self)

    def setChildrenParent(self):
        for c in self.children:
            c.parent = self

    def layoutChildren(self, rcAvail):
        share = int(self.getLayoutAvail(rcAvail))
        totalWeight = sum(c.weight for c in self.children)
        take = lambda c: int(share * c.weight / totalWeight)
        takes = [take(c) for c in self.children]
        share -= sum(takes)
        takes[:share] = [t + 1 for t in takes[:share]]
        index = self.getLayoutInitial(rcAvail)
        for c, take in zip(self.children, takes):
            rc = self.getLayoutRect(rcAvail, index, take)
            c.layoutChildren(rc)
            index += take

    # set weight
    def __mul__(self, weight):
        self.weight = weight
        return self

    # layout horizontally
    def __or__(self, other):
        return HorzCanvasGroup(self, other)

    # layout vertically
    def __sub__(self, other):
        return VertCanvasGroup(self, other)

class HorzCanvasGroup(CanvasGroup):

    def getLayoutAvail(self, rc):
        return rc.width()

    def getLayoutInitial(self, rc):
        return rc.left()

    def getLayoutRect(self, rc, x, width):
        return QRectF(x, rc.top(), width - 1, rc.height())

    # layout horizontally
    def __or__(self, other):
        other.parent = self
        self.children.append(other)
        return self

    def __repr__(self):
        return '({})'.format('|'.join(map(str, self.children)))

class VertCanvasGroup(CanvasGroup):

    def getLayoutAvail(self, rc):
        return rc.height()

    def getLayoutInitial(self, rc):
        return rc.top()

    def getLayoutRect(self, rc, y, height):
        return QRectF(rc.left(), y, rc.width(), height - 1)

    # layout vertically
    def __sub__(self, other):
        other.parent = self
        self.children.append(other)
        return self

    def __repr__(self):
        return '({})'.format('-'.join(map(str, self.children)))

class SingletonCanvasGroup(CanvasGroup):

    def layoutChildren(self, rcAvail):
        c = self.children[0]
        c.draw(rcAvail)

    def __init__(self, cvs):
        self.initBasic(cvs)

    def __repr__(self):
        return repr(self.children[0])

canvas = CanvasManager()
