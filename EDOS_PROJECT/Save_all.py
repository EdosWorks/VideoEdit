import subprocess
def modify_filename(filename):
     newfilename=''
     for(i in filename):
          if i=='\\':
               newfilename+='\\'
          newfilename+=i
     return newfilename
def save_feature(videos_sequence_list[],output_video_name):

     ##### This method stitches every all the videos together and saves it as one ######
     ## Text file to store the names of the video files to be stitched #####
     ## The output Video name to be sent with the path ##

     videos_file=open("concat.txt",'w')
     for i in video_sequence_list:
          modified_name=modify_filename(i)
          videos_file.write(modified_name+'\n')
     videos_file.close()

     cmd="ffmpeg -f concat -safe 0 -i "+videos_file+" -c copy "+output_video_name
     subprocess_call(cmd.split())
     

          
          
          
     
     
     
