import subprocess
from moviepy.editor import *
import math
import os
from moviepy.config import get_setting

## A list to store the paths of the edited video list for later use
edited_videos_list=[]
path_to_edited_videos="C:\\edited_videos"

def ffmpeg_extract_subclip(filename, t1, t2, targetname=None):
    """ makes a new video file playing video file ``filename`` between
        the times ``t1`` and ``t2``. """
    name,ext = os.path.splitext(filename)
    if not targetname:
        T1, T2 = [int(1000*t) for t in [t1, t2]]
        targetname = name+ "%sSUB%d_%d.%s"(name, T1, T2, ext)
    
    cmd = [get_setting("FFMPEG_BINARY"),"-y",
      "-i", filename,
      "-ss", "%0.2f"%t1,
      "-t", "%0.2f"%(t2-t1),
      "-vcodec", "copy", "-acodec", "copy", targetname]

    p = subprocess.Popen(cmd, shell=True,
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = p.communicate()[0]
    #subprocess_call(cmd)

def create_new_directory():
    ## Create a folder 
    
    if not os.path.exists(path_to_edited_videos):
        os.makedirs(path_to_edited_videos)
    

def modify_filename(filename):
     newfilename=''
     for i in filename:
          if i=='\\':
               newfilename+='\\'
          newfilename+=i
     return newfilename

    
def trimmer(original_video,edited_video_name,modifier_list):
     ''' The following function take the starting and ending times which specify the unwanted bit of the video
          To eleminate the same two parts of the video is made
          One from the very beginning to the start time and one from the end time till the very end
          The two parts are concatenated to give back the video without the specified bit '''
     
     pname=path_to_edited_videos+"\\"
     extension=original_video[original_video.rfind("."):]
     edited_video_name=modify_filename(edited_video_name)
     ##############THE FOLLOWING LOOP IS TO MODIFY THE PATH NAME SUCH THAT IT IS ACCEPATBLE BY THE COMMADLINE FUNCTION##################

     #An object created   
     clip = VideoFileClip(original_video) 

     #Converting the start and end times to     
     starttime=math.ceil(modifier_list[0]/1000)
     endtime=math.ceil(modifier_list[1]/1000)

     #Creating the text file
     textfilename=""
     textfilename+=path_to_edited_videos+"\\concat.txt"
     print(textfilename)
     #Opening a file to write the names of the videos to be concantenated 
     f1=open(textfilename,'w')
     name=str(1)+extension
     ffmpeg_extract_subclip(original_video,0,starttime,targetname=name)
     f1.write("file"+pname+name+"\n")
     name=str(2)+extension
     ffmpeg_extract_subclip(original_video,endtime+1,math.ceil(clip.duration),targetname=name)
     f1.write("file"+pname+name+"\n")
     f1.close()

     #FFMPEG Command to concatenate videos 
     cmd="ffmpeg -f concat -safe 0 -i "+textfilename+" -c copy "+edited_video_name
     p = subprocess.Popen(cmd.split(), shell=True,
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
     output = p.communicate()[0]
     #subprocess_call(cmd.split())



def save_feature():

     ##### This method stitches  all the videos together and saves it as one 
     ## Text file to store the names of the video files to be stitched 
     ## The output Video name to be sent with the path 

     videos_file=open("C:\\edited_videos\\concatall.txt",'w')
     for i in edited_videos_list:
          modified_name=modify_filename(i)
          videos_file.write("file"+modified_name+'\n')
     videos_file.close()

     cmd="ffmpeg -f concat -safe 0 -i "+videos_file+" -c copy "+output_video_name
     subprocess_call(cmd.split())
     

def speed_changer(original_video,edited_video_name,modifier_list):
     ''' The following function take the starting , ending timesand the speed 
          To slow down or speed up the video
          Three parts are made
          1-Beginning the start time
          2-The part which needs speed modification
          3-End time till the video lasts
          These three parts are concatenated to give back the input video with modified speed'''


     if modifier_list[2]==0:
          v_speed=0.68
          a_speed=1.467
     elif modifier_list[2]==1:
          v_speed=0.5
          a_speed=2.0
     elif modifier_list[2]==2:
          v_speed=1.467
          a_speed=0.68
     elif modifier_list[2]==3:
          v_speed=2.0
          a_speed=0.5
          
     vname=modify_filename(edited_video_name)
     pname=modify_filename(path_to_edited_videos)+"\\"+"\\"
     extension=original_video[original_video.rfind("."):]
     ##############THE FOLLOWING LOOP IS TO MODIFY THE PATH NAME SUCH THAT IT IS ACCEPATBLE BY THE COMMADLINE FUNCTION##################

     #An object created   
     clip = VideoFileClip(original_video_file) 

     #Converting the start and end times to     
     starttime=math.ceil(modifier_list[0]/1000)
     endtime=math.ceil(modifier_list[1]/1000)

     #Creating the text file 
     textfilename+=path_to_edited_videos+"\\concat.txt"

     #Opening a file to write the names of the videos to be concantenated 
     f1=open(textfilename,'w')
     name=str(1)+extension
     ffmpeg_extract_subclip(original_video_file,0,starttime,targetname=name)
     f1.write("file"+pname+name+"\n")
     to_modify_name=str(2)+extension
     ffmpeg_extract_subclip(original_video_file,starttime,endtime,targetname=to_modify_name)
     f1.write("file"+pname+to_modify_name+"\n")
     name=str(3)+extension
     f1.write("file"+pname+name+"\n")
     
     f1.close()
     
     #Speeding up the specified part
     cmd="ffmpeg -i "+original_video_file+" -vf \"setpts="+str(v_speed)+"*PTS\" -filter:a \"atempo="+str(a_speed)+" "+pname+name
     p = subprocess.Popen(cmd, shell=True,
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
     output = p.communicate()[0]
     
     #FFMPEG Command to concatenate videos  
     cmd="ffmpeg -f concat -safe 0 -i "+textfilename+" -c copy "+original_video_file
     subprocess_call(cmd.split())

          
###################                     THE ACTUAL INTERFACING FUNCTION                  #################
def get_video_data(file_path,operations_dictionary):
    #Call to create new directory function
    
    create_new_directory()
    ## CREATE NEW VIDEO FILENAME 
    extension_begin_pos=file_path.rfind(".")
    extension=file_path[extension_begin_pos:]
    new_name=file_path[:extension_begin_pos]
    new_name+="_edit"+file_path[extension_begin_pos:]

    edited_videos_list.append(new_name)

    if "trim" in operations_dictionary.keys():
        for i in operations_dictionary["trim"]:
            trimmer(file_path,new_name,i)

    if "speed" in operations_dictionary.keys():
        for i in operations_dictionary["speed"]:
            trimmer(file_path,new_name,i)

    
        


    

    
    
    
    




          
          
     
     
     
