from pygui import *
from PySide.QtGui import *

def adraw():
    setfont(16)
    drawrect(rect())
    drawtext('canvas a')

def bdraw():
    setbrush(color=QColor(0,0,255))
    fillellipse(rect())
    setfont(200)
    drawtext('b')

def cdraw():
    setfont(40)
    setpen(color=QColor(200,0,0))
    drawtext('this is the c canvas')

a = canvas(adraw)
b = canvas(bdraw)
c = canvas(cdraw)
((a - a) | b * 2 | a) - c
