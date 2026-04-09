import tkinter as tk
import sys
import os
import json
from utility_functions import create_label, create_inverted_label
from filters_page import SettingsView, SettingsViewInverted
from manage_braillers import ManageBraillersView, ManageBraillersViewInverted
from live_feed_page import IndividualBraillerView, IndividualBraillerViewInverted

class App:
    def __init__(self, root):
        self.root = root

        self.settings_path = self.app.ensure_data_file("Data/load_settings.txt")

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
                "image_path": self.resource_path("Images"),
                "inverted": False
            },
            "dark": {
                "bg": "#000000",
                "header_bg": "#000000",
                "hbg": "#FFFFFF",
                "hth": 1,
                "fg": "#FFFFFF",
                "label": create_inverted_label,
                "image_path": self.resource_path("Images/Inverted Images"),
                "inverted": True
            }
        }

        font_path_1 = self.resource_path("Fonts/RobotoCondensed-Italic-VariableFont_wght.ttf")
        font_path_2 = self.resource_path("Fonts/RobotoCondensed-VariableFont_wght.ttf")


        self.load_fonts(font_path_1)
        self.load_fonts(font_path_2)

        self.current_page = None

        if self.state["inverted"]:
            self.show_manage_braillers_inverted()
        else:
            self.show_manage_braillers()

    def writeable_path(self, relative_path):
        base_path = os.path.dirname(sys.executable)  # folder where exe is
        return os.path.join(base_path, relative_path)

    def resource_path(self, relative_path):
        base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
        return os.path.join(base_path, relative_path)

    def ensure_data_file(self, relative_path):
        writable = self.writeable_path(relative_path)
        resource = self.resource_path(relative_path)

        # Make sure folder exists
        os.makedirs(os.path.dirname(writable), exist_ok=True)

         # If file doesn't exist outside → copy it from EXE
        if not os.path.exists(writable):
            try:
                with open(resource, "r", encoding="utf-8") as src:
                    content = src.read()
            except Exception:
                content = ""  # fallback if something goes wrong

            with open(writable, "w", encoding="utf-8") as dst:
                dst.write(content)

        return writable

    def load_fonts(self, font_path):
        import ctypes

        FR_PRIVATE = 0x10
        
        return ctypes.windll.gdi32.AddFontResourceExW(font_path, FR_PRIVATE, 0)
        

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_settings(self):
        self.clear()
        self.state["inverted"] = False
        self.state["current_brailler"] = None
        with open(self.settings_path, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=4, ensure_ascii=False)
        self.root.geometry("1050x700")
        SettingsView(self.root, self, self.THEMES)

    def show_settings_inverted(self):
        self.clear()
        self.state["inverted"] = True
        self.state["current_brailler"] = None
        with open(self.settings_path, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=4, ensure_ascii=False)
        self.root.geometry("1050x700")
        SettingsViewInverted(self.root, self, self.THEMES)

    def show_manage_braillers(self):
        self.clear()
        self.state["inverted"] = False
        self.state["current_brailler"] = None
        with open(self.settings_path, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=4, ensure_ascii=False)
        self.root.geometry("1050x750")
        ManageBraillersView(self.root, self, self.THEMES)

    def show_manage_braillers_inverted(self):
        self.clear()
        self.state["inverted"] = True
        self.state["current_brailler"] = None
        with open(self.settings_path, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=4, ensure_ascii=False)
        self.root.geometry("1050x750")
        ManageBraillersViewInverted(self.root, self, self.THEMES)

    def show_text_page(self, brailler_name):
        self.clear()
        self.state["inverted"] = False
        self.state["current_brailler"] = brailler_name
        with open(self.settings_path, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=4, ensure_ascii=False)
        self.root.geometry("1050x700")
        IndividualBraillerView(self.root, self, brailler_name, self.THEMES)

    def show_text_page_inverted(self, brailler_name):
        self.clear()
        self.state["inverted"] = True
        self.state["current_brailler"] = brailler_name
        with open(self.settings_path, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=4, ensure_ascii=False)
        self.root.geometry("1050x700")
        IndividualBraillerViewInverted(self.root, self, brailler_name, self.THEMES)

root = tk.Tk()
root.geometry("1050x700")
root.resizable(False, False)

app = App(root)
root.mainloop()

print("test")