from moviepy.editor import *
import math
import subprocess
def speed_changer(original_video,modifier_list):
     ''' The following function take the starting , ending timesand the speed 
          To slow down or speed up the video
          Three parts are made
          1-begining the start time
          2-the part which needs speed modification
          3-end time till the video lasts
          These three parts are concatenated to gve back the input video with modified speed'''


     if modifier_list[4]==0:
          v_speed=0.68
          a_speed=1.467
     elif modifier_list[4]==1:
          v_speed=0.5
          a_speed=2.0
     elif modifier_list[4]==2:
          v_speed=1.467
          a_speed=0.68
     elif modifier_list[4]==0:
          v_speed=2.0
          a_speed=0.5
          
     
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
     extension_pos=original_video_file.rfind(".")
     extension=original_video_file[extension_pos:]
     path=original_video_file[:last_pos+1]
     textfilename=path+"concatenate.txt"

     #Opening a file to write the names of the videos to be concantenated 
     f1=open(textfilename,'w')
     name=str(1)+extension
     ffmpeg_extract_subclip(original_video_file,0,starttime,targetname=name)
     f1.write(path+name+"\n")
     name=str(2)+extension
     ffmpeg_extract_subclip(original_video_file,starttime,endtime,targetname=name)
     f1.write(path+name+"\n")
     name=str(3)+extension
     f1.close()
     
     #Speeding up the specified part
     cmd="ffmpeg -i "+original_video_file+" -vf \"setpts="+str(v_speed)+"*PTS\" -filter:a \"atempo="+str(a_speed)+"\" output-video.mp4"
     p = subprocess.Popen(cmd, shell=True,
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
     output = p.communicate()[0]
     
     #FFMPEG Command to concatenate videos 
     cmd="ffmpeg -f concat -safe 0 -i "+textfilename+" -c copy "+original_video_file
     subprocess_call(cmd.split())



