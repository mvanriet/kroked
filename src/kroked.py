

import wx
from krokedform import KrokedForm



app = wx.App(False)

mainform = KrokedForm()
mainform.Show()

app.MainLoop()
