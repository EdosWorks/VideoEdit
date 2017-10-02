"""
The first two values in trim_list are starting and ending seconds for trim.
The 3rd and the 4th values are the starting and ending seconds for dispalying the text on the video.
"""
import subprocess
import os
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
	 start_frame_trim=int(trim_list[0]*fps)
	 stop_frame_trim=int(trim_list[1]*fps)
	 start_frame_addtext=int(trim_list[2]*fps)
	 stop_frame_addtext=int(trim_list[3]*fps)
	 p=0
	 if start_frame_addtext>=stop_frame_trim:
	 	p=1
	 if start_frame_addtext>=start_frame_trim and start_frame_addtext<=stop_frame_trim:
	 	start_frame_addtext=start_frame_addtext-(start_frame_addtext-start_frame_trim)
	 print("Start Frame for trim = "+str(start_frame_trim))
	 print("Stop Frame for trim = "+str(stop_frame_trim))
	 print("Start Frame for add_text = "+str(start_frame_addtext))
	 print("Stop Frame for add_text = "+str(stop_frame_addtext))
	 skipped_frames = 0
	 while(cap.isOpened()):
		 #print 'inside while loop'
		 ret, frame = cap.read()
		 if ret==True:
			  #print(counter)
			  if counter >= start_frame_trim and counter<=stop_frame_trim:
				   skipped_frames += 1
				   #print("ignoring frame - work in progress")
			  else:
			  	   #print("start_frame_addtext + skipped_frames = "+str(start_frame_addtext+skipped_frames))
			  	   #print("stop_frame_addtext = "+ str(stop_frame_addtext))
			  	   #print("counter " + str(counter))
			  	   if p==1 and (counter<=stop_frame_addtext) and (counter>=start_frame_addtext):
			  	   	cv2.putText(frame, "hello world", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (225, 225, 255), 2)

				   elif(start_frame_addtext+skipped_frames<=stop_frame_addtext) and (counter<=stop_frame_addtext) and (counter>=start_frame_addtext):
				   	cv2.putText(frame, "hello world", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (225, 225, 255), 2)
				   	start_frame_addtext+=1
				   	#print("adding_text")
				   out.write(frame)
				   #cv2.imshow('frame',frame)

			  if cv2.waitKey(1) & 0xFF == ord('q'):
				   print("exiting")
				   break
			  counter += 1
		 else:
			  break
	 #print "skipped_frames = " + str(skipped_frames)
	 #print "counter	= " + str(counter)
	 cap.release()
	 out.release()
	 cv2.destroyAllWindows()
	 
		  
trim_func("most.mp4",[100,150,110,160])

"""
Following functions are for extracting audio out of the video then trimming it and finally joining it with the final video named "output_final"
"""

command = "ffmpeg -i most.mp4 -ab 160k -ac 2 -ar 44100 -vn audio.mp3" #takes out audio from the video file "most.mp3"

subprocess.call(command, shell=True)

command = "ffmpeg -ss 0 -i audio.mp3 -t 100 output1.mp3" #For the first audio cut
subprocess.call(command, shell=True)
command = "ffmpeg -ss 150 -i audio.mp3 -t 374 output2.mp3" #The second cut part of the audio
subprocess.call(command, shell=True)


#Here my list is a txt file with text inside it as-  file 'output1.mp3' \n file 'output2.mp3'
#\n denotes new line. file 'output2.mp3' is written in a new line after file 'output1.mp3'. 
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

#the list format is as follows

#trim_list[0] :start time
#trim_list[1] :stop time

		  
