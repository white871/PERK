import tkinter as tk
from tkinter import filedialog, messagebox
import tkinter.font as tkfont
from PIL import Image, ImageTk
import random
import json
from utility_functions import load_img, create_label, create_image_canvas, create_triangle_button, create_interactive_icon, make_interactive_image, create_display_frame_header, create_display_frame
from dm import load_settings_page
from dm_inverted import load_settings_page_inverted
from manage_braillers import load_manage_braillers_page


class App:
    def __init__(self, root):
        self.root = root

        # GLOBAL UI STATE
        self.state = {
            "inverted": False,
            "current_brailler": None,
            "root": root
        }

        self.current_page = None
        self.show_settings()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_settings(self):
        self.clear()
        root.geometry("1050x700")
        load_settings_page(self.root, self)

    def show_settings_inverted(self):
        self.clear()
        self.state["inverted"] = True
        load_settings_page_inverted(self.root, self)

    def show_manage_braillers(self):
        self.clear()
        root.geometry("1050x750")
        load_manage_braillers_page(self.root, self)



root = tk.Tk()
root.geometry("1050x700")
root.resizable(False, False)

app = App(root)
root.mainloop()

print("test")