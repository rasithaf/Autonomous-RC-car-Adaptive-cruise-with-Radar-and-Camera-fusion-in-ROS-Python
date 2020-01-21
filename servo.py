#!/usr/bin/env python3
# Rasitha Fernando
# 12/29/2019

import rospy
from std_msgs.msg import String

pwm = 0.15  # minimum not to rotate the wheels 
ang = 100   # Steering zero

import signal
from adafruit_servokit import ServoKit
import board
import busio
import time

i2c_bus0=(busio.I2C(board.SCL_1,board.SDA_1))
kit = ServoKit(channels=16)

kit.continuous_servo[3].throttle = 0.0
time.sleep(1)
kit.continuous_servo[3].throttle = 0.05
time.sleep(1)
kit.continuous_servo[3].throttle = 0.1
time.sleep(1)
kit.continuous_servo[3].throttle = 0.2
time.sleep(1)
kit.continuous_servo[3].throttle = 0.0
kit.servo[0].angle = 35
time.sleep(1)
kit.servo[0].angle = 145
time.sleep(1)
kit.servo[0].angle = 100 # Straight Angle

####################################################################

def callback1(data):
	global ang
	ang = int(data.data)

  

def callback2(data):
	global pwm
	pwm = int(data.data)
	pwm = round(float(pwm/1000.0),3)
	fusion()



def fusion(): 
	global ang
	global pwm
	print("Angle = ", (ang),'pwm = ', pwm)
  
	kit.servo[0].angle = int(ang) 
	kit.continuous_servo[3].throttle = pwm 

	if ang == 0:
		kit.servo[0].angle = 100 
		kit.continuous_servo[3].throttle = 0.15 



def listener():

	rospy.init_node('servo', anonymous=True)  
	rospy.Subscriber('cam_talk', String, callback1, queue_size=1)
	rospy.Subscriber('Radar_talk', String, callback2, queue_size=1)  
	rospy.spin()



if __name__ == '__main__':
	try:     
		global dec 
		dec = String   
		listener()
	except rospy.ROSInterruptException:
		pass
 

