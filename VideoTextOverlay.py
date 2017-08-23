import subprocess
from moviepy.editor import *
import math
import os
from moviepy.config import get_setting


def modify_filename(filename):
     newfilename=''
     for i in filename:
          if i=='\\':
               newfilename+='\\'
          newfilename+=i
     return newfilename



def putText(original_video,new_name,text_list):
    input_file=modify_filename(original_video)
    for i in text_list:
        start=i[0]#/1000
        end=i[1]#/1000
        cmd="ffmpeg -y -i "+input_file+" -vf drawtext=enable=\'between(t,"+str(start)+","+str(end)+")\':fontfile=C\:\\\\\\\\ffmpeg\\\\\\\\arial.ttf\:text="+i[2]+"\:x="+str(i[3][0])+"\:y="+str(i[3][1])+" "+modify_filename(new_name)
        #cmd=[get_setting("FFMPEG_BINARY"),"-y","-i",input_file,"-vf","drawtext=enable=\'between(t,"+str(start)+","+str(end)+")\'","\:fontfile=C\://ffmpeg//arial.ttf","\:text="+i[2],"\:x="+str(i[3][0]),"\:y="+str(i[3][1]),modify_filename(new_name)]
        '''cmd = [get_setting("FFMPEG_BINARY"),"-y",
        "-i", filename,
        "-ss", "%0.2f"%t1,
        "-t", "%0.2f"%(t2-t1),
        "-vcodec", "copy", "-acodec", "copy", targetname]

    p = subprocess.Popen(cmd, shell=True,
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = p.communicate()[0]'''
        print(cmd)
        p = subprocess.Popen(cmd.split(), shell=True,
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = p.communicate()[0]
        print(output)

putText("C:\moviepy-master\moviepy-master\lecture7.mp4","C:\moviepy-master\moviepy-master\image_videotext.mp4",[[5,50,"helloworld",(100,100)]])
