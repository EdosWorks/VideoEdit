import numpy as np
import cv2

cap = cv2.VideoCapture('C:\\moviepy-master\\moviepy-master\\lecture7.mp4')
#finding framerate

#finds the version of opencv
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

#and uses corresponding function to find the frame rate
if int(major_ver)  < 3 :
        fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
        print type(fps)
        print "Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps)
else :
        fps = cap.get(cv2.CAP_PROP_FPS)
        print type(fps)
        print "Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps)


# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('C:\\moviepy-master\\moviepy-master\\outs.mp4',fourcc, fps, (640,480))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        out.write(frame)

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
#out.release()
cv2.destroyAllWindows()
