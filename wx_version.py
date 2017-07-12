import wx
import wx.media
import os
import moviepy.editor as mp
import wx.lib.scrolledpanel

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

class TestPanel(wx.Frame):

    def __init__(self,parent,id,title):
       #First retrieve the screen size of the device
        screenSize = wx.DisplaySize()
        self.screenWidth = screenSize[0]
        self.screenHeight = screenSize[1]

        #Create a frame
        wx.Frame.__init__(self,parent,id,title,size=screenSize, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

        self.media_player_panel= wx.Panel(self,size=(3/5*self.screenWidth,4*self.screenHeight/5), pos=(self.screenWidth/5,0), style=wx.SIMPLE_BORDER)
        #self.media_player_panel.SetBackgroundColour('#333333')
        self.sequence_video_panel = wx.lib.scrolledpanel.ScrolledPanel(self,-1, size=(self.screenWidth/5,self.screenHeight), pos=(0,0), style=wx.SIMPLE_BORDER)
        self.sequence_video_panel.SetupScrolling()
        self.sequence_video_panel.SetBackgroundColour('#777777')
        self.video_operators_panel = wx.Panel(self,size=(3*self.screenWidth/5,self.screenHeight/5), pos=(self.screenWidth/5,4*self.screenHeight/5), style=wx.SIMPLE_BORDER)
        self.video_operators_panel.SetBackgroundColour('#FFFFFF')
        self.imported_video_panel = wx.lib.scrolledpanel.ScrolledPanel(self,-1, size=(self.screenWidth/5,self.screenHeight), pos=(4*self.screenWidth/5,0), style=wx.SIMPLE_BORDER)
        self.imported_video_panel.SetupScrolling()
        self.imported_video_panel.SetBackgroundColour('#777777')

        self.videos_list=[]#list that holds the paths of inserted videos
        self.sequence_video_list=[]#list that holds the paths of sequenced videos in order

        bSizer = wx.BoxSizer( wx.HORIZONTAL )


        button1 = wx.Button(self.video_operators_panel,label="Button 1",pos=(50,40),size=(50,50))
        button1.Bind(wx.EVT_BUTTON,self.set_up)
        bSizer.Add( button1, 0, wx.ALL, 5 )


        load_button = wx.Button(self.video_operators_panel,label="Load File",pos=(100,40),size=(50,50))
        load_button.Bind(wx.EVT_BUTTON, self.OnLoadFile, load_button)
        bSizer.Add(load_button,0,wx.ALL,5)

        play_button = wx.Button(self.video_operators_panel, -1, "Play",pos=(150,40),size=(50,50))
        play_button.Bind(wx.EVT_BUTTON, self.OnPlay, play_button)
        self.playBtn = play_button
        bSizer.Add(play_button,0,wx.ALL,5)
        self.st_size = StaticText(self, -1, size=(100,-1))
        self.st_len  = StaticText(self, -1, size=(100,-1))
        self.st_pos  = StaticText(self, -1, size=(100,-1))

        self.SetSizer( bSizer )



        wx.CallAfter(self.DoLoadFile, os.path.abspath("data/testmovie.mpg"))

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.timer.Start(100)

        '''

        #btn3 = wx.Button(self, -1, "Pause")
        # self.Bind(wx.EVT_BUTTON, self.OnPause, btn3)

        tbtn = wx.ToggleButton(panel1 , -1, "Play/Pause")
        #panel1.Bind(wx.EVT_TOGGLEBUTTON,panel1.OnPlay,tbtn)
        panel1.playBtn=tbtn


        btn4 = wx.Button(panel1, -1, "Stop")
        #panel1.Bind(wx.EVT_BUTTON, self.OnStop, btn4)'''



        slider = wx.Slider(self.video_operators_panel, -1, 0, 0, 100)
        self.slider = slider
        slider.SetMinSize((3*self.screenWidth/5, -1))
        self.Bind(wx.EVT_SLIDER, self.OnSeek, slider)
        bSizer = wx.BoxSizer( wx.VERTICAL )
        bSizer.Add(slider, 0,)
        self.SetSizer( bSizer )



        self.button_list=[]

        self.imported_video_position=0

       # Create some controls
        #self.mc = wx.media.MediaCtrl(self.media_player_panel, style=wx.SIMPLE_BORDER,)

        try:
            self.media_player_panel.mc = wx.media.MediaCtrl(self.media_player_panel, style=wx.SIMPLE_BORDER,)
            self.media_player_panel.SetInitialSize((765,575))
            but = wx.Button(self.imported_video_panel,label="Button 1",pos=(20,self.imported_video_position),size=(50,50))

            #panel1.Bind(wx.media.EVT_MEDIA_LOADED, panel1.OnMediaLoaded)
            msizer=wx.BoxSizer(wx.VERTICAL)
            #panel1.mc.SetInitialSize((500,500))
            msizer.Add(but,0,flag=wx.EXPAND)
            self.media_player_panel.SetSizer(msizer)
            self.mc=self.media_player_panel.mc
            self.mc.ShowPlayerControls()

        except NotImplementedError:
            self.media_player_panel.Destroy()
            raise
        self.Bind(wx.media.EVT_MEDIA_LOADED, self.OnMediaLoaded)



    def set_up(self,file_path):
        self.imported_video_position+=100
        button1 = wx.Button(self.imported_video_panel,label="Button 1",pos=(20,self.imported_video_position),size=(50,50))
        button1.Bind(wx.EVT_BUTTON,self.add_video_to_sequence)
        self.button_list.append(button1)
        self.show_buttons()
    def show_buttons(self):
        self.imported_video_panel.SetupScrolling()
        bSizer = wx.BoxSizer( wx.VERTICAL )
        for i in self.button_list:
            bSizer.Add( i, 0, wx.ALL, 5 )
        self.imported_video_panel.SetSizer(bSizer)
    def add_video_to_sequence(self):
        self.sequence_video_panel.SetupScrolling()







    def OnLoadFile(self, evt):


        dlg = wx.FileDialog(self, message="Choose a media file",
                            defaultDir=os.getcwd(), defaultFile="",
                            style=wx.OPEN | wx.CHANGE_DIR )

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.set_up(path)
            self.DoLoadFile(path)


        dlg.Destroy()


    def DoLoadFile(self, path):

        self.playBtn.Enable()

        if not self.mc.Load(path):
            wx.MessageBox("Unable to load %s: Unsupported format?" % path,
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
        else:
            self.videos_list.append(path)
            self.mc.SetInitialSize((765,575))
            self.media_player_panel.GetSizer().Layout()
            self.slider.SetRange(0, self.mc.Length())


    def OnMediaLoaded(self, evt):

        self.playBtn.Enable()


    def OnPlay(self, evt):
        if not self.mc.Play():
            wx.MessageBox("Unable to Play media : Unsupported format?",
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
        else:
            self.mc.SetInitialSize((765,575))
            self.media_player_panel.GetSizer().Layout()
            self.slider.SetRange(0, self.mc.Length())





    #    def OnPause(self, evt):

    #        self.mc.Pause()


    def OnStop(self, evt):

        self.mc.Stop()
        self.mc.ShowPlayerControls()
        self.mc.SetPlaybackRate(2)


    def OnSeek(self, evt):
        offset = self.slider.GetValue()
        self.det()
        self.mc.Seek(offset)
    def det(self):
        print self.mc.Tell()

    def OnTimer(self, evt):
        offset = self.mc.Tell()
        self.slider.SetValue(offset)
        self.st_size.SetLabel('size: %s' % self.mc.GetBestSize())
        self.st_len.SetLabel('length: %d seconds' % (self.mc.Length()/1000))
        self.st_pos.SetLabel('position: %d' % offset)

    def ShutdownDemo(self):
        self.timer.Stop()
        del self.timer

app = wx.App()
frame = TestPanel(parent=None, id=-1, title="Test")
frame.ShowFullScreen(True)
#frame.Show()
app.MainLoop()

