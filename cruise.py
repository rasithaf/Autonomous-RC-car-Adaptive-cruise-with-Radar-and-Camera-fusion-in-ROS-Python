#!/usr/bin/env python
# Rasitha Fernando
# 12/29/2019

import rospy
import numpy as np 
from can_msgs.msg import Frame
from std_msgs.msg import String
from std_msgs.msg import Int16
from std_msgs.msg import UInt8MultiArray
import datetime

global All_Range, All_Speed
theta = Int16
theta = 15
distance = Int16    
distance = 70 #in meters
speed = 0
pwm = 0.15
pwm_max = 0.3
distance_max = 1.8

def callback(data):
	global theta,distance,speed,pwm
	if data.id != 1343:
      
		a = UInt8MultiArray
		a = [0,0,0,0,0,0,0,0]
		for i in range (8):
			a[i] = ord(data.data[i]) # CAN values are converted from ASCII to integer values

			byte_L4 = '{0:08b}'.format(a[5]) # converting integer to binary
			byte_H4 = '{0:08b}'.format(a[6]) 
			Angle = byte_H4[3:8]+byte_L4[0:6]
			Angle = int(Angle,2)  # converting binary to integer
			Angle = Angle*0.1     # scaled value
			if Angle > 102.3:
				Angle = Angle-204.8
			else: Angle = Angle
				Angle = round(Angle, 2)

			if -theta < Angle < theta:  #15, -15      
				byte_L1 = '{0:08b}'.format(a[0])
				byte_H1 = '{0:08b}'.format(a[1]) 
				Radial_range = byte_H1[1:8]+byte_L1
				Radial_range = int(Radial_range,2)
				Radial_range = Radial_range*0.01     # scaled value
				Radial_range = round(Radial_range, 2)
            
				if Radial_range < distance:	# get the min value
					distance = Radial_range
					byte_L2 = '{0:08b}'.format(a[2])
					byte_H2 = '{0:08b}'.format(a[3]) 
					Radial_Speed = byte_H2[2:8]+byte_L2
					Radial_Speed = int(Radial_Speed,2)
					Radial_Speed = Radial_Speed*0.01     # scaled value
					if Radial_Speed > 81.91:
						Radial_Speed = Radial_Speed-163.83
					else: Radial_Speed = Radial_Speed
						speed = round(Radial_Speed, 2)
    
	if data.id >= 1343: 
		if distance <= distance_max:
			pwm = 0.15
		elif distance > distance_max and speed > 0:
			pwm = pwm + 0.01
			if pwm > pwm_max: pwm = pwm_max
			print ("Greater")
		elif distance > 3.5:
			pwm = .3
		elif distance > distance_max and speed < 0:
			print ("lesser")
			pwm = pwm - 0.01
			if pwm < 0.15: pwm = 0.15
     
		pwm = round(pwm,2) 
		pwm = int(pwm*1000)
		y = str(pwm)
		pwm = round(float(pwm/1000.0),2)
		pub = rospy.Publisher('Radar_talk', String, queue_size=10)
		pub.publish(y)  
		distance = 70 #in meters make it to initial value



def listener():
	rospy.init_node('Radar', anonymous=True)    
	rospy.Subscriber('/can_tx', Frame, callback, queue_size=64)
	rospy.spin()


if __name__ == '__main__':
	listener()

   
