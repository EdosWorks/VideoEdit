import wx
import wx.media
import os
import wx.lib.scrolledpanel
from moviepy.editor import VideoFileClip, concatenate_videoclips
from PIL import Image
import numpy as np
import time
import wx.lib.buttons
import shutil
#----------------------------------------------------------------------

class StaticText(wx.StaticText):
    """
    A StaticText that only updates the label if it has changed, to
    help reduce potential flicker since these controls would be
    updated very frequently otherwise.
    """
    def SetLabel(self, label):

        if label <> self.GetLabel():
            wx.StaticText.SetLabel(self, label)

#----------------------------------------------------------------------
class dropDown_menu:
    counter=300

    id=1
    def __init__(self,place,option_list):
        self.screenWidth=wx.DisplaySize()[0]
        self.screenHeight=wx.DisplaySize()[1]
        self.id=dropDown_menu.id
        if dropDown_menu.id==1:
            dropDown_menu.counter=self.get_relative_X(300)
        dropDown_menu.id+=1
        self.create(place,option_list)
        dropDown_menu.counter+=self.get_relative_X(150)
    def create(self,place,option_list):

        # Add a panel so it looks the correct on all platforms
        if dropDown_menu.counter==self.get_relative_X(300):
            default_value="Speed"
        else:
            default_value="Shape"


        sampleList = []
        self.cb = wx.ComboBox(place,value=default_value,pos=(dropDown_menu.counter,self.get_relative_Y(50)),
                              size=(self.get_relative_X(100),self.get_relative_Y(50)),
                              choices=sampleList)
        self.widgetMaker(self.cb, option_list)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.cb, 0, wx.ALL, 5)
        place.SetSizer(sizer)

    #----------------------------------------------------------------------
    def widgetMaker(self, widget, objects):
        """"""
        for obj in objects:
            widget.Append(obj, obj)
        widget.Bind(wx.EVT_COMBOBOX, self.onSelect)

    #----------------------------------------------------------------------
    def onSelect(self, event):
        obj = self.cb.GetClientData(self.cb.GetSelection())
        if(self.id==1):
            frame.speed_menu_output(obj)
        elif(self.id==2):
            frame.shape_menu_output(obj)


    def get_relative_Y(self,y):
        h=(self.screenHeight*y)/720
        return h



    def get_relative_X(self,x):
        w=(self.screenWidth*x)/1280
        return w

