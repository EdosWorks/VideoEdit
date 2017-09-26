import numpy as np
import cv2
filename='C:\\edited_videos\\2try.mp4'
cap = cv2.VideoCapture(filename)

extension=filename.split(".")[1]

#finding the codec
if extension=="mp4":
     codec='H264'
elif extension=="avi":
     codec='XVID'
     

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
fourcc = cv2.VideoWriter_fourcc(*codec)
out = cv2.VideoWriter('C:\\edited_videos\\outs.mp4',fourcc, fps, (long(cap.get(3)),long(cap.get(4))))#,480)
counter=0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        out.write(frame)
        counter=counter+1;

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
#out.release()
cv2.destroyAllWindows()
print(counter)
