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
import matplotlib.widgets as widgets
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import math
import back_end
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
        self.cb = wx.ComboBox(place,value=default_value,pos=(dropDown_menu.counter-self.get_relative_X(65),self.get_relative_Y(90)),
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



class ParallelWindow(wx.Frame):
    isLeftDown = False
    def __init__(self,parent,id,title,sizee,posi):
        self.screenWidth = frame.screenWidth
        self.screenHeight = frame.screenHeight
        wx.Frame.__init__(self,parent,id,title,size=sizee, pos=posi,  style = wx.CLOSE_BOX | wx.STAY_ON_TOP )
        self.zoomed_panels=[]
        self.text_labels=[]
        self.drawing_list=[]
        self.motion_sensor_list=[]
        self.temp_list=[]
        self.brush_color=(0,0,0)
        self.drawing_lock=0


    def add_text_to_screen(self,text_value,text_position):
        Label=wx.StaticText(self,id=wx.ID_ANY, label="",style=wx.ALIGN_CENTRE)
        font = wx.Font(15, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        Label.SetFont(font)
        self.label=Label
        self.label.SetBackgroundColour('black')
        self.label.SetForegroundColour('white')
        #panel.SetBackgroundColour('red')
        self.label.SetLabelText(text_value)
        #self.panel.SetSize(self.label.GetSize())
        self.label.SetPosition((self.set_text_position(text_position)))
        self.text_labels.append(self.label)
        frame.text_value=[self.label,text_position]
        self.drawing_lock=1


    def set_zoom(self,event):
        self.zoom_parameters=[]
        press=frame.press_list[len(frame.press_list)-2]
        release=frame.release_list[-1]
        breadth=math.fabs(release[0]-press[0])
        height=math.fabs(press[1]-release[1])
        relative_breadth,relative_height=self.relative_zoom(breadth,height)
        relative_x,relative_y=self.relative_position(press)
        self.zoom_area=wx.Panel(self,-1,size=(relative_breadth,relative_height),pos=(relative_x,relative_y))
        self.zoom_area.SetBackgroundColour('red')
        self.zoomed_panels.append(self.zoom_area)
        self.zoom_parameters.append(press)
        self.zoom_parameters.append(release)
        self.zoom_parameters.append(self.zoom_area)
        parallel_frame.Show()
        self.drawing_lock=1
        plt.close()
        frame.mc.Play()

    def relative_zoom(self,breadth,height):
        panel_width=self.GetSize()[0]
        panel_height=self.GetSize()[1]
        image_width=frame.image_size[0]
        image_height=frame.image_size[1]
        relative_breadth=(breadth*panel_width)/image_width
        relative_height=(height*panel_height)/image_height
        #print panel_height,panel_width
        return relative_breadth,relative_height


    def relative_position(self,CoOrds):
        panel_width=self.GetSize()[0]
        panel_height=self.GetSize()[1]
        image_width=frame.image_size[0]
        image_height=frame.image_size[1]
        relative_x=(CoOrds[0]*panel_width)/image_width
        reative_y=(CoOrds[1]*panel_height)/image_height
        return relative_x,reative_y


    def set_text_position(self,text_position):
        panel_x=self.GetPosition()[0]
        panel_y=self.GetPosition()[1]
        relative_x=text_position[0]-panel_x
        relative_y=text_position[1]-panel_y
        return relative_x,relative_y



    def OnLeftDown(self, event):
        pos = event.GetPositionTuple()
        self.temp_list.append(pos)
        self.dc = wx.ClientDC(self)
        self.drawing_list.append(self.dc)
        #dc.Clear()
        self.dc.SetPen(wx.Pen(self.brush_color, 0))
        self.dc.SetBrush(wx.Brush(self.brush_color))
        self.dc.DrawCircle(pos[0], pos[1], 2)
        self.isLeftDown = True


    def OnLeftUp(self, event):
        self.isLeftDown = False
        self.motion_sensor_list.append(self.temp_list)
        self.temp_list=[]

    def OnMove(self, event):
        if self.isLeftDown:
            pos = event.GetPositionTuple()
            self.temp_list.append(pos)
            #dc = wx.ClientDC(self)
            #dc.Clear()
            self.dc.SetPen(wx.Pen(self.brush_color, 0))
            self.dc.SetBrush(wx.Brush(self.brush_color))
            self.dc.DrawCircle(pos[0], pos[1], 2)

        if self.drawing_lock==1:
            self.redraw_on_screen()
            self.drawing_lock=0

    def BIND_MOUSE_EVENTS(self,color):
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMove)
        self.Bind(wx.EVT_RIGHT_DOWN,self.clear_drawing)
        self.brush_color=color
        print self.brush_color

    def UNBIND_MOUSE_EVENTS(self):
        self.Unbind(wx.EVT_LEFT_DOWN)
        self.Unbind(wx.EVT_LEFT_UP)
        self.Unbind(wx.EVT_MOTION)
        self.Unbind(wx.EVT_RIGHT_DOWN)

    def clear_drawing(self,event):
        self.dc.Clear()
        self.motion_sensor_list.pop(-1)
        for each_action in self.motion_sensor_list:
            for each_point in each_action:
                self.dc.DrawCircle(each_point[0],each_point[1],2)


    def redraw_on_screen(self):
        self.dc.Clear()
        for each_action in self.motion_sensor_list:
            for each_point in each_action:
                self.dc.DrawCircle(each_point[0],each_point[1],2)
        print self.motion_sensor_list

class TestPanel(wx.Frame):

    def __init__(self,parent,id,title):
       #First retrieve the screen size of the device
        screenSize = wx.DisplaySize()
        self.screenWidth = screenSize[0]
        self.screenHeight = screenSize[1]

        #Create a frame
        wx.Frame.__init__(self,parent,id,title,size=screenSize, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.Bind(wx.EVT_CLOSE, self.ShutdownDemo)
        self.Bind(wx.EVT_ICONIZE, self.OnMinimize)

        self.media_player_panel= wx.Panel(self,size=(8*self.screenWidth/10,3.7*self.screenHeight/5), pos=(self.screenWidth/10,0), style=wx.SIMPLE_BORDER)

        self.sequence_video_panel = wx.lib.scrolledpanel.ScrolledPanel(self,-1, size=(self.screenWidth/10,4*self.screenHeight/5+self.screenHeight/16), pos=(0,0), style=wx.SIMPLE_BORDER)
        self.sequence_video_panel.SetupScrolling()
        self.sequence_video_panel.SetBackgroundColour('#777777')

        self.video_operators_panel = wx.Panel(self,size=(8*self.screenWidth/10,1.3*self.screenHeight/5), pos=(self.screenWidth/10,3.7*self.screenHeight/5), style=wx.SIMPLE_BORDER)
        self.video_operators_panel.SetBackgroundColour('#FFFFFF')

        self.imported_video_panel = wx.lib.scrolledpanel.ScrolledPanel(self,-1, size=(self.screenWidth/10,4*self.screenHeight/5+self.screenHeight/16), pos=(9*self.screenWidth/10,0), style=wx.SIMPLE_BORDER)
        self.imported_video_panel.SetupScrolling()
        self.imported_video_panel.SetBackgroundColour('#777777')

        self.slider_panel = wx.Panel(self.video_operators_panel,size=(8*self.screenWidth/10,self.screenHeight/16), pos=(0,1.1*self.screenHeight/20), style=wx.SIMPLE_BORDER)
        self.slider_panel.SetBackgroundColour('#AAAAAA')


        self.text_panel = wx.Panel(self.video_operators_panel,size=(8*self.screenWidth/10,1.1*self.screenHeight/20), pos=(0,0), style=wx.SIMPLE_BORDER)
        self.text_panel.SetBackgroundColour('#FFFFFF')

        self.import_undo_panel = wx.Panel(self,size=(1*self.screenWidth/10,11*self.screenHeight/80), pos=(9*self.screenWidth/10,69*self.screenHeight/80), style=wx.SIMPLE_BORDER)
        self.import_undo_panel.SetBackgroundColour('#777777')

        self.sequence_undo_panel = wx.Panel(self,size=(1*self.screenWidth/10,11*self.screenHeight/80), pos=(0,69*self.screenHeight/80), style=wx.SIMPLE_BORDER)
        self.sequence_undo_panel.SetBackgroundColour('#777777')


        bSizer = wx.BoxSizer( wx.HORIZONTAL )


        load_button = wx.Button(self.video_operators_panel,label="Load File",pos=(self.get_relative_X(5),self.get_relative_Y(87)),size=(self.get_relative_X(100),self.get_relative_Y(30)))
        load_button.Bind(wx.EVT_BUTTON, self.OnLoadFile, load_button)

        trim_button = wx.ToggleButton(self.video_operators_panel, -1, "TRIM",pos=(self.get_relative_X(170-45),self.get_relative_Y(87)),size=(self.get_relative_X(100),self.get_relative_Y(30)))
        trim_button.Bind(wx.EVT_TOGGLEBUTTON, self.on_trim, trim_button)
        self.trim_but = trim_button

        text_button = wx.ToggleButton(self.video_operators_panel, -1, "ADD TEXT",pos=(self.get_relative_X(450-105),self.get_relative_Y(87)),size=(self.get_relative_X(100),self.get_relative_Y(30)))
        text_button.Bind(wx.EVT_TOGGLEBUTTON, self.on_text_entry, text_button)
        self.text_but=text_button

        self.done_button = wx.Button(self.video_operators_panel, -1, "DONE",pos=(self.get_relative_X(900-105),self.get_relative_Y(87)),size=(self.get_relative_X(100),self.get_relative_Y(30)))
        self.done_button.Bind(wx.EVT_BUTTON, self.on_done, self.done_button)

        self.undo_op_but = wx.Button(self.video_operators_panel, -1, "UNDO CHANGE",pos=(self.get_relative_X(800-105),self.get_relative_Y(87)),size=(self.get_relative_X(100),self.get_relative_Y(30)))
        self.undo_op_but.Bind(wx.EVT_BUTTON, self.undo_operation, self.undo_op_but)

        self.zoom_but = wx.ToggleButton(self.video_operators_panel, -1, "ZOOM",pos=(self.get_relative_X(690-105),self.get_relative_Y(87)),size=(self.get_relative_X(100),self.get_relative_Y(30)))
        self.zoom_but.Bind(wx.EVT_TOGGLEBUTTON, self.on_zoom, self.zoom_but)

        self.draw_but = wx.ToggleButton(self.video_operators_panel, -1, "DRAW",pos=(self.get_relative_X(570-105),self.get_relative_Y(87)),size=(self.get_relative_X(100),self.get_relative_Y(30)))
        self.draw_but.Bind(wx.EVT_TOGGLEBUTTON, self.on_draw, self.draw_but)


        exit_button = wx.Button(self.video_operators_panel, -1, "EXIT",pos=(self.get_relative_X(900),self.get_relative_Y(87)),size=(self.get_relative_X(100),self.get_relative_Y(30)))
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
        bSizer.Add(self.done_button,0,wx.ALL,5)
        bSizer.Add(self.zoom_but,0,wx.ALL,5)
        bSizer.Add(self.draw_but,0,wx.ALL,5)
        bSizer.Add(self.undo_op_but,0,wx.ALL,5)

        self.SetSizer( bSizer )



        self.speed_menu=dropDown_menu(self.video_operators_panel,['0.25','0.5','1','1.5','2'])
        #self.shape_menu=dropDown_menu(self.video_operators_panel,['square','triangle','rectangle','circle'])

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


        self.operation_duration_list=[]
        self.operations_performed_list=[]

        self.images_size_list=[]


        self.play_flag=0
        self.current_operation_dict={0.25:'brown',0.5:'blue',1:'green',1.5:'yellow',2:'red',0:'black',-5:'pink',-6:'violet',-7:'orange'}
        self.status_panel_list=[]
        self.slider_blocks_list=[]
        self.time_elapsed=0
        self.App_folder=os.path.join(os.path.expandvars("%userprofile%"),"Desktop\\Edos\\temporary_images\\")


        self.start_time=0
        self.end_time=0
        self.trim_value=0
        self.text_value=[]
        self.speed_value=1
        self.zoom_value=[]
        self.draw_value=[]


        Label=wx.StaticText(self.text_panel,id=wx.ID_ANY, label='',size=(8*self.screenWidth/10,1.1*self.screenHeight/20),style=wx.ALIGN_CENTRE)
        font = wx.Font(25, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        Label.SetFont(font)
        self.label=Label
        self.label.SetBackgroundColour('black')
        self.label.SetForegroundColour('white')

        self.operations_indices_dict={2:'trim',3:'text',4:'speed',5:'zoom',6:'shapes'}
        self.final_operations_dict={'trim':[],'speed':[],'text':[],'zoom':[],'shapes':[]}#Every operation data is saved here

        #self.Bind(wx.EVT_PAINT, self.OnPaint)

       # Create some controls

        try:
            self.media_player_panel.mc = wx.media.MediaCtrl(self.media_player_panel, style=wx.SIMPLE_BORDER,)
            self.media_player_panel.SetInitialSize((8*self.screenWidth/10,3.7*self.screenHeight/5))
            msizer=wx.BoxSizer(wx.VERTICAL)
            self.media_player_panel.SetSizer(msizer)
            self.mc=self.media_player_panel.mc
            self.mc.ShowPlayerControls()

        except NotImplementedError:
            self.media_player_panel.Destroy()
            raise
        self.Bind(wx.media.EVT_MEDIA_LOADED, self.OnMediaLoaded)
        self.mc.Bind(wx.media.EVT_MEDIA_STOP,self.on_media_finished)

############################################METHODS######################################################################

    def check_file_existance(self,file,list_id):
        if((file not in self.videos_list and list_id==1) or (file not in self.sequence_video_list and list_id==2)):
            if(list_id==1):
                self.videos_list.append(file)
            else:
                self.sequence_video_list.append(file)
            return True
        else:
            parallel_frame.Hide()
            wx.MessageDialog(None,'FILE ALREADY EXISTS', 'Cannot add file', wx.OK | wx.ICON_INFORMATION).ShowModal()
            return False



    def import_videos(self,file_path):
        if(self.check_file_existance(file_path,1) and self.get_file_name(file_path)):
            self.undo_imp_but.Enable()
            self.imported_video_position+=self.get_relative_Y(100)
            button_image=str(self.get_image_from_video(file_path,'thumb_nail'))
            bmp = wx.Bitmap(button_image, wx.BITMAP_TYPE_ANY)
            #button = wx.Button(self.imported_video_panel,label=self.get_file_name(file_path),pos=(self.get_relative_X(50),self.imported_video_position),size=(self.get_relative_X(100),self.get_relative_X(100)))
            button = wx.BitmapButton(self.imported_video_panel,id=wx.ID_ANY, bitmap=bmp,size=(self.get_relative_X(120),self.get_relative_Y(85)))
            Label=wx.StaticText(self.imported_video_panel,id=wx.ID_ANY, label=self.get_file_name(file_path),size=(self.get_relative_X(120),self.get_relative_Y(15)),style=wx.ALIGN_CENTRE)
            Label.SetBackgroundColour((255,255,255))
            button.Bind(wx.EVT_BUTTON,lambda temp=file_path: self.add_video_to_sequence(file_path,button_image))
            self.imported_button_list.append([button,Label])
            self.show_buttons(1)
        parallel_frame.Show()



    def get_image_from_video(self,file_path,purpose):
        clip = VideoFileClip(file_path)
        if purpose=='thumb_nail':
            image_time=int(clip.duration/2)
        elif purpose=='zoom':
            image_time=int(self.mc.Tell()/1000)
        f=clip.get_frame(image_time)
        img=Image.fromarray(f)
        self.image_size= img.size
        if purpose=='thumb_nail':
            self.images_size_list.append(img.size)
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
        else:
            parallel_frame.Show()




    def OnLoadFile(self, evt):
        parallel_frame.Hide()
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
        parallel_frame.Show()




    def DoLoadFile(self, path):
        if len(self.sequence_video_list)>0:
            self.sequence_video_pointer=self.sequence_video_list.index(path)
            #print self.sequence_video_pointer

        if not self.mc.Load(path):
            wx.MessageBox("Unable to load %s: Unsupported format?" % path,
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
        else:
            self.mc.SetInitialSize((8*self.screenWidth/10,3.7*self.screenHeight/5))
            self.media_player_panel.GetSizer().Layout()
            self.slider.SetRange(0, self.mc.Length())
            self.play_flag=0
            try:
                parallel_frame.zoom_area.Destroy()
            except AttributeError:
                pass
            video_index=self.videos_list.index(path)
            self.video_width= self.images_size_list[video_index][0]
            self.video_height=self.images_size_list[video_index][1]
            media_width=8*self.screenWidth/10
            parallel_frame_width=(3.24*self.screenHeight/5*self.video_width)/self.video_height
            displacement=(media_width-parallel_frame_width)/2
            parallel_frame.SetSize((parallel_frame_width,3.24*self.screenHeight/5))
            parallel_frame.SetPosition((self.screenWidth/10+displacement,self.screenHeight/31))
            for each_object in self.status_panel_list:
                each_object[0].Destroy()
                try:
                    each_object[1].Destroy()
                except IndexError:
                    pass
            #for i in range(len(self.status_panel_list)):
            #    self.status_panel_list.pop(0)
            self.status_panel_list=[]
            self.time_elapsed=0
            self.operations_performed_list=[]
            self.create_parallel_window((parallel_frame_width,3.24*self.screenHeight/5),(self.screenWidth/10+displacement,self.screenHeight/31))

    def create_parallel_window(self,panel_size,panel_position):
        global parallel_frame
        parallel_frame.Destroy()
        parallel_frame=ParallelWindow(parent=None, id=-1, title="",sizee=panel_size,posi=panel_position)
        parallel_frame.SetTransparent(100)
        app.SetTopWindow(parallel_frame)
        parallel_frame.Show()




    def OnMediaLoaded(self, evt):
        pass



    def play(self):
        if not self.mc.Play():
            wx.MessageBox("Unable to Play media : Unsupported format?",
            "ERROR",
            wx.ICON_ERROR | wx.OK)
        else:
            self.mc.SetInitialSize((8*self.screenWidth/10,3.7*self.screenHeight/5))
            self.media_player_panel.GetSizer().Layout()
            self.slider.SetRange(0, self.mc.Length())
            self.adjust_slider_color(1)
            self.speed_value=1



    def OnSeek(self, evt):
        offset = self.slider.GetValue()
        self.mc.Seek(offset)



    def OnTimer(self, evt):
        offset = self.mc.Tell()
        self.slider.SetValue(offset)
        if self.mc.Tell()>0 and self.play_flag==0:
            self.play()
            self.play_flag=1
            self.done_button.Disable()

        value=0
        try:
            value=(17.2/17.5)*(offset*self.screenWidth*8)/(10*self.mc.Length())
        except ZeroDivisionError:
            pass
        try:
            if value!=0:
                self.status_panel_list[-1][0].SetSize((value-self.time_elapsed,self.get_relative_Y(20)))
        except IndexError:
            pass



    def adjust_slider_color(self,operation_id):
        previos_operation_end=0
        actual_id=0
        if operation_id==-5 or operation_id==-6 or operation_id==-7:
            actual_id=operation_id
            operation_id=self.mc.GetPlaybackRate()
        try:
            previos_operation_end=self.status_panel_list[-1][0].GetSize()[0]
            self.time_elapsed+=previos_operation_end
        except:
            pass
        self.operation_duration_list.append([self.mc.Tell(),previos_operation_end])
        new_color_panel=wx.Panel(self.slider_panel,size=(0,0), pos=(self.get_relative_X(7)+self.time_elapsed,self.get_relative_Y(20)), style=wx.SIMPLE_BORDER)
        color=self.current_operation_dict[operation_id]
        new_color_panel.SetBackgroundColour(color) #do this while creating the panel; avoid fetching
        if actual_id!=0:
            block=wx.Panel(self.slider_panel,size=(self.get_relative_X(10),self.get_relative_Y(20)),pos=(self.get_relative_X(7)+self.time_elapsed,self.get_relative_Y(20)),style=wx.SIMPLE_BORDER)
            color=self.current_operation_dict[actual_id]
            block.SetBackgroundColour(color)
            self.status_panel_list.append([new_color_panel,block])
        else:
            self.status_panel_list.append([new_color_panel])


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
        self.add_operation(4)
        self.speed_value=speed_factor
        self.adjust_slider_color(speed_factor)



    def shape_menu_output(self,shape):
        wx.MessageDialog(None,shape, 'SHAPE SELECTED', wx.OK | wx.ICON_INFORMATION).ShowModal()



    def on_trim(self,event):
        state = event.GetEventObject().GetValue()
        if state==True:
            self.add_operation(2)
            self.adjust_slider_color(0)
            self.text_but.Disable()
            self.speed_menu.cb.Disable()
            self.zoom_but.Disable()
            self.draw_but.Disable()
            self.trim_value=1

        else:
            self.adjust_slider_color(self.mc.GetPlaybackRate())
            self.text_but.Enable()
            self.speed_menu.cb.Enable()
            self.zoom_but.Enable()
            self.draw_but.Enable()
            self.add_operation(2)
            self.trim_value=0



    def on_text_entry(self,event):
        state = event.GetEventObject().GetValue()
        if state==True:
            parallel_frame.Hide()
            self.mc.Pause()
            dlg = wx.TextEntryDialog(frame, 'Enter some text','PLACE TOP LEFT OF DIALOG AT DESIRED POSITION')
            if dlg.ShowModal() == wx.ID_OK:
                self.add_operation(3)
                text=str(dlg.GetValue())
                self.adjust_slider_color(-5)
                #self.label.SetLabel(self.text_value)
                text_position=dlg.GetScreenPositionTuple()
                parallel_frame.add_text_to_screen(text,text_position)
                #Label.SetBackgroundColour((255,255,255))

            else:
                self.text_but.SetValue(False)
            dlg.Destroy()
            self.mc.Play()
            parallel_frame.Show()
        else:
            self.add_operation(3)
            self.adjust_slider_color(-5)
            self.text_value=[]
            #self.label.SetLabel('')
            parallel_frame.label.Hide()



    def onselect(self,eclick, erelease):
        if eclick.ydata>erelease.ydata:
            eclick.ydata,erelease.ydata=erelease.ydata,eclick.ydata
        if eclick.xdata>erelease.xdata:
            eclick.xdata,erelease.xdata=erelease.xdata,eclick.xdata
        self.ax.set_ylim(erelease.ydata,eclick.ydata)
        self.ax.set_xlim(eclick.xdata,erelease.xdata)
        self.fig.canvas.draw()



    def onclick(self,event):
        self.press_CoOrd=[event.xdata, event.ydata]
        self.press_list.append(self.press_CoOrd)


    def onrelease(self,event):
        self.release_CoOrd=[event.xdata,event.ydata]
        self.release_list.append(self.release_CoOrd)


    def on_zoom(self,event):
        state = event.GetEventObject().GetValue()

        if state==True:
            self.zoom_value=[]
            self.add_operation(5)
            self.adjust_slider_color(-6)
            self.mc.Pause()
            parallel_frame.Hide()
            self.fig = plt.figure()
            self.ax = self.fig.add_subplot(111)
            filename=self.get_image_from_video(self.sequence_video_list[self.sequence_video_pointer],'zoom')
            im = Image.open(filename)
            arr = np.asarray(im)
            plt_image=plt.imshow(arr)
            rs=widgets.RectangleSelector(
            self.ax, self.onselect, drawtype='box',
            rectprops = dict(facecolor='red', edgecolor = 'black', alpha=0.5, fill=True))
            self.press_list=[]
            self.release_list=[]
            cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
            cid1 = self.fig.canvas.mpl_connect('button_release_event', self.onrelease)
            but_config = plt.axes([0.81, 0.01, 0.1, 0.075])
            zoom_button = Button(but_config, 'SET')
            zoom_button.on_clicked(parallel_frame.set_zoom)
            self.fig.patch.set_visible(False)
            self.ax.axis('off')
            plt.show()
            #self.undo_op_but.Disable()
        else:
            self.zoom_value=parallel_frame.zoom_parameters
            self.add_operation(5)
            self.zoom_value=[]
            self.adjust_slider_color(-6)
            parallel_frame.zoom_area.Hide()
            #self.undo_op_but.Enable()


    def on_draw(self,event):
        state = event.GetEventObject().GetValue()

        if state==True:
            self.add_operation(6)
            self.adjust_slider_color(-7)
            parallel_frame.motion_sensor_list=[]
            self.mc.Pause()
            parallel_frame.Hide()
            dlg = wx.ColourDialog(self)

            # Ensure the full colour dialog is displayed,
            # not the abbreviated version.
            dlg.GetColourData().SetChooseFull(True)

            if dlg.ShowModal() == wx.ID_OK:
                self.color = dlg.GetColourData()
                #print 'You selected: %s\n' % str(data.GetColour().Get())

            dlg.Destroy()
            parallel_frame.BIND_MOUSE_EVENTS(self.color.GetColour().Get())
            parallel_frame.Show()
        else:
            self.draw_color=self.color.GetColour().Get()
            parallel_frame.UNBIND_MOUSE_EVENTS()
            self.panel_width=parallel_frame.GetSize()[0]
            self.panel_height=parallel_frame.GetSize()[1]
            draw_list=[]
            for each_action in parallel_frame.motion_sensor_list:
                for each_point in each_action:
                    relative_x=self.video_width*each_point[0]/self.panel_width
                    relative_y=self.video_height*each_point[1]/self.panel_height
                    pos=(relative_x,relative_y)
                    draw_list.append(pos)
            try:
                draw_list=draw_list+self.draw_value[1]
            except IndexError:
                pass
            self.draw_value=[self.draw_color,draw_list]
            self.add_operation(6)
            self.adjust_slider_color(-7)
            self.draw_value=[]
            parallel_frame.dc.Clear()
            parallel_frame.motion_sensor_list=[]









    def add_operation(self,index):
        self.end_time=self.mc.Tell()
        current_operation_details=[index,self.start_time,self.end_time,self.trim_value,self.text_value,self.speed_value,self.zoom_value,self.draw_value]
        self.operations_performed_list.append(current_operation_details)
        self.start_time=self.end_time



    def on_done(self,event):
        try:
            print self.operations_performed_list
            for each_entry in self.final_operations_dict:
                self.final_operations_dict[each_entry]=[]
            op_list=[[],[],[],[],[]]
            start=0

            for each_operation in self.operations_performed_list:
                operation=self.operations_indices_dict[each_operation[0]]
                print operation

                if operation=='trim':
                    if op_list[0]==[]:
                        op_list[0].append(each_operation[2])
                    else:
                        op_list[0].append(each_operation[2])
                        self.final_operations_dict[operation].append(op_list[0])
                        op_list[0]=[]
                if operation=='text':
                    if op_list[1]==[]:
                        op_list[1].append(each_operation[2])
                    else:
                        op_list[1].append(each_operation[2])
                        datas=each_operation[4]
                        text=str(datas[0].GetLabelText())
                        CoOrds=datas[1]
                        modi_x=(self.video_width*CoOrds[0])/self.panel_width
                        modi_y=(self.video_height*CoOrds[1])/self.panel_height
                        modi_CoOrds=(modi_x,modi_y)
                        op_list[1].append(text)
                        op_list[1].append(modi_CoOrds)
                        self.final_operations_dict[operation].append(op_list[1])
                        op_list[1]=[]
                if operation=='speed':
                    if start==0:
                        op_list[2].append(start)

                        op_list[2].append(each_operation[2])
                        op_list[2].append(each_operation[5])
                        self.final_operations_dict[operation].append(op_list[2])
                        op_list[2]=[]

                    if start!=0:
                        op_list[2].append(start)

                        op_list[2].append(each_operation[2])
                        op_list[2].append(each_operation[5])
                        self.final_operations_dict[operation].append(op_list[2])
                        op_list[2]=[]
                    start=each_operation[2]

                if operation=='zoom':
                    if op_list[3]==[]:
                        op_list[3].append(each_operation[2])
                    else:
                        op_list[3].append(each_operation[2])
                        datas=each_operation[6]
                        press_CoOrds=datas[0]
                        realease_CoOrds=datas[1]
                        op_list[3].append(press_CoOrds)
                        op_list[3].append(realease_CoOrds)
                        self.final_operations_dict[operation].append(op_list[3])
                        op_list[3]=[]

                if operation=='shapes':
                    if op_list[4]==[]:
                        op_list[4].append(each_operation[2])
                    else:
                        op_list[4].append(each_operation[2])
                        datas=each_operation[7]
                        color=datas[0]
                        CoOrds=datas[1]
                        op_list[4].append(color)
                        op_list[4].append(CoOrds)
                        self.final_operations_dict[operation].append(op_list[4])
                        op_list[4]=[]

            self.final_operations_dict['speed'].append([start,self.mc.Length(),self.speed_value])
            print self.final_operations_dict
            back_end.get_video_data(self.sequence_video_list[self.sequence_video_pointer],self.final_operations_dict)
            self.sequence_video_pointer+=1
            self.DoLoadFile(self.sequence_video_list[self.sequence_video_pointer])
        except IndexError:
            pass #add the concatenation of all videos function or code here




    def undo_operation(self,event):
        try:
            self.mc.Seek(self.operation_duration_list[-1][0])
            self.time_elapsed-=self.operation_duration_list[-1][1]
            self.operation_duration_list.pop(-1)
            if len(self.status_panel_list[-1])==1:
                last_panel=self.status_panel_list.pop(-1)[0]
                last_panel.Destroy()
            else:
                total_panel=self.status_panel_list.pop(-1)
                last_panel=total_panel[0]
                last_panel.Destroy()
                last_block=total_panel[1]
                last_block.Destroy()
            previos_operation_data=self.operations_performed_list.pop(-1)
            self.index=previos_operation_data[0]
            self.start_time=previos_operation_data[1]
            self.trim_value=previos_operation_data[3]
            self.text_value=previos_operation_data[4]
            self.speed_value=previos_operation_data[5]
            self.zoom_value=previos_operation_data[6]
            self.draw_value=previos_operation_data[7]

            if self.index==2:
                if self.trim_value==1:
                    self.trim_but.SetValue(True)
                    self.text_but.Disable()
                    self.speed_menu.cb.Disable()
                    self.zoom_but.Disable()
                    self.draw_but.Disable()
                else:
                    self.trim_but.SetValue(False)
                    self.text_but.Enable()
                    self.speed_menu.cb.Enable()
                    self.zoom_but.Enable()
                    self.draw_but.Enable()

            if self.index==3:
                if self.text_value!=[]:
                    self.text_but.SetValue(True)
                    self.text_value[0].Show()
                    parallel_frame.label=self.text_value[0]
                    #ADD new text GUI
                else:
                    self.text_but.SetValue(False)
                    parallel_frame.label.Hide()

            if self.index==5:
                if self.zoom_value!=[]:
                    self.zoom_but.SetValue(True)
                    self.zoom_value[2].Show()
                    parallel_frame.zoom_area=self.zoom_value[2]
                    #self.undo_op_but.Disable()

                else:
                    self.zoom_but.SetValue(False)
                    parallel_frame.zoom_area.Hide()
                    #self.undo_op_but.Enable()

            if self.index==6:
                if self.draw_value!=[]:
                    self.draw_but.SetValue(True)
                    parallel_frame.BIND_MOUSE_EVENTS(self.draw_value[0])
                    parallel_frame.dc.Clear()
                    parallel_frame.dc.SetPen(wx.Pen(self.draw_value[0], 0))
                    parallel_frame.dc.SetBrush(wx.Brush(self.draw_value[0]))
                    for each_point in self.draw_value[1]:
                        actual_x=(each_point[0]*self.panel_width)/self.video_width
                        actual_y=(each_point[1]*self.panel_height)/self.video_height
                        parallel_frame.dc.DrawCircle(actual_x,actual_y,2)

                    #self.undo_op_but.Disable()

                else:
                    self.draw_but.SetValue(False)
                    parallel_frame.dc.Clear()
                    parallel_frame.UNBIND_MOUSE_EVENTS()
                    #self.undo_op_but.Enable()

            print self.index
            self.mc.SetPlaybackRate(self.speed_value)

        except:
            self.mc.Seek(0)
            self.adjust_slider_color(1)



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


    def on_media_finished(self,event):
        self.done_button.Enable()



    def OnMinimize(self,event):
        if  self.IsIconized():
            parallel_frame.Hide()
        else:
            parallel_frame.Show()




    def ShutdownDemo(self,event):
        if os.path.exists(self.App_folder):
            shutil.rmtree(self.App_folder)
        self.timer.Stop()
        del self.timer
        self.Destroy()
        parallel_frame.Destroy()



app = wx.App()
frame = TestPanel(parent=None, id=-1, title="Sports Video Editor")
frame.Maximize(True)
frame.Show()
parallel_frame=ParallelWindow(parent=None, id=-1, title="",sizee=(8*frame.screenWidth/10,3.24*frame.screenHeight/5), posi=(frame.screenWidth/10,frame.screenHeight/31))
parallel_frame.SetTransparent(100)
app.SetTopWindow(parallel_frame)
parallel_frame.Show()
app.MainLoop()
