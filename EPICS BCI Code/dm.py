import tkinter as tk
from tkinter import filedialog
import tkinter.font as tkfont
from PIL import Image, ImageTk, ImageOps
import random
from utility_functions import load_img, create_label, create_inverted_label, create_image_canvas, create_triangle_button, create_interactive_icon, create_display_frame_header, create_display_frame

def load_settings_page(root):
    # Set geometry
    root.configure(bg="#FFFFFF")

    file_path = "Data\\brailler_output.txt"
    #"brailler_output.txt"

    circle_buttons = []


    #################################################
    #Functions we reuse a whole lot
    #################################################

    ###### Making circle buttons ######
    def create_circle_button(
        canvas, center, radius, label, img_obj=None, 
        img_on_click=None, selected=False, on_select=None):

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

        circle_buttons.append(button_state)

        def sublabel_on_enter(event):
            canvas.itemconfig(circle_id, outline="gray", width=4)
            label.config(font=("Roboto Condensed", 18, 'bold', 'italic'))

        def sublabel_on_leave(event):
            canvas.itemconfig(circle_id, outline="", width=2)
            label.config(font=("Roboto Condensed", 18, 'normal', 'roman'))

        def sublabel_on_click(event):
            canvas_click(event, clicked_btn=button_state)
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

    def canvas_motion(event):
        for btn in circle_buttons:
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

    def preview_canvas_click(event):
        for btn in circle_buttons:
            x1, y1, x2, y2 = btn["img_canvas"].coords(btn["circle"])
            cx = (x1 + x2)/2
            cy = (y1 + y2)/2
            r = (x2 - x1)/2
            dx = event.x - cx
            dy = event.y - cy
            if dx*dx + dy*dy <= r*r:
                canvas_click(event, clicked_btn=btn)
                break  # only select the first circle under cursor

    def canvas_click(event, clicked_btn=None):
        for btn in circle_buttons:
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


                
    def show_text_visibility():
        text_visibility_frame.tkraise()

    def show_filters():
        filters_frame.tkraise()


    ########TITLE/HEADER FORMATTING###########
    title_header_canvas = tk.Canvas(root, width=1035, height=110, background="#eeeeee", highlightthickness=0, relief="solid", bd=2)
    title_header_canvas.place(x=5, y=5, anchor="nw")

    title = create_label(root, 'nw', txt="PERK Brailler Digital Interface",  font_txt="Roboto Condensed", font_size=37, bold='bold', italic='roman', backround='#eeeeee', location=(50, 30))

    perk_braille_img = load_img("EPICS BCI Code\\Images\\PERK_Braille_Image_grey.png", size=(302,110))
    perk_logo = create_label(root, 'nw', img=perk_braille_img, bd_width=0, location=(695, 6))
    ########################################
    #Creating Frames
    #######################################

    display_container = tk.Frame(root, bg="#FFFFFF", bd=3, relief="solid")
    display_container.place(x=530, y=140, width=470, height=500)

    text_visibility_frame = create_display_frame(display_container, start_display=True)
    text_visibility_label, line_canvas =  create_display_frame_header(text_visibility_frame, "Text/Visibility", 'n', coords=(470/2, 10))

    contraction_library_frame = create_display_frame(display_container)
    contraction_library_label, line_canvas =  create_display_frame_header(contraction_library_frame, "Contractions", 'n', coords=(470/2, 10))

    filters_frame = create_display_frame(display_container)
    filters_library_label, line_canvas = create_display_frame_header(filters_frame, "Filters", 'n', coords=(470/2, 10))

    # load all the images, but don't show
    filter_images = {
        "default": load_img("EPICS BCI Code/Images/circles_icon1.png", size=(39,85)),
        "inverted": load_img("EPICS BCI Code/Images/circles_icon2.png", size=(39,85)),
    }

    default_image = {
        True: filter_images["default"],
        False: filter_images["inverted"]
    }

    inverted_image = {
        True: filter_images["inverted"],
        False: filter_images["default"]
    }

    # make my preview canvas
    preview_canvas, canvas_img_obj = create_image_canvas(
        filters_frame,
        39, 85, 0, 0, "nw", filter_images["default"]
    )
    preview_canvas.place(x=15, y=68)


    def default_filter_load():
        return

    def inverted_filter_load():
        for widget in root.winfo_children():
            widget.destroy()  # clear old widgets
        load_settings_page_inverted(root)
        return

    ########################################################
    #Default and Inverted Section
    ###################################################

    default_label =  create_label(filters_frame, 'w', txt="Default",  font_txt="Roboto Condensed", font_size=18, bold='normal', italic='roman', backround='white', location=(60,90))
    default_circle = create_circle_button(preview_canvas, (18.5, 22), 12, default_label, canvas_img_obj, default_image, selected=True, on_select=default_filter_load)

    inverted_label =  create_label(filters_frame, 'w', txt="Inverted",  font_txt="Roboto Condensed", font_size=18, bold='normal', italic='roman', backround='white', location=(60,130))
    inverted_circle = create_circle_button(preview_canvas, (18.5, 62), 12, inverted_label, canvas_img_obj, inverted_image, selected=False, on_select=inverted_filter_load)

    preview_canvas.bind("<Motion>", canvas_motion)
    preview_canvas.bind("<Button-1>", preview_canvas_click)

    ######################################################################
    #Device Management Section
    ######################################################################

    home_image = load_img("EPICS BCI Code/Images/Home_icon.png", size=(105,110))
    home_icon, home_img_obj = create_image_canvas(root, 105, 110, 0, 0, 'center', home_image, location=(100, 340))
    label_sub_title_2 = create_label(root, 'w', txt="Device Management",  font_txt="Roboto Condensed", font_size=25, bold='normal', italic='roman', backround='white', location=(165, 337))
    home_circle = create_interactive_icon(home_icon, label_sub_title_2, (52, 52), 41, on_select=lambda: load_manage_braillers_page(root))

    ########################################################
    #Settings Section
    ###################################################

    settings_image = load_img("EPICS BCI Code/Images/settings_icon.png", size=(113,100))
    settings_icon, settings_img_obj = create_image_canvas(root, 113, 100, 0, 0, 'nw', settings_image, location=(50, 160))
    label_sub_title_1 = create_label(root, 'w', txt="Settings",  font_txt="Roboto Condensed", font_size=25, bold='bold', italic='roman', backround='white', location=(162, 210))

    # load 
    root.mainloop()


