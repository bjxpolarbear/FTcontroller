import sys

import serial
import threading
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *



# from tictoc import *

# import pyqtgraph as pg

from ScanData import *          ## All data structure used to store the scan
from PyQtGraphSerialReader import *         ## A fetching script from a given serial port





class MainUI(QMainWindow):

    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent=parent)
        
        self.setMinimumSize(800,600)

        self.currentScanUI = ScanUI(self)

        self.announcer = QTextEdit()
        self.announcer.setReadOnly(True)
        # self.announcer.setFixedHeight(100)
        self.announcer.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)
        self.announcer.ensureCursorVisible()

        self.masterPortLabel = QLabel("Master Port: ")
        # self.masterPortLabel.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Ignored)
        self.masterPortText = QLineEdit("COM5")
        # self.masterPortText.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Ignored)
        self.slavePortLabel = QLabel("Slave Port: ")
        # self.slavePortLabel.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Ignored)
        self.slavePortText = QLineEdit("COM7")
        # self.slavePortText.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Ignored)
        self.portLayout1 = QHBoxLayout()
        self.portLayout2 = QHBoxLayout()
        self.portLayout1.addWidget(self.masterPortLabel,Qt.AlignTop)
        self.portLayout1.addWidget(self.masterPortText,Qt.AlignTop)
        self.portLayout2.addWidget(self.slavePortLabel,Qt.AlignTop)
        self.portLayout2.addWidget(self.slavePortText,Qt.AlignTop)
        self.portLayout = QVBoxLayout()
        self.portLayout.addLayout(self.portLayout1)
        self.portLayout.addLayout(self.portLayout2)
        self.portLayout.setAlignment(Qt.AlignLeft)

        self.endMasterSerialBtn = QPushButton('End Master Serial')
        self.endSlaveSerialBtn = QPushButton('End Slave Serial')
        self.connectMasterSerialBtn = QPushButton('Connect Master Serial')
        self.connectSlaveSerialBtn = QPushButton('Connect Slave Serial')
        self.resetMasterBtn = QPushButton('Reset Master')
        self.resetSlaveBtn = QPushButton('Reset Slave')
        self.startListenBtn = QPushButton('Start Listen')
        self.stopListenBtn = QPushButton('Stop Listen')
        self.runBtn = QPushButton('Run')
        self.stopBtn = QPushButton('Stop')
        self.downloadBtn = QPushButton('Download')
        self.uploadBtn = QPushButton('Upload')


        self.btnLayout = QGridLayout()

        self.btnLayout.addWidget(self.downloadBtn,0,2)
        self.btnLayout.addWidget(self.uploadBtn,1,2)
        self.btnLayout.addWidget(self.runBtn,2,2)
        self.btnLayout.addWidget(self.stopBtn,3,2)
        self.btnLayout.addWidget(self.resetMasterBtn,0,1)
        self.btnLayout.addWidget(self.resetSlaveBtn,1,1)
        self.btnLayout.addWidget(self.endMasterSerialBtn,2,1)
        self.btnLayout.addWidget(self.endSlaveSerialBtn,3,1)
        self.btnLayout.addWidget(self.connectMasterSerialBtn,0,0)
        self.btnLayout.addWidget(self.connectSlaveSerialBtn,1,0)
        self.btnLayout.addWidget(self.startListenBtn,2,0)
        self.btnLayout.addWidget(self.stopListenBtn,3,0)

        # self.plotTab = QTabWidget()
        # self.plotTab.setFixedHeight(275)
        # self.scanCanvas = pg.PlotWidget(self)
        # self.plotTab.addTab(self.scanCanvas,'Scan Function')
        # self.spectrumCanvas = pg.PlotWidget(self)
        # self.plotTab.addTab(self.spectrumCanvas,'Spectrum')

        layout = QGridLayout()

        layout.addLayout(self.btnLayout,0,1)
        layout.addWidget(self.announcer,1,1,2,1)
        layout.addWidget(self.currentScanUI,1,0)
        # layout.addWidget(self.plotTab,2,0)
        layout.addLayout(self.portLayout,0,0,alignment = Qt.AlignRight)
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(layout)
        self.setCentralWidget(self.mainWidget)
        # self.mainWidget.layout().addWidget(self.currentScanUI)


    def closeEvent(self, event):
        FishTankEngine.instance().announce('CLOSING!!!!!')
        FishTankEngine.instance().end_master_serial()
        FishTankEngine.instance().end_slave_serial()
        event.accept()


