import math
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.tools import subprocess_call
import os #from subprocess import call

def trimmer(original_video,modifier_list):
     original_video_file="C:\\moviepy-master\\lecture4.mp4"
     clip = VideoFileClip(original_video_file)
     starttime=math.ceil(modifier_list[0]/10)
     endtime=math.ceil(modifier_list[1]/10)
     textfilename="C:\\moviepy-master\\concatenate.txt"
     f1=open(textfilename,'w')
     name=str(1)+".mp4"
     ffmpeg_extract_subclip(original_video_file,0,starttime,targetname=name)
     f1.write("file C:"+"\\"+"\moviepy-master"+"\\"+"\\"+name+"\n")
     name=str(2)+".mp4"
     ffmpeg_extract_subclip(original_video_file,endtime+1,math.ceil(clip.duration),targetname=name)
     f1.write("file C:"+"\\"+"\moviepy-master"+"\\"+"\\"+name+"\n")
     f1.close()

     cmd="ffmpeg -f concat -safe 0 -i "+textfilename+" -c copy C:\\moviepy-master\\+"+original_video
     #+original_video_file
     subprocess_call(cmd.split())
