# import the opencv library 
import cv2
import time 

# define a video capture object 
vid = cv2.VideoCapture(cv2.CAP_V4L2) 


fourcc = cv2.VideoWriter.fourcc(*'mp4v')
out = cv2.VideoWriter('outputs/output.mp4', fourcc, 30, (640, 480))

if not vid.isOpened():
    print("Cannot open...")
    exit()
    
while(True): 
    # Capture the video frame by frame 
    ret, frame = vid.read() 

    #used for orientation of cam
    frame = cv2.flip(frame, 0)
    
    out.write(frame)
    
    # Display the resulting frame 
    cv2.imshow('frame', frame) 
    
    # the 'q' button is set as the 
    # quitting button you may use any 
    # desired button of your choice 
    if cv2.waitKey(1) == ord('q'): 
        break


# After the loop release the vid and out object 
vid.release()
out.release() 

# Destroy all the windows 
cv2.destroyAllWindows() 

