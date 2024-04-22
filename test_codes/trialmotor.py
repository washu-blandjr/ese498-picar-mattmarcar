import math
from board import SCL,SDA
import busio
from adafruit_pca9685 import PCA9685
import time
import adafruit_motor.servo

def Servo_Motor_Initialization():
   i2c_bus = busio.I2C(SCL,SDA)
   pca = PCA9685(i2c_bus)
   pca.frequency = 100
   return pca
   
def Motor_Speed(pca,percent):
   #converts a -1 to 1 value to 16-bit duty cycle
   speed = ((percent) * 3277) + 65535 * 0.15
   pca.channels[15].duty_cycle = math.floor(speed)
   print(speed/65535)

#initialization
pca = Servo_Motor_Initialization()

for i in range(2):
    Motor_Speed(pca, 0)   #stop/neutral position
    time.sleep(3)
    print("R")
    Motor_Speed(pca, -0.15)   #reverse
    time.sleep(3)
    Motor_Speed(pca, 0)   #stop/neutral position
    time.sleep(3)
    print("F")
    Motor_Speed(pca, 0.15)   #forward
    time.sleep(3)
    Motor_Speed(pca, 0)   #stop/neutral position
    time.sleep(3)
    Motor_Speed(pca, -0.15)   #reverse
    time.sleep(3)
    Motor_Speed(pca, 0)   #stop/neutral position
    time.sleep(3)
