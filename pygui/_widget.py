from PySide.QtCore import *
from PySide.QtGui import *

import _util
import _canvas

__metaclass__ = _util.metaclass

class WidgetManager:

    def postinit(self):
        widgets = []
        for g in _canvas.canvas.groups:
            w = Widget(canvas=g)
            g.widget = w
            widgets.append(w)
        desktop = QDesktopWidget()
        rcWork = desktop.availableGeometry()
        totalWidth = sum(w.frameGeometry().width() for w in widgets)
        x = rcWork.left() + (rcWork.width() - totalWidth) / 2.0
        y = rcWork.top() + (rcWork.height() - widgets[0].frameGeometry().height()) / 2.0
        for w in widgets:
            w.move(x, y)
            x += w.frameGeometry().width()
        return widgets


class Widget(QDialog):

    __metaclass__ = _util.metaclass

    def __init__(self, parent=None, canvas=None):
        self.super().__init__(parent)
        self.canvas = canvas
        self.resize(640, 480)
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        _canvas.canvas.painter = painter
        self.canvas.draw(QRectF(self.rect()))
        painter.end()

widget = WidgetManager()
