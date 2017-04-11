import pyqtgraph as pg

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
# from ScanData import *

import pdb
class SettingsUI(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.mainLayout = QGridLayout()

        self.masterLabel = QLabel('Master: ')
        self.masterEdit = QLineEdit()
        self.masterConnectBtn = QPushButton('Connect Master')
        self.masterDisconnectBtn = QPushButton('Disconnect Master')

        self.mainLayout.addWidget(self.masterLabel, 0, 0)
        self.mainLayout.addWidget(self.masterEdit, 0, 1)
        self.mainLayout.addWidget(self.masterConnectBtn, 1, 0)
        self.mainLayout.addWidget(self.masterDisconnectBtn, 1, 1)
        self.hline1 = QFrame()
        self.hline1.setFrameShape(QFrame.HLine)
        self.mainLayout.addWidget(self.hline1,2,0,1,2)

        self.slaveLabel = QLabel('Slave: ')
        self.slaveEdit = QLineEdit()
        self.slaveConnectBtn = QPushButton('Connect Slave')
        self.slaveDisconnectBtn = QPushButton('Disconnect Slave')

        self.mainLayout.addWidget(self.slaveLabel, 3, 0)
        self.mainLayout.addWidget(self.slaveEdit, 3, 1)
        self.mainLayout.addWidget(self.slaveConnectBtn, 4, 0)
        self.mainLayout.addWidget(self.slaveDisconnectBtn, 4, 1)



        self.setLayout(self.mainLayout)
        self.show()
        self.__connectSlots()

    def __connectSlots(self):
        mainwindow = self.parent()
        self.masterConnectBtn.clicked.connect(lambda: mainwindow.connectMasterSerial(self.masterEdit.text()))
        self.masterDisconnectBtn.clicked.connect(mainwindow.endMasterSerial)
        self.slaveConnectBtn.clicked.connect(lambda: mainwindow.connectSlaveSerial(self.slaveEdit.text()))
        self.slaveDisconnectBtn.clicked.connect(mainwindow.endSlaveSerial)

class PlotUI(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.mainLayout = QGridLayout()
        self.spectrumCanvas = pg.PlotWidget(self)
        self.mainLayout.addWidget(self.spectrumCanvas)

        self.setLayout(self.mainLayout)

    def plotSpec(self,x,y):
        self.spectrumCanvas.plot(x, y, clear=True)

class SegmentUI(QWidget):
    """docstring for Scan"""
    isChangedSignal = pyqtSignal()
    def __init__(self, parent=None):

        super(SegmentUI, self).__init__(parent=parent)

        ROW_NUM = 32

        # self.idx = idx_in
        self.name = ''
        self.nameLabel = QLabel('Name')
        self.nameLine = QLineEdit()
        self.durationLabel = QLabel('Duration')
        self.durationLine = QLineEdit()
        self.durationLine.setText('10')
        self.nameLayout = QHBoxLayout()
        self.nameLayout.addWidget(self.nameLabel, Qt.AlignTop)
        self.nameLayout.addWidget(self.nameLine, Qt.AlignTop)
        self.durationLayout = QHBoxLayout()
        self.durationLayout.addWidget(self.durationLabel, Qt.AlignTop)
        self.durationLayout.addWidget(self.durationLine, Qt.AlignTop)
        # self.nameLine.returnPressed.connect(self.change_name)

        self.segmentTypeText = 'f'
        self.segmentType = QComboBox()
        self.segmentType.addItem("Fixed")
        self.segmentType.addItem("Ramp")
        self.segmentType.addItem("Mass Analysis")
        self.segmentType.addItem("Dump")
        self.segmentType.addItem("Custom")

        self.segmentType.activated[str].connect(self.type_select)

        self.parameterLabel1 = QLabel()
        self.parameterBox1 = QLineEdit()
        self.parameter1 = QHBoxLayout()
        self.parameter1.addWidget(self.parameterLabel1, Qt.AlignTop)
        self.parameter1.addWidget(self.parameterBox1, Qt.AlignTop)

        self.parameterLabel2 = QLabel()
        self.parameterBox2 = QLineEdit()
        self.parameter2 = QHBoxLayout()
        self.parameter2.addWidget(self.parameterLabel2, Qt.AlignTop)
        self.parameter2.addWidget(self.parameterBox2, Qt.AlignTop)

        self.parameterLabel3 = QLabel()
        self.parameterBox3 = QLineEdit()
        self.parameter3 = QHBoxLayout()
        self.parameter3.addWidget(self.parameterLabel3, Qt.AlignTop)
        self.parameter3.addWidget(self.parameterBox3, Qt.AlignTop)

        self.parameterTable = QTableWidget()
        self.parameterTable.setColumnCount(1)
        self.parameterTable.setRowCount(ROW_NUM)

        self.parameterTable.horizontalHeader().setStretchLastSection(True)
        self.parameterTable.horizontalHeader().hide()
        self.parameterTable.verticalHeader().hide()
        self.parameterTable.verticalHeader().setDefaultSectionSize(24)
        for row in range(ROW_NUM//2,ROW_NUM):
            comboBox = QComboBox()
            comboBox.addItem('False')
            comboBox.addItem('True')
            self.parameterTable.setCellWidget(row, 0, comboBox)
        self.parameterTable.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.segmentLayout = QVBoxLayout()
        self.segmentLayout.addLayout(self.nameLayout)
        self.segmentLayout.addLayout(self.durationLayout)
        self.segmentLayout.addWidget(self.segmentType)
        self.segmentLayout.addLayout(self.parameter1)
        self.segmentLayout.addLayout(self.parameter2)
        self.segmentLayout.addLayout(self.parameter3)
        self.segmentLayout.addWidget(self.parameterTable)
        self.segmentLayout.setAlignment(Qt.AlignTop)

        self.setLayout(self.segmentLayout)

        self.setFixedWidth(220)

        self.type_select('Fixed')
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setFixedHeight(272+ROW_NUM*32)

    def type_select(self, inpStr):
        try:
            self.parameterBox1.textChanged.disconnect() #Ensure parameter1 and 2 aren't mirroring each other for other segment types
        except:
            pass

        if inpStr == 'Fixed':
            self.segmentTypeText = 'f'
            self.parameterLabel1.show()
            self.parameterBox1.show()
            self.parameterLabel2.show()
            self.parameterBox2.show()
            self.parameterLabel3.show()
            self.parameterBox3.show()
            self.parameterLabel1.setText("Start Frequency")
            self.parameterBox1.setText('100000')
            self.parameterBox1.setEnabled(True)
            self.parameterLabel2.setText("End Frequency")
            self.parameterBox2.setText(self.parameterBox1.text())
            self.parameterBox1.textChanged.connect(self.parameterBox2.setText) #Mirror parameter1 and 2 for Fixed frequency
            self.parameterBox2.setEnabled(False)
            self.parameterLabel3.setText("Duty Cycle")
            self.parameterBox3.setText('50')
            self.parameterBox3.setEnabled(True)
            self.parameterTable.show()

        elif inpStr == 'Ramp':
            self.segmentTypeText = 'r'
            self.parameterLabel1.show()
            self.parameterBox1.show()
            self.parameterLabel2.show()
            self.parameterBox2.show()
            self.parameterLabel3.show()
            self.parameterBox3.show()
            self.parameterLabel1.setText("Start Frequency")
            self.parameterBox1.setText('100000')
            self.parameterBox1.setEnabled(True)
            self.parameterLabel2.setText("End Frequency")
            self.parameterBox2.setText('200000')
            self.parameterBox2.setEnabled(True)
            self.parameterLabel3.setText("Duty Cycle")
            self.parameterBox3.setText('50')
            self.parameterBox3.setEnabled(True)
            self.parameterTable.show()

        elif inpStr == 'Mass Analysis':
            self.segmentTypeText = 'm'
            self.parameterLabel1.show()
            self.parameterBox1.show()
            self.parameterLabel2.show()
            self.parameterBox2.show()
            self.parameterLabel3.show()
            self.parameterBox3.show()
            self.parameterLabel1.setText("Start Frequency")
            self.parameterBox1.setText('400000')
            self.parameterBox1.setEnabled(True)
            self.parameterLabel2.setText("End Frequency")
            self.parameterBox2.setText('100000')
            self.parameterBox2.setEnabled(True)
            self.parameterLabel3.setText("ps per step")
            self.parameterBox3.setText('5')
            self.parameterBox3.setEnabled(True)
            self.parameterTable.show()

        elif inpStr == 'Dump':
            self.segmentTypeText = 'q'
            self.parameterLabel1.show()
            self.parameterBox1.show()
            self.parameterLabel2.show()
            self.parameterBox2.show()
            self.parameterLabel3.show()
            self.parameterBox3.show()
            self.parameterLabel1.setText("Start Frequency")
            self.parameterBox1.setText('N/A')
            self.parameterBox1.setEnabled(False)
            self.parameterLabel2.setText("End Frequency")
            self.parameterBox2.setText('N/A')
            self.parameterBox2.setEnabled(False)
            self.parameterLabel3.setText("Duty Cycle")
            self.parameterBox3.setText('N/A')
            self.parameterBox3.setEnabled(False)
            self.parameterTable.show()

        elif inpStr == 'Custom':
            self.segmentTypeText = 'c'
            self.parameterLabel1.show()
            self.parameterBox1.show()
            self.parameterLabel2.show()
            self.parameterBox2.show()
            self.parameterLabel3.show()
            self.parameterBox3.show()
            self.parameterLabel1.setText("Start Segment")
            self.parameterBox1.setText('1')
            self.parameterBox1.setEnabled(True)
            self.parameterLabel2.setText("End Segment")
            self.parameterBox2.setText('2')
            self.parameterBox2.setEnabled(True)
            self.parameterLabel3.setText("Iteration Number")
            self.parameterBox3.setText('3')
            self.parameterBox3.setEnabled(True)
            self.parameterTable.show()

        # Signals that segment changed - for real time plot updating
        self.segmentType.activated[str].connect(self.isChanged)
        self.parameterBox1.textChanged.connect(self.isChanged)
        self.parameterBox2.textChanged.connect(self.isChanged)
        self.parameterBox3.textChanged.connect(self.isChanged)
        self.durationLine.textChanged.connect(self.isChanged)

    def isChanged(self):
        self.isChangedSignal.emit()

    def toDict(self):
        outputDict={}
        outputDict['type']=self.segmentTypeText
        try:
            outputDict['para1']=float(self.parameterBox1.text())
        except ValueError:
            outputDict['para1'] = None
        try:
            outputDict['para2']=float(self.parameterBox2.text())
        except ValueError:
            outputDict['para2'] = None
        try:
            outputDict['para3']=float(self.parameterBox3.text())
        except ValueError:
            outputDict['para3'] = None
        try:
            outputDict['duration']=float(self.durationLine.text())
        except ValueError:
            outputDict['duration'] = None


        outputDict['analog']=[]
        for row in range(16):
            if self.parameterTable.item(row,0) == None:
                outputDict['analog'].append(None)
                continue
            try:
                outputDict['analog'].append(float(self.parameterTable.item(row,0).text()))
            except ValueError:
                self.parent.announce('Analog value error')


        outputDict['digital'] = []
        for row in range(16,32):

            if self.parameterTable.cellWidget(row, 0).currentText() == 'True':
                outputDict['digital'].append(True)
            elif self.parameterTable.cellWidget(row, 0).currentText() == 'False':
                outputDict['digital'].append(False)

        return outputDict

    def isValid(self):
        return True

'''
    def get_segmentdata(self):
        self.segmentData = SegmentData()
        # print(type(self.segmentTypeText))
        self.segmentData.duration = int(self.durationLine.text())

        self.segmentData.dw1data.type = self.segmentTypeText

        try:
            self.segmentData.dw1data.para1 = int(self.parameterBox1.text())
        except:
            self.segmentData.dw1data.para1 == None
        try:
            self.segmentData.dw1data.para2 = int(self.parameterBox2.text())
        except:
            self.segmentData.dw1data.para2 == None
        try:
            self.segmentData.dw1data.para3 = int(self.parameterBox3.text())
        except:
            self.segmentData.dw1data.para3 == None

        for i in range(16):
            if self.parameterTable.item(i, 0) is None:
                self.segmentData.analog_ini[i] = None
            else:
                self.segmentData.analog_ini[i] = int(self.parameterTable.item(i, 0).text())

        for i in range(16):
            if self.parameterTable.cellWidget(i+16, 0).currentText() == 'True':
                self.segmentData.binary[i] = True
            elif self.parameterTable.cellWidget(i+16, 0).currentText() == 'False':
                self.segmentData.binary[i] = False

        return self.segmentData

    def get_segmentplot(self):
        self.get_segmentdata()
        x = list(range(1, self.segmentData.duration + 1))
        if self.segmentData.dw1data.type == 'f':
            y = [self.segmentData.dw1data.para1] * len(x)
            return (x, y)
        elif self.segmentData.dw1data.type in {'r', 'm'}:
            y = []
            for i in range(len(x)):
                y.append(self.segmentData.dw1data.para1 + (
                self.segmentData.dw1data.para2 - self.segmentData.dw1data.para1) / len(x) * i)
            return (x, y)
        elif self.segmentData.dw1data.type == 'q':
            y = [0] * len(x)
            return (x, y)

        elif self.segmentData.dw1data.type == 'c':
            x = []
            y = []
            for i in range(self.segmentData.dw1data.para3):
                # for segmentUI in FishTankEngine.instance().main_UI.currentScanUI.segmentUIList[
                #                  self.segmentData.dw1data.para1 - 1:self.segmentData.dw1data.para2]:
                #     (tmpX, tmpY) = segmentUI.get_segmentplot()
                #     if x == []:
                #         x = tmpX
                #     else:
                #         x += [a + x[-1] for a in tmpX]
                #     y += tmpY
                pass
            return (x, y)

'''
'''
class ScanUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # this is the list container for the segmentUIs
        self.segmentUIList = []
        self.scanData = ScanData()
        # this is an area to display the segments
        self.scanArea = QScrollArea()
        # this will be the parent widget of all segments
        self.scanContent = QWidget()
        # this will be the layout of the parent widget
        self.scanLayout = QHBoxLayout()

        # set the relationship
        self.scanContent.setLayout(self.scanLayout)
        self.scanArea.setWidget(self.scanContent)
        self.scanLayout.setAlignment(Qt.AlignLeft)
        # Important: allow the widget to update the size dynamically
        self.scanArea.setWidgetResizable(True)

        self.addSegmentBtn = QPushButton('Add')
        self.removeSegmentBtn = QPushButton('Remove')
        self.insertSegmentBtn = QPushButton('Insert')

        self.btnLayout3 = QVBoxLayout()
        self.btnLayout3.addWidget(self.addSegmentBtn)
        self.btnLayout3.addWidget(self.insertSegmentBtn)
        self.btnLayout3.addWidget(self.removeSegmentBtn)
        self.btnLayout3.setAlignment(Qt.AlignTop)

        layout = QHBoxLayout()

        layout.addLayout(self.btnLayout3)
        layout.addWidget(self.scanArea)
        self.setLayout(layout)

        self.add_segment()

    def add_segment(self):

        self.segmentUIList.append(SegmentUI())
        self.scanLayout.addWidget(self.segmentUIList[-1])
        try:
            pass
            # FishTankEngine.instance().main_UI
        except:
            pass
        else:
            pass
            # FishTankEngine.instance().announce(('There are ' + str(len(self.segmentUIList)) + ' segments.'))

    def remove_segment(self):
        if len(self.segmentUIList) > 0:
            # I am not sure why it need to be hided pre remove, but otherwise bugs show up
            self.segmentUIList[-1].hide()
            self.scanLayout.removeWidget(self.segmentUIList[-1])
            del (self.segmentUIList[-1])
        else:
            pass
            # FishTankEngine.instance().announce('Error: You need at least one segment')

    def get_scandata(self):
        self.scanData = ScanData()
        for segmentUI in self.segmentUIList:
            segmentUI.get_segmentdata()
            self.scanData.segment_list.append(segmentUI.get_segmentdata())

        return self.scanData

    def get_scanplot(self):
        self.get_scandata()
        x = []
        y = []
        for segmentUI in self.segmentUIList:
            (tmpX, tmpY) = segmentUI.get_segmentplot()
            if x == []:
                x = tmpX
            else:
                x += [a + x[-1] for a in tmpX]
            y += tmpY
        return (x, y)
'''
