def trimmer(original_video,modifier_list):
     '''video_file_name=''
     for i in range (0,len(original_video),1):
          if original_video[i]=="\\":
               video_file_name+="\\"
          video_file_name+=video_file_name[i]'''
          
     
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

     cmd="ffmpeg -f concat -safe 0 -i "+textfilename+" -c copy "+original_video
     #+original_video_file
     subprocess_call(cmd.split())
