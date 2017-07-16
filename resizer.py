#using moviepy it takes really long 
import moviepy.editor as mp
#import imageio
#imageio.plugins.ffmpeg.download()
clip=mp.VideoFileClip("extract1.mp4")
new_size=clip.resize((426,240))
new_size.write_videofile("RESIZED1.mp4")

#the alternative seems to have an error 
import subprocess
import os

pathtovid=os.path.abspath('trial.mp4')
cmd="ffmpeg -i "+pathtovid+"-vf scale=640:360 movie_360p.mp4"
subprocess.call(cmd.split())



#The extract bit
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
ffmpeg_extract_subclip("lecture5.mp4",6,55,targetname="extract2.mp4")

#trim bit

import subprocess
import os
seconds = "4"
mypath=os.path.abspath('trial.mp4')
subprocess.call(['ffmpeg', '-i',mypath, '-ss', seconds, 'trimmed.mp4'])


