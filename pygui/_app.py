import sys
import atexit

import _canvas
import _widget

from PySide.QtGui import QApplication

def runapp():
    persistants = []
    persistants.append(_canvas.canvas.postinit())
    persistants.append(_widget.widget.postinit())
    app.exec_()

app = QApplication(sys.argv)
atexit.register(runapp)
