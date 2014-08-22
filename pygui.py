import sys
import atexit

from PySide.QtCore import *
from PySide.QtGui import *

__all__ = []

def export(func):
    __all__.append(func.func_name)
    return func

@export
def do(func, *args, **kwas):
    return lambda: func(*args, **kwas)

@export
def key(keyname, callback):
    _keyDownHandlers.add(keyname, callback)

@export
def text(s):
    text.s = s
    _widget.update()
text.s = ''

_app = QApplication(sys.argv)

def _super(cls):
    setattr(cls, '_super', lambda self: super(cls, self))
    return cls

class HandlerDict:
    def __init__(self):
        self.d = {}

    def add(self, key, handler):
        if key not in self.d:
            self.d[key] = []
        self.d[key].append(handler)

    def __getitem__(self, key):
        return self.d[key]

_keyDownHandlers = HandlerDict()

@_super
class _Widget(QDialog):

    def __init__(self, parent=None):
        self._super().__init__(parent)
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        font = painter.font()
        font.setPixelSize(self.height() / 10.0)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignCenter, text.s)

    def keyPressEvent(self, event):
        global _keyDownHandlers
        try:
            handlers = _keyDownHandlers[event.text()]
            for handler in handlers:
                handler()
        except KeyError:
            self._super().keyPressEvent(event)

_widget = _Widget()

def _runQApp(app):
    app.exec_()

atexit.register(_runQApp, _app)
