
def speed_change(original_video,modifier_list):
     '''original_video_file="C:\\moviepy-master\\lecture4.mp4"
     clip = VideoFileClip(original_video_file)
     starttime=100#modifier_list[0]
     endtime=400#modifier_list[1]
     textfilename="C:\\moviepy-master\\concatenate.txt"
     f1=open(textfilename,'w')
     name=str(1)+".mp4"
     ffmpeg_extract_subclip(original_video_file,0,starttime,targetname=name)
     f1.write("file C:"+"\\"+"\moviepy-master"+"\\"+"\\"+name+"\n")
     name=str(2)+".mp4"
     ffmpeg_extract_subclip(original_video_file,starttime,endtime,targetname=name)
     f1.write("file C:"+"\\"+"\moviepy-master"+"\\"+"\\"+name+"\n")
     name=str(3)+".mp4"
     ffmpeg_extract_subclip(original_video_file,endtime+1,math.ceil(clip.duration),targetname=name)
     f1.write("file C:"+"\\"+"\moviepy-master"+"\\"+"\\"+name+"\n")
     f1.close()

     original_video_file="C:\\Users\\sanat\\Desktop\\EDOS\\D4.mp4"
     clip = VideoFileClip(original_video_file)
     starttime=math.ceil(modifier_list[0]/10)
     endtime=math.ceil(modifier_list[1]/10)
     textfilename="C:\\Users\\sanat\\Desktop\\EDOS\\concatenate.txt"
     f1=open(textfilename,'w')
     name=str(1)+".mp4"
     ffmpeg_extract_subclip(original_video_file,0,starttime,targetname=name)
     f1.write("file C:"+"\\"+"\Users"+"\\"+"\sanat"+"\\"+"\Desktop"+"\\"+"\EDOS"+"\\"+"\\"+name+"\n")
     name=str(2)+".mp4"
     ffmpeg_extract_subclip(original_video_file,endtime+1,math.ceil(clip.duration),targetname=name)
     f1.write("file C:"+"\\"+"\Users"+"\\"+"\sanat"+"\\"+"\Desktop"+"\\"+"\EDOS"+"\\"+"\\"+name+"\n")
     f1.close()


     '''
     cmd="ffmpeg -i C:\\Users\\sanat\\Desktop\\EDOS\\D4.mp4 -filter_complex \"[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]\" -map \"[v]\" -map \"[a]\" 2.mp4"
     subprocess_call(cmd.split))
      
     #cmd=cmd="ffmpeg -f concat -safe 0 -i "+textfilename+" -c copy C:\\moviepy-master\\+"+original_video
     #subprocess_call(cmd.split())
      
     
speed_change("t",[])
