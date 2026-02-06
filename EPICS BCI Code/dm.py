import tkinter as tk
from tkinter import filedialog
import tkinter.font as tkfont
from PIL import Image, ImageTk, ImageOps
import random

root = tk.Tk()


# Set geometry
root.geometry("1050x700")
root.resizable(False, False)
root.configure(bg="#FFFFFF")

file_path = "Data\\brailler_output.txt"
#"brailler_output.txt"

circle_buttons = []

#for filter stuff:
all_labels = []
all_buttons = []
all_canvases = []
all_frames = []

#################################################
#Functions we reuse a whole lot
#################################################
def load_img(path, size=(80,80)):
    img = Image.open(path)
    img = img.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

#this one should help me with inverting and adding filters later on:
def load_pil_img(path, size=None):
    img = Image.open(path)
    if size:
        img = img.resize(size, Image.Resampling.LANCZOS)
    return img

def create_label(root, anchr, txt=None, img=None, font_txt=None, font_size=None, bold=None, italic=None, backround=None, bd_width=None, location=(0, 0)):
    if img==None:
        label = tk.Label(root, text=txt, font=(font_txt, font_size, bold, italic), bg=backround)
    elif txt==None:
        label = tk.Label(root, image=img, borderwidth=bd_width)
    label.place(x=location[0], y=location[1], anchor = anchr)
    all_labels.append(label) #for filter
    return label

def create_image_canvas(root, wdth, hght, highlightthick, border, anchr, img, location=(0, 0)):
    canvas = tk.Canvas(root, width=wdth, height=hght, highlightthickness=highlightthick, bd=border)
    canvas.place(x=location[0], y=location[1], anchor=anchr)
    img_obj = canvas.create_image(0, 0, anchor='nw', image=img)
    all_canvases.append(canvas) #for filter

    return canvas, img_obj


def create_triangle_button(
    canvas, coords, label, img_obj=None, 
    img_on_click=None, selected=False, on_select=None):
    """
    Creates a triangle-shaped button on a canvas with hover and click interactions.
    Args:
        canvas: the Tkinter Canvas to draw on
        coords: tuple of triangle coordinates
        img_obj: canvas image object to change when clicked
        img_on_click: dict {True_image, False_image} to swap on click
        selected: initial selected state
   """
    # Draw the triangle
    triangle_id = canvas.create_polygon(coords, fill="", outline="")

    button_data = {
        "tri": triangle_id,
        "label": label,
        "selected": selected,
        "img_obj": img_obj,
        "img_on_click": img_on_click
    }
    
    triangle_buttons.append(button_data)
    all_labels.append(label) #for filter


    def update_fonts_and_images():
        """Deselect all others, select this one, and update images."""
        for btn in triangle_buttons:
            if btn["tri"] == triangle_id:
                btn["selected"] = True
                btn["label"].config(font=("Roboto Condensed", 20, 'bold', 'roman'))
                if btn["img_obj"] and btn["img_on_click"]:
                    canvas.itemconfig(btn["img_obj"], image=btn["img_on_click"]["True"])
                if on_select:
                    on_select()
            else:
                btn["selected"] = False
                btn["label"].config(font=("Roboto Condensed", 20, 'normal', 'roman'))
                if btn["img_obj"] and btn["img_on_click"]:
                    canvas.itemconfig(btn["img_obj"], image=btn["img_on_click"]["False"])

        ## i need to add something here saying if selecting a certain filter command, apply that filter to the ui?

    # Hover effects
    def on_enter(event):
        canvas.itemconfig(triangle_id, outline="gray", width=3)
        if not button_data["selected"]:
            label.config(font=("Roboto Condensed", 20, 'bold', 'italic'))

    def on_leave(event):
        canvas.itemconfig(triangle_id, outline="", width=1)
        if not button_data["selected"]:
            label.config(font=("Roboto Condensed", 20, 'normal', 'roman'))

    def on_click(event):
        update_fonts_and_images()

    # Bind events
    canvas.tag_bind(triangle_id, "<Enter>", on_enter)
    canvas.tag_bind(triangle_id, "<Leave>", on_leave)
    canvas.tag_bind(triangle_id, "<Button-1>", on_click)

    label.bind("<Enter>", on_enter)
    label.bind("<Leave>", on_leave)
    label.bind("<Button-1>", on_click)

    if selected:
        update_fonts_and_images()
    return triangle_id

