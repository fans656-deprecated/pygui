import sys
import atexit

from PySide.QtCore import *
from PySide.QtGui import *

__all__ = ['text']

def text(s):
    global _text
    _text += s + u'\n'

_app = QApplication(sys.argv)

def _super(cls):
    setattr(cls, '_super', lambda self: super(cls, self))
    return cls

@_super
class _Widget(QDialog):

    def __init__(self, parent=None):
        self._super().__init__(parent)
        self.show()

    def paintEvent(self, event):
        global _text
        painter = QPainter(self)
        font = painter.font()
        font.setPixelSize(self.height() / 10.0)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignCenter, _text)

_widget = _Widget()
_text = ''

def _runQApp(app):
    app.exec_()

atexit.register(_runQApp, _app)
