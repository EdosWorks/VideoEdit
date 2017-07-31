from moviepy.editor import *
import math
def trimmer(original_video,modifier_list):
     ''' The following function take the starting and ending times which specify the unwanted bit of the video
          To eleminate the same two parts of the video is made
          One from the very beginning to the start time and one from the end time till the very end
          The two parts are concatenated to give back the video without the specified bit '''



     
     original_video_file=""
     ##############THE FOLLOWING LOOP IS TO MODIFY THE PATH NAME SUCH THAT IT IS ACCEPATBLE BY THE COMMADLINE FUNCTION##################
     for i in original_video:
          if i=="\\":
               original_video_file+="\\"
          original_video_file+=i

     #An object created   
     clip = VideoFileClip(original_video_file) 

     #Converting the start and end times to
     
     starttime=math.ceil(modifier_list[0]/1000)
     endtime=math.ceil(modifier_list[1]/1000)

     #Following steps create the text file 
     last_pos=original_video_file.rfind("\\")
     path=original_video_file[:last_pos+1]
     textfilename=path+"concatenate.txt"

     #Opening a file to write the names of the videos to be concantenated 
     f1=open(textfilename,'w')
     name=str(1)+".mp4"
     ffmpeg_extract_subclip(original_video_file,0,starttime,targetname=name)
     f1.write(path+name+"\n")
     name=str(2)+".mp4"
     ffmpeg_extract_subclip(original_video_file,endtime+1,math.ceil(clip.duration),targetname=name)
     f1.write(path+name+"\n")
     f1.close()
     #FFMPEG Command to concatenate videos 
     cmd="ffmpeg -f concat -safe 0 -i "+textfilename+" -c copy "+original_video_file
     subprocess_call(cmd.split())


trimmer("c:\jkj\sdh\yha.mp4",[1,2])
