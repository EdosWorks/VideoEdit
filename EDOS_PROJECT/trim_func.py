'''
The function takes in an input file and the pause time and the length of the pause

'''
import subprocess
import numpy as np
import cv2
def trim_func(filename,trim_list):
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
     print major_ver
     print minor_ver
     print subminor_ver

     #and uses corresponding function to find the frame rate
     if int(major_ver)  < 3 :
     	print 'here1'
     	fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
     	print type(fps)
     	print "Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps)
     else :
     	print 'here2'
     	fps = cap.get(cv2.CAP_PROP_FPS)
     	print type(fps)
     	print "Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps)

     fourcc = cv2.VideoWriter_fourcc(*codec)
     out = cv2.VideoWriter('outs1.mp4',fourcc, fps, (long(cap.get(3)),long(cap.get(4))))#,480)
     counter=1
     start_frame=int(trim_list[0]*fps)
     stop_frame=int(trim_list[1]*fps)
     skipped_frames = 0
     while(cap.isOpened()):
     	 #print 'inside while loop'
         ret, frame = cap.read()
         if ret==True:
              #print(counter)
              if counter >= start_frame and counter<=stop_frame:
                   skipped_frames += 1
                   #print("ignoring frame - work in progress")
              else:
                   out.write(frame)
                   #cv2.imshow('frame',frame)

              if cv2.waitKey(1) & 0xFF == ord('q'):
                   print("exiting")
                   break
              counter += 1
         else:
              break
     print "skipped_frames = " + str(skipped_frames)
     print "counter	= " + str(counter)
     cap.release()
     out.release()
     cv2.destroyAllWindows()
     
          
trim_func("most.mp4",[100,150])
command = "ffmpeg -i most.mp4 -ab 160k -ac 2 -ar 44100 -vn audio.mp3"

subprocess.call(command, shell=True)

command = "ffmpeg -ss 0 -i audio.mp3 -t 100 output1.mp3"
subprocess.call(command, shell=True)
command = "ffmpeg -ss 150 -i audio.mp3 -t 374 output2.mp3"
subprocess.call(command, shell=True)

command ="ffmpeg -f concat -i mylist.txt -c copy output.mp3"
subprocess.call(command, shell=True)

command="ffmpeg -i outs1.mp4 -i output.mp3 -c:v copy -c:a aac -strict experimental output_final.mp4"
subprocess.call(command, shell=True)

print ("done")
#the list format is as follows

#trim_list[0] :start time
#trim_list[1] :stop time

          
     
'''
https://stackoverflow.com/questions/26741116/python-extract-wav-from-video-file

https://stackoverflow.com/questions/7629873/how-do-i-mix-audio-files-using-python
'''