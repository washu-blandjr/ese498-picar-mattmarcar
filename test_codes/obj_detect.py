# TOO SLOW!!!!!  TENSORFLOW IS A RESOURCE HOG!!!

import cv2
import cvlib as cvl
from cvlib.object_detection import draw_bbox
import tensorflow

# Mostly from: https://www.youtube.com/watch?v=V62M9d8QkYM

vid = cv2.VideoCapture(cv2.CAP_V4L2) 

if not vid.isOpened():
    print("Cannot open...")
    exit()
    
while(True): 
    # Capture the video frame by frame 
    ret, frame = vid.read() 
    bbox, label, conf = cvl.detect_common_objects(frame)
    output_image = draw_bbox(frame, bbox, label, conf)
    
    #used for orientation of cam
    frame = cv2.flip(frame, 0)
    
    # Display the resulting frame 
    cv2.imshow('frame', frame)
    
    # the 'q' button is set as the 
    # quitting button you may use any 
    # desired button of your choice 
    if cv2.waitKey(1) == ord('q'): 
        break


# After the loop release the vid object 
vid.release()

# Destroy all the windows 
cv2.destroyAllWindows() 
