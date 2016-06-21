import sys
import serial
import json

import PyQt4
from PyQt4.QtGui import * 
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore


import pfqt

import time
import os
import RPi.GPIO as GPIO
import mainwindow_auto

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(16, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(20, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(21, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(25, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)


ser=serial.Serial("/dev/ttyAMA0", 115200, timeout=0.5)

#while True:
    #json_input = ser.readline()
    #decoded = json.loads(json_input)
    #print (decoded['T_plate_avg'])
        
class MainWindow(QMainWindow, mainwindow_auto.Ui_MainWindow):     

    def presflow(self):
	pres,flo=pfqt.onetime()
	
	
	self.label_27.setText(str(pres))
	self.label_29.setText(str(flo))	  
          
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

   
    def tabSelected(self, arg=None):
        print '\n\t tabSelected() current Tab index =', arg

    def whatTab(self):
        currentIndex=self.tabWidget.currentIndex()
        currentWidget=self.tabWidget.currentWidget()

        print '\n\t Query: current Tab index =', currentIndex


    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
                    
       
	self.tabWidget.connect(self.tabWidget, SIGNAL("currentChanged(int)"), self.tabSelected)

        self.wheel_button.setCheckable(True)
        self.wheel_button.clicked.connect(lambda: self.btnstate())
	
	pres,flo=pfqt.onetime()
	
	
	self.label_27.setText(str(pres))
	self.label_29.setText(str(flo))
                    
def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    
    sys.exit(app.exec_())

if __name__=="__main__":
    main()

