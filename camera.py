#!/usr/bin/env python
# Rasitha Fernando
# 12/29/2019


import rospy
from std_msgs.msg import String
import cv2
import numpy as np

def talker():
	video_capture = cv2.VideoCapture(0)
	video_capture.set(3,160)
	video_capture.set(4,120)

	while not rospy.is_shutdown():
		val = "0"
		rospy.init_node('camera', anonymous=True)

		ret, frame = video_capture.read()
		_, img = video_capture.read()

		if ret:
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			blur = cv2.GaussianBlur(hsv,(5,5),0)    

			ret,thresh = cv2.threshold(hsv,60,120,cv2.THRESH_BINARY_INV)    
	    
			lower_red = np.array([0,50,50]) 
			upper_red = np.array([10,255,255])    

			red = cv2.inRange(hsv, lower_red, upper_red)	      
			kernal = np.ones((5, 5), "uint8") 	 
			red = cv2.dilate(red,kernal)    
			res_red = cv2.bitwise_and(frame, frame, mask = red)
			contours,hierarchy = cv2.findContours(red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	     
			for cnt in contours:
				approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
				cv2.drawContours(img, [approx], 0, (0), 5)
				x = approx.ravel()[0]
				y = approx.ravel()[1]
		
			# Detecting contours
			if len(contours) > 0:

				c = max(contours, key=cv2.contourArea)
				M = cv2.moments(c)

				cx = int(M['m10']/M['m00'])
				cy = int(M['m01']/M['m00'])

				cv2.line(frame,(cx,0),(cx,720),(255,0,0),1)
				cv2.line(frame,(0,cy),(1280,cy),(255,0,0),1)
				cv2.drawContours(frame, contours, -1, (255,128,213), 1)

				val = String
				# Our RC car has steering range between 55 and 145
				# wheel position: 55 -> left most, 100 -> straight, 145 -> right most
				# frame has been segmented to 5 main positions

				if cx >= 130 and cx < 160:
					val = "145" # take extreme right

				elif cx < 130 and cx >= 86:
					val = "120" # take right

				elif cx < 86 and cx >= 76:
					dec  =  100 + 4*(cx -81)
					val = str(int(dec)) # steer continuosly

				elif cx < 76 and cx >= 30:
					val = "79" # take left

				elif cx < 30 and cx > 0:
					val = "55" # take extreme left
			else:
				val = "0"
				print ("Nothing found...") 

			cv2.imshow('frame',frame)
			cv2.imshow('red',red)
			cv2.imshow('res_red',res_red)

		else: 
			val = "0"
			print ("Nothing found...")   

		if cv2.waitKey(1) & 0xFF == ord('q'):
			video_capture.release()
			cv2.destroyAllWindows()        
			break

		pub = rospy.Publisher('cam_talk', String, queue_size=1)
		pub.publish(val)
		rospy.loginfo(val)

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass




