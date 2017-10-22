import time
import socket 
import spidev
import RPi.GPIO as GPIO
import motor_controller as MC
import irdistance as IR
import ultrasonic as US


# Vikingbot Main Python Script


# Ip addresses and the port numbers for the Android phone and the Raspberry Pi board

UDP_IP = "192.168.0.100"
UDP_IP_SEND = "192.168.0.101"

# Portnumber for the phone and Raspberry Pi
UDP_PORT = 4444

GPIO.setmode(GPIO.BCM)
vikingbotMotors = MC.MotorController()

ir = IR.IRSensor(0)
us = US.Ultrasonic()
us.setup_GPIO()

vikingbotMotors.setup_GPIO(1,0)

vikingbotMotors.setup_PWM()
vikingbotMotors.start_PWM()

vikingbotMotors.set_motorSpeed(70, 70)
vikingbotMotors.set_SleepTime(0.25)	


# UDP connection settings for receive and send data
sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_receive.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_receive.bind((UDP_IP, UDP_PORT))

mode = 0 

# mapping funtions maps values between the givin range
def map(input, in_min, in_max, out_min, out_max):
	return ((input - in_min) * (out_max - out_min) / (in_max -in_min) + out_min)

# check sensor calues if there is any obstacle
def obstacle_detection(threshold_left, threshold_right, threshold_back):
	Sensor_msg = "-"
	if (ir.read_channel(1, 3) > threshold_left):
		Sensor_msg = Sensor_msg + "Obstacle on the left"
	if(ir.read_channel(0, 3) > threshold_right):
		Sensor_msg = Sensor_msg + "Obstacle on the right"
	if(int(us.measure_average()) < threshold_back):
		Sensor_msg = Sensor_msg + "Obstacle on the back"

	sock_send.sendto(Sensor_msg, (UDP_IP_SEND, UDP_PORT))

	return Sensor_msg

# main loop
while True:
	
	# Make the robot stop and waiting for the next command
	vikingbotMotors.stop()

	# Waiting until receiving a command
	data, addr = sock_receive.recvfrom(1024)	
				
	# Check the mode type slected by the user
	if (data == "Drone" or data == "Voice"):
		print data
		mode  = 1
		vikingbotMotors.set_SleepTime(0.5)
	
	elif (data == "Prog"):
		mode  = 2
		vikingbotMotors.set_SleepTime(1)

	elif (data == "Fingersfree"):
		mode  = 3
		vikingbotMotors.set_SleepTime(0.2)

	elif (data == "Sensor"):
		mode = 4
	
	# Drone Mode, Fingersfree and Voice Mode
	if (mode == 1 or mode == 3):

		# If the command is "Forward"	
		if (data == "Forward"):
			vikingbotMotors.goForward()
			if (mode == 1):
				obstacle_detection(400, 400, 5)
			
		# If the command is "Left"
		elif (data == "Left"):
			vikingbotMotors.turnLeft()

			if (mode == 1):
				obstacle_detection(400, 400, 5)

		# If the command is "Right"
		elif (data == "Right"):
			vikingbotMotors.turnRight()
			
			if (mode == 1):
				obstacle_detection(400, 400, 5)

		# If the command is "Back"
		elif (data == "Back"):
			vikingbotMotors.goBack()

			if (mode == 1):
				obstacle_detection(400, 400, 5)

		# If the command is "Stop"
		elif (data == "Stop"):
			vikingbotMotors.stop()

		# If the command is "Speed"
		elif ("Speed" in data):
			list_data = data.split("-")
			new_speed = int(list_data[1])
			new_speed = map(new_speed, 0, 100, 40, 100)
			print new_speed
			vikingbotMotors.set_motorSpeed(new_speed, new_speed)
			
	# Programming Mode
	elif (mode == 2):
                 
        for i in range(0, len(data)):

		# 1 = go forward
			if (data[i] == "1"):
				vikingbotMotors.goForward()
			
		# 2 = turn left
			elif (data[i] == "2"):
				vikingbotMotors.turnLeft()
		
		# turn right
			elif (data[i] == "3"):
				vikingbotMotors.turnRight()
		
		# go back
			elif (data[i] == "4"):
				vikingbotMotors.goBack()

		# stop
			elif (data[i] == "5"):
				vikingbotMotors.stop()
			
		# wait
			elif (data[i] == "6"):
				vikingbotMotors.stop()
				temp = ""
				while (data[i+1] != '*'):
					temp = temp + data[i+1]
					i = i + 1
				time.sleep(int(temp))

	# sensor read mode
	elif (mode == 4):
		
		while(True):
			all_sensors = ""
			button, addr = sock_receive.recvfrom(1024)	
			if (button == "exit"):
				mode = 0
				break
			sensorFrontLeft = ir.read_channel(1, 3)
			sensorFrontRight = ir.read_channel(0, 3)
			sensorBack = int(us.measure_average())
			print us.get_distance()
			print sensorBack 
			print "----"
			all_sensors = str(sensorFrontLeft) + "-" + str(sensorFrontRight) + "-" + str(sensorBack)
			sock_send.sendto(all_sensors, (UDP_IP_SEND, UDP_PORT))

GPIO.cleanup()


