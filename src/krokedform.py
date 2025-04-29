#  _  _____  ___  _  _____ ___  
# | |/ / _ \/ _ \| |/ / __|   \    Kroki Editor - diagrams using Kroki
# | ' <|   / (_) | ' <| _|| |) |   (c) 2025 Marc Van Riet - Apache License 2.0
# |_|\_\_|_\\___/|_|\_\___|___/    See https://github.com/mvanriet/kroked
# ____________________________________________________________________________

import configparser
import os
import wx
from formsbase import KrokedForm_Base
import requests

from krokifile import KrokiFile

INIFILENAME = os.path.join(os.path.dirname(__file__), "kroked.ini")

class KrokedForm(KrokedForm_Base):
    def __init__(self):
        super().__init__(None)

        self.RestorePosition()

        self.dir_in_tree = None
        self.doc = KrokiFile()


    def OnFormClose( self, event ):
        self.save_current_file()
        self.SavePosition()     
        self.Destroy()                                              # delete the frame
        wx.GetApp().ExitMainLoop()


    def RestorePosition( self ):
        ''' Restore the position of the window and the panes
        '''
        section = "MAINFORM_LAYOUT"

        ini = configparser.ConfigParser()
        ini.read( [INIFILENAME] )
        
        # restore window and pane position
        
        if ini.has_section(section):
            x = ini.getint(section, "WindowX")
            y = ini.getint(section, "WindowY")
            width = ini.getint(section, "WindowWidht" )
            height = ini.getint(section, "WindowHeight" )
            
            self.SetPosition((x,y))
            self.SetSize((width, height))


    def SavePosition( self, also_save_user = False ):
        ''' Save the position of the window and the panes
        '''
        section = "MAINFORM_LAYOUT"
        
        x, y = self.GetPosition()
        width, height = self.GetSize()
        
        ini = configparser.ConfigParser()
        ini.read( [INIFILENAME] )
        if not ini.has_section(section):
            ini.add_section(section)
        ini.set(section, "WindowX", str(x) )
        ini.set(section, "WindowY", str(y) )
        ini.set(section, "WindowWidht", str(width) )
        ini.set(section, "WindowHeight", str(height) )
                        
        with open(INIFILENAME, "w") as inifile:
            ini.write(inifile)   


    def OnBtnOpenFolder(self, event):
        ''' Open a folder and scan it for Kroki files.
            The folder is saved in the INI file, so it can be restored next time.
        '''
        section = "FOLDERS"

        ini = configparser.ConfigParser()
        ini.read( [INIFILENAME] )

        prev_folder = ""       
        if ini.has_section(section):
            dirname = ini.get(section, "PreviousDir")
            if os.path.isdir(dirname):
                prev_folder = dirname

        dirname = None
        with wx.DirDialog(self, "Choose a directory",
                            style=wx.DD_DEFAULT_STYLE,
                            defaultPath=prev_folder) as dialog:
            
            if dialog.ShowModal() == wx.ID_OK:
                dirname = dialog.GetPath()

                self.dir_in_tree = dirname

                if not ini.has_section(section):
                    ini.add_section(section)
                ini.set(section, "PreviousDir", dirname )

                with open(INIFILENAME, "w") as inifile:
                    ini.write(inifile)        

                self.ScanFolder(dirname)


    def OnBtnRescan( self, event ):
        if self.dir_in_tree is not None and os.path.isdir(self.dir_in_tree):
            self.ScanFolder(self.dir_in_tree)
        else:
            wx.MessageBox("No valid folder selected", "Error", wx.OK | wx.ICON_ERROR)


    def OnBtnSave( self, event ):
       pass


    def OnBtnRefresh( self, event ):
        # self.m_htmlPreview.LoadPage("http://httpforever.com/")
        self.show_graph_preview()

    def OnBtnCopyPng( self, event ):
        path = self.doc.png_filename
        if not os.path.exists(path):
            wx.MessageBox(f"PNG file {path} does not exist", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        command = f"powershell Set-Clipboard -LiteralPath {path}"
        os.system(command)


    def OnTreeSelect( self, event ):
        item = self.m_FileTree.GetSelection()
        if item:
            path = self.m_FileTree.GetItemData(item)
            if path:
                self.load_file(path)
                self.show_graph_preview()


    def ScanFolder(self, folder_path):
        if not os.path.isdir(folder_path):
            return
        
        self.Title = "Kroked - " + folder_path

        self.m_FileTree.DeleteAllItems()
        root = self.m_FileTree.AddRoot(os.path.dirname(folder_path))

        self.AddFiles(root, folder_path, 0)


    def AddFiles(self, root, dir, level):
        ''' Scans a single directory and adds files to the given tree node.
            For each node in the tree, the full pathnames is added as data.
            This is called recursively for each subdirectory.
        '''

        if level>5: return False

        havefiles = False                   # are there any kroki files in this directory?

        files = []

        for file_name in os.listdir(dir):

            if os.path.isdir(os.path.join(dir, file_name)):
                subdir = self.m_FileTree.AppendItem(root, file_name)
                if not self.AddFiles(subdir, os.path.join(dir, file_name), level+1):
                    self.m_FileTree.Delete(subdir)

            elif file_name.endswith(('.kro', '.kroki')):
                files.append(file_name)

        files.sort()
        for file_name in files:
            item = self.m_FileTree.AppendItem(root, file_name, data=os.path.join(dir, file_name))
            self.m_FileTree.SetItemText(item, file_name)
            havefiles = True

        return havefiles



    def show_graph_preview(self):

        html_content = '<html><body><p>Loading...</p></body></html>'
        self.m_htmlPreview.SetPage(html_content)
        wx.Yield()

        self.save_current_file()                            # save current file if necessary

        have_png = self.doc.create_png()                  # create a PNG file from the content

        if have_png:
            html_content = f'<html><body><p>{self.doc.png_filename}</p><p><img src="{self.doc.png_filename}" alt="PNG Image"></p><p>...</p></body></html>'
        else:
            html_content = f'<html><body><p>Failed to create PNG image {self.doc.png_filename}.</p></body></html>'

        self.m_htmlPreview.SetPage(html_content)





                 



    def load_file( self, path ):

        self.save_current_file()                            # save current file if necessary

        self.m_txtEditor.Clear()
        self.doc.load_file(path)                          # load new file

        if not self.doc.have_file:
            wx.MessageBox(f"Could not read file {path}", "Error", wx.OK | wx.ICON_ERROR)
            return

        self.m_txtEditor.SetValue(self.doc.content)          # set the content in the editor
        self.m_txtEditor.SetFocus()

    def save_current_file( self ):

        content = self.m_txtEditor.GetValue()
        self.doc.save_file(content)