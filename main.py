import sys
import serial
import json

import PyQt4
from PyQt4.QtGui import * 
from PyQt4.QtCore import *


import time
import os
import RPi.GPIO as GPIO
import mainwindow_auto

#GPIO.setmode(GPIO.BCM)
ser=serial.Serial("/dev/ttyAMA0", 115200, timeout=0.1)

#decoded = json.loads(json_input)


class MainWindow(QMainWindow, mainwindow_auto.Ui_MainWindow):
        
    def btnstate(self):
        if self.wheel_button.isChecked():
            self.wheel_button.setText("Wheel Open")
            print("Opening wheel")
            a={'contact':1}
            json_out=json.dumps(a)
            print(json_out)
            ser.write(json_out)
            
        else:
            self.wheel_button.setText("Wheel Closed")
            print("Closing wheel")
            a={'contact':0}
            json_out=json.dumps(a)
            print(json_out)
            ser.write(json_out)

    def serialRead(self):
        if ser.isOpen():
            try:
                json_input=ser.readline()
                decoded = json.loads(json_input)
                print "Plate temperature", decoded['T_plate_avg']
                self.T_plate.setNum(decoded['T_plate_avg'])
            except:
                print "ERROR"

        #def pressedW_close(self):
        #print("Closing wheel")

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

    
        #json_input = ser.read()
        #decoded = json.loads(json_input)
        #print(decoded['T_plate'])
        
        self.wheel_button.setCheckable(True)
        self.wheel_button.clicked.connect(lambda: self.btnstate())
        #self.T_plate.connect(self.serialRead())
            
def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()

    sys.exit(app.exec_())

if __name__=="__main__":
    main()