def load_settings_page_inverted(root):

    # Set geometry
    root.configure(bg="#000000")

    file_path = "Data\\brailler_output.txt"
    #"brailler_output.txt"

    circle_buttons = []


    #################################################
    #Functions we reuse a whole lot
    #################################################

    ###### Making circle buttons ######
    def create_circle_button(
        canvas, center, radius, label, img_obj=None, 
        img_on_click=None, selected=False, on_select=None):

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

        circle_buttons.append(button_state)

        def sublabel_on_enter(event):
            canvas.itemconfig(circle_id, outline="gray", width=4)
            label.config(font=("Roboto Condensed", 18, 'bold', 'italic'))

        def sublabel_on_leave(event):
            canvas.itemconfig(circle_id, outline="", width=2)
            label.config(font=("Roboto Condensed", 18, 'normal', 'roman'))

        def sublabel_on_click(event):
            canvas_click(event, clicked_btn=button_state)
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

    def canvas_motion(event):
        for btn in circle_buttons:
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

    def preview_canvas_click(event):
        for btn in circle_buttons:
            x1, y1, x2, y2 = btn["img_canvas"].coords(btn["circle"])
            cx = (x1 + x2)/2
            cy = (y1 + y2)/2
            r = (x2 - x1)/2
            dx = event.x - cx
            dy = event.y - cy
            if dx*dx + dy*dy <= r*r:
                canvas_click(event, clicked_btn=btn)
                break  # only select the first circle under cursor

    def canvas_click(event, clicked_btn=None):
        for btn in circle_buttons:
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


                
    ########TITLE/HEADER FORMATTING###########
    title_header_canvas = tk.Canvas(root, width=1035, height=110, background="#000000", highlightbackground="#FFFFFF", highlightthickness=1, relief="solid", bd=2)
    title_header_canvas.place(x=5, y=5, anchor="nw")

    title = create_inverted_label(root, 'nw', txt="PERK Brailler Digital Interface",  font_txt="Roboto Condensed", font_size=37, bold='bold', italic='roman', backround='#000000', location=(50, 30))

    perk_braille_img = load_img("EPICS BCI Code\\Images\\Inverted Images\\PERK_Braille_Image_inverted.png", size=(302,110))
    perk_logo = create_label(root, 'nw', img=perk_braille_img, bd_width=0, location=(695, 6))

    ########################################
    #Creating Frames
    #######################################
    display_container = tk.Frame(root, bg="#000000", bd=3, relief="solid")
    display_container.place(x=530, y=145, width=470, height=500)

    filters_frame = create_display_frame(display_container, bg="#000000", start_display=True, inverted=True)
    filters_library_label, line_canvas = create_display_frame_header(filters_frame, "Filters", 'n', coords=(470/2, 10), bg="#000000", fg="#FFFFFF", line_color="#FFFFFF")

    # load all the images, but don't show
    filter_images = {
        "default": load_img("EPICS BCI Code/Images/Inverted Images/circles_icon1_inverted.png", size=(39,85)),
        "inverted": load_img("EPICS BCI Code/Images/Inverted Images/circles_icon2_inverted.png", size=(39,85)),
    }

    default_image = {
        True: filter_images["default"],
        False: filter_images["inverted"]
    }

    inverted_image = {
        True: filter_images["inverted"],
        False: filter_images["default"]
    }

    # make my preview canvas
    preview_canvas, canvas_img_obj = create_image_canvas(
        filters_frame,
        39, 85, 0, 0, "nw", filter_images["default"]
    )
    preview_canvas.place(x=15, y=68)


    def default_filter_load():
        for widget in root.winfo_children():
            widget.destroy()  # clear old widgets
        load_settings_page(root)
        return

    def inverted_filter_load():
        return

    ########################################################
    #Default and Inverted Section
    ###################################################

    default_label =  create_inverted_label(filters_frame, 'w', txt="Default",  font_txt="Roboto Condensed", font_size=18, bold='normal', italic='roman', backround='black', location=(60,90))
    default_circle = create_circle_button(preview_canvas, (18.5, 22), 12, default_label, canvas_img_obj, default_image, selected=False, on_select=default_filter_load)

    inverted_label =  create_inverted_label(filters_frame, 'w', txt="Inverted",  font_txt="Roboto Condensed", font_size=18, bold='normal', italic='roman', backround='black', location=(60,130))
    inverted_circle = create_circle_button(preview_canvas, (18.5, 62), 12, inverted_label, canvas_img_obj, inverted_image, selected=True, on_select=inverted_filter_load)

    preview_canvas.bind("<Motion>", canvas_motion)
    preview_canvas.bind("<Button-1>", preview_canvas_click)

    ######################################################################
    #Device Management Section
    ######################################################################

    home_image = load_img("EPICS BCI Code/Images/Inverted Images/Home_icon_inverted.png", size=(105,110))
    home_icon, home_img_obj = create_image_canvas(root, 105, 110, 0, 0, 'center', home_image, location=(100, 340))
    label_sub_title_2 = create_inverted_label(root, 'w', txt="Device Management",  font_txt="Roboto Condensed", font_size=25, bold='normal', italic='roman', backround='black', location=(165, 337))
    home_circle = create_interactive_icon(home_icon, label_sub_title_2, (52, 52), 41)

    ########################################################
    #Settings Section
    ###################################################

    settings_image = load_img("EPICS BCI Code/Images/Inverted Images/settings_icon_inverted.png", size=(113,100))
    settings_icon, settings_img_obj = create_image_canvas(root, 113, 100, 0, 0, 'nw', settings_image, location=(50, 160))
    label_sub_title_1 = create_inverted_label(root, 'w', txt="Settings",  font_txt="Roboto Condensed", font_size=25, bold='bold', italic='roman', backround='black', location=(162, 210))

    # load 
    root.mainloop()


