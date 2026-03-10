import tkinter as tk
from tkinter import filedialog
import tkinter.font as tkfont
from PIL import Image, ImageTk, ImageOps
import random
import json
from utility_functions import load_img, create_label, create_image_canvas, create_interactive_icon, create_display_frame_header, create_display_frame

#class BraillerSettings:

class SettingsView:

    def __init__(self, root, app):

        self.root = root
        self.app = app

        self.root.configure(bg="#FFFFFF")

        # STATE VARIABLES
        self.circle_buttons = []

        self.settings_path = "EPICS BCI Code/Data/settings.json"

        # LOAD DATA
        self.load_settings()

        # BUILD UI
        self.build_header()
        self.build_main_frames()
        self.build_navigation_buttons()
        self.build_filters_section()

    def load_settings(self):
        try:
            with open(self.settings_path, "r", encoding="utf-8") as f:
                self.settings = json.load(f)
        except FileNotFoundError:
            self.settings = {}
    
    def build_header(self):

        title_header_canvas = tk.Canvas(
            self.root,
            width=1035,
            height=110,
            background="#eeeeee",
            highlightthickness=0,
            relief="solid",
            bd=2
        )
        title_header_canvas.place(x=5, y=5, anchor="nw")
        title = create_label(
            self.root, 'nw',
            txt="PERK Brailler Digital Interface",
            font_txt="Roboto Condensed",
            font_size=37,
            bold='bold',
            italic='roman',
            backround='#eeeeee',
            location=(50, 30)
        )

        self.perk_braille_img = load_img(
            "EPICS BCI Code/Images/PERK_Braille_Image_grey.png",
            size=(302,110)
        )

        perk_logo = create_label(
            self.root, 'nw',
            img=self.perk_braille_img,
            bd_width=0,
            location=(695, 6)
        )

    def build_main_frames(self):

        settings_container = tk.Frame(
            self.root,
            bg="#FFFFFF",
            bd=3,
            relief="solid"
        )
        settings_container.place(x=530, y=145, width=470, height=500)

        self.settings_frame = create_display_frame(
            settings_container,
            start_display=True
        )

        settings_label, line_canvas = create_display_frame_header(
            self.settings_frame,
            "Settings",
            'n',
            coords=(470/2, 10)
        )

    def home_select(self):
        self.app.show_manage_braillers()

    def settings_select(self):
        self.app.show_settings()
    
    def build_navigation_buttons(self):

        self.home_image = load_img(
            "EPICS BCI Code/Images/Home_icon.png",
            size=(105,110)
        )

        home_icon, home_img_obj = create_image_canvas(
            self.root,
            105, 110, 0, 0,
            'center', self.home_image,
            location=(100, 445)
        )

        label_home = create_label(
            self.root, 'w',
            txt="Device Management",
            font_txt="Roboto Condensed",
            font_size=25,
            bold='normal',
            italic='roman',
            backround='white',
            location=(165, 442)
        )

        home_circle = create_interactive_icon(
            home_icon,
            label_home,
            (52, 54),
            41,
            on_select=lambda: self.home_select()
        )

    def build_filters_section(self):

        filters_frame = tk.Frame(
            self.settings_frame,
            bg="white"
        )

        filters_frame.place(
            x=10,
            y=60,
            width=450,
            height=350
        )

        label = create_label(
            filters_frame,
            'nw',
            txt="Display Filters",
            font_txt="Roboto Condensed",
            font_size=18,
            bold='bold',
            italic='roman',
            backround='white',
            location=(0,0)
        )

        # Example circle buttons
        self.create_filter_button(
            filters_frame,
            "Default",
            (50,100),
            self.default_filter_load
        )

        self.create_filter_button(
            filters_frame,
            "Inverted",
            (200,100),
            self.inverted_filter_load
        )
    
    def create_filter_button(self, parent, text, position, command):

        canvas = tk.Canvas(
            parent,
            width=80,
            height=80,
            bg="white",
            highlightthickness=0
        )

        canvas.place(x=position[0], y=position[1])

        circle = canvas.create_oval(
            10,10,70,70,
            fill="#d9d9d9"
        )

        canvas.create_text(
            40,40,
            text=text,
            font=("Roboto Condensed", 10)
        )

        canvas.bind("<Button-1>", lambda e: command())

        #self.circle_buttons.append(canvas)
    
    def default_filter_load(self):
        print("Default filter selected")

    def inverted_filter_load(self):
        self.app.show_settings_inverted()
        

    def create_circle_button(self, 
        canvas, center, radius, label, img_obj=None, 
        img_on_click=None, selected=False, on_select=None):

        x, y = center
        r = radius
        #draw circle
        circle_id = canvas.create_oval(x - r, y - r, x + r, y + r, fill="", outline="", width=2)
        
        button_state = {
            "circle": circle_id,
            "label": label,
            "selected": selected,
            "img_obj": img_obj,
            "img_canvas": canvas,
            "img_on_click": img_on_click,
            "on_select": on_select
        }

        self.circle_buttons.append(button_state)

        def sublabel_on_enter(event):
            canvas.itemconfig(circle_id, outline="gray", width=4)
            label.config(font=("Roboto Condensed", 18, 'bold', 'italic'))

        def sublabel_on_leave(event):
            canvas.itemconfig(circle_id, outline="", width=2)
            label.config(font=("Roboto Condensed", 18, 'normal', 'roman'))

        def sublabel_on_click(event):
            self.canvas_click(event, clicked_btn=button_state)
            print('Circle Clicked!')

        label.bind("<Enter>", sublabel_on_enter)
        label.bind("<Leave>", sublabel_on_leave)
        label.bind("<Button-1>", sublabel_on_click)


        if selected and img_obj and img_on_click:
            canvas.itemconfig(img_obj, image=img_on_click[True])

        return circle_id


    #################################################
    # Canvas Dispatcher Functions
    #################################################

    def canvas_motion(self, event):
        for btn in self.circle_buttons:
            x1, y1, x2, y2 = btn["img_canvas"].coords(btn["circle"])
            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2
            r = (x2 - x1) / 2
            dx = event.x - cx
            dy = event.y - cy

            if dx*dx + dy*dy <= r*r:
                btn["img_canvas"].itemconfig(btn["circle"], outline="gray", width=4)
                btn["label"].config(font=("Roboto Condensed", 18, 'bold', 'italic'))
            else:
                btn["img_canvas"].itemconfig(btn["circle"], outline="", width=2)
                btn["label"].config(font=("Roboto Condensed", 18, 'normal', 'roman'))

    def preview_canvas_click(self, event):
        for btn in self.circle_buttons:
            x1, y1, x2, y2 = btn["img_canvas"].coords(btn["circle"])
            cx = (x1 + x2)/2
            cy = (y1 + y2)/2
            r = (x2 - x1)/2
            dx = event.x - cx
            dy = event.y - cy
            if dx*dx + dy*dy <= r*r:
                self.canvas_click(event, clicked_btn=btn)
                break  # only select the first circle under cursor

    def canvas_click(self, event, clicked_btn=None):
        for btn in self.circle_buttons:
            if clicked_btn is btn:
                # This is the one clicked
                btn["selected"] = True
                btn["label"].config(font=("Roboto Condensed", 18, "bold", "roman"))
                if btn["img_obj"] and btn["img_on_click"]:
                    btn["img_canvas"].itemconfig(btn["img_obj"], image=btn["img_on_click"][True])
                if btn["on_select"]:
                    btn["on_select"]()
            else:
                # Deselect others
                btn["selected"] = False
                btn["label"].config(font=("Roboto Condensed", 18, "normal", "roman"))
                if btn["img_obj"] and btn["img_on_click"]:
                    btn["img_canvas"].itemconfig(btn["img_obj"], image=btn["img_on_click"][False])
'''if __name__ == "__main__":
    root = tk.Tk()
    app = None
    SettingsView(root, app)
    root.mainloop()'''
