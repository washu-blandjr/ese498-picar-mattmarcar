#!/usr/bin/env python3

import rospy
import time
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

def talker():
    pub = rospy.Publisher('vid_stream/image_raw', Image, queue_size=10)
    rospy.init_node('talk_cam', anonymous=True)
    
    rate = rospy.Rate(10) # every 2 seconds
    
    video = cv2.VideoCapture(cv2.CAP_V4L2)

    if not video.isOpened():
        print("Cannot open...")
        exit()
    
    bridge = CvBridge()
    
    while not rospy.is_shutdown():
        ret, frame = video.read()
        
        if not ret:
            break;
        
        else:
            frame = cv2.flip(frame,0)
            
            # Color Detection
            
            hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Purple
            bound_lower = np.array([130, 50, 50])
            bound_upper = np.array([170, 255, 255])

            mask_purple = cv2.inRange(hsv_img, bound_lower, bound_upper)
            kernel = np.ones((7, 7), np.uint8)

            mask_purple = cv2.morphologyEx(mask_purple, cv2.MORPH_CLOSE, kernel)
            mask_purple = cv2.morphologyEx(mask_purple, cv2.MORPH_OPEN, kernel)

            seg_frame = cv2.bitwise_and(frame, frame, mask=mask_purple)
            contours, hier = cv2.findContours(
                mask_purple.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            output = cv2.drawContours(seg_frame, contours, -1, (0, 0, 255), 3)
            
            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if(area > 300):
                    x, y, w, h = cv2.boundingRect(contour)
                    frame = cv2.rectangle(frame, (x, y),
                                               (x + w, y + h),
                                               (130, 50, 50), 2)

                    cv2.putText(frame, "Purple Colour", (x, y),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1.0, (130, 50, 50))
                
            ret, buffer = cv2.imencode('.jpeg',frame)
            pub.publish(bridge.cv2_to_imgmsg(frame, encoding="bgr8"))
        
        rate.sleep()
        
    video.release()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