class SegmentUI(QWidget):
    """docstring for Scan"""
    def __init__(self , parent=None):
        super(SegmentUI, self).__init__(parent=parent)
        
        # self.idx = idx_in
        self.name = ''
        self.nameLabel = QLabel('Name')
        self.nameLine = QLineEdit()
        self.durationLabel = QLabel('Duration')
        self.durationLine = QLineEdit()
        self.durationLine.setText('10')
        self.nameLayout =QHBoxLayout()
        self.nameLayout.addWidget(self.nameLabel,Qt.AlignTop)
        self.nameLayout.addWidget(self.nameLine,Qt.AlignTop)
        self.durationLayout =QHBoxLayout()
        self.durationLayout.addWidget(self.durationLabel,Qt.AlignTop)
        self.durationLayout.addWidget(self.durationLine,Qt.AlignTop)
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
        self.parameter1.addWidget(self.parameterLabel1,Qt.AlignTop)
        self.parameter1.addWidget(self.parameterBox1,Qt.AlignTop)

        self.parameterLabel2 = QLabel()
        self.parameterBox2 = QLineEdit()
        self.parameter2 = QHBoxLayout()
        self.parameter2.addWidget(self.parameterLabel2,Qt.AlignTop)
        self.parameter2.addWidget(self.parameterBox2,Qt.AlignTop)

        self.parameterLabel3 = QLabel('')
        self.parameterBox3 = QLineEdit()
        self.parameter3 = QHBoxLayout()
        self.parameter3.addWidget(self.parameterLabel3,Qt.AlignTop)
        self.parameter3.addWidget(self.parameterBox3,Qt.AlignTop)



        self.parameterTable = QTableWidget()
        self.parameterTable.setColumnCount(2)
        self.parameterTable.setRowCount(32)
        self.parameterTable.setColumnWidth(0,70)
        self.parameterTable.setColumnWidth(1,70)
        self.parameterTable.setHorizontalHeaderLabels(['Analog','Digital'])
        for row in range(32):
            comboBox = QComboBox()
            comboBox.addItem('True')
            comboBox.addItem('False')
            self.parameterTable.setCellWidget(row,1,comboBox)
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

        self.setFixedWidth(240)

        self.type_select('Fixed')
        self.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.setFixedHeight(1150)

    def type_select(self, inpStr):
        if inpStr == 'Fixed':
            self.segmentTypeText = 'f'
            self.parameterLabel1.show()
            self.parameterBox1.show()
            self.parameterLabel2.show()
            self.parameterBox2.show()           
            self.parameterLabel3.hide()
            self.parameterBox3.hide()           
            self.parameterLabel1.setText("Frequency: ")
            self.parameterBox1.setText('100000')
            self.parameterLabel2.setText("Duty Cycle: ")
            self.parameterBox2.setText('50')
            self.parameterLabel3.setText("")
            self.parameterTable.show()

        elif inpStr == 'Ramp':
            self.segmentTypeText = 'r'
            self.parameterLabel1.show()
            self.parameterBox1.show()
            self.parameterLabel2.show()
            self.parameterBox2.show()           
            self.parameterLabel3.show()
            self.parameterBox3.show()           
            self.parameterLabel1.setText("Start Frequency: ")
            self.parameterBox1.setText('100000')
            self.parameterLabel2.setText("End Frequency: ")
            self.parameterBox2.setText('200000')
            self.parameterLabel3.setText("Duty Cycle: ")
            self.parameterBox3.setText('50')
            self.parameterTable.show()


        elif inpStr == 'Mass Analysis':
            self.segmentTypeText = 'm'
            self.parameterLabel1.show()
            self.parameterBox1.show()
            self.parameterLabel2.show()
            self.parameterBox2.show()           
            self.parameterLabel3.show()
            self.parameterBox3.show()           
            self.parameterLabel1.setText("Start Frequency: ")
            self.parameterBox1.setText('400000')
            self.parameterLabel2.setText("End Frequency: ")
            self.parameterBox1.setText('100000')
            self.parameterLabel3.setText("ps per step: ")
            self.parameterBox1.setText('5')
            self.parameterTable.show()

        elif inpStr == 'Dump':
            self.segmentTypeText = 'q'
            self.parameterLabel1.hide()
            self.parameterBox1.hide()
            self.parameterLabel2.hide()
            self.parameterBox2.hide()           
            self.parameterLabel3.hide()
            self.parameterBox3.hide()           
            self.parameterLabel1.setText("0")
            self.parameterLabel2.setText("0")
            self.parameterLabel3.setText("0")
            self.parameterTable.hide()

        elif inpStr == 'Custom':
            self.segmentTypeText = 'c'
            self.parameterLabel1.show()
            self.parameterBox1.show()
            self.parameterLabel2.show()
            self.parameterBox2.show()           
            self.parameterLabel3.show()
            self.parameterBox3.show()           
            self.parameterLabel1.setText("Start Segment: ")
            self.parameterBox1.setText('1')
            self.parameterLabel2.setText("End Segment: ")
            self.parameterBox2.setText('2')
            self.parameterLabel3.setText("Iteration Number: ")
            self.parameterBox3.setText('3')
            self.parameterTable.hide()

    def get_segmentdata(self):
        self.segmentData = SegmentData()
        # print(type(self.segmentTypeText))
        self.segmentData.duration = int(self.durationLine.text())

        self.segmentData.dw1data.type = self.segmentTypeText
      
        try:
            self.segmentData.dw1data.para1 = int(self.parameterBox1.text())
        except :
            self.segmentData.dw1data.para1 == None
        try:
            self.segmentData.dw1data.para2 = int(self.parameterBox2.text())
        except :
            self.segmentData.dw1data.para2 == None
        try:
            self.segmentData.dw1data.para3 = int(self.parameterBox3.text())
        except :
            self.segmentData.dw1data.para3 == None

        for i in range(24):
            if self.parameterTable.item(i,0) is None:
                self.segmentData.analog_ini[i] = None
            else:
                self.segmentData.analog_ini[i] = int(self.parameterTable.item(i,0).text())
        
        for i in range(32):
            if self.parameterTable.cellWidget(i,1).currentText() == 'True':
               self.segmentData.binary[i] = True
            elif self.parameterTable.cellWidget(i,1).currentText() == 'False':
               self.segmentData.binary[i] = False

        return self.segmentData

    def get_segmentplot(self):
        self.get_segmentdata()
        x = list(range(1,self.segmentData.duration+1))
        if self.segmentData.dw1data.type == 'f':
            y = [self.segmentData.dw1data.para1]*len(x)
            return (x,y)
        elif self.segmentData.dw1data.type in {'r','m'}:
            y = []
            for i in range(len(x)):
                y.append(self.segmentData.dw1data.para1+(self.segmentData.dw1data.para2-self.segmentData.dw1data.para1)/len(x)*i)
            return (x,y)
        elif self.segmentData.dw1data.type == 'q':
            y = [0]*len(x)
            return (x,y)
            
        elif self.segmentData.dw1data.type == 'c':
            x = []
            y = []
            for i in range(self.segmentData.dw1data.para3):
                for segmentUI in FishTankEngine.instance().main_UI.currentScanUI.segmentUIList[self.segmentData.dw1data.para1-1:self.segmentData.dw1data.para2]:
                    (tmpX, tmpY) = segmentUI.get_segmentplot()
                    if x == []:
                        x =tmpX
                    else:
                        x += [a+x[-1] for a in tmpX]
                    y += tmpY
            return (x,y)


