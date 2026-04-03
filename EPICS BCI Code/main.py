import tkinter as tk
from utility_functions import create_label, create_inverted_label
from filters_page import SettingsView, SettingsViewInverted
from manage_braillers import ManageBraillersView, ManageBraillersViewInverted
from live_feed_page import IndividualBraillerView, IndividualBraillerViewInverted

class App:
    def __init__(self, root):
        self.root = root

        # GLOBAL UI STATE
        self.state = {
            "inverted": False,
            "current_brailler": None,
            "root": root
        }

        
        self.THEMES = {
            "light": {
                "bg": "#FFFFFF",
                "header_bg": "#eeeeee",
                "hbg": "#000000",
                "hth": 1,
                "fg": "#000000",
                "label": create_label,
                "image_path": "EPICS BCI Code/Images/",
                "inverted": False
            },
            "dark": {
                "bg": "#000000",
                "header_bg": "#000000",
                "hbg": "#FFFFFF",
                "hth": 1,
                "fg": "#FFFFFF",
                "label": create_inverted_label,
                "image_path": "EPICS BCI Code/Images/Inverted Images/",
                "inverted": True
            }
        }

        font_path_1 = "EPICS BCI Code/Fonts/RobotoCondensed-Italic-VariableFont_wght.ttf"
        font_path_2 = "EPICS BCI Code/Fonts/RobotoCondensed-VariableFont_wght.ttf"


        self.load_fonts(font_path_1)
        self.load_fonts(font_path_2)

        self.current_page = None
        self.show_manage_braillers()

    def load_fonts(self, font_path):
        import ctypes

        FR_PRIVATE = 0x10
        
        return ctypes.windll.gdi32.AddFontResourceExW(font_path, FR_PRIVATE, 0)
        

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_settings(self):
        self.clear()
        self.root.geometry("1050x700")
        SettingsView(self.root, self, self.THEMES)

    def show_settings_inverted(self):
        self.clear()
        self.root.geometry("1050x700")
        SettingsViewInverted(self.root, self, self.THEMES)

    def show_manage_braillers(self):
        self.clear()
        self.root.geometry("1050x750")
        ManageBraillersView(self.root, self, self.THEMES)

    def show_manage_braillers_inverted(self):
        self.clear()
        self.root.geometry("1050x750")
        ManageBraillersViewInverted(self.root, self, self.THEMES)

    def show_text_page(self, brailler_name):
        self.clear()
        self.root.geometry("1050x700")
        IndividualBraillerView(self.root, self, brailler_name, self.THEMES)

    def show_text_page_inverted(self, brailler_name):
        self.clear()
        self.root.geometry("1050x700")
        IndividualBraillerViewInverted(self.root, self, brailler_name, self.THEMES)

root = tk.Tk()
root.geometry("1050x700")
root.resizable(False, False)

app = App(root)
root.mainloop()

print("test")