def create_interactive_icon(canvas, label,
    circle_center, circle_radius):
    """
    Creates an interactive canvas with image and a circular hover area,
    plus a label that reacts on hover and click.
    Returns canvas, circle_id, label
    """
    # Create circular hover area
    x, y = circle_center
    r = circle_radius
    circle_id = canvas.create_oval(x-r, y-r, x+r, y+r, fill="", outline="", width=3)

    
    # Cursor detection
    def cursor_in_circle(event):
        dx = event.x - x
        dy = event.y - y
        return dx*dx + dy*dy <= r*r

    # Hover motion
    def hover_motion(event):
        if cursor_in_circle(event):
            canvas.itemconfig(circle_id, outline="gray", width=4)
            label.config(font=("Roboto Condensed", 25, 'bold', 'italic'))
        else:
            canvas.itemconfig(circle_id, outline="", width=2)
            label.config(font=("Roboto Condensed", 25, 'normal', 'roman'))

    # Click
    def on_click(event):
        if cursor_in_circle(event):
            print(f"{label} clicked!")

    # Bind events
    canvas.bind("<Motion>", hover_motion)
    canvas.bind("<Button-1>", on_click)
    
    def sublabel_on_enter(event):
        canvas.itemconfig(circle_id, outline="gray", width=4)
        label.config(font=("Roboto Condensed", 25, 'bold', 'italic'))

    def sublabel_on_leave(event):
        canvas.itemconfig(circle_id, outline="", width=2)
        label.config(font=("Roboto Condensed", 25, 'normal', 'roman'))

    def sublabel_on_click(event):
        print('Circle Clicked!')

    label.bind("<Enter>", sublabel_on_enter)      # mouse enters
    label.bind("<Leave>", sublabel_on_leave)      # mouse leaves
    label.bind("<Button-1>", sublabel_on_click)   # left mouse click

    return circle_id

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
        "img_on_click": img_on_click,
        "on_select": on_select
    }

    circle_buttons.append(button_state)
    all_labels.append(label) #for filter

    
    def update_selection():
        for btn in circle_buttons:
            if btn["circle"] == circle_id:
                btn["selected"] = True
                btn["label"].config(
                    font=("Roboto Condensed", 25, "bold", "roman")
                )
                if btn["img_obj"] and btn["img_on_click"]:
                    canvas.itemconfig(btn["img_obj"], image=btn["img_on_click"])
                if on_select:
                    on_select()
            else:
                btn["selected"] = False
                btn["label"].config(
                    font=("Roboto Condensed", 25, "normal", "roman")
                )
                if btn["img_obj"] and btn["img_on_click"]:
                    canvas.itemconfig(btn["img_obj"], image=btn["img_on_click"])

    # Cursor detection
    def cursor_in_circle(event):
        dx = event.x - x
        dy = event.y - y
        return dx*dx + dy*dy <= r*r

    # Hover motion
    def hover_motion(event):
        if cursor_in_circle(event):
            canvas.itemconfig(circle_id, outline="gray", width=4)
            label.config(font=("Roboto Condensed", 25, 'bold', 'italic'))
        else:
            canvas.itemconfig(circle_id, outline="", width=2)
            label.config(font=("Roboto Condensed", 25, 'normal', 'roman'))


    def on_click_circle(event):
        update_selection()

    # Bind events
    canvas.bind("<Motion>", hover_motion)
    canvas.bind("<Button-1>", on_select)
    
    def sublabel_on_enter(event):
        canvas.itemconfig(circle_id, outline="gray", width=4)
        label.config(font=("Roboto Condensed", 25, 'bold', 'italic'))

    def sublabel_on_leave(event):
        canvas.itemconfig(circle_id, outline="", width=2)
        label.config(font=("Roboto Condensed", 25, 'normal', 'roman'))

    def sublabel_on_click(event):
        print('Circle Clicked!')
        on_select()

    label.bind("<Enter>", sublabel_on_enter)
    label.bind("<Leave>", sublabel_on_leave)
    label.bind("<Button-1>", sublabel_on_click)

    if selected:
         update_selection()

    return circle_id
        
             

        




def make_interactive_image(canvas, image, x, y, highlight_color="gray", on_click = None):
    """
    Makes a canvas image interactive with hover highlighting and click action.

    Args:
        canvas: Tkinter Canvas where the image is placed
        img_obj: canvas image object (returned from create_image)
        highlight_color: border color on hover
        on_click: function to call on click
    """
    # Create a rectangle around the image for highlighting
    label_img = tk.Label(canvas, image=image, bd=0, bg="#FFFFFF", highlightthickness=0)
    label_img.place(x=x, y=y, anchor='nw')
    all_labels.append(label_img) #for filters

    def on_enter(event):
        label_img.config(highlightbackground=highlight_color,highlightthickness=2)

    def on_leave(event):
        label_img.config(highlightthickness=0)

    def click(event):
        if on_click:
            on_click()

    # Bind events
    label_img.bind("<Enter>", on_enter)
    label_img.bind("<Leave>", on_leave)
    label_img.bind("<Button-1>", click)
    
    return label_img

