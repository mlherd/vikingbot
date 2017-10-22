#!/usr/bin/env python

import spidev
import time

#This class reads the sensor values that are connected to the 8 channel ADC

class IRSensor:
	
	spi = None

	def __init__(self, spi_port):
		self.spi=spidev.SpiDev()
		self.spi.open(0,spi_port)

	def read_channel(self, channel_number, sample_count):

		counter = 0
		total = 0

		while counter < sample_count:
			resp = self.spi.xfer([1, (8 + channel_number)<<4,0]) # 8 + channel 0<=channel<=7	
			if 0<= resp[1]<=3: 
				analog_value = ((resp[1]<<8)+resp[2]) # * 0.0032
				total = analog_value + total
				counter= counter + 1
			time.sleep(0.05)

		total = total/sample_count
		return total