class ScanUI(QWidget):
    

    def __init__(self,parent=None):
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
        #Important: allow the widget to update the size dynamically
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
             FishTankEngine.instance().main_UI
        except:
             pass
        else:
            FishTankEngine.instance().announce(('There are ' + str(len(self.segmentUIList)) + ' segments.'))


    def remove_segment(self):
        if len(self.segmentUIList) > 0:
            # I am not sure why it need to be hided pre remove, but otherwise bugs show up
            self.segmentUIList[-1].hide()                    
            self.scanLayout.removeWidget(self.segmentUIList[-1])
            del(self.segmentUIList[-1])
        else:
            FishTankEngine.instance().announce('Error: You need at least one segment')
            

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
                x =tmpX
            else:
                x += [a+x[-1] for a in tmpX]
            y += tmpY
        return (x,y)


class FishTankEngine(QApplication):

    def __init__(self, args):
        super(FishTankEngine, self).__init__(args)
        
        self.main_UI = MainUI()
        self.main_UI.show()
        self.__conect_slots()
        
        
        # self.serialSlaveReader = SerialReader(self.serialSlavePort)
        # self.serialSlaveReader.start()

        # self.displaySerialThread = threading.Thread(target=self.display_serial)
        # self.displaySerialThread.start()


        timer_scan = QTimer(self)
        timer_scan.timeout.connect(self.update_scanplot)
        timer_scan.start(200)


        


        '''
    def display_serial(self):
        while True:
            if len(self.serialPort.readThread.buffer) > 0:
                print(self.serialPort.readThread.buffer[0])
                self.main_UI.announcer.append(str(self.serialPort.readThread.buffer.pop(0)))
        '''
    def __conect_slots(self):
        self.setQuitOnLastWindowClosed(True)

        self.main_UI.runBtn.clicked.connect(self.run_scan)
        self.main_UI.stopBtn.clicked.connect(self.stop_scan)
        self.main_UI.downloadBtn.clicked.connect(self.download_scan)
        self.main_UI.uploadBtn.clicked.connect(self.upload_scan)
        self.main_UI.resetMasterBtn.clicked.connect(self.reset_master)
        self.main_UI.resetSlaveBtn.clicked.connect(self.reset_slave)
        self.main_UI.endMasterSerialBtn.clicked.connect(self.end_master_serial)
        self.main_UI.endSlaveSerialBtn.clicked.connect(self.end_slave_serial)
        self.main_UI.connectMasterSerialBtn.clicked.connect(lambda: self.connect_master_serial(self.main_UI.masterPortText.text()))
        self.main_UI.connectSlaveSerialBtn.clicked.connect(lambda: self.connect_slave_serial(self.main_UI.slavePortText.text()))
        self.main_UI.startListenBtn.clicked.connect(self.start_listen)
        self.main_UI.stopListenBtn.clicked.connect(self.stop_listen)
        self.main_UI.currentScanUI.addSegmentBtn.clicked.connect(self.main_UI.currentScanUI.add_segment)
        self.main_UI.currentScanUI.removeSegmentBtn.clicked.connect(self.main_UI.currentScanUI.remove_segment)



    def connect_slave_serial(self, port):
        try:
            self.serialSlavePort = serial.Serial(port)
            self.serialSlaveReader = SerialReader(self.serialSlavePort)
            self.serialSlaveReader.start()
        except OSError:
            self.announce('Slave Connection Failed')
        else:
            self.announce('Slave Serial Connected')
        
    def end_master_serial(self):
        try:
            self.serialPort.ser_write(b'E')
            self.serialPort.statusOn = False
            self.serialPort.ser.close()
            self.announce('I terminated the master serial port')
        except:
            self.announce('No master serial found')

    def end_slave_serial(self):
        try:
            # self.serialSlavePort.close()
            self.serialSlaveReader.port.close()
            self.announce('I terminated the slave serial port')
        except:
            self.announce('No slave serial found')

    def start_listen(self):
        self.timer_spec = QTimer(self)
        self.timer_spec.timeout.connect(self.serial_plot_update)
        self.timer_spec.start(0)
        self.announce('Plotting started')

    def stop_listen(self):
        self.timer_spec.stop()
        self.announce('Plotting stopped')


    def serial_plot_update(self):
        
        t,v,r = self.serialSlaveReader.get(1000*1024, downsample=1)
        
        self.main_UI.spectrumCanvas.plot(t, v, clear=True)
        self.main_UI.spectrumCanvas.setTitle('Sample Rate: %0.2f'%r)
        
        '''
        if not self.main_UI.spectrumCanvas.isVisible():
            self.serialSlaveReader.exit()
            self.timer_spec.stop()
        # toc()   
        '''

    def update_scanplot(self):
        # (x,y) = self.main_UI.currentScanUI.get_scanplot()
        # self.main_UI.scanCanvas.plot(x, y, clear=True)
        pass

    def run_scan(self):
        self.serialPort.ser_write(b'R')
        self.announce('I ran')

    def stop_scan(self):
        self.serialPort.ser_write(b'S')
        self.announce('I stopped')

    def upload_scan(self):
        self.serialPort.ser_write(b'U')
        self.announce('I asked upload')

    def download_scan(self):
        # self.serialPort.ser_write(b'S')
        self.announce('I downloaded')
        self.currentScanData = self.main_UI.currentScanUI.get_scandata()
        tmpStr = self.currentScanData.pack_scan_data()
        self.announce(tmpStr)
        self.serialPort.ser_write(tmpStr.encode('ascii'))

    def reset_master(self):
        self.serialPort.ser_write(b'X')
        self.announce('I reset master')

    def reset_slave(self):
        self.serialPort.ser_write(b'Z')
        self.announce('I reset slave')

    def announce(self, text, *remote ):
        # announce the text in the announcer in the program
        cursor = self.main_UI.announcer.textCursor()
        # cursor.movePosition(QTextCursor.End)
        self.main_UI.announcer.setTextCursor(cursor)
        if len(remote) > 0:
            self.main_UI.announcer.insertPlainText(('Remote: '+ str(text)))
        else:
            self.main_UI.announcer.insertPlainText(('Local: '+ str(text) + '\r\n'))
        


class SerialPort(QWidget):
    

    def __init__(self, *arg):
        super(SerialPort, self).__init__()
        self.ser = serial.Serial(*arg, baudrate=115200, timeout = 0)
        self.statusOn = True

        self.readThread = threading.Thread(target=self.ser_read_inner)
        self.readThread.start()

    def ser_write(self, inStr):
        self.statusOn = False
        self.ser.write(inStr)
        self.statusOn = True
        

    # def ser_read_outer(self):
    #     timer_readFromArduino = QTimer(self)
    #     timer_readFromArduino.timeout.connect(self.ser_read_inner)
    #     timer_readFromArduino.start(100)

    def ser_read_inner(self):
        while self.statusOn:
            line = self.ser.readline().decode('ascii')
            
            # time.sleep(0.1)
            if len(line) > 0:
                print(line)
                FishTankEngine.instance().announce(str(line),1)
                

if __name__ == "__main__":
    
    ft_engine = FishTankEngine(sys.argv)
    # ft_engine.setWindowIcon(QIcon('Mcluckey-Logo.png'))

    sys.exit(ft_engine.exec_())