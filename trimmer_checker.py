from moviepy.editor import *
import math
import subprocess
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
    
    subprocess_call(cmd)


    
def trimmer(original_video="fgh",edited_video_name="C:\\edited_videos\\sdfgh.mp4",modifier_list=[]):
     ''' The following function take the starting and ending times which specify the unwanted bit of the video
          To eleminate the same two parts of the video is made
          One from the very beginning to the start time and one from the end time till the very end
          The two parts are concatenated to give back the video without the specified bit'''
     '''
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
     f1.write("file "+modify_filename(pname)+name+"\n")
     name=str(2)+extension
     ffmpeg_extract_subclip(original_video,endtime+1,math.ceil(clip.duration),targetname=name)
     f1.write("file "+modify_filename(pname)+name+"\n")
     f1.close()
   '''
     #FFMPEG Command to concatenate videos
     print(edited_video_name)
     cmd="ffmpeg -f concat -safe 0 -i "+"C:\\edited_videos\\concat.txt"+" -c copy "+edited_video_name
     p = subprocess.Popen(cmd.split(), shell=True,
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
     output = p.communicate()[0]
     #subprocess_call(cmd.split())
     print("done with function")

trimmer()
