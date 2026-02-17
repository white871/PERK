import tkinter as tk
import math
import tkinter.font as tkfont
from PIL import Image, ImageTk

#################################################
#Functions we reuse a whole lot
#################################################
def load_img(path, size=(80,80)):
    img = Image.open(path)
    img = img.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

def create_label(
    root, anchr,
    txt=None,
    img=None,
    font_txt="Roboto Condensed",
    font_size=16,
    bold="normal",
    italic="roman",
    backround="white",
    bd_width=0,
    location=(0, 0)):

    if img is None:
        label = tk.Label(
            root,
            text=txt,
            font=(font_txt, font_size, bold, italic),
            bg=backround
        )
    else:
        label = tk.Label(
            root,
            image=img,
            borderwidth=bd_width,
            bg=backround
        )

    label.place(x=location[0], y=location[1], anchor=anchr)
    return label


def create_image_canvas(root, wdth, hght, highlightthick, border, anchr, img, location=(0, 0)):
    canvas = tk.Canvas(root, width=wdth, height=hght, highlightthickness=highlightthick, bd=border)
    canvas.place(x=location[0], y=location[1], anchor=anchr)
    img_obj = canvas.create_image(0, 0, anchor='nw', image=img)
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

def create_display_frame_header(parent, text, anchor, coords=(0,0),font=("Roboto Condensed", 22, 'bold'), bg="#FFFFFF"):
    label = tk.Label(parent, text=text, font=font, bg=bg)
    label.place(x=coords[0], y=coords[1], anchor=anchor)
    
    line_canvas = tk.Canvas(parent, height=2, bg="white", highlightthickness=0)
    line_canvas.place(x=10, y=50, width=450, height = 2)
    line_canvas.create_line(0, 1, 440, 1)   # x1, y1, x2, y2

    return label, line_canvas

def create_display_frame(parent, rel_fill = (1, 1), bg="#FFFFFF", start_display=False):
    frame = tk.Frame(parent, bg=bg)
    frame.place(relwidth=rel_fill[0], relheight=rel_fill[1])
    if start_display:
        frame.tkraise()
    return frame

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

    brailler_popup.place(x=50, y=540, width=950, height=50)
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
root = tk.Tk()
root.geometry("1050x700")
root.resizable(False, False)
root.configure(bg="#FFFFFF")

# Header
title_header_canvas = tk.Canvas(root, width=1035, height=110, background="#eeeeee", highlightthickness=0, relief="solid", bd=2)
title_header_canvas.place(x=5, y=5, anchor="nw")

title = create_label(root, 'nw', txt="PERK Brailler Digital Interface",  font_txt="Roboto Condensed", font_size=37, bold='bold', italic='roman', backround='#eeeeee', location=(50, 30))

perk_braille_img = load_img("EPICS BCI Code\\Images\\PERK_braille_Image_grey.png", size=(302,110))
perk_logo = create_label(root, 'nw', img=perk_braille_img, bd_width=0, location=(695, 6))

# Manage Braillers row
home_icon = load_img("EPICS BCI Code\\Images\\Home_icon.png", size=(75, 75))
home_image = create_label(
root,
anchr="nw",
img=home_icon,
location=(30, 150)
)

Braillers_logo = create_label(
    root,
    anchr="nw",
    txt="Manage Braillers",
    font_txt="Roboto Condensed",
    font_size=25,
    bold="normal",
    backround="white",
    location=(105, 170)
)

pair_button = create_label(
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
#start_x = 110
#start_y = 250
#x_gap = 350
#y_gap = 60
#brailler_status_dots = {}
#STATUS_RADIUS = 6
#STATUS_GREEN = "#93c47d"
#STATUS_RED = "#e06666"
#status_dots = {}


#for i, name in enumerate(braillers):
#    row = i // 3
#    col = i % 3

#    x = start_x + col * x_gap
#    y = start_y + row * y_gap

#    lbl = create_label(
#        root,
#        anchr="nw",
#        txt=name,
#        font_txt="Roboto Condensed",
#        font_size=18,
#        bold="normal",
#        backround="white",
#        location=(x, y)
#    )

#    lbl.is_bold = False
#    lbl.config(cursor="hand2")
#    lbl.bind("<Button-1>", lambda e, l=lbl, n=name: on_brailler_click(l, n))

#    dot_canvas = tk.Canvas(
#        root,
#        width=STATUS_RADIUS * 2,
#        height=STATUS_RADIUS * 2,
#       bg="white",
#        highlightthickness=0
#    )
#    dot_canvas.place(x=x - 20, y=y + 5, anchor="nw")  

#    dot = dot_canvas.create_oval(
#        0, 0,
#        STATUS_RADIUS * 2,
#        STATUS_RADIUS * 2,
#        outline=""
#    )

#    brailler_status_dots[name] = (dot_canvas, dot)

start_y = 250
bottom_limit = 550   # where bottom buttons start
available_height = bottom_limit - start_y

max_columns = 3
total_braillers = len(braillers)


total_rows = math.ceil(total_braillers / max_columns)

row_height = available_height / total_rows   # THIS is the key

window_width = 1250
left_margin = 110
right_margin = 110
usable_width = window_width - left_margin - right_margin
column_width = usable_width / max_columns

brailler_status_dots = {}
STATUS_RADIUS = 6
STATUS_GREEN = "#93c47d"
STATUS_RED = "#e06666"

for i, name in enumerate(braillers):
    row = i // max_columns
    col = i % max_columns

    x = left_margin + col * column_width
    y = start_y + row * row_height

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
set_brailler_status("Mary's Brailler", False)
set_brailler_status("Jane's Brailler", True)
set_brailler_status("Josh's Brailler", False)
set_brailler_status("Chloe's Brailler", True)
set_brailler_status("Ashley's Brailler", False)
set_brailler_status("Gina's Brailler", True)

#Bottom actions
bt_icon = load_img("EPICS BCI Code\Images\Bluetooth_icon.png", size=(75, 75))
bt_label = create_label(
    root,
    anchr="sw",
    img=bt_icon,
    location=(30, 670)
)

pairing_label = create_label(
    root,
    anchr="sw",
    txt="Start Pairing Process",
    font_txt="Roboto Condensed",
    font_size=25,
    bold="normal",
    backround="white",
    location=(105, 660)
)

gear_icon = load_img("EPICS BCI Code\Images\settings_icon.png", size=(75, 75))
gear_label = create_label(
    root,
    anchr="se",
    img=gear_icon,
    location=(855, 670)
)

settings_label = create_label(
    root,
    anchr="se",
    txt="Settings",
    font_txt="Roboto Condensed",
    font_size=25,
    bold="normal",
    backround="white",
    location=(970, 660)
)

#Brailler popup stuff
current_brailler_label=None

brailler_popup=create_display_frame(
    root, 
    rel_fill=(0,0),
    bg="#eeeeee",
    start_display=False
)

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
