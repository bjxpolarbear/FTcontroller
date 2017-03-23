
from PyQt5.QtCore import pyqtProperty, pyqtSignal, QObject, QUrl
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView

import objectlistmodel_rc


class DataObject(QObject):

    nameChanged = pyqtSignal()

    @pyqtProperty(str, notify=nameChanged)
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if self._name != name:
            self._name = name
            self.nameChanged.emit()

    colorChanged = pyqtSignal()

    @pyqtProperty(str, notify=colorChanged)
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        if self._color != color:
            self._color = color
            self.colorChanged.emit()

    def __init__(self, name='', color='', parent=None):
        super(DataObject, self).__init__(parent)

        self._name = name
        self._color = color


if __name__ == '__main__':
    import sys

    app = QGuiApplication(sys.argv)

    dataList = [DataObject("Item 1", 'red'),
                DataObject("Item 2", 'green'),
                DataObject("Item 3", 'blue'),
                DataObject("Item 4", 'yellow')]

    view = QQuickView()
    view.setResizeMode(QQuickView.SizeRootObjectToView)
    ctxt = view.rootContext()
    ctxt.setContextProperty('myModel', dataList)

    view.setSource(QUrl('qrc:view.qml'))
    view.show()

    sys.exit(app.exec_())