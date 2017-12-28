import subprocess
import os
import numpy as np
import cv2
from moviepy.editor import VideoFileClip
def pause_voiceover(filename, pause_prms):
     cap = cv2.VideoCapture(filename)
     extension=filename.split(".")[1]

     #finding the codec
     if extension=="mp4":
          codec='H264'
     elif extension=="avi":
          codec='XVID'

     #finds the version of opencv
     (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
     print major_ver
     print minor_ver
     print subminor_ver

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
     start_frame=int(pause_prms[0]*fps)
     stop_frame=int(pause_prms[1]*fps)+start_frame
     print start_frame
     print stop_frame
     skipped_frames = 0
     while(cap.isOpened()):
         if counter!=start_frame:
          ret, frame = cap.read()
         if ret==True:
              #print(counter)
              if (counter == (start_frame - 1)):
                   paused_frame = frame 

              if counter == start_frame and skipped_frames <= (stop_frame - start_frame):
                   skipped_frames += 1
                   out.write(paused_frame)
                   #print("Stopped")
                   #print("ignoring frame - work in progress")
              else:
                   out.write(frame)
                   counter += 1
                   #cv2.imshow('frame',frame)

              if cv2.waitKey(1) & 0xFF == ord('q'):
                   print("exiting")
                   break
              
         else:
              break
     #print "skipped_frames = " + str(skipped_frames)
     #print "counter	= " + str(counter)
     cap.release()
     out.release()
     cv2.destroyAllWindows()
     
          
clip = VideoFileClip("most.mp4")
length=clip.duration
print( length )  
l=[100,162]
#length is the length of the orignal video
#l[0] is the starting second where pause button will be hit in the front-end
#l[1] is the time till which the recording button is holded       
pause_voiceover("most.mp4",l)
"""
Following functions are for extracting audio out of the video then trimming it and finally joining it with the final video named "output_final"
"""

command = "ffmpeg -i most.mp4 -ab 160k -ac 2 -ar 44100 -vn audio.mp3" #takes out audio from the video file "most.mp3"

subprocess.call(command, shell=True)

command = "ffmpeg -ss 0 -i audio.mp3 -t " + str(l[0]) +" output1.mp3" #For the first audio cut
subprocess.call(command, shell=True)
command = "ffmpeg -ss " + str(l[0]) + " -i audio.mp3 -t " + str(length-(l[0]+l[1])) + " output2.mp3" #The second cut part of the audio
subprocess.call(command, shell=True)
#Here my list is a txt file with text inside it as-  file 'output1.mp3' \n file 'insert.mp3' \n file 'output2.mp3
#\n denotes new line. file 'output2.mp3' is written in a new line after file 'output1.mp3'. 
#insert.mp3 is the audio file to be inserted
#following command is to create the mylist.txt text file
with open('mylist.txt', 'w') as the_file:
    the_file.write("file output1.mp3\n")
    the_file.write("file insert.mp3\n")
    the_file.write('file output2.mp3\n')

command ="ffmpeg -f concat -i mylist.txt -c copy output.mp3" #To merge the two audio file so as to create a trimmed audio file
subprocess.call(command, shell=True)

command="ffmpeg -i outs1.mp4 -i output.mp3 -c:v copy -c:a aac -strict experimental output_final.mp4" #Finallly joining the audio and the video
subprocess.call(command, shell=True)

os.remove("output2.mp3")
os.remove("output1.mp3")
os.remove("outs1.mp4")
os.remove("output.mp3")
os.remove("audio.mp3")
print ("done")

          
