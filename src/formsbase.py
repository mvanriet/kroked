# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.richtext
import wx.html

###########################################################################
## Class KrokedForm_Base
###########################################################################

class KrokedForm_Base ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Kroked", pos = wx.DefaultPosition, size = wx.Size( 956,565 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        self.m_statusBar2 = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
        bSizer16 = wx.BoxSizer( wx.VERTICAL )

        self.m_splitter2 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
        self.m_splitter2.Bind( wx.EVT_IDLE, self.m_splitter2OnIdle )

        self.m_panel2 = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_THEME|wx.TAB_TRAVERSAL )
        self.m_panel2.SetMinSize( wx.Size( 200,-1 ) )

        bSizer19 = wx.BoxSizer( wx.VERTICAL )

        bSizer231 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_btnOpenFolder = wx.Button( self.m_panel2, wx.ID_ANY, u"Open folder...", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer231.Add( self.m_btnOpenFolder, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_btnRescan = wx.Button( self.m_panel2, wx.ID_ANY, u"Rescan", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer231.Add( self.m_btnRescan, 0, wx.ALL, 5 )


        bSizer19.Add( bSizer231, 0, wx.EXPAND, 5 )

        self.m_FileTree = wx.TreeCtrl( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE|wx.TR_HIDE_ROOT )
        bSizer19.Add( self.m_FileTree, 1, wx.ALL|wx.EXPAND, 5 )


        self.m_panel2.SetSizer( bSizer19 )
        self.m_panel2.Layout()
        bSizer19.Fit( self.m_panel2 )
        self.m_panel3 = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_THEME|wx.TAB_TRAVERSAL )
        self.m_panel3.SetMinSize( wx.Size( 400,-1 ) )

        bSizer20 = wx.BoxSizer( wx.VERTICAL )

        self.m_splitter3 = wx.SplitterWindow( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
        self.m_splitter3.Bind( wx.EVT_IDLE, self.m_splitter3OnIdle )

        self.m_panel5 = wx.Panel( self.m_splitter3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.m_panel5.SetMinSize( wx.Size( 200,-1 ) )

        bSizer23 = wx.BoxSizer( wx.VERTICAL )

        bSizer25 = wx.BoxSizer( wx.HORIZONTAL )


        bSizer25.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_btnSave = wx.Button( self.m_panel5, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_btnSave.Enable( False )

        bSizer25.Add( self.m_btnSave, 1, wx.ALL, 5 )

        self.m_button26 = wx.Button( self.m_panel5, wx.ID_ANY, u"Revert", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button26.Enable( False )

        bSizer25.Add( self.m_button26, 1, wx.ALL, 5 )

        self.m_button27 = wx.Button( self.m_panel5, wx.ID_ANY, u"Close", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button27.Enable( False )

        bSizer25.Add( self.m_button27, 1, wx.ALL, 5 )


        bSizer23.Add( bSizer25, 0, wx.EXPAND, 5 )

        self.m_txtEditor = wx.richtext.RichTextCtrl( self.m_panel5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
        self.m_txtEditor.SetFont( wx.Font( 10, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Courier New" ) )

        bSizer23.Add( self.m_txtEditor, 1, wx.EXPAND |wx.ALL, 5 )


        self.m_panel5.SetSizer( bSizer23 )
        self.m_panel5.Layout()
        bSizer23.Fit( self.m_panel5 )
        self.m_panel6 = wx.Panel( self.m_splitter3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.m_panel6.SetMinSize( wx.Size( -200,-1 ) )

        bSizer22 = wx.BoxSizer( wx.VERTICAL )

        bSizer26 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_btnRefresh = wx.Button( self.m_panel6, wx.ID_ANY, u"Refresh", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer26.Add( self.m_btnRefresh, 0, wx.ALL, 5 )

        self.m_btnCopyPng = wx.Button( self.m_panel6, wx.ID_ANY, u"Copy PNG", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer26.Add( self.m_btnCopyPng, 0, wx.ALL, 5 )


        bSizer22.Add( bSizer26, 0, wx.EXPAND, 5 )

        self.m_htmlPreview = wx.html.HtmlWindow( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.html.HW_SCROLLBAR_AUTO|wx.BORDER_THEME )
        bSizer22.Add( self.m_htmlPreview, 1, wx.ALL|wx.EXPAND, 5 )


        self.m_panel6.SetSizer( bSizer22 )
        self.m_panel6.Layout()
        bSizer22.Fit( self.m_panel6 )
        self.m_splitter3.SplitVertically( self.m_panel5, self.m_panel6, 0 )
        bSizer20.Add( self.m_splitter3, 1, wx.EXPAND, 5 )


        self.m_panel3.SetSizer( bSizer20 )
        self.m_panel3.Layout()
        bSizer20.Fit( self.m_panel3 )
        self.m_splitter2.SplitVertically( self.m_panel2, self.m_panel3, 241 )
        bSizer16.Add( self.m_splitter2, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer16 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.Bind( wx.EVT_CLOSE, self.OnFormClose )
        self.m_btnOpenFolder.Bind( wx.EVT_BUTTON, self.OnBtnOpenFolder )
        self.m_btnRescan.Bind( wx.EVT_BUTTON, self.OnBtnRescan )
        self.m_FileTree.Bind( wx.EVT_TREE_SEL_CHANGED, self.OnTreeSelect )
        self.m_btnSave.Bind( wx.EVT_BUTTON, self.OnBtnSave )
        self.m_btnRefresh.Bind( wx.EVT_BUTTON, self.OnBtnRefresh )
        self.m_btnCopyPng.Bind( wx.EVT_BUTTON, self.OnBtnCopyPng )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def OnFormClose( self, event ):
        event.Skip()

    def OnBtnOpenFolder( self, event ):
        event.Skip()

    def OnBtnRescan( self, event ):
        event.Skip()

    def OnTreeSelect( self, event ):
        event.Skip()

    def OnBtnSave( self, event ):
        event.Skip()

    def OnBtnRefresh( self, event ):
        event.Skip()

    def OnBtnCopyPng( self, event ):
        event.Skip()

    def m_splitter2OnIdle( self, event ):
    	self.m_splitter2.SetSashPosition( 241 )
    	self.m_splitter2.Unbind( wx.EVT_IDLE )

    def m_splitter3OnIdle( self, event ):
    	self.m_splitter3.SetSashPosition( 0 )
    	self.m_splitter3.Unbind( wx.EVT_IDLE )


