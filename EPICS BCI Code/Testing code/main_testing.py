import tkinter as tk
import sys
import os
import json
from utility_functions import create_label, create_inverted_label
from filters_page_testing import SettingsView, SettingsViewInverted
from manage_braillers_testing import ManageBraillersView, ManageBraillersViewInverted
from live_feed_page_testing import IndividualBraillerView, IndividualBraillerViewInverted

class App:
    def __init__(self, root):
        self.root = root

        self.settings_path = "EPICS BCI Code/Data/load_settings.txt"

        try:
            with open(self.settings_path, "r", encoding="utf-8") as f:
                self.state = json.load(f)
        except FileNotFoundError:
            self.state = {}

        self.THEMES = {
            "light": {
                "bg": "#FFFFFF",
                "header_bg": "#eeeeee",
                "hbg": "#000000",
                "hth": 1,
                "fg": "#000000",
                "label": create_label,
                "image_path": "EPICS BCI Code/Images",
                "inverted": False
            },
            "dark": {
                "bg": "#000000",
                "header_bg": "#000000",
                "hbg": "#FFFFFF",
                "hth": 1,
                "fg": "#FFFFFF",
                "label": create_inverted_label,
                "image_path": "EPICS BCI Code/Images/Inverted Images",
                "inverted": True
            }
        }

        font_path_1 = "EPICS BCI Code/Fonts/RobotoCondensed-Italic-VariableFont_wght.ttf"
        font_path_2 = "EPICS BCI Code/Fonts/RobotoCondensed-VariableFont_wght.ttf"


        self.load_fonts(font_path_1)
        self.load_fonts(font_path_2)

        self.current_page = None

        if self.state["inverted"]:
            self.show_manage_braillers_inverted()
        else:
            self.show_manage_braillers()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        # This finds every child window (popups) and destroys them
        for child in self.root.winfo_children():
            if isinstance(child, tk.Toplevel):
                child.destroy()
        
        # Finally, destroy the main window
        self.root.destroy()

    def load_fonts(self, font_path):
        import ctypes

        FR_PRIVATE = 0x10
        
        return ctypes.windll.gdi32.AddFontResourceExW(font_path, FR_PRIVATE, 0)
        

    def clear(self):
        for widget in self.root.winfo_children():
            if not isinstance(widget, tk.Toplevel):
                widget.destroy()

    def save_settings(self, inverted, brailler):
        self.state["inverted"] = inverted
        self.state["current_brailler"] = brailler
        with open(self.settings_path, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=4, ensure_ascii=False)

    def show_settings(self):
        self.clear()
        self.save_settings(False, None)
        self.root.geometry("1050x700")
        SettingsView(self.root, self, self.THEMES)

    def show_settings_inverted(self):
        self.clear()
        self.save_settings(True, None)
        self.root.geometry("1050x700")
        SettingsViewInverted(self.root, self, self.THEMES)

    def show_manage_braillers(self):
        self.clear()
        self.save_settings(False, None)
        self.root.geometry("1050x750")
        ManageBraillersView(self.root, self, self.THEMES)

    def show_manage_braillers_inverted(self):
        self.clear()
        self.save_settings(True, None)
        self.root.geometry("1050x750")
        ManageBraillersViewInverted(self.root, self, self.THEMES)

    def show_text_page(self, brailler_name, open_tab="live_feed"):
        self.clear()
        self.save_settings(False, brailler_name)
        self.root.geometry("1050x700")
        IndividualBraillerView(self.root, self, brailler_name, self.THEMES, open_tab)

    def show_text_page_inverted(self, brailler_name, open_tab="live_feed"):
        self.clear()
        self.save_settings(True, brailler_name)
        self.root.geometry("1050x700")
        IndividualBraillerViewInverted(self.root, self, brailler_name, self.THEMES, open_tab)

root = tk.Tk()
root.geometry("1050x700")
root.resizable(False, False)

app = App(root)
root.mainloop()

print("test")