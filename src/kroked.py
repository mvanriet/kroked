#  _  _____  ___  _  _____ ___  
# | |/ / _ \/ _ \| |/ / __|   \    Kroki Editor - diagrams using Kroki
# | ' <|   / (_) | ' <| _|| |) |   (c) 2025 Marc Van Riet - Apache License 2.0
# |_|\_\_|_\\___/|_|\_\___|___/    See https://github.com/mvanriet/kroked
# ____________________________________________________________________________



import wx
from krokedform import KrokedForm



app = wx.App(False)

mainform = KrokedForm()
mainform.Show()

app.MainLoop()
