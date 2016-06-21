#!/usr/bin/python
#--------------------------------------   
# This script reads data from a 
# MCP3008 ADC device using the SPI bus.
#
# Author : Matt Hawkins
# Date   : 13/10/2013
#
# http://www.raspberrypi-spy.co.uk/
#
#--------------------------------------

import spidev
import time
import os

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

# Function to convert data to voltage level,
# rounded to specified number of decimal places. 
def ConvertVolts(data,places):
  volts = (data * 3.3) / float(1023)
  volts = round(volts,places)  
  return volts
  
# Function to calculate pressure from
# TMP36 data, rounded to specified
# number of decimal places.
def ConvertPress(data,places):
 
  press = ((data * 17.05)/float(1023))-2.58
  press = round(press,places)
  
  if press<0:

	press=0

  return press


def ConvertFlow(data,places):

  flow = ((data * 1.52)/float(1023))-0.22
  flow = round(flow,places)

  if flow<0:
		
	flow=0

  return flow
  
# Define sensor channels
flow_channel = 0
press_channel  = 1



def onetime()

	while True:

 		# Read the flow sensor data
  		flow_level = ReadChannel(flow_channel)
  		flow_volts = ConvertVolts(flow_level,2)
  		flow       = ConvertFlow(flow_level,2)

  		# Read the pressure sensor data
  		press_level = ReadChannel(press_channel)
  		press_volts = ConvertVolts(press_level,2)
  		press       = ConvertPress(press_level,2)

  		# Print out results
  		print "--------------------------------------------"  
  		print("Flow      : {} ({}V) {} l".format(flow_level,flow_volts,flow))  
  		print("Pressure  : {} ({}V) {} bar".format(press_level,press_volts,press))    

  return press,flow
 
