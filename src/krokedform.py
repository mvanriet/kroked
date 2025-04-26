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

INIFILENAME = os.path.join(os.path.dirname(__file__), "kroked.ini")

URL = "https://kroki.io/"

FORMATS = {
    "blockdiag": "png,svg,pdf",
    "graphviz": "png,svg,jpg,pdf",
    "seqdiag": "png,svg,pdf",
    "mermaid": "png,svg",
    "packetdiag": "png,svg,pdf",
    "wireviz": "png,svg",
    }

class KrokedForm(KrokedForm_Base):
    def __init__(self):
        super().__init__(None)

        self.RestorePosition()

        self.open_files = []

        self.file_in_editor = None


    def OnBtnOpenFolder(self, event):

        dirname = None

        # Open a directory selection dialog
        with wx.DirDialog(self, "Choose a directory", style=wx.DD_DEFAULT_STYLE) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                dirname = dialog.GetPath()

        self.ScanFolder(dirname)

    def OnFormClose( self, event ):
        self.save_current_file()
        self.SavePosition()     
        self.Destroy()                                              # delete the frame
        wx.GetApp().ExitMainLoop()

    def ScanFolder(self, folder_path):


        if not os.path.isdir(folder_path):
            return
        
        self.Title = "Kroked - " + folder_path

        self.m_FileTree.DeleteAllItems()
        root = self.m_FileTree.AddRoot(os.path.dirname(folder_path))

        self.AddFiles(root, folder_path, 0)

    def AddFiles(self, root, dir, level):

        if level>3: return False
        havefiles = False

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

    def OnBtnSave( self, event ):
       pass



    def OnBtnRefresh( self, event ):
        # self.m_htmlPreview.LoadPage("http://httpforever.com/")
        self.show_graph_preview()

    def show_graph_preview(self):
        diagram_source = self.m_txtEditor.GetValue()

        (firstline, _, source) = diagram_source.partition("\n")

        diagtype, formats = self.get_type_info(firstline)

        if diagtype is None:
            wx.MessageBox("Didn't find valid diagram type on first line", "Error", wx.OK | wx.ICON_ERROR)
            return

        if not 'png' in formats:
            wx.MessageBox("Cannot show this diagram, only export to file", "Error", wx.OK | wx.ICON_ERROR)
            return

        html_content = '<html><body><p>Loading...</p></body></html>'
        self.m_htmlPreview.SetPage(html_content)
        wx.Yield()

        data = {"output_format": "png", "diagram_type": diagtype, "diagram_source": source}
        response = requests.post(URL, json=data)

        if response.status_code == 200:
            with open("image.png", "wb") as file:
                file.write(response.content)
            html_content = f'<html><body><p>{self.file_in_editor}</p><p><img src="image.png" alt="PNG Image"></p><p>...</p></body></html>'

            self.m_htmlPreview.SetPage(html_content)
        else:
            print(response.text)

            wx.MessageBox(f"Failed to fetch image. Status code: {response.status_code}", "Error", wx.OK | wx.ICON_ERROR)

    def get_type_info(self, firstline):
        
        result = (None, None)
        for key, value in FORMATS.items():
            if key in firstline:
                result = (key, value.split(","))

        return result




    def show_svg(self):

        url = "https://kroki.io/graphviz/svg/eNpLyUwvSizIUHBXqPZIzcnJ17ULzy_KSanlAgB1EAjQ"


        response = requests.get(url)
        if response.status_code == 200:
            svg_content = response.text

            with open("svg_image.svg", "w", encoding="utf-8") as file:
                file.write(svg_content)

            html_content = '<html><body><img src="svg_image.svg" alt="SVG Image"></body></html>'

            self.m_htmlPreview.SetPage(html_content)

        else:
            wx.MessageBox(f"Failed to load SVG. Status code: {response.status_code}", "Error", wx.OK | wx.ICON_ERROR)

    def OnTreeDoubleClick( self, event ):
        item = self.m_FileTree.GetSelection()
        if item:
            path = self.m_FileTree.GetItemData(item)
            if path:
                print(f"Loading file: {path}")
                self.load_file(path)
                self.show_graph_preview()


    def OnDropdownFileSelect( self, event ):
        fname = self.m_cboFilename.GetStringSelection()
        if not fname:
            return

        self.load_file(fname)
        self.show_graph_preview()

    def load_file( self, path ):

        if self.file_in_editor:
            self.save_current_file()
            self.file_in_editor = None

        self.m_txtEditor.Clear()
        self.m_txtEditor.LoadFile(path,  wx.richtext.RICHTEXT_TYPE_TEXT)
        self.m_txtEditor.SetFocus()
        self.file_in_editor = path

        if path not in self.open_files:
            self.open_files.append(path)
            self.m_cboFilename.SetItems(self.open_files)
            idx = self.m_cboFilename.FindString(path)
            self.m_cboFilename.SetSelection(idx)

    def save_current_file( self ):
        fname = self.file_in_editor

        if fname:
            print(f"Saving file: {fname}")
            self.m_txtEditor.SaveFile(fname,  wx.richtext.RICHTEXT_TYPE_TEXT)
            self.m_txtEditor.SetFocus()


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
            
            # if ini.has_option(section, "pane_layout"):
            #     panes = ini.get(section, "pane_layout")
            #     try:
            #         self.m_mgr.LoadPerspective(panes, False)
            #     except:
            #         pass


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
        
        # ini.set(section, "pane_layout", self.m_mgr.SavePerspective() )
                        
        with open(INIFILENAME, "w") as inifile:
            ini.write(inifile)                    