import subprocess
from moviepy.editor import *
import math
import os
from moviepy.config import get_setting
import cv2

## A list to store the paths of the edited video list for later use
edited_videos_list=[]
path_to_edited_videos="C:\\edited_videos"
 
output_video_name="C:\edited_videos\final.mp4"


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
     edited_video=modify_filename(edited_video_name)
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
     name=pname+str(1)+extension
     ffmpeg_extract_subclip(original_video,0,starttime,targetname=name)
     f1.write("file "+modify_filename(name)+"\n")
     name=pname+str(2)+extension
     ffmpeg_extract_subclip(original_video,endtime+1,math.ceil(clip.duration),targetname=name)
     f1.write("file "+modify_filename(name)+"\n")
     f1.close()

     #FFMPEG Command to concatenate videos 
     print("0000000000"+edited_video_name+"000000000000000")
     cmd = [get_setting("FFMPEG_BINARY"),"-y",
      "-f","concat","-safe","0","-i", textfilename,"-c","copy",edited_video]
    #cmd="ffmpeg -y -f concat -safe 0 -i "+textfilename+" -c copy "+edited_video
     p = subprocess.Popen(cmd, shell=True,
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
     output = p.communicate()[0]
     #subprocess_call(cmd.split())
     os.remove("C:\\edited_videos\\1.mp4")
     os.remove("C:\\edited_videos\\2.mp4")
     print("done with function")
     return edited_video_name


def save_feature():

     ##### This method stitches  all the videos together and saves it as one 
     ## Text file to store the names of the video files to be stitched 
     ## The output Video name to be sent with the path 

     videos_file=open("C:\edited_videos\concatall.txt",'w')
     for i in edited_videos_list:
          modified_name=modify_filename(i)
          videos_file.write("file "+modified_name+'\n')
     videos_file.close()

     cmd="ffmpeg -y -f concat -safe 0 -i C:\\edited_videos\\concatall.txt -c copy C:\\edited_videos\\final_video.mp4"
     
     p = subprocess.Popen(cmd.split(), shell=True,
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
     output = p.communicate()[0]
     print (output)
     return "C:\\edited_videos\\final_video.mp4"
     

def speed_changer(original_video,edited_video_name,modifier_list):
     ''' The following function take the starting , ending timesand the speed 
          To slow down or speed up the video
          Three parts are made
          1-Beginning the start time
          2-The part which needs speed modification
          3-End time till the video lasts
          These three parts are concatenated to give back the input video with modified speed'''
     pname=path_to_edited_videos+"\\"
     extension=original_video[original_video.rfind("."):]
     edited_video_name=modify_filename(edited_video_name)
    
     if modifier_list[2]==1.5:
          v_speed=0.68
          a_speed=1.467
     elif modifier_list[2]==2.0:
          v_speed=0.5
          a_speed=2.0
     elif modifier_list[2]==0.5:
          v_speed=1.467
          a_speed=0.68
     elif modifier_list[2]==0.25:
          v_speed=2.0
          a_speed=0.5
     elif modifier_list[2]==1:
         return
     

     #An object created   
     clip = VideoFileClip(original_video) 

     #Converting the start and end times to     
     starttime=math.ceil(modifier_list[0]/1000)
     endtime=math.ceil(modifier_list[1]/1000)

     #Creating the text file 
     textfilename=path_to_edited_videos+"\\concat.txt"

     #Opening a file to write the names of the videos to be concantenated 
     f1=open(textfilename,'w')

     name=path_to_edited_videos+"\\"+str(1)+extension
     ffmpeg_extract_subclip(original_video,0,starttime,targetname=name)   #Part1
     f1.write("file "+modify_filename(name)+"\n")

     to_modify_name=path_to_edited_videos+"\\"+str(2)+extension
     ffmpeg_extract_subclip(original_video,starttime,endtime,targetname=to_modify_name)#Part2
     f1.write("file "+modify_filename(path_to_edited_videos)+"\\"+"\\"+str(23)+extension+"\n")

     name=path_to_edited_videos+"\\"+str(3)+extension
     ffmpeg_extract_subclip(original_video,endtime+1,math.ceil(clip.duration),targetname=name)#Part3
     f1.write("file "+modify_filename(name)+"\n")
     
     f1.close()
     
     #Speeding up the specified part
     cmd="ffmpeg -y -i "+to_modify_name+" -vf setpts="+str(v_speed)+"*PTS -filter:a atempo="+str(a_speed)+" "+path_to_edited_videos+"\\"+str(23)+extension
     print(cmd)
     p = subprocess.Popen(cmd.split(), shell=True,
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
     output = p.communicate()[0]
     print(output)
     #FFMPEG Command to concatenate videos  
     cmd="ffmpeg -y -f concat -safe 0 -i "+textfilename+" -c copy "+edited_video_name
     p = subprocess.Popen(cmd.split(), shell=True,
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
     output = p.communicate()[0]
     print("concat gave-->"+output)
     os.remove("C:\\edited_videos\\1.mp4")
     os.remove("C:\\edited_videos\\2.mp4")
     os.remove("C:\\edited_videos\\3.mp4")
     os.remove("C:\\edited_videos\\23.mp4")
     return edited_video_name 
    
def putText(original_video,new_name,text_list):
    input_file=modify_filename(original_video)
    for i in text_list:
        start=i[0]/1000
        end=i[1]/1000
        cmd="ffmpeg -y -i "+input_file+" -vf drawtext=enable=\'between(t,"+str(start)+","+str(end)+")\':fontfile=C:\\\\\\\\ffmpeg\\\\\\\\arial.ttf:text="+i[2]+":x="+str(i[3][0])+":y="+str(i[3][1])+" "+modify_filename(new_name)
        print(cmd)
        p = subprocess.Popen(cmd.split(), shell=True,
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = p.communicate()[0]
        print(output)
    #print(text_list[0][3])


def draw(original_video,new_name,parameter_list):
    cap = cv2.VideoCapture(original_video)
    extension=original_video.split(".")[1]
    #finding the codec
         
    if extension=="mp4":
        codec='MP4V'
    elif extension=="avi" or extension=="AVI":
        codec='XVID'
        
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

    #and uses corresponding function to find the frame rate
    if int(major_ver)  < 3 :
        fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
        print type(fps)
        print "Frames pper second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps)
    else :
        fps = cap.get(cv2.CAP_PROP_FPS)
        print type(fps)
        print "Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps)

    fourcc = cv2.VideoWriter_fourcc(*codec)
    print(fourcc)
    out = cv2.VideoWriter('edits1.avi',fourcc, fps, (int(cap.get(3)),int(cap.get(4))),True)#,480)
    counter=1
    pause_frame=fps*parameter_list[0]
    rgb_value=parameter_list[2]
    
    write_same_frame=(parameter_list[1] - parameter_list[0])*fps
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret==True:
            print(counter)
            if counter == pause_frame:
                counter=counter+1
                cv2.imwrite("tempimg.jpg")
                img = cv2.imread('tempimg.jpg')
                parameter_list[3].pop(0)
                index = 0
                for i in range(0,len(parameter_list[3]),1):
                    if parameter_list[3][i][0] == -1:
                        print "-1 encountered at "+str(i)
                        print " range from "+ str(index+1)+" to "+str(i) 
                        for j in range(index+1,i,1):
                            start=parameter_list[3][j-1]
                            end=parameter_list[3][j]
                            print start , end
                            print
                            cv2.line(img,start,end,rgb_value)                     
                        index = i+1
                cv2.imwrite('tempimg.jpg',img)
                img=cv2.imread('tempimg.jpg')
                while write_same_frame>0:
                        out.write(img)
                        cv2.imshow('frame',img)
                        write_same_frame=write_same_frame-1
                        print("same frame work")
            else:
                    out.write(frame)
                    cv2.imshow('frame',frame)
                    counter=counter+1

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("exiting")
                break
            else:
                break
              
    cap.release()
    out.release()
    cv2.destroyAllWindows()   
        
             
     
    
    
###################--------------------THE ACTUAL INTERFACING FUNCTION------------------#################
def get_video_data(file_path,operations_dictionary):
    #Call to create new directory function
    create_new_directory()
    ## CREATE NEW VIDEO FILENAME 
    new_name=path_to_edited_videos+file_path[file_path.rfind("\\"):file_path.rfind(".")]
    name_only=new_name[:]
    new_name+="_edit"+file_path[file_path.rfind("."):]
    print(new_name+"******")
    edited_videos_list.append(new_name)
    print operations_dictionary
    if operations_dictionary["trim"]!=[]:
        for i in operations_dictionary["trim"]:
            new_name=trimmer(file_path,new_name,i)

    if operations_dictionary["speed"]!=[]:
        list_of_speed_changes=operations_dictionary["speed"]
        for i in range(1,len(list_of_speed_changes)):            
            speed_changer(file_path,new_name,list_of_speed_changes[i])

    if operations_dictionary["text"]!=[]:
        putText(file_path,new_name,operations_dictionary["text"])

    if operations_dictionary["shapes"]!=[]:
        print("Came into the draw function!")
        #print(parameter_list)
        print("is the one we need to think about now !!!")
        draw(file_path,new_name,operations_dictionary["shapes"][0])
        '''
        rgb_value=parameter_list[0][2]
        #1,241)]
        index = 0
        img = cv2.imread('1200.jpg')
        parameter_list[0][3].pop(0)
        for i in range(0,len(parameter_list[0][3]),1):            
             if parameter_list[0][3][i][0] == -1:
                 print "-1 encountered at "+str(i)
                 print " range from "+ str(index+1)+" to "+str(i) 
                 for j in range(index+1,i,1):
                     start=parameter_list[0][3][j-1]
                     end=parameter_list[0][3][j]
                     print start , end
                     print
                     #img = cv2.imread('1200.jpg')
                     cv2.line(img,start,end,rgb_value)                     
                 index = i+1
             
        cv2.imwrite('1200.jpg',img)
        #cv2.imshow("img",img)
        cv2.waitKey()
        cv2.destroyAllWindows()
        '''
        


    
#convert_to_yuv("c:\\edited_videos\\1.mp4")
    
    
    
    




          
          
     
     
     
