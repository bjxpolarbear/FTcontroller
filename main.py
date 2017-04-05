#Hi Jason! How are you?
#I am great!
import os
import sys
import pdb
import json
import serial
import threading
import pyqtgraph as pg
from time import sleep

from ui.ui_mainwindowftcontroller import Ui_MainWindow

from ui.UIs import SegmentUI, SettingsUI, PlotUI
from PyQtGraphSerialReader import SerialReader

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class FTMainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)
        # self.model = scanClass.ScanListModel()
        self.scanList = []

        self.scanContent = QWidget()
        self.scanLayout = QHBoxLayout()
        self.scanContent.setLayout(self.scanLayout)
        self.scanArea.setWidget(self.scanContent)
        self.scanLayout.setAlignment(Qt.AlignLeft)
        # (min,max) = self.splitter.getRange(0)  #trying to set the default position of the splitter
        # self.splitter.moveSplitter(max,0)



        self.__genHeader()
        self.__genPlot()
        # self.scanArea.setWidgetResizable(True)      #Important: allow the widget to update the size dynamically
        self.__connectSlot()

    def __genHeader(self):
        self.headerTable = QTableWidget()
        self.headerTable.setColumnCount(1)
        self.headerTable.setRowCount(32)
        self.headerTable.horizontalHeader().hide()
        self.headerTable.verticalHeader().hide()
        self.headerTable.horizontalHeader().setStretchLastSection(True)
        self.headerTable.setFixedWidth(80)
        self.headerTable.setFixedHeight(1055)
        self.headerTable.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.headerTable.verticalHeader().setDefaultSectionSize(24)
        self.headerSpacer = QSpacerItem(80, 90, QSizePolicy.Fixed)
        self.headerLayout = QVBoxLayout()
        self.headerLayout.addItem(self.headerSpacer)
        self.headerLayout.addWidget(self.headerTable)
        self.scanLayout.addLayout(self.headerLayout)

        for row in range(16):
            self.headerTable.setItem(row, 0, QTableWidgetItem("A "+str(row+1)))
        for row in range(16,32):
            self.headerTable.setItem(row, 0, QTableWidgetItem("D "+str(row-15)))

    def __genPlot(self):

        self.specDialog = PlotUI(self)
        self.specDialog.show()

    def __connectSlot(self):
        self.addBtn.clicked.connect(self.addSegment)
        self.removeBtn.clicked.connect(self.removeSegment)
        self.downloadBtn.clicked.connect(self.downloadScan)

        self.actionSettings.triggered.connect(self.settingsDialog)

    def removeSegment(self):

        if len(self.scanList)>0:
            # pdb.set_trace()
            self.scanList[-1].hide()
            self.scanLayout.removeWidget(self.scanList[-1])
            self.scanList.pop()

            self.announce('Last segment removed!')
        else:
            self.announce('Not enough segments')



    def addSegment(self):
        self.scanList.append(SegmentUI(parent=self))
        self.scanLayout.addWidget(self.scanList[-1])
        self.announce('One segment added!')

    def announce(self, text):
        self.announcer.appendPlainText(text)


    def isValid(self):
        pass

    def toJSON(self):
        tmpScanList = []
        for segment in self.scanList:
            tmpScanList.append(segment.toDict())
        outputDict={}
        outputDict['job']='download'
        outputDict['data']=tmpScanList
        outputString = json.dumps(outputDict,sort_keys=True)

        self.announce(outputString)
        return outputString

    def downloadScan(self):
        '''
        x= [1,2,3,4,5,6,7,8,9]
        y= [1,0,-1,1,0,-1,1,0,-1,]
        self.specDialog.plotSpec(x,y)
        '''
        outputString = self.toJSON()
        if self.serialPort:
            #self.serialPort.ser_write(outputString)
            self.announce("Scan downloaded")
        else:
            self.announce("No serial port found!")



    def settingsDialog(self):
        self.settingsDialog = SettingsUI(self)

        self.settingsDialog.show()

    def listenThread(self):
        self.announce('The start of listenThread')

        while self.serialPort.statusOn:
            sleep(0.1)
            if self.serialPort.ser_read_inner:
                line = self.serialPort.ser_read_inner()
                if line is not None:
                    print(line)
                # self.announce(line)

    def connectMasterSerial(self, port):
        try:
            self.serialPort = SerialPort(port=port)#,parent=self)

        except OSError:
            self.announce('Master Connection Failed')
        else:
            self.announce('Master Serial Connected')
        # strIn = self.serialPort.ser_read_inner()
        # self.announce(strIn)
        # pdb.set_trace()
        self.readThread = threading.Thread(target=self.listenThread)
        self.readThread.start()


    def endMasterSerial(self):
        try:
            self.serialPort.ser_write(b'E')
            self.serialPort.statusOn = False
            self.serialPort.ser.close()
            self.announce('Master serial port terminated')
        except:
            self.announce('Error: No master serial found')

    def connectSlaveSerial(self, port):
        try:
            self.slaveSerialPort = SerialPort(port)
        except OSError:
            self.announce('Slave Connection Failed')
        else:
            self.announce('Slave Serial Connected')

    def endSlaveSerial(self):
        try:
            self.slaveSerialPort.ser_write(b'E')
            self.slaveSerialPort.statusOn = False
            self.slaveSerialPort.ser.close()
            self.announce('Slave serial port terminated')
        except:
            self.announce('Error: No slave serial found')




class SerialPort(QWidget):
    def __init__(self, parent=None, port=None):
        super().__init__()


        self.ser = serial.Serial(port, baudrate=115200, timeout=0)
        self.statusOn = True



    def ser_write(self, inStr):
        inStr = inStr + '#'

        self.statusOn = False
        self.ser.write(inStr.encode('ascii'))
        self.statusOn = True

    # def ser_read_outer(self):
    #     timer_readFromArduino = QTimer(self)
    #     timer_readFromArduino.timeout.connect(self.ser_read_inner)
    #     timer_readFromArduino.start(100)

    def ser_read_inner(self):
        # pdb.set_trace()
        # print('read inner')
        if self.ser and self.statusOn:
            line = self.ser.readline().decode('ascii').strip('\r\n')
            if line is not '':
                # print(line)
                return line



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = FTMainWindow()
    form.show()
    app.exec_()

