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
class horizontal_button_group:
    def __init__(self,master,name,task):
        self.button=Button(master,text=name,fg='white',bg='red',command=task)
        self.button.pack(padx=10,side=LEFT)
class create_label:
    def __init__(self,frame,message,font_color,padingx,padingy):
        self.label=Label(frame,text=message,fg=font_color)
        self.label.pack(pady=padingy)
class create_frame:
    def __init__(self,master,fheight,fwidth,place,bg_color,filling):
        self.frame=Frame(master,bg=bg_color,width=fwidth,height=fheight)
        self.frame.pack(side=place,fill=filling)
        self.frame.propagate(0)
########################################SETTING UP THE APPLICATION######################################################
class set_up_GUI:
    ###############################INITIALIZE THE GUI###########################################
    def __init__(self,root):
        self.videos_list=[]#list that holds the paths of inserted videos
        self.sequence_video_list=[]#list that holds the paths of sequenced videos in order
        root.attributes('-fullscreen', True)
        root.title("Sports Video Editor")
        root.aspect(1,1,1,1)
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        self.toolbar3=create_frame(root,0.15*self.screen_height,self.screen_width,BOTTOM,'gray80',X)#frame for video controls
        self.label_controls=create_label(self.toolbar3.frame,"Controls area",'red',30,0)
        self.toolbar=create_frame(root,0.85*self.screen_height,0.1*self.screen_width,LEFT,'blue',Y,)#frame for videos in sequence
        self.label_selected_videos=create_label(self.toolbar.frame,"Select videos",'red',30,30)
        self.toolbar1=create_frame(root,0.85*self.screen_height,0.8*self.screen_width,LEFT,'snow1',Y)#frame for video player
        self.label_video_area=create_label(self.toolbar1.frame,"Video area",'red',460,30)
        self.toolbar2=create_frame(root,0.85*self.screen_height,0.1*self.screen_width,RIGHT,'blue',Y)#frame for imported videos
        self.label_imported_video=create_label(self.toolbar2.frame,"Import videos",'red',30,30)
        self.browse_button=simple_button(self.toolbar2.frame,'Browse files','white','blue',self.browse_options)
        self.undo_button=horizontal_button_group(self.toolbar3.frame,'UNDO',self.dummy_function)
        self.trim_button=horizontal_button_group(self.toolbar3.frame,'TRIM VIDEO',self.dummy_function)
        self.speed_button=horizontal_button_group(self.toolbar3.frame,'CHANGE SPEED',self.dummy_function)
        self.zoom_button=horizontal_button_group(self.toolbar3.frame,'ZOOM',self.dummy_function)
        self.exit_button=horizontal_button_group(self.toolbar3.frame,'EXIT',root.quit)
    ########################Methods to import and select the videos########################################
    def check_file_existance(self,file,list_id):
        if((file.name not in self.videos_list and list_id==1) or (file.name not in self.sequence_video_list and list_id==2)):
            if(list_id==1):
                self.videos_list.append(file.name)
            else:
                self.sequence_video_list.append(file.name)
            return TRUE
        else:
            tkMessageBox.showinfo("Title", "File already exists")
            return FALSE
    def set_video_to_button(self,file_name):
        os.system(file_name)
    def insert_video_to_sequence(self,file):
        if(self.check_file_existance(file,2)):
            sequence_video=simple_button(self.toolbar.frame,self.get_file_name(file),'blue','white',lambda: self.set_video_to_button(file.name))
    def get_file_name(self,file):
        name=str(file.name)
        name=list(name.split('/'))
        name=name[len(name)-1]
        type=list(name.split('.'))
        extensions=['m1v', 'mpeg', 'mov', 'qt', 'mpa', 'mpg', 'mpe', 'avi', 'movie', 'mp4','wmv']
        if(type[len(type)-1].lower() in extensions):#also include all the desired extensions.
            return name
        else:
            raise RuntimeError("Looks like this is not a video file")
    def insert_video(self,file):
        if(self.check_file_existance(file,1)):
            name=self.get_file_name(file)
            new_video=simple_button(self.toolbar2.frame,name,'blue','white',lambda: self.insert_video_to_sequence(file))
    def browse_options(self):
        file = tkFileDialog.askopenfile(parent=root,mode='rb',title='Choose a file')
        if file != None:
            try:
                self.insert_video(file)
            except RuntimeError as e:
                tkMessageBox.showinfo("Title", e)
            file.close()
    def dummy_function(self):#Does Nothing,just for testing purpose.
        print ""
##########################################Main program starts###########################################################
root=Tk()
Video_App=set_up_GUI(root)
root.mainloop()




