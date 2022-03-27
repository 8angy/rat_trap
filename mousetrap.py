#!/usr/bin/python
# Mike Bangham 2015 - RPi MouseTrap

import RPi.GPIO as GPIO
from time import sleep
import subprocess
from subprocess import call
import sys
from PyQt5 import QtWidgets, QtCore
		   
pir_sensor = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pir_sensor, GPIO.IN)
current_state = 0
waitime = 0.1/float(1000)  # speed of stepper motor

seq = [[1,0,0,1],
	   [1,0,0,0],
	   [1,1,0,0],
	   [0,1,0,0],
	   [0,1,1,0],
	   [0,0,1,0],
	   [0,0,1,1],
	   [0,0,0,1]]


step_count = len(seq)
step_dir = -1  # anti-clockwise


class Trap:
	def __init__(self):
		super().__init__()
		self.init_motion_thread()

	def init_motion_thread(self):
		self.worker = MotionThread()
		self.workerthread = QtCore.QThread()
		self.worker.signal.connect(self.Motor)
		self.workerthread.start()

	def _motor(self, t):
		print(t)
		# Motor activation to pull pin and release trap door
		sleep(10)
		# Need to pause for a moment to allow the mouse to enter the chamber and begin eating.
		GPIO.setmode(GPIO.BCM)
		step_pins = [5, 6, 12, 13]

		for pin in step_pins:
			GPIO.setup(pin,GPIO.OUT)
			GPIO.output(pin, False)
		 
		step_counter = 0
		loop-count = 8000
		i=1

		while i < loop-count:  
			for pin in range(0,4):
				xpin=step_pins[pin]# Get GPIO
				if seq[step_counter][pin]!=0:
					print ("Motor Rotating...")
					GPIO.output(xpin, True)
				else:
					GPIO.output(xpin, False)
		  
		step_counter += step_dir

		if (step_counter >= step_count):
			step_counter = 0
		if (step_counter < 0):
			step_counter = step_count + step_dir
		i += 1 
		sleep(waitime)


class MotionThread(QtCore.QObject):
	# Our thread to detect motion in the rat trap 
	signal = QtCore.pyqtSignal(str)
 
	def __init__(self):
		super().__init__()

	@QtCore.pyqtSlot()
	def run(self):
		while True:
			sleep(0.1)
			current_state = GPIO.input(pir_sensor)
			if current_state == 1:
				self.signal.emit('Motion detetced!')
				break
			else:
				continue


if __name__ == '__main__':
	app = QtWidgets.QApplication([])
	gui = Trap()
	sys.exit(app.exec_())

