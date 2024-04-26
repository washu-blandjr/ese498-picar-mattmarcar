# motor and lidar
import math
from board import SCL,SDA
import busio
from adafruit_pca9685 import PCA9685
import time
from adafruit_motor import servo

# lidar
import sys
import numpy as np
from adafruit_rplidar import RPLidar

def Servo_Motor_Initialization():
   i2c_bus = busio.I2C(SCL,SDA)
   pca = PCA9685(i2c_bus)
   pca.frequency = 100
   
   return pca
   

# Initialization Vars
channel_num = 14
pca = Servo_Motor_Initialization()
servo7 = servo.Servo(pca.channels[channel_num])
PORT_NAME = '/dev/ttyUSB0'

def Motor_Speed(pca,percent):
   #converts a -1 to 1 value to 16-bit duty cycle
   speed = ((percent) * 3277) + 65535 * 0.15
   pca.channels[15].duty_cycle = math.floor(speed)
   print(speed/65535)

# issue if ran with run()
def turn(dir):
    # Back
    if dir == "B":
        print("Wall! Back")
        
    # Front
    elif dir == "F":
        print("Wall! Front")
    
    # Left
    elif dir == "L":
        print("Wall! Left")
        for f in range(0.5,0.75,0.01):
            servo7.fraction = f
            time.sleep(0.03)
        time.sleep(2)
        turn("N")
            
    # Right
    elif dir == "R":
        print("Wall! Right")
        for f in range(0.5,0.25,-0.01):
            servo7.fraction = f
            time.sleep(0.03)
        time.sleep(2)
        turn("N")
    
    elif dir == "N":
        servo7.fraction = 0.50
        time.sleep(0.03)
        print("Servo angle reset to neutral: " + str(servo7.angle))

    # run()

def run():
    lidar = RPLidar(None, PORT_NAME, timeout=3)

    # Motor_Speed(pca, 0.15)
    servo7.fraction = 0.50
    time.sleep(1.5)
    
    try:
        print('Lidar is measuring... Press Crl+C to stop.')
        for scan in lidar.iter_scans():
            for (_, angle, dist) in scan:
                # Back
                if dist <= 200 and (angle in range(315, 360) or angle in range(0,45)):
                    turn("B")
                    
                # Front
                elif dist <= 200 and (angle in range(135, 225)):
                    turn("F")
                
                # Left
                elif dist <= 200 and (angle in range(45, 135)):
                    turn("L")
                        
                # Right
                elif dist <= 200 and (angle in range(225, 360)):
                    turn("R")
                
                else:
                    print("No Motion...")
                # #Neutral
                # elif servo7.fraction not in range(0.40, 0.60):
                    # turn("N")
                
    except KeyboardInterrupt:
        print('Stoping.')
    lidar.stop()
    lidar.disconnect()
    
if __name__ == '__main__':
    run()

    
