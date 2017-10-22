import motor_controller as MC
import ultrasonic as US
import RPi.GPIO as GPIO

#set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# create objects for motor controller and distance sensor
vikingbotMotors = MC.MotorController()
ultrasonicSensorBack = US.Ultrasonic()

#GPIO.cleanup()

# setup the motors
vikingbotMotors.setup_GPIO(1,0)

# setup and start PWM set the dulty cycles to 90
vikingbotMotors.setup_PWM()
vikingbotMotors.start_PWM()
vikingbotMotors.set_motorSpeed(90,90)

# set the delay between motions to 2 seconds
vikingbotMotors.set_SleepTime(2)

#Test the movements
vikingbotMotors.goForward()
vikingbotMotors.sset_SleepTime(1)
vikingbotMotors.turnLeft()
vikingbotMotors.set_SleepTime(1)
vikingbotMotors.turnRight()
vikingbotMotors.set_SleepTime(2)
vikingbotMotors.goBack()

#test for distance sensor
#setup the distance sensor
#ultrasonicSensorBack.setup_GPIO()

#while(True):
#if distance is more than 10 cm. go back. Ig there is an obstacle stop
#        if (ultrasonicSensorBack.get_distance() > 10):
#                vikingbotMotors.goBack()

GPIO.cleanup()