class TestPanel(wx.Frame):

    def __init__(self,parent,id,title):
       #First retrieve the screen size of the device
        screenSize = wx.DisplaySize()
        self.screenWidth = screenSize[0]
        self.screenHeight = screenSize[1]

        #Create a frame
        wx.Frame.__init__(self,parent,id,title,size=screenSize, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.Bind(wx.EVT_CLOSE, self.ShutdownDemo)
        self.media_player_panel= wx.Panel(self,size=(8/10*self.screenWidth,4*self.screenHeight/5), pos=(self.screenWidth/10,0), style=wx.SIMPLE_BORDER)
        self.sequence_video_panel = wx.lib.scrolledpanel.ScrolledPanel(self,-1, size=(self.screenWidth/10,4*self.screenHeight/5+self.screenHeight/16), pos=(0,0), style=wx.SIMPLE_BORDER)
        self.sequence_video_panel.SetupScrolling()
        self.sequence_video_panel.SetBackgroundColour('#777777')
        self.video_operators_panel = wx.Panel(self,size=(8*self.screenWidth/10,self.screenHeight/5), pos=(self.screenWidth/10,4*self.screenHeight/5), style=wx.SIMPLE_BORDER)
        self.video_operators_panel.SetBackgroundColour('#FFFFFF')
        self.imported_video_panel = wx.lib.scrolledpanel.ScrolledPanel(self,-1, size=(self.screenWidth/10,4*self.screenHeight/5+self.screenHeight/16), pos=(9*self.screenWidth/10,0), style=wx.SIMPLE_BORDER)
        self.imported_video_panel.SetupScrolling()
        self.imported_video_panel.SetBackgroundColour('#777777')
        self.slider_panel = wx.Panel(self.video_operators_panel,size=(8*self.screenWidth/10,self.screenHeight/16), pos=(0,0), style=wx.SIMPLE_BORDER)
        self.slider_panel.SetBackgroundColour('#AAAAAA')


        self.import_undo_panel = wx.Panel(self,size=(1*self.screenWidth/10,11*self.screenHeight/80), pos=(9*self.screenWidth/10,69*self.screenHeight/80), style=wx.SIMPLE_BORDER)
        self.import_undo_panel.SetBackgroundColour('#777777')

        self.sequence_undo_panel = wx.Panel(self,size=(1*self.screenWidth/10,11*self.screenHeight/80), pos=(0,69*self.screenHeight/80), style=wx.SIMPLE_BORDER)
        self.sequence_undo_panel.SetBackgroundColour('#777777')


        bSizer = wx.BoxSizer( wx.HORIZONTAL )


        load_button = wx.Button(self.video_operators_panel,label="Load File",pos=(self.get_relative_X(50),self.get_relative_Y(47)),size=(self.get_relative_X(100),self.get_relative_Y(30)))
        load_button.Bind(wx.EVT_BUTTON, self.OnLoadFile, load_button)

        trim_button = wx.ToggleButton(self.video_operators_panel, -1, "TRIM",pos=(self.get_relative_X(170),self.get_relative_Y(47)),size=(self.get_relative_X(100),self.get_relative_Y(30)))
        trim_button.Bind(wx.EVT_TOGGLEBUTTON, self.on_trim, trim_button)
        self.playBtn = trim_button

        text_button = wx.ToggleButton(self.video_operators_panel, -1, "ADD TEXT",pos=(self.get_relative_X(570),self.get_relative_Y(47)),size=(self.get_relative_X(100),self.get_relative_Y(30)))
        text_button.Bind(wx.EVT_TOGGLEBUTTON, self.on_text_entry, text_button)
        self.text_but=text_button

        done_button = wx.Button(self.video_operators_panel, -1, "DONE",pos=(self.get_relative_X(690),self.get_relative_Y(47)),size=(self.get_relative_X(100),self.get_relative_Y(30)))
        done_button.Bind(wx.EVT_BUTTON, self.on_done, done_button)

        exit_button = wx.Button(self.video_operators_panel, -1, "EXIT",pos=(self.get_relative_X(810),self.get_relative_Y(47)),size=(self.get_relative_X(100),self.get_relative_Y(30)))
        exit_button.Bind(wx.EVT_BUTTON, self.ShutdownDemo, exit_button)

        self.undo_imp_but = wx.Button(self.import_undo_panel, -1, "UNDO IMPORT",pos=(0,0),size=(1*self.screenWidth/10,11*self.screenHeight/220))
        self.undo_imp_but.Bind(wx.EVT_BUTTON, self.undo_import, self.undo_imp_but)

        self.undo_seq_but = wx.Button(self.sequence_undo_panel, -1, "UNDO SEQUENCE",pos=(0,0),size=(1*self.screenWidth/10,11*self.screenHeight/220))
        self.undo_seq_but.Bind(wx.EVT_BUTTON, self.undo_sequence, self.undo_seq_but)


        bSizer.Add(load_button,0,wx.ALL,5)
        bSizer.Add(trim_button,0,wx.ALL,5)
        bSizer.Add(text_button,0,wx.ALL,5)
        bSizer.Add(exit_button,0,wx.ALL,5)
        bSizer.Add(self.undo_imp_but,0,wx.ALL,5)
        bSizer.Add(self.undo_seq_but,0,wx.ALL,5)

        self.SetSizer( bSizer )



        self.speed_menu=dropDown_menu(self.video_operators_panel,['0.25','0.5','1','1.5','2'])
        self.shape_menu=dropDown_menu(self.video_operators_panel,['square','triangle','rectangle','circle'])

        wx.CallAfter(self.DoLoadFile, os.path.abspath("data/testmovie.mpg")) #check



        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.timer.Start(100)



        slider = wx.Slider(self.slider_panel, -1, 206, 0, 255)
        self.slider = slider
        slider.SetMinSize((8*self.screenWidth/10, -1))
        self.Bind(wx.EVT_SLIDER, self.OnSeek, slider)
        #self.Bind(wx.EVT_COMMAND_SCROLL, self.OnSeek, slider)
        bSizer = wx.BoxSizer( wx.VERTICAL )
        bSizer.Add(slider, 0,)
        self.SetSizer( bSizer )


        self.videos_list=[]#list that holds the paths of inserted videos
        self.sequence_video_list=[]#list that holds the paths of sequenced videos in order
        self.sequence_video_pointer=0


        self.imported_button_list=[]
        self.sequence_button_list=[]

        self.imported_video_position=0
        self.sequence_video_position=0


        self.preferance_list=['trim','text','speed']
        self.operations_performed_list=[]
        self.operations_id_stack=[]


        self.play_flag=0
        self.current_operation_dict={0.25:'brown',0.5:'blue',1:'green',1.5:'yellow',2:'red',0:'black',-5:'pink'}
        self.status_panel_list=[]
        self.time_elapsed=0
        self.App_folder=os.path.join(os.path.expandvars("%userprofile%"),"Desktop\\Edos\\temporary_images\\")


        self.start_time=0
        self.end_time=0
        self.trim_value=0
        self.text_value=False
        self.speed_value=1


       # Create some controls

        try:
            self.media_player_panel.mc = wx.media.MediaCtrl(self.media_player_panel, style=wx.SIMPLE_BORDER,)
            self.media_player_panel.SetInitialSize((self.get_relative_X(1025),self.get_relative_Y(575)))
            but = wx.Button(self.imported_video_panel,label="Button 1",pos=(self.get_relative_X(20),self.imported_video_position),size=(self.get_relative_X(50),self.get_relative_X(50)))
            msizer=wx.BoxSizer(wx.VERTICAL)
            msizer.Add(but,0,flag=wx.EXPAND)
            self.media_player_panel.SetSizer(msizer)
            self.mc=self.media_player_panel.mc
            self.mc.ShowPlayerControls()

        except NotImplementedError:
            self.media_player_panel.Destroy()
            raise
        self.Bind(wx.media.EVT_MEDIA_LOADED, self.OnMediaLoaded)

############################################METHODS######################################################################

    def check_file_existance(self,file,list_id):
        if((file not in self.videos_list and list_id==1) or (file not in self.sequence_video_list and list_id==2)):
            if(list_id==1):
                self.videos_list.append(file)
            else:
                self.sequence_video_list.append(file)
            return True
        else:
            wx.MessageDialog(None,'FILE ALREADY EXISTS', 'Cannot add file', wx.OK | wx.ICON_INFORMATION).ShowModal()
            return False


    def import_videos(self,file_path):
        if(self.check_file_existance(file_path,1) and self.get_file_name(file_path)):
            self.undo_imp_but.Enable()
            self.imported_video_position+=self.get_relative_Y(100)
            button_image=str(self.get_image_from_video(file_path))
            bmp = wx.Bitmap(button_image, wx.BITMAP_TYPE_ANY)
            #button = wx.Button(self.imported_video_panel,label=self.get_file_name(file_path),pos=(self.get_relative_X(50),self.imported_video_position),size=(self.get_relative_X(100),self.get_relative_X(100)))
            button = wx.BitmapButton(self.imported_video_panel,id=wx.ID_ANY, bitmap=bmp,size=(self.get_relative_X(120),self.get_relative_Y(85)))
            Label=wx.StaticText(self.imported_video_panel,id=wx.ID_ANY, label=self.get_file_name(file_path),size=(self.get_relative_X(120),self.get_relative_Y(15)),style=wx.ALIGN_CENTRE)
            Label.SetBackgroundColour((255,255,255))
            button.Bind(wx.EVT_BUTTON,lambda temp=file_path: self.add_video_to_sequence(file_path,button_image))
            self.imported_button_list.append([button,Label])
            self.show_buttons(1)


    def get_image_from_video(self,file_path):
        clip = VideoFileClip(file_path)
        image_time=int(clip.duration/2)
        f=clip.get_frame(image_time) # shows the frame of the clip at t=10.5s
        img=Image.fromarray(f)
        img=img.resize((100,70))
        file_name=self.get_file_name(file_path).split('.')[0]+'.png'
        if not os.path.exists(self.App_folder):
            os.makedirs(self.App_folder)
        image_path = os.path.expanduser(self.App_folder+file_name)
        img.save(image_path)
        return image_path




    def get_file_name(self,file):
        name=str(file)
        name=list(name.split('\\'))
        name=name[len(name)-1]
        type=list(name.split('.'))
        extensions=['m1v', 'mpeg', 'mov', 'qt', 'mpa', 'mpg', 'mpe', 'avi', 'movie', 'mp4','wmv','mkv']
        if(type[len(type)-1].lower() in extensions):#also include all the desired extensions.
            return name
        else:
            raise RuntimeError("Looks like this is not a video file\n."+type[len(type)-1].lower()+" file is not supported")



    def show_buttons(self,id):
        if (id==1):
            self.imported_video_panel.SetupScrolling()
            self.iSizer = wx.BoxSizer( wx.VERTICAL )
            for i in self.imported_button_list:
                self.iSizer.Add( i[0], 0, wx.ALL, 0 )
                self.iSizer.Add(i[1],0,wx.ALL,0)
            self.imported_video_panel.SetSizer(self.iSizer)
        elif (id==2):
            self.sequence_video_panel.SetupScrolling()
            self.sSizer = wx.BoxSizer( wx.VERTICAL )
            for i in self.sequence_button_list:
                #if self.sequence_button_list.index(i)!=0:
                    #i.Disable()
                self.sSizer.Add( i[0], 0, wx.ALL, 0 )
                self.sSizer.Add(i[1],0,wx.ALL,0)
            self.sequence_video_panel.SetSizer(self.sSizer)




    def add_video_to_sequence(self,file_path,image_path):
        if(self.check_file_existance(file_path,2) and self.get_file_name(file_path)):
            self.undo_seq_but.Enable()
            self.sequence_video_position+=self.get_relative_Y(100)
            bmp = wx.Bitmap(image_path, wx.BITMAP_TYPE_ANY)
            button = wx.BitmapButton(self.sequence_video_panel,id=wx.ID_ANY,bitmap=bmp,size=(self.get_relative_X(120),self.get_relative_Y(85)))
            Label=wx.StaticText(self.sequence_video_panel,id=wx.ID_ANY, label=self.get_file_name(file_path),size=(self.get_relative_X(120),self.get_relative_Y(15)),style=wx.ALIGN_CENTRE)
            Label.SetBackgroundColour((255,255,255))
            #button = wx.Button(self.sequence_video_panel,label=self.get_file_name(file_path),pos=(self.get_relative_X(0),self.sequence_video_position),size=(self.get_relative_X(120),self.get_relative_Y(105)))
            button.Bind(wx.EVT_BUTTON,lambda temp=file_path: self.DoLoadFile(file_path))
            self.sequence_button_list.append([button,Label])
            self.show_buttons(2)





    def OnLoadFile(self, evt):
        dlg = wx.FileDialog(self, message="Choose a media file",
                            defaultDir=os.getcwd(), defaultFile="",
                            style=wx.OPEN | wx.CHANGE_DIR )

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            try:
                self.import_videos(path)
            except RuntimeError as e:
                wx.MessageDialog(None,str(e), 'INVALID FILE', wx.OK | wx.ICON_INFORMATION).ShowModal()
        dlg.Destroy()




    def DoLoadFile(self, path):
        if len(self.sequence_video_list)>0:
            self.sequence_video_pointer=self.sequence_video_list.index(path)
            print self.sequence_video_pointer

        if not self.mc.Load(path):
            wx.MessageBox("Unable to load %s: Unsupported format?" % path,
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
        else:
            self.mc.SetInitialSize((self.get_relative_X(1025),self.get_relative_Y(575)))
            self.media_player_panel.GetSizer().Layout()
            self.slider.SetRange(0, self.mc.Length())
            self.play_flag=0
            for each_object in self.status_panel_list:
                each_object.Destroy()
            for i in range(len(self.status_panel_list)):
                self.status_panel_list.pop(0)
            self.time_elapsed=0



    def OnMediaLoaded(self, evt):
        self.playBtn.Enable()



    def play(self):
        if not self.mc.Play():
            wx.MessageBox("Unable to Play media : Unsupported format?",
            "ERROR",
            wx.ICON_ERROR | wx.OK)
        else:
            self.mc.SetInitialSize((self.get_relative_X(1025),self.get_relative_Y(575)))
            self.media_player_panel.GetSizer().Layout()
            self.slider.SetRange(0, self.mc.Length())
            self.adjust_slider_color(1)
            self.speed_value=1






    def OnSeek(self, evt):
        offset = self.slider.GetValue()
        self.det()
        self.mc.Seek(offset)



    def det(self):
        pass


    def OnTimer(self, evt):
        offset = self.mc.Tell()
        self.slider.SetValue(offset)
        if self.mc.Tell()>0 and self.play_flag==0:
            self.play()
            self.operations_id_stack.append(1)
            self.play_flag=1
        #if int(self.mc.Tell()/1000)==int(self.mc.Length()/1000) and self.mc.Length()>0:
        #    try:
        #        self.sequence_video_pointer+=2
        #        self.DoLoadFile(self.sequence_video_list[self.sequence_video_pointer])
        #    except IndexError:
        #        pass
        value=0
        try:
            value=(17.2/17.5)*(offset*self.screenWidth*8)/(10*self.mc.Length())
        except ZeroDivisionError:
            pass
        try:
            self.status_panel_list[len(self.status_panel_list)-1].SetSize((value-self.time_elapsed,10))
        except IndexError:
            pass





    def adjust_slider_color(self,operation_id):
        try:
            previos_operation_end=self.status_panel_list[len(self.status_panel_list)-1].GetSize()[0]
            self.time_elapsed+=previos_operation_end
        except:
            pass
        new_color_panel=wx.Panel(self.slider_panel,size=(0,0), pos=(self.get_relative_X(7)+self.time_elapsed,20), style=wx.SIMPLE_BORDER)
        #new_color_panel
        self.status_panel_list.append(new_color_panel)
        color=self.current_operation_dict[operation_id]
        self.status_panel_list[len(self.status_panel_list)-1].SetBackgroundColour(color) #do this while creating the panel; avoid fetching



    def get_relative_Y(self,y):
        h=(self.screenHeight*y)/720
        return h



    def get_relative_X(self,x):
        w=(self.screenWidth*x)/1280
        return w



    def speed_menu_output(self,number):
        try:
            self.mc.SetPlaybackRate(int(number))
            speed_factor=int(number)
        except ValueError:
            self.mc.SetPlaybackRate(float(number))
            speed_factor=float(number)
        self.speed_value=speed_factor
        if -5 not in self.operations_id_stack:
            self.adjust_slider_color(speed_factor)
        else:
            self.adjust_slider_color(-5)
        self.operations_id_stack.append(speed_factor)
        self.add_operation()



    def shape_menu_output(self,shape):
        wx.MessageDialog(None,shape, 'SHAPE SELECTED', wx.OK | wx.ICON_INFORMATION).ShowModal()

    def on_trim(self,event):
        state = event.GetEventObject().GetValue()
        if state==True:
            self.add_operation()
            self.adjust_slider_color(0)
            self.text_but.Disable()
            self.speed_menu.cb.Disable()
            self.shape_menu.cb.Disable()
            self.operations_id_stack.append(0)
            self.trim_value=1

        else:
            self.operations_id_stack.pop(-1)
            self.adjust_slider_color(self.operations_id_stack[-1])
            self.text_but.Enable()
            self.speed_menu.cb.Enable()
            self.shape_menu.cb.Enable()
            self.add_operation()
            self.trim_value=0

    def on_text_entry(self,event):
        state = event.GetEventObject().GetValue()
        if state==True:
            self.mc.Pause()
            dlg = wx.TextEntryDialog(frame, 'Enter some text','Text Entry')
            if dlg.ShowModal() == wx.ID_OK:
                self.add_operation()
                self.text_value=str(dlg.GetValue())
                self.adjust_slider_color(-5)
                self.operations_id_stack.append(-5)
                #print('You entered: %s\n' % dlg.GetValue())
            else:
                self.text_but.SetValue(False)
            dlg.Destroy()
            self.mc.Play()
        else:
            self.add_operation()
            self.operations_id_stack.pop(self.operations_id_stack.index(-5))
            self.adjust_slider_color(self.operations_id_stack[-1])
            self.text_value=False

    def add_operation(self):
        self.end_time=self.mc.Tell()
        current_operation_details=[self.start_time,self.end_time,self.trim_value,self.text_value,self.speed_value]
        self.operations_performed_list.append(current_operation_details)
        self.start_time=self.end_time

    def on_done(self,event):
        print self.operations_performed_list

    def undo_import(self,event):
        try:

            #self.imported_button_list[-1][0].Destroy()
            #self.imported_button_list[-1][1].Destroy()
            self.videos_list.pop(-1)
            self.iSizer.Hide(2*len(self.videos_list)+1)
            self.iSizer.Hide(2*len(self.videos_list))
            self.iSizer.Remove(2*len(self.videos_list)+1)
            self.iSizer.Remove(2*len(self.videos_list))
            self.imported_button_list.pop(-1)
        except IndexError:
            self.undo_imp_but.Disable()


    def undo_sequence(self,event):
        try:
            #self.sequence_button_list[-1][0].Destroy()
            #self.sequence_button_list[-1][1].Destroy()
            self.sequence_video_list.pop(-1)
            self.sSizer.Hide(2*len(self.sequence_video_list)+1)
            self.sSizer.Hide(2*len(self.sequence_video_list))
            self.sSizer.Remove(2*len(self.sequence_video_list)+1)
            self.sSizer.Remove(2*len(self.sequence_video_list))
            self.sequence_button_list.pop(-1)
        except IndexError:
            self.undo_seq_but.Disable()



    def ShutdownDemo(self,event):
        if os.path.exists(self.App_folder):
            shutil.rmtree(self.App_folder)
        self.timer.Stop()
        del self.timer
        self.Destroy()



app = wx.App()
frame = TestPanel(parent=None, id=-1, title="Test")
#frame.ShowFullScreen(True)
frame.Maximize(True)
frame.SetTitle("Sports Video Editor")
frame.Show()
app.MainLoop()