def show_text_visibility():
    text_visibility_frame.tkraise()
    

def show_filters():
    filters_frame.tkraise()


def show_contraction_library():
    contraction_library_frame.tkraise()

def show_textvisbility_feed():
    text_visibility_frame.tkraise()
    

def create_display_frame_header(parent, text, anchor, coords=(0,0),font=("Roboto Condensed", 22, 'bold'), bg="#FFFFFF"):
    label = tk.Label(parent, text=text, font=font, bg=bg)
    label.place(x=coords[0], y=coords[1], anchor=anchor)
    all_labels.append(label) #for filters
    
    line_canvas = tk.Canvas(parent, height=2, bg="white", highlightthickness=0)
    line_canvas.place(x=10, y=50, width=450, height = 2)
    line_canvas.create_line(0, 1, 440, 1)   # x1, y1, x2, y2
    all_canvases.append(line_canvas) #for filters

    return label, line_canvas

def create_display_frame(parent, rel_fill = (1, 1), bg="#FFFFFF", start_display=False):
    frame = tk.Frame(parent, bg=bg)
    frame.place(relwidth=rel_fill[0], relheight=rel_fill[1])
    all_frames.append(frame) #for filters
    if start_display:
        frame.tkraise()
    return frame

current_mode = "live"

'''
def toggle_braille_selection():
    global current_mode, file_path

    if current_mode == "live":
        current_mode = "braille"
        file_path = "braille_binary.txt"
        braille_selection_box_icon.config(image=braille_selection_box_img_2)
        text_display.config(font=("Cascadia Mono", 20))
    else:
        current_mode = "live"
        file_path = "braille_output.txt"
        braille_selection_box_icon.config(image=braille_selection_box_img)
        text_display.config(font=("Roboto Condensed", 14))

    update_live_feed(force_full_refresh=True)
    '''

translations = {
    "000000": "⠀",  # U+2800
    "000001": "⠠",  # U+2820
    "000010": "⠐",  # U+2810
    "000011": "⠰",  # U+2830
    "000100": "⠈",  # U+2808
    "000101": "⠨",  # U+2828
    "000110": "⠘",  # U+2818
    "000111": "⠸",  # U+2838

    "001000": "⠄",  # U+2804
    "001001": "⠤",  # U+2824
    "001010": "⠔",  # U+2814
    "001011": "⠴",  # U+2834
    "001100": "⠌",  # U+280C
    "001101": "⠬",  # U+282C    
    "001110": "⠜",  # U+281C
    "001111": "⠼",  # U+283C

    "010000": "⠂",  # U+2802
    "010001": "⠢",  # U+2822
    "010010": "⠒",  # U+2812
    "010011": "⠲",  # U+2832
    "010100": "⠊",  # U+280A
    "010101": "⠪",  # U+282A
    "010110": "⠚",  # U+281A
    "010111": "⠺",  # U+283A

    "011000": "⠆",  # U+2806
    "011001": "⠦",  # U+2826
    "011010": "⠖",  # U+2816
    "011011": "⠶",  # U+2836
    "011100": "⠎",  # U+280E
    "011101": "⠮",  # U+282E
    "011110": "⠞",  # U+281E
    "011111": "⠾",  # U+283E

    "100000": "⠁",  # U+2801
    "100001": "⠡",  # U+2821
    "100010": "⠑",  # U+2811
    "100011": "⠱",  # U+2831
    "100100": "⠉",  # U+2809
    "100101": "⠩",  # U+2829
    "100110": "⠙",  # U+2819
    "100111": "⠹",  # U+2839

    "101000": "⠅",  # U+2805
    "101001": "⠥",  # U+2825
    "101010": "⠕",  # U+2815
    "101011": "⠵",  # U+2835
    "101100": "⠍",  # U+280D
    "101101": "⠭",  # U+282D
    "101110": "⠝",  # U+281D
    "101111": "⠽",  # U+283D

    "110000": "⠃",  # U+2803
    "110001": "⠣",  # U+2823
    "110010": "⠓",  # U+2813
    "110011": "⠳",  # U+2833
    "110100": "⠋",  # U+280B
    "110101": "⠫",  # U+282B
    "110110": "⠛",  # U+281B
    "110111": "⠻",  # U+283B

    "111000": "⠇",  # U+2807
    "111001": "⠧",  # U+2827
    "111010": "⠗",  # U+2817
    "111011": "⠷",  # U+2837
    "111100": "⠏",  # U+280F
    "111101": "⠯",  # U+282F
    "111110": "⠟",  # U+281F
    "111111": "⠿",  # U+283F
}

