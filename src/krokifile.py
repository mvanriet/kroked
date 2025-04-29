#  _  _____  ___  _  _____ ___  
# | |/ / _ \/ _ \| |/ / __|   \    Kroki Editor - diagrams using Kroki
# | ' <|   / (_) | ' <| _|| |) |   (c) 2025 Marc Van Riet - Apache License 2.0
# |_|\_\_|_\\___/|_|\_\___|___/    See https://github.com/mvanriet/kroked
# ____________________________________________________________________________

import datetime
import os
import requests

URL = "https://kroki.io/"


FORMATS = {
    "blockdiag": "png,svg,pdf",
    "graphviz": "png,svg,jpg,pdf",
    "seqdiag": "png,svg,pdf",
    "mermaid": "png,svg",
    "packetdiag": "png,svg,pdf",
    "wireviz": "png,svg",
    "plantuml": "png,svg,pdf",
    "@startuml": "png,svg,pdf",
    }


class KrokiFile(object):
    """
    KrokiFile is a class that represents a file to be processed by Kroki.
    It contains the file path and the type of diagram it represents.
    """

    def __init__(self):

        self.filename = None
        self.file_datetime = None
        self.orig_content = None

    @property
    def content(self):
        if self.orig_content is None:
            return ""
        return self.orig_content   

    @property
    def have_file(self):
        """ Returns True if a file is loaded.
        """
        return self.filename is not None and self.orig_content is not None

    @property
    def png_filename(self):
        """ Returns the name of the PNG file.
            An underscore is added to the filename to indicate it is a generterated file.
        """
        if self.filename is None:
            return None

        name = os.path.splitext(self.filename)[0] + "_.png"
        return name.replace("\\", "/")


    def load_file(self, path):
        """ Loads the file and remembers its content.
        """
        self.filename = None
        self.orig_content = None

        if not os.path.exists(path):
            raise FileNotFoundError(f"File {path} does not exist.")

        self.filename = path
        print(f"Loading file: {self.filename}")
        with open(path, "r", encoding="utf-8") as file:
            self.orig_content = file.read()

        self.file_datetime = os.path.getmtime(path)  # get the datetime of the file


    def save_file(self, content):
        """ Checks if a file is changed, and saves it if necessary.
        """
        if not self.have_file: return               # nothing to save if no file loaded
        if self.orig_content == content: return     # content is unchanged

        print(f"Saving file: {self.filename}")
        with open(self.filename, "w", encoding="utf-8") as file:
            file.write(content)

        self.orig_content = content
        self.file_datetime = os.path.getmtime(self.filename)  # remember when last saved

    def get_type_info(self, firstline):
        
        result = (None, None)
        for key, value in FORMATS.items():
            if key in firstline:
                result = (key, value.split(","))

        return result

    def create_png(self, content = None):
        """ Creates a PNG file from the content.
        """
        if not self.have_file: return False               # nothing to save if no file loaded

        if content is not None: self.save_file(content)  # save the content if provided


        if os.path.exists(self.png_filename):               # check if PNG needs to be updated

            png_time = os.path.getmtime(self.png_filename)
            # print(f"source timestamp: {self.file_datetime}")
            # print(f"png timestamp: {png_time}")

            if png_time - self.file_datetime > 0.1:               # if the PNG file is newer than the source file, no need to update
                # print(f"PNG is newer, so no need to update.")
                return True
            
        print(f"Creating PNG file: {self.png_filename}")

        (firstline, _, source) = self.content.partition("\n")   # get the first line and the rest of the content

        diagtype, formats = self.get_type_info(firstline)       # get diagram type and available output formats

        if diagtype is None:
            print("Didn't find valid diagram type on first line")
            return False

        if not 'png' in formats:
            print("Cannot show this diagram, only export to file")
            return False

        if diagtype == "@startuml":                   # special case for PlantUML   
            diagtype = "plantuml"                            
            source = self.content

        data = {"output_format": "png", "diagram_type": diagtype, "diagram_source": source}
        response = requests.post(URL, json=data, timeout=10)

        if response.status_code == 200:
            with open(self.png_filename, "wb") as file:
                file.write(response.content)
            return True
        else:
            print(response.text)
            return False


    # def show_svg(self):

    #     url = "https://kroki.io/graphviz/svg/eNpLyUwvSizIUHBXqPZIzcnJ17ULzy_KSanlAgB1EAjQ"


    #     response = requests.get(url)
    #     if response.status_code == 200:
    #         svg_content = response.text

    #         with open("svg_image.svg", "w", encoding="utf-8") as file:
    #             file.write(svg_content)

    #         html_content = '<html><body><img src="svg_image.svg" alt="SVG Image"></body></html>'

    #         self.m_htmlPreview.SetPage(html_content)

    #     else:
    #         wx.MessageBox(f"Failed to load SVG. Status code: {response.status_code}", "Error", wx.OK | wx.ICON_ERROR)