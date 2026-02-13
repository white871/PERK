import tkinter as tk
from tkinter import filedialog, messagebox
import tkinter.font as tkfont
from PIL import Image, ImageTk
import random
import json
from utility_functions import load_img, create_label, create_image_canvas, create_triangle_button, create_interactive_icon, make_interactive_image, create_display_frame_header, create_display_frame
from dm import load_settings_page, load_settings_page_inverted, load_manage_braillers_page

root = tk.Tk()
root.geometry("1050x700")
root.resizable(False, False)

load_settings_page(root)