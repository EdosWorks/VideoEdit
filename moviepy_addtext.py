'''
The following function is to add text to the video so as of now the function works this way.
-Takes the start and end time where the text should be there
-makes a SUBCLIP of it adds the desired text to that and SAVES THE SUBCLIP ONLY TO THE FILE NAME SPECIFIED
-PARAMETERS REQUIRED:
     
     original file name with path
     new file name with path
     start and end times in seconds
     the text to be added
'''

#Note that the values shown to be hardcoded can be made variable once this function is choden as the backend function from text

#The file name if contains a \ shouldbe given with \\ as \ is a character that is included before an escape character symbol so
#       if we want \ to be recogonised we give it with \\


from moviepy.editor import *
def addtext_m(original_filename,new_filename,start,end,add_text):
     #the following line makes a subclip from the start to end time (subclip is an object now )
     video = VideoFileClip(original_filename).subclip(start,end)

     #The line to create a clip of the text wanted so that it can be added onto the video(text clip is an object now)
     #hardcoded values of fontsize to 70 and poition to center
     txt_clip = ( TextClip(add_text,fontsize=70,color='white').set_position('center').set_duration(end-start) )


     #The following line is to put the text clip on top of the video
     result = CompositeVideoClip([video, txt_clip])

     #Follwing line is to write the object to a file and the FRAME RATE IS HARDCODED TO 25 
     result.write_videofile(new_filename,fps=25)


addtext_m("C:\\edited_videos\\image_video.mp4","C:\\edited_videos\\2try.mp4",30,60,"trial text")