########TITLE/HEADER FORMATTING###########
title_header_canvas = tk.Canvas(root, width=1035, height=110, background="#eeeeee", highlightthickness=0, relief="solid", bd=2)
title_header_canvas.place(x=5, y=5, anchor="nw")

title = create_label(root, 'nw', txt="PERK Brailler Digital Interface",  font_txt="Roboto Condensed", font_size=37, bold='bold', italic='roman', backround='#eeeeee', location=(50, 30))

perk_braille_img = load_img("EPICS BCI Code\\Images\\PERK_Braille_Image.png", size=(302,110))
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

#######################################################
#Creating images and canvas for triangle selection box
######################################################
triangle_image_1 = load_img("EPICS BCI Code/Images/triangles_icon.png", size=(60,115))
triangle_image_2 = load_img("EPICS BCI Code/Images/triangles_icon_flipped.png", size=(60,115))

triangle_canvas, triangle_img_obj = create_image_canvas(root, 60, 115, 0, 0, 'nw', triangle_image_1, location=(150, 230))

triangle_buttons = []  # global list of all triangle buttons

########################################################
#Settings Section
###################################################

settings_image = load_img("EPICS BCI Code/Images/settings_icon.png", size=(113,100))
settings_icon, settings_img_obj = create_image_canvas(root, 113, 100, 0, 0, 'nw', settings_image, location=(50, 130))
label_sub_title_1 = create_label(root, 'w', txt="Settings",  font_txt="Roboto Condensed", font_size=25, bold='normal', italic='roman', backround='white', location=(165, 180))
settings_circle = create_interactive_icon(settings_icon, label_sub_title_1, (54, 49), 41)

# load all the images, but don't show
filter_images = {
    "default": load_img("EPICS BCI Code/Images/circles_icon1.png", size=(45,160)),
    "inverted": load_img("EPICS BCI Code/Images/circles_icon2.png", size=(45,160)),
}

# make my preview canvas
preview_canvas, canvas_img_obj = create_image_canvas(
    filters_frame,
    45, 160, 0, 0, "nw", filter_images["default"]
)
preview_canvas.place(x=15, y=68)


def default_filter_load():
    for lbl in all_labels:
        lbl.config(fg="black", bg="white")
    for btn in all_buttons:
        btn.config(bg="white", fg="black", activebackground="white")
    for fr in all_frames:
        fr.config(bg="white")
    '''for cnv in all_canvases:
        for item in cnv.find_all():
            item_type = cnv.type(item)
            if item_type in ("rectangle", "oval", "polygon", "line"):
                cnv.itemconfig(item, fill="black")'''

def grayscale_filter_load():
    #frames
    for fr in all_frames:
        fr.config(bg="#DDDDDD")
    #labels
    for lbl in all_labels:
        lbl.config(fg="#777777")
    #buttons
    for btn in all_buttons:
        btn.config(bg="#E0E0E0", fg="#888888")
    #canvases
    '''for cnv in all_canvases:
        if getattr(cnv, "is_ui_canvas", False):
            continue
        for item in cnv.find_all():
            if cnv.type(item) in ("rectangle", "oval", "polygon", "line"):
                cnv.itemconfig(item, fill="#888888")'''

def inverted_filter_load():
    for lbl in all_labels:
        try:
            lbl.config(fg="white", bg="black")
        except tk.TclError:
            pass  # some widgets may not support fg/bg
    for btn in all_buttons:
        try:
            btn.config(fg="white", bg="black", activebackground="#333333")
        except tk.TclError:
            pass
    for fr in all_frames:
        try:
            fr.config(bg="#222222")
        except tk.TclError:
            pass
    '''for cnv in all_canvases:
        try:
            cnv.config(bg="#222222")
        except tk.TclError:
            pass

        for item in cnv.find_all():
            item_type = cnv.type(item)
            if item_type in ("rectangle", "oval", "polygon", "line"):
                cnv.itemconfig(item, fill="#555555")  # dark gray shapes
            elif item_type == "image":
                # Invert the original image
                if hasattr(cnv, "original_images") and item in cnv.original_images:
                    pil_img = cnv.original_images[item]
                    inverted_img = ImageOps.invert(pil_img.convert("RGB"))
                    tk_img = ImageTk.PhotoImage(inverted_img)
                    cnv.itemconfig(item, image=tk_img)
                    # Store reference to prevent garbage collection
                    if not hasattr(cnv, "tk_images"):
                        cnv.tk_images = {}
                    cnv.tk_images[item] = tk_img'''
                    

