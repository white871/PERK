import tkinter as tk
from tkinter import filedialog
import tkinter.font as tkfont
from PIL import Image, ImageTk, ImageOps
import random
import json
from utility_functions import load_img, create_label, create_inverted_label, create_image_canvas, create_interactive_icon, create_display_frame_header, create_display_frame

#class BraillerSettings:

class SettingsViewBase:

    def __init__(self, root, app, THEMES, theme_name="light"):

        self.root = root
        self.app = app

        theme = THEMES[theme_name]
        self.bg = theme["bg"]
        self.header_bg = theme["header_bg"]
        self.hbg = theme["hbg"]
        self.hth = theme["hth"]
        self.fg = theme["fg"]
        self.label_fn = theme["label"]
        self.image_path = theme["image_path"]
        self.inverted = theme["inverted"]

        self.root.configure(bg=self.bg)

        # STATE VARIABLES
        self.circle_buttons = []

        
        # BUILD UI
        self.build_header()
        self.build_main_frames()
        self.build_navigation_buttons()
        self.build_filters_section()

    def build_header(self):

        title_header_canvas = tk.Canvas(
            self.root,
            width=1035,
            height=110,
            background= self.header_bg,
            highlightbackground=self.hbg,
            highlightthickness=self.hth,
            relief="solid",
            bd=2
        )
        title_header_canvas.place(x=5, y=5, anchor="nw")

        title = self.label_fn(
            self.root, 'nw',
            txt="PERK Brailler Digital Interface",
            font_txt="Roboto Condensed",
            font_size=37,
            bold='bold',
            italic='roman',
            backround=self.header_bg,
            location=(50, 30)
        )

        self.perk_braille_img = load_img(
            self.app.resource_path(self.image_path + "PERK_Braille_Image_grey.png"),
            size=(302,110)
        )

        perk_logo = self.label_fn(
            self.root, 'nw',
            img=self.perk_braille_img,
            bd_width=0,
            location=(695, 6)
        )

    def build_main_frames(self):

        display_container = tk.Frame(
            self.root,
            bg=self.bg,
            bd=0,
            highlightthickness=0
        )
        display_container.place(x=530, y=145, width=470, height=500)

        self.filters_frame = create_display_frame(
            display_container,
            bg=self.bg,
            start_display=True,
            border_color=self.fg
        )

        filters_label, line_canvas = create_display_frame_header(
            self.filters_frame,
            "Settings",'n',
            coords=(470/2, 10),
            bg=self.bg,
            fg=self.fg,
            line_color=self.fg
        )

    def home_select(self):
        if self.inverted:
            self.app.show_manage_braillers_inverted()
        else:
            self.app.show_manage_braillers()

    def build_navigation_buttons(self):

        self.home_image = load_img(
            self.app.resource_path(self.image_path + "Home_icon.png"),
            size=(105,110)
        )

        home_icon, home_img_obj = create_image_canvas(
            self.root,
            105, 110, 0, 0,
            'center', self.home_image,
            location=(100, 340)
        )

        label_home = self.label_fn(
            self.root, 'w',
            txt="Device Management",
            font_txt="Roboto Condensed",
            font_size=25,
            bold='normal', italic='roman',
            backround=self.bg,
            location=(165, 337)
        )

        self.home_circle = create_interactive_icon(
            home_icon,
            label_home,
            (52, 54), 41,
            on_select=lambda: self.home_select()
        )

        self.settings_image = load_img(
            self.app.resource_path(self.image_path + "settings_icon.png"), 
            size=(113,100)
        )

        settings_icon, settings_img_obj = create_image_canvas(
            self.root, 
            113, 100, 0, 0, 
            'nw', 
            self.settings_image, 
            location=(50, 160)
        )

        label_settings = self.label_fn(
            self.root, 'w',
            txt="Settings",  
            font_txt="Roboto Condensed", 
            font_size=25, 
            bold='bold', italic='roman', 
            backround=self.bg, 
            location=(162, 210)
        )


    def create_circle_button(
        self, canvas, center, radius, label, selected=False, on_select=None):

        """
        Creates a triangle-shaped button on a canvas with hover and click interactions.
        Args:
            canvas: the Tkinter Canvas to draw on
            center: the center coordinates of the circle
            radius: the radius of the circle
            img_obj: canvas image object to change when clicked
            img_on_click: dict {True_image, False_image} to swap on click
            selected: initial selected state
        """
        x, y = center
        r = radius
        #draw circle
        circle_id = canvas.create_oval(
            x - r, y - r, 
            x + r, y + r, 
            fill="", 
            outline="", 
            width=2
        )
        
        button_state = {
            "circle": circle_id,
            "label": label,
            "selected": selected,
            "on_select": on_select
        }

        self.circle_buttons.append(button_state)

        label.bind("<Enter>", lambda e: self.sublabel_on_enter(e, canvas, circle_id, label))
        label.bind("<Leave>", lambda e: self.sublabel_on_leave(e, canvas, circle_id, label))
        label.bind("<Button-1>", lambda e: self.sublabel_on_click(e, button_state))

        return circle_id

    def sublabel_on_enter(self, event, canvas, circle_id, label):
        canvas.itemconfig(circle_id, outline="gray", width=4)
        label.config(font=("Roboto Condensed", 18, 'bold', 'italic'))

    def sublabel_on_leave(self, event, canvas, circle_id, label):
        canvas.itemconfig(circle_id, outline="", width=2)
        label.config(font=("Roboto Condensed", 18, 'normal', 'roman'))

    def sublabel_on_click(self, event, button_state):
        self.canvas_click(event, clicked_btn=button_state)

    def canvas_motion(self, event):
        for btn in self.circle_buttons:
            x1, y1, x2, y2 = self.preview_canvas.coords(btn["circle"])
            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2
            r = (x2 - x1) / 2
            dx = event.x - cx
            dy = event.y - cy

            if dx*dx + dy*dy <= r*r:
                self.preview_canvas.itemconfig(btn["circle"], outline="gray", width=4)
                btn["label"].config(font=("Roboto Condensed", 18, 'bold', 'italic'))
            else:
                self.preview_canvas.itemconfig(btn["circle"], outline="", width=2)
                btn["label"].config(font=("Roboto Condensed", 18, 'normal', 'roman'))

    def preview_canvas_click(self, event):
        for btn in self.circle_buttons:
            x1, y1, x2, y2 = self.preview_canvas.coords(btn["circle"])
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
               
                if btn["on_select"]:
                    btn["on_select"]()
                    return
            else:
                # Deselect others
                btn["selected"] = False
                btn["label"].config(font=("Roboto Condensed", 18, "normal", "roman"))
               

    def build_filters_section(self):

        self.button_img = load_img(
            self.app.resource_path(self.image_path + "circles_icon1.png"), 
            size=(39,85)
        )

        self.preview_canvas, self.preview_img_obj = create_image_canvas(
            self.filters_frame,
            39, 85, 0, 0, "nw", self.button_img
        )
        self.preview_canvas.place(x=15, y=68)
        
        default_label =  self.label_fn(
            self.filters_frame, 
            'w', txt="Default",  
            font_txt="Roboto Condensed", 
            font_size=18, 
            bold='normal', italic='roman', 
            backround=self.bg, 
            location=(60,90)
        )
        
        default_circle = self.create_circle_button(
            self.preview_canvas, 
            (18.5, 22), 12, 
            default_label,  
            selected=True, 
            on_select=self.default_filter_load
        )

        inverted_label =  self.label_fn(
            self.filters_frame, 
            'w', txt="Inverted",  
            font_txt="Roboto Condensed", 
            font_size=18, 
            bold='normal', italic='roman', 
            backround=self.bg, 
            location=(60,130)
        )
        
        inverted_circle = self.create_circle_button(
            self.preview_canvas, 
            (18.5, 62), 12, 
            inverted_label, 
            selected=False, 
            on_select=self.inverted_filter_load
        )

        self.preview_canvas.bind("<Motion>", self.canvas_motion)
        self.preview_canvas.bind("<Button-1>", self.preview_canvas_click)

            
    def default_filter_load(self):
        if self.inverted:
            self.app.show_settings()

    def inverted_filter_load(self):
        if not self.inverted:
            self.app.show_settings_inverted()


class SettingsView(SettingsViewBase):
    def __init__(self, root, app, THEMES):
        super().__init__(root, app, THEMES, theme_name="light")

class SettingsViewInverted(SettingsViewBase):
    def __init__(self, root, app, THEMES):
        super().__init__(root, app, THEMES, theme_name="dark")