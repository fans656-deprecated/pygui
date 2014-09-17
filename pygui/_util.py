from PySide.QtCore import QObject

class metaclass(QObject.__class__):
    def __new__(cls, name, bases, attrs):
        attrs['super'] = lambda self: super(self.__class__, self)
        return super(metaclass, cls).__new__(cls, name, bases, attrs)