def load_manage_braillers_page(root):
    for widget in root.winfo_children():
            widget.destroy()

    def toggle_brailler_popup(brailler_name):
        global current_brailler

        if current_brailler==brailler_name:
            brailler_popup.place_forget()
            current_brailler=None
            return
        current_brailler=brailler_name
        brailler_popup.place(x=50, y=520, width=950, height=50)
        brailler_popup.tkraise()


    def on_brailler_click(label, name):
        global current_brailler_label

        # If clicking the same label → unbold + hide popup
        if current_brailler_label == label:
            label.config(font=("Roboto Condensed", 18, "normal", "roman"))
            label.is_bold = False

            brailler_popup.place_forget()
            current_brailler_label = None
            return

        # If clicking a different brailler
        if current_brailler_label:
            current_brailler_label.config(
                font=("Roboto Condensed", 18, "normal", "roman")
            )
            current_brailler_label.is_bold = False

        # Bold new one
        label.config(font=("Roboto Condensed", 18, "bold", "roman"))
        label.is_bold = True

        brailler_popup.place(x=50, y=520, width=950, height=50)
        brailler_popup.tkraise()

        current_brailler_label = label

    def set_brailler_status(name, connected):
        if name not in brailler_status_dots:
            return

        canvas, dot = brailler_status_dots[name]
        color = STATUS_GREEN if connected else STATUS_RED
        canvas.itemconfig(dot, fill=color)


    braillers = [
        "Mark's Brailler", "Nash's Brailler", "Lucy's Brailler",
        "Diana's Brailler", "Mohammad's Brailler", "Sarvesh's Brailler",
        "Ayona's Brailler", "Felix's Brailler", "Joe's Brailler"
    ]

    # Main window
    root.configure(bg="#FFFFFF")

    # Header
    title_header_canvas = tk.Canvas(root, width=1035, height=110, background="#eeeeee", highlightthickness=0, relief="solid", bd=2)
    title_header_canvas.place(x=5, y=5, anchor="nw")

    title = create_label(root, 'nw', txt="PERK Brailler Digital Interface",  font_txt="Roboto Condensed", font_size=37, bold='bold', italic='roman', backround='#eeeeee', location=(50, 30))

    perk_braille_img = load_img("EPICS BCI Code/Images/PERK_Braille_Image_grey.png", size=(302,110))
    perk_logo = create_label(root, 'nw', img=perk_braille_img, bd_width=0, location=(695, 6))

    # Manage Braillers row
    home_icon = load_img("EPICS BCI Code/Images/Home_icon.png", size=(75, 75))
    create_label(
        root,
        anchr="nw",
        img=home_icon,
        location=(30, 150)
    )

    home_label = create_label(
        root,
        anchr="nw",
        txt="Manage Braillers",
        font_txt="Roboto Condensed",
        font_size=25,
        bold="normal",
        backround="white",
        location=(105, 170)
    )

    create_label(
        root,
        anchr="ne",
        txt="Pair All",
        font_txt="Roboto Condensed",
        font_size=25,
        bold="normal",
        backround="white",
        location=(980, 170)
    )

    # Brailler list 
    start_x = 110
    start_y = 250
    x_gap = 350
    y_gap = 100
    brailler_status_dots = {}
    STATUS_RADIUS = 6
    STATUS_GREEN = "#93c47d"
    STATUS_RED = "#e06666"
    status_dots = {}


    for i, name in enumerate(braillers):
        row = i // 3
        col = i % 3

        x = start_x + col * x_gap
        y = start_y + row * y_gap

        lbl = create_label(
            root,
            anchr="nw",
            txt=name,
            font_txt="Roboto Condensed",
            font_size=18,
            bold="normal",
            backround="white",
            location=(x, y)
        )

        lbl.is_bold = False
        lbl.config(cursor="hand2")
        lbl.bind("<Button-1>", lambda e, l=lbl, n=name: on_brailler_click(l, n))

        dot_canvas = tk.Canvas(
            root,
            width=STATUS_RADIUS * 2,
            height=STATUS_RADIUS * 2,
            bg="white",
            highlightthickness=0
        )
        dot_canvas.place(x=x - 20, y=y + 5, anchor="nw")  

        dot = dot_canvas.create_oval(
            0, 0,
            STATUS_RADIUS * 2,
            STATUS_RADIUS * 2,
            outline=""
        )

        brailler_status_dots[name] = (dot_canvas, dot)

    set_brailler_status("Mark's Brailler", False)
    set_brailler_status("Nash's Brailler", False)
    set_brailler_status("Ayona's Brailler", True)
    set_brailler_status("Joe's Brailler", False)
    set_brailler_status("Lucy's Brailler", True)
    set_brailler_status("Diana's Brailler", False)
    set_brailler_status("Mohammad's Brailler", True)
    set_brailler_status("Sarvesh's Brailler", True)
    set_brailler_status("Felix's Brailler", False)

    # Bottom actions
    bt_icon = load_img("EPICS BCI Code\\Images\\Bluetooth_icon.png", size=(75, 75))
    create_label(
        root,
        anchr="sw",
        img=bt_icon,
        location=(30, 650)
    )

    create_label(
        root,
        anchr="sw",
        txt="Start Pairing Process",
        font_txt="Roboto Condensed",
        font_size=25,
        bold="normal",
        backround="white",
        location=(105, 640)
    )

    gear_icon = load_img("EPICS BCI Code\\Images\\settings_icon.png", size=(75, 75))
    create_label(
        root,
        anchr="se",
        img=gear_icon,
        location=(855, 650)
    )

    create_label(
        root,
        anchr="se",
        txt="Settings",
        font_txt="Roboto Condensed",
        font_size=25,
        bold="normal",
        backround="white",
        location=(970, 640)
    )

    #Brailler popup stuff
    current_brailler_label=None

    brailler_popup=create_display_frame(
        root, 
        rel_fill=(0,0),
        bg="#eeeeee",
        start_display=False
    )

    brailler_popup.place(x=50, y=530, width=950, height=50)
    brailler_popup.place_forget()

    brailler_popup.config(
        highlightbackground="black",
        highlightthickness=1
    )

    popup_buttons=[]
    button_names= "Live Feed", "Disconnect Brailler", "Pair Device", "Rename Device"
    x_positions=[60, 250, 530, 730]

    for name, x in zip(button_names, x_positions):
        lbl=create_label(
            brailler_popup, 
            anchr="nw",
            txt=name, 
            font_txt="Roboto Condensed", 
            font_size=18, 
            bold="normal", 
            backround="#eeeeee",
            location=(x, 5)
            )
        lbl.config(cursor="hand2")
        popup_buttons.append(lbl)

    root.mainloop()
