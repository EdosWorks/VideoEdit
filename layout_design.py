################################################Import modules##########################################################
try:
    from Tkinter import *#version 2.7
except ImportError:
    from tkinter import *#version 3.0
#from PIL import ImageTk,Image
import tkFileDialog,tkMessageBox
import os
###########################################classes for widgets##########################################################
class simple_button:
    def __init__(self,master,name,font_color,backg_color,task):
        self.create_button=Button(master,text=name,fg=font_color,bg=backg_color,command=task)
        self.create_button.pack(pady=10)

class create_label:
    def __init__(self,frame,message,font_color,padingx,padingy):
        self.label=Label(frame,text=message,fg=font_color)
        self.label.pack(pady=padingy)
class create_frame:
    def __init__(self,master,fheight,fwidth,place,bg_color,filling):
        self.frame=Frame(master,bg=bg_color,width=fwidth,height=fheight)
        self.frame.pack(side=place,fill=filling)
        self.frame.propagate(0)
################################Methods to import and select the videos#################################################
videos_list=[]#list that holds the paths of inserted videos
sequence_video_list=[]#list that holds the paths of sequenced videos in order
def check_file_existance(file,list_id):
    if((file.name not in videos_list and list_id==1) or (file.name not in sequence_video_list and list_id==2)):
        if(list_id==1):
            videos_list.append(file.name)
        else:
            sequence_video_list.append(file.name)
        return TRUE
    else:
        tkMessageBox.showinfo("Title", "File already exists")
        return FALSE
def set_video_to_button(file_name):
     os.system(file_name)
def insert_video_to_sequence(file):
    if(check_file_existance(file,2)):
        sequence_video=simple_button(toolbar.frame,get_file_name(file),'blue','white',lambda: set_video_to_button(file.name))
def get_file_name(file):
    name=str(file.name)
    name=list(name.split('/'))
    name=name[len(name)-1]
    type=list(name.split('.'))
    extensions=['m1v', 'mpeg', 'mov', 'qt', 'mpa', 'mpg', 'mpe', 'avi', 'movie', 'mp4','wmv']
    if(type[len(type)-1].lower() in extensions):#also include all the desired extensions.
        return name
    else:
        raise RuntimeError("Looks like this is not a video file")
def insert_video(file):
    if(check_file_existance(file,1)):
        name=get_file_name(file)
        new_video=simple_button(toolbar2.frame,name,'blue','white',lambda: insert_video_to_sequence(file))
def browse_options():
    file = tkFileDialog.askopenfile(parent=root,mode='rb',title='Choose a file')
    if file != None:
        try:
            insert_video(file)
        except RuntimeError as e:
                tkMessageBox.showinfo("Title", e)
        file.close()
##########################################Main program starts###########################################################
root=Tk()
root.attributes('-fullscreen', True)
root.title("Sports Video Editor")
root.aspect(1,1,1,1)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
toolbar3=create_frame(root,0.15*screen_height,screen_width,BOTTOM,'gray80',X)#frame for video controls
label_controls=create_label(toolbar3.frame,"Controls area",'red',30,0)
toolbar=create_frame(root,0.85*screen_height,0.1*screen_width,LEFT,'blue',Y,)#frame for videos in sequence
label_selected_videos=create_label(toolbar.frame,"Select videos",'red',30,30)
toolbar1=create_frame(root,0.85*screen_height,0.8*screen_width,LEFT,'snow1',Y)#frame for video player
label_video_area=create_label(toolbar1.frame,"Video area",'red',460,30)
toolbar2=create_frame(root,0.85*screen_height,0.1*screen_width,RIGHT,'blue',Y)#frame for imported videos
label_imported_video=create_label(toolbar2.frame,"Import videos",'red',30,30)
browse_button=simple_button(toolbar2.frame,'Browse files','white','blue',browse_options)
exit_button=simple_button(toolbar3.frame,'EXIT','red','white',root.quit)
root.mainloop()