def inverted_grayscale_filter_load():
    #stuff
    return

########################################################
#Default Section
###################################################
default_image = filter_images["default"]
default_label =  create_label(filters_frame, 'w', txt="Default",  font_txt="Roboto Condensed", font_size=25, bold='normal', italic='roman', backround='white', location=(60,90))
default_circle = create_circle_button(preview_canvas, (20,23), 12, default_label, canvas_img_obj, default_image, selected=True, on_select=default_filter_load)

########################################################
#Grayscale Section
###################################################
grayscale_image = filter_images["grayscale"]
grayscale_label = create_label(filters_frame, 'w', txt="Grayscale", font_txt="Roboto Condensed", font_size=25, bold='normal', italic='roman', backround='white', location=(60, 130))
grayscale_circle = create_circle_button(preview_canvas, (20, 65.4), 12, grayscale_label, canvas_img_obj, grayscale_image, selected=False, on_select=grayscale_filter_load)

########################################################
#Inverted Section
###################################################
inverted_image = filter_images["inverted"]
inverted_label =  create_label(filters_frame, 'w', txt="Inverted",  font_txt="Roboto Condensed", font_size=25, bold='normal', italic='roman', backround='white', location=(60,170))
inverted_circle = create_circle_button(preview_canvas, (20, 107.25), 12, inverted_label, canvas_img_obj, inverted_image, selected=False, on_select=inverted_filter_load)

########################################################
#Inverted Grayscale Section
###################################################
inverted_grayscale_image= filter_images["inverted_grayscale"]
inverted_grayscale_label =  create_label(filters_frame, 'w', txt="Inverted Grayscale",  font_txt="Roboto Condensed", font_size=25, bold='normal', italic='roman', backround='white', location=(60,210))
inverted_grayscale_circle = create_circle_button(preview_canvas, (20, 145), 12, inverted_grayscale_label, canvas_img_obj, inverted_grayscale_image, selected=False, on_select=inverted_grayscale_filter_load)

######################################################################
#Device Management Section
######################################################################

home_image = load_img("EPICS BCI Code/Images/Home_icon.png", size=(105,110))
home_icon, home_img_obj = create_image_canvas(root, 105, 110, 0, 0, 'center', home_image, location=(100, 440))
label_sub_title_2 = create_label(root, 'w', txt="Device Management",  font_txt="Roboto Condensed", font_size=25, bold='normal', italic='roman', backround='white', location=(165, 437))
home_circle = create_interactive_icon(home_icon, label_sub_title_2, (52, 54), 41)

######################################################################
#Filters Button
#################################################################
'''label_textvisibility = create_label(root, 'w', txt="Text/Visibility",  font_txt="Roboto Condensed", font_size=20, bold='bold', italic='roman', backround='white', location=(224, 256))
triangle_textvisibility_coords = (12, 9, 12, 46, 48, 28)

triangle_txtvis = create_triangle_button(
    triangle_canvas, triangle_textvisibility_coords, label_textvisibility, img_obj=triangle_img_obj, 
    img_on_click={"True": triangle_image_1, "False": triangle_image_2}, selected=True,
    on_select= show_text_visibility)'''
label_filters = create_label(root, 'w', txt="Filters",  font_txt="Roboto Condensed", font_size=20, bold='bold', italic='roman', backround='white', location=(224, 256))
triangle_filters_coords = (12, 9, 12, 46, 48, 28)

triangle_filters = create_triangle_button(
    triangle_canvas, triangle_filters_coords, label_filters, img_obj=triangle_img_obj, 
    img_on_click={"True": triangle_image_1, "False": triangle_image_2}, selected=True,
    on_select= show_filters)

########################################################
#Text Visibility Button
#################################################################
label_textvisibility = create_label(root, 'w', txt="Text/Visibility",  font_txt="Roboto Condensed", font_size=20, bold='normal', italic='roman', backround='white', location=(224, 317))
triangle_textvisibility_coords = (12, 68, 12, 105, 48, 87)


triangle_txtvis = create_triangle_button(
    triangle_canvas, triangle_textvisibility_coords, label_textvisibility, img_obj=triangle_img_obj, 
    img_on_click={"True": triangle_image_2, "False": triangle_image_1}, selected=False, 
    on_select= show_text_visibility)




root.mainloop()