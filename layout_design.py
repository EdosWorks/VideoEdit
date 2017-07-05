################################################Import modules##########################################################
try:
    from Tkinter import *#version 2.7
except ImportError:
    from tkinter import *#version 3.0
from PIL import ImageTk,Image
import tkFileDialog,tkMessageBox
import os
import cv2
###########################################classes for widgets##########################################################
class simple_button:
    def __init__(self,master,name,font_color,backg_color,task):
        self.create_button=Button(master,text=name,fg=font_color,bg=backg_color,command=task)
        self.create_button.pack(pady=10)
class horizontal_button_group:
    def __init__(self,master,name,task):
        screen_width=root.winfo_screenwidth()
        width_padding=(3*screen_width)/128
        self.button=Button(master,text=name,fg='white',bg='red',command=task,width=20)
        self.button.pack(padx=width_padding,side=LEFT)
        self.button.propagate(0)
class standard_dropDown_menu:
    def __init__(self,obj,master,name,purpose):
        screen_width=root.winfo_screenwidth()
        width_padding=(2*screen_width)/128
        self.variable = StringVar(master)
        self.variable.set(name) # default value
        if(purpose=='shape'):
            self.variable.trace("w", obj.shapes_output__function)
            self.menu = OptionMenu(master, self.variable, "SQUARE", "TRIANGLE", "CIRCLE","ARROW")
        elif(purpose=='speed'):
            self.variable.trace("w", obj.speed_output__function)
            self.menu = OptionMenu(master, self.variable, "0.25 x", "0.5 x", "1.5 x","2.0 x")
        self.menu.pack(padx=width_padding,side=LEFT)
        self.menu.config(bg='red',fg='white',width=width_padding)
        self.menu.propagate(0)
class create_label:
    def __init__(self,frame,message,font_color,padingx,padingy):
        self.label=Label(frame,text=message,fg=font_color)
        self.label.pack(pady=padingy)
class create_frame:
    def __init__(self,master,fheight,fwidth,place,bg_color,filling):
        self.frame=Frame(master,bg=bg_color,width=fwidth,height=fheight)
        self.frame.pack(side=place,fill=filling)
        self.frame.propagate(0)
########################################RUNNING THE APPLICATION######################################################
class set_up_GUI:
    def __init__(self,root):
    ###############################INITIALIZE THE GUI###########################################
        self.videos_list=[]#list that holds the paths of inserted videos
        self.sequence_video_list=[]#list that holds the paths of sequenced videos in order
        root.attributes('-fullscreen', True)
        root.title("Sports Video Editor")
        root.aspect(1,1,1,1)
        self.cap=FALSE
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        self.toolbar3=create_frame(root,0.15*self.screen_height,self.screen_width,BOTTOM,'gray80',X)#frame for video controls
        self.label_controls=create_label(self.toolbar3.frame,"Controls area",'red',30,0)
        self.toolbar=create_frame(root,0.85*self.screen_height,0.1*self.screen_width,LEFT,'blue',Y,)#frame for videos in sequence
        self.label_selected_videos=create_label(self.toolbar.frame,"Select videos",'red',30,30)
        self.toolbar1=create_frame(root,0.85*self.screen_height,0.8*self.screen_width,LEFT,'snow1',Y)#frame for video player
        self.video_holder = Label(self.toolbar1.frame)
        #self.video_holder.pack(side=LEFT,fill=X)#,expand=True)
        #self.video_holder.config(width=int(1.85*self.screen_width))
        self.toolbar2=create_frame(root,0.85*self.screen_height,0.1*self.screen_width,RIGHT,'blue',Y)#frame for imported videos
        self.label_imported_video=create_label(self.toolbar2.frame,"Import videos",'red',30,30)
        self.browse_button=simple_button(self.toolbar2.frame,'Browse files','white','blue',self.browse_options)
        self.undo_button=horizontal_button_group(self.toolbar3.frame,'UNDO',self.dummy_function)
        self.trim_button=horizontal_button_group(self.toolbar3.frame,'TRIM VIDEO',self.dummy_function)
        self.speed_menu=standard_dropDown_menu(self,self.toolbar3.frame,"CHANGE SPEED","speed")
        self.zoom_button=horizontal_button_group(self.toolbar3.frame,'ZOOM',self.dummy_function)
        self.shape_menu=standard_dropDown_menu(self,self.toolbar3.frame,"SHAPE","shape")
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
                tkMessageBox.showinfo("Error", e)
            file.close()
    #######################################Video_Modification_Controls##################################################
    def shapes_output__function(self,*args):
        tkMessageBox.showinfo("Shape selected",self.shape_menu.variable.get())
    def speed_output__function(self,*args):
        tkMessageBox.showinfo("Speed selected",self.speed_menu.variable.get())
    def dummy_function(self):#Does Nothing,just for testing purpose.
        print ""
    #######################################Display Videos###############################################################
    def set_video_to_button(self,file_name):
        if self.cap!=FALSE:
            self.cap.release()
            self.video_holder.destroy()
            cv2.destroyAllWindows()
        self.video_holder = Label(self.toolbar1.frame)
        self.video_holder.pack(side=LEFT,fill=X)
        self.cap = cv2.VideoCapture(file_name)

        def show_frame():
            _, frame = self.cap.read()
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_holder.imgtk = imgtk
            self.video_holder.configure(image=imgtk)
            self.video_holder.after(2, show_frame)
        show_frame()


##########################################Main program starts###########################################################
root=Tk()
Video_App=set_up_GUI(root)
root.mainloop()


