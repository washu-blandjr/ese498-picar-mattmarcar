# COMMENT what you don't want dto use with Ctrl + /

# print ('Hello! Initializing LIDAR CODE')
# print('https://wiki.ros.org/nmea_navsat_driver')
# print('https://github.com/pcdangio/ros-driver_mt3339')
# print('https://github.com/adafruit/Adafruit_CircuitPython_GPS')
# print('https://learn.adafruit.com/adafruit-ultimate-gps/circuitpython-parsing')

#-----------------------------------------------------------------------
# # from: https://rplidar.readthedocs.io/en/latest/
# from adafruit_rplidar import RPLidar

# # Setup the RPLidar
# PORT_NAME = '/dev/ttyUSB0'
# lidar = RPLidar(None, PORT_NAME, timeout=3)

# info = lidar.info
# print(info)

# health = lidar.health
# print(health)

# for i, scan in enumerate(lidar.iter_scans()):
    # print('%d: Got %d measurments' % (i, len(scan)))
    # if i > 10:
        # break

# lidar.stop()
# lidar.stop_motor()
# lidar.disconnect()
#-----------------------------------------------------------------------
# #!/usr/bin/env python3
# '''WONKY VERSION, use one below this code section!'''
# '''Records measurments to a given file. Usage example:

# $ ./record_measurments.py out.txt'''

# import sys
# from adafruit_rplidar import RPLidar


# PORT_NAME = '/dev/ttyUSB0'

# def run(path):
    # '''Main function'''
    # lidar = RPLidar(None, PORT_NAME,timeout=3)
    # outfile = open(path, 'w')
    # try:
        # print('Recording measurments... Press Crl+C to stop.')

        # # outputs scan quality, heading angle and obj distance
        # for measurment in lidar.iter_scans(500): 
            # line = '\t'.join(str(v) for v in measurment)
            # outfile.write(line + '\n')
            # dist = lidar.iter_scans().distance
            # if (dist <= 120):
                # print("TOO CLOSE! Distance: %d" % dist)
    # except KeyboardInterrupt:
        # print('Stoping.')
    # lidar.stop()
    # lidar.disconnect()
    # outfile.close()

# if __name__ == '__main__':
    # # can type sys.argv[1] to supply another file output from cmd line
    # run("/home/mattmarcar/Documents/ESE498/test_codes/lidar-out.txt")
#-----------------------------------------------------------------------
# #!/usr/bin/env python3
# '''Records scans to command line
# Usage example:

# $ python3 triallidar.txt scans.py out.txt'''
import sys
import numpy as np
from adafruit_rplidar import RPLidar

# LIDAR sections (from Car's POV):
# 315 -  45: Back
# 45  - 135: Left
# 135 - 225: Front
# 225 - 315: Right


PORT_NAME = '/dev/ttyUSB0'

def run():
    '''Main function'''
    lidar = RPLidar(None, PORT_NAME, timeout=3)

    try:
        print('Recording measurments... Press Crl+C to stop.')
        for scan in lidar.iter_scans():
            for (_, angle, dist) in scan:
                
                if dist <= 400 and (angle in range(315, 360) or angle in range(0,45)):
                
                    print("Too Close!") 
                    
                    # Print Out Data
                    f_dist = f"{dist:.2f}"
                    f_angle = f"{angle:.2f}"
                    print(f"D: {f_dist} mm, A: {f_angle} deg")
            
            
    except KeyboardInterrupt:
        print('Stoping.')
    lidar.stop()
    lidar.disconnect()
    
if __name__ == '__main__':
    run()
