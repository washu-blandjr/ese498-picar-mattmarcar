#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image
import time
from cv_bridge import CvBridge 
import cv2
import numpy
import threading
from flask import Flask, render_template, Response, stream_with_context, request

app = Flask('__name__')
bridge = CvBridge()
cv_img = None

# Camera Streaming
def call_cam(data):
    global cv_img
    try:
        cv_img = bridge.imgmsg_to_cv2(data, "bgr8")
    except Exception as e:
        print(e)    

def video_stream():
    global cv_img
    while True:
            
            ret, buffer = cv2.imencode('.jpeg',cv_img)
            frame = buffer.tobytes()
            yield (b' --frame\r\n' b'Content-type: image/jpeg\r\n\r\n' + frame +b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

def listener():
    
    threading.Thread(target=lambda: rospy.init_node('listener', disable_signals=True)).start()
    rospy.Subscriber('vid_stream/image_raw' , Image, call_cam)
  

if __name__ == '__main__':
    listener()
    app.run(host='0.0.0.0', port='5000', debug=False)
