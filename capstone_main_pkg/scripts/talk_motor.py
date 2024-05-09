#!/usr/bin/env python3

import rospy
import time
from sensor_msgs.msg import Image
import math
import os
import time
import busio
from math import cos, sin, pi, floor
from board import SCL, SDA
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
from adafruit_rplidar import RPLidar
import trialmotor as momo

i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 100

os.putenv('SDL_FBDEV', '/dev/fb1')
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME, timeout=3)
steering_channel = 14
motor_channel = 15
servo_steering = servo.Servo(pca.channels[steering_channel])

def update_steering_angle(angle):
    servo_steering.angle = angle
    
def scale_lidar_distance(distance, max_distance=3000):
    return min(distance, max_distance) / max_distance

def talker():
    pub = rospy.Publisher('vid_stream/image_raw', Image, queue_size=10)
    rospy.init_node('talk_cam', anonymous=True)
    
    rate = rospy.Rate(10) # every 2 seconds
    
    while not rospy.is_shutdown():
    
        # neutral
        update_steering_angle(100)
        time.sleep(0.1)
        momo.Motor_Speed(pca,0.15)
        count = 0
        reset = False
        
        try:
            scan_data = [0]*360
            while True:
                for scan in lidar.iter_scans():
                    for (_, angle, distance) in scan:
                        angle = int(angle)
                        
                        # Print Out Data
                        f_dist = f"{distance:.2f}"
                        f_angle = f"{angle:.2f}"
                        print(f"D: {f_dist} mm, A: {f_angle} deg")
                        
                        # Back
                        if distance <= 200 and (angle in range(315, 360) or angle in range(0,45)):
                            print("Object Behind!")
                            
                            
                        # Front
                        if distance <= 200 and (angle in range(135, 225)):
                            print("Object Front!")
                            
                            
                        # Left
                        if distance <= 200 and (angle in range(45, 135)):
                            print("Open space on the left side!")
                            update_steering_angle(120)
                            
                            
                        # Right
                        if distance <= 200 and (angle in range(225, 315)):
                            print("Open space on the right side!")
                            update_steering_angle(60)
                            
                        
                    # LIDAR scaling
                    for angle in range(360):
                        distance = scan_data[angle]
                        if distance:
                            scaled_distance = scale_lidar_distance(distance)
                            radians = angle * pi / 180
                            x = scaled_distance * cos(radians) * 119
                            y = scaled_distance * sin(radians) * 119
                            point = (160 + int(x), 120 + int(y))
                            
        except KeyboardInterrupt:
            print('Stopping.')
        finally:
            lidar.stop()
            lidar.disconnect()
        
        rate.sleep()
            
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
