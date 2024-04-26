import cv2
import numpy
from flask import Flask, render_template, Response, stream_with_context, request

# mostly from: https://github.com/avseng/LiveStramingCamera/blob/main/

video = cv2.VideoCapture(cv2.CAP_V4L2)
app = Flask('__name__')

if not video.isOpened():
    print("Cannot open...")
    exit()

def video_stream():
    while True:
        ret, frame = video.read()
        
        if not ret:
            break;
        else:
            frame = cv2.flip(frame,0)
            
            ret, buffer = cv2.imencode('.jpeg',frame)
            frame = buffer.tobytes()
            yield (b' --frame\r\n' b'Content-type: image/jpeg\r\n\r\n' + frame +b'\r\n')


@app.route('/camera')
def camera():
    return render_template('camera.html')


@app.route('/video_feed')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


app.run(host='0.0.0.0', port='5000', debug=False)
