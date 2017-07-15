import wx
import wx.media
import os
#import moviepy.editor as mp
import wx.lib.scrolledpanel
import time
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

        self.media_player_panel= wx.Panel(self,size=(8/10*self.screenWidth,4*self.screenHeight/5), pos=(self.screenWidth/10,0), style=wx.SIMPLE_BORDER)
        self.sequence_video_panel = wx.lib.scrolledpanel.ScrolledPanel(self,-1, size=(self.screenWidth/10,self.screenHeight), pos=(0,0), style=wx.SIMPLE_BORDER)
        self.sequence_video_panel.SetupScrolling()
        self.sequence_video_panel.SetBackgroundColour('#777777')
        self.video_operators_panel = wx.Panel(self,size=(8*self.screenWidth/10,self.screenHeight/5), pos=(self.screenWidth/10,4*self.screenHeight/5), style=wx.SIMPLE_BORDER)
        self.video_operators_panel.SetBackgroundColour('#FFFFFF')
        self.imported_video_panel = wx.lib.scrolledpanel.ScrolledPanel(self,-1, size=(self.screenWidth/10,self.screenHeight), pos=(9*self.screenWidth/10,0), style=wx.SIMPLE_BORDER)
        self.imported_video_panel.SetupScrolling()
        self.imported_video_panel.SetBackgroundColour('#777777')
        self.slider_panel = wx.Panel(self.video_operators_panel,size=(8*self.screenWidth/10,self.screenHeight/16), pos=(0,0), style=wx.SIMPLE_BORDER)
        self.slider_panel.SetBackgroundColour('#AAAAAA')
        self.status_informer = wx.Panel(self.slider_panel,size=(0,0), pos=(self.get_relative_X(7),20), style=wx.SIMPLE_BORDER)



        self.videos_list=[]#list that holds the paths of inserted videos
        self.sequence_video_list=[]#list that holds the paths of sequenced videos in order

        bSizer = wx.BoxSizer( wx.HORIZONTAL )


        load_button = wx.Button(self.video_operators_panel,label="Load File",pos=(self.get_relative_X(50),self.get_relative_Y(40)),size=(self.get_relative_X(100),self.get_relative_Y(50)))
        load_button.Bind(wx.EVT_BUTTON, self.OnLoadFile, load_button)

        trim_button = wx.Button(self.video_operators_panel, -1, "TRIM",pos=(self.get_relative_X(170),self.get_relative_Y(40)),size=(self.get_relative_X(100),self.get_relative_Y(50)))
        #play_button.Bind(wx.EVT_BUTTON, self.OnPlay, play_button)
        self.playBtn = trim_button

        exit_button = wx.Button(self.video_operators_panel, -1, "EXIT",pos=(self.get_relative_X(570),self.get_relative_Y(40)),size=(self.get_relative_X(100),self.get_relative_Y(50)))
        exit_button.Bind(wx.EVT_BUTTON, self.ShutdownDemo, exit_button)

        bSizer.Add(load_button,0,wx.ALL,5)
        bSizer.Add(trim_button,0,wx.ALL,5)
        bSizer.Add(exit_button,0,wx.ALL,5)
        self.SetSizer( bSizer )



        x=dropDown_menu(self.video_operators_panel,['0.25','0.5','1','1.5','2'])
        y=dropDown_menu(self.video_operators_panel,['square','triangle','rectangle','circle'])



        wx.CallAfter(self.DoLoadFile, os.path.abspath("data/testmovie.mpg"))



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



        self.imported_button_list=[]
        self.sequence_button_list=[]

        self.imported_video_position=0
        self.sequence_video_position=0



        self.play_flag=0
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
        if(self.check_file_existance(file_path,1)):
            self.imported_video_position+=self.get_relative_Y(100)
            button = wx.Button(self.imported_video_panel,label=self.get_file_name(file_path),pos=(self.get_relative_X(50),self.imported_video_position),size=(self.get_relative_X(100),self.get_relative_X(100)))
            button.Bind(wx.EVT_BUTTON,lambda temp=file_path: self.add_video_to_sequence(file_path))
            self.imported_button_list.append(button)
            self.videos_list.append(file_path)
            self.show_buttons(1)





    def get_file_name(self,file):
        name=str(file)
        name=list(name.split('\\'))
        name=name[len(name)-1]
        type=list(name.split('.'))
        extensions=['m1v', 'mpeg', 'mov', 'qt', 'mpa', 'mpg', 'mpe', 'avi', 'movie', 'mp4','wmv']
        if(type[len(type)-1].lower() in extensions):#also include all the desired extensions.
            return name
        else:
            raise RuntimeError("Looks like this is not a video file\n."+type[len(type)-1].lower()+" file is not supported")



    def show_buttons(self,id):
        if (id==1):
            self.imported_video_panel.SetupScrolling()
            iSizer = wx.BoxSizer( wx.VERTICAL )
            for i in self.imported_button_list:
                iSizer.Add( i, 0, wx.ALL, 5 )
            self.imported_video_panel.SetSizer(iSizer)
        elif (id==2):
            self.sequence_video_panel.SetupScrolling()
            sSizer = wx.BoxSizer( wx.VERTICAL )
            for i in self.sequence_button_list:
                sSizer.Add( i, 0, wx.ALL, 5 )
            self.sequence_video_panel.SetSizer(sSizer)




    def add_video_to_sequence(self,file_path):
        if(self.check_file_existance(file_path,2)):
            self.sequence_video_position+=self.get_relative_Y(100)
            button = wx.Button(self.sequence_video_panel,label=self.get_file_name(file_path),pos=(self.get_relative_X(0),self.sequence_video_position),size=(self.get_relative_X(100),self.get_relative_X(100)))
            button.Bind(wx.EVT_BUTTON,lambda temp=file_path: self.DoLoadFile(file_path))
            self.sequence_button_list.append(button)
            self.sequence_video_list.append(file_path)
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

        self.playBtn.Enable()

        if not self.mc.Load(path):
            wx.MessageBox("Unable to load %s: Unsupported format?" % path,
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
        else:
            self.mc.SetInitialSize((self.get_relative_X(1025),self.get_relative_Y(575)))
            self.media_player_panel.GetSizer().Layout()
            self.slider.SetRange(0, self.mc.Length())
            self.play_flag=0



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
            self.play_flag=1
        value=0
        try:
            value=(17.2/17.5)*(offset*self.screenWidth*8)/(10*self.mc.Length())
        except ZeroDivisionError:
            pass
        #self.slider.SetBackgroundColour(wx.Colour(50,100,200))
        #event = wx.SysColourChangedEvent()
        #self.ProcessEvent(event)
        self.status_informer.SetBackgroundColour("blue")
        self.status_informer.SetSize((value,10))



    def ShutdownDemo(self,event):
        self.timer.Stop()
        del self.timer
        self.Destroy()



    def get_relative_Y(self,y):
        h=(self.screenHeight*y)/720
        return h



    def get_relative_X(self,x):
        w=(self.screenWidth*x)/1280
        return w



    def speed_menu_output(self,number):
        try:
            self.mc.SetPlaybackRate(int(number))
        except ValueError:
            self.mc.SetPlaybackRate(float(number))
        offset=self.mc.Tell()
        print offset


    def shape_menu_output(self,shape):
        wx.MessageDialog(None,shape, 'SHAPE SELECTED', wx.OK | wx.ICON_INFORMATION).ShowModal()





app = wx.App()
frame = TestPanel(parent=None, id=-1, title="Test")
frame.ShowFullScreen(True)
app.MainLoop()

