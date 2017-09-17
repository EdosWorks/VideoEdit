import sys
from back_end import convert_to_yuv

#The following lines sets the encoding format to utf8
reload(sys)
sys.setdefaultencoding('utf8')  

#call the change to yuv format function here
#the file is save as - the_name_your_video_fileyuv.yuv i.e a yuv added to the original filename and .yuv extension added

fin=open("C:\\edited_videos\\1yuv.yuv","rb") 
fout=open("C:\\edited_videos\\output_file.yuv","wb")

frame_num=0
height = 720
width = 1280
frame_size = height*width
byte=[]

byte = fin.read(frame_size)
while(byte):
     data=[]
     if(byte):
          for i in byte:
               data.append(i)
          data.append('\0')
          #some function is done
          #assuming the array was modified

          newdata=''
          for i in data:
               newdata+=i
          fout.write(newdata.encode('utf-8'))
     byte = fin.read(frame_size)
     
          

          
     
          
