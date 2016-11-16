import motor_controller as MC
import ultrasonic as US

GPIO.setmode(GPIO.BCM)
vikingbotMotors = MC.MotorController()
ultrasonicSensorBack = US.Ultrasonic()

#GPIO.cleanup()

vikingbotMotors.setup_GPIO(1,0)
vikingbotMotors.setup_PWM()
vikingbotMotors.start_PWM()
vikingbotMotors.set_motorSpeed(90,90)
vikingbotMotors.set_SleepTime(0.030)
vikingbotMotors.goForward()
vikingbotMotors.sset_SleepTime(1)
vikingbotMotors.turnLeft()
vikingbotMotors..set_SleepTime(1)
vikingbotMotors.turnRight()
vikingbotMotors.set_SleepTime(2)
vikingbotMotors.goBack()

#ultrasonicSensorBack.setup_GPIO()

#while(True):

#        if (ultrasonicSensorBack.get_distance() > 10):
#                vikingbotMotors.goBack()


GPIO.cleanup()
