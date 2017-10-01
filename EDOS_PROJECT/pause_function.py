'''
The function takes in an input file and the pause time and the length of the pause

'''
import numpy as np
import cv2
def pause_func(filename,pause_list):
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

     fourcc = cv2.VideoWriter_fourcc(*codec)
     out = cv2.VideoWriter('outs1.mp4',fourcc, fps, (long(cap.get(3)),long(cap.get(4))))#,480)
     counter=1
     pause_frame=fps*pause_list[0]

     write_same_frame=(pause_list[2] - pause_list[1])*fps
     while(cap.isOpened()):
         ret, frame = cap.read()
         if ret==True:
              
              #print(counter)
              if counter == pause_frame:
                   while write_same_frame>0:
                        out.write(frame)
                        cv2.imshow('frame',frame)
                        counter=counter+1
                        write_same_frame=write_same_frame-1
                        #print("same frame work")
              else:
                   out.write(frame)
                   cv2.imshow('frame',frame)
                   counter=counter+1

              if cv2.waitKey(1) & 0xFF == ord('q'):
                   print("exiting")
                   break
         else:
              break
     cap.release()
     #out.release()
     cv2.destroyAllWindows()
     
          
pause_func("most.mp4",[100,100,150])

print ("done")
#the list format is as follows
#pause_list[0] : filename
#pause_list[1] : 
          
     
