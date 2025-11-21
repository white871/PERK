import tkinter as tk
from tkinter import filedialog
import tkinter.font as tkfont
from PIL import Image, ImageTk
import random

root = tk.Tk()


# Set geometry
root.geometry("1050x700")
root.resizable(False, False)
root.configure(bg="#FFFFFF")

file_path = "brailler_output.txt"

#################################################
#Functions we reuse a whole lot
#################################################
def load_img(path, size=(80,80)):
    img = Image.open(path)
    img = img.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

def create_label(root, anchr, txt=None, img=None, font_txt=None, font_size=None, bold=None, italic=None, backround=None, bd_width=None, location=(0, 0)):
    if img==None:
        label = tk.Label(root, text=txt, font=(font_txt, font_size, bold, italic), bg=backround)
    elif txt==None:
        label = tk.Label(root, image=img, borderwidth=bd_width)
    label.place(x=location[0], y=location[1], anchor = anchr)
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

def show_live_feed():
    live_feed_frame.tkraise()

def show_contraction_library():
    contraction_library_frame.tkraise()

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

current_mode = "live"

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
title_canvas = tk.Canvas(root, width=1026, height=100, bg="#eeeeee", highlightthickness=2, highlightbackground="black")
title_canvas.place(x=10, y=10)

title = create_label(title_canvas, 'nw', txt="PERK Brailler Digital Interface",  font_txt="Roboto Condensed", font_size=37, bold='bold', italic='roman', backround='#eeeeee', location=(50, 25))

perk_braille_img = load_img("EPICS BCI Code/PERK_braille_Image_grey.png", size=(272,96))
perk_logo = create_label(title_canvas, 'nw', img=perk_braille_img, bd_width=0, location=(695, 5))
########################################
#Creating Frames
#######################################

display_container = tk.Frame(root, bg="#FFFFFF", bd=3, relief="solid")
display_container.place(x=530, y=140, width=470, height=500)

live_feed_frame = create_display_frame(display_container, start_display=True)
live_feed_label, line_canvas =  create_display_frame_header(live_feed_frame, "Live Text Feed", 'n', coords=(470/2, 10))

contraction_library_frame = create_display_frame(display_container)
contraction_library_label, line_canvas =  create_display_frame_header(contraction_library_frame, "Contraction Library", 'n', coords=(470/2, 10))

#######################################################
#Creating images and canvas for triangle selection box
######################################################
triangle_image_1 = load_img("EPICS BCI Code/triangles_icon.png", size=(60,115))
triangle_image_2 = load_img("EPICS BCI Code/triangles_icon_flipped.png", size=(60,115))

triangle_canvas, triangle_img_obj = create_image_canvas(root, 60, 115, 0, 0, 'nw', triangle_image_1, location=(150, 230))

triangle_buttons = []  # global list of all triangle buttons

########################################################
#Live Feed Button
#################################################################
label_live_text_feed = create_label(root, 'w', txt="Live Text Feed",  font_txt="Roboto Condensed", font_size=20, bold='bold', italic='roman', backround='white', location=(224, 256))
triangle_live_feed_coords = (12, 9, 12, 46, 48, 28)

triangle_live_feed = create_triangle_button(
    triangle_canvas, triangle_live_feed_coords, label_live_text_feed, img_obj=triangle_img_obj, 
    img_on_click={"True": triangle_image_1, "False": triangle_image_2}, selected=True,
    on_select= show_live_feed)

########################################################
#Contraction Library Button
#################################################################
triangle_contraction_library_coords = (12, 68, 12, 105, 48, 87)
label_contraction_library = create_label(root, 'w', txt="Contraction Library",  font_txt="Roboto Condensed", font_size=20, bold='normal', italic='roman', backround='white', location=(224, 317))

triangle_contraction_library = create_triangle_button(
    triangle_canvas, triangle_contraction_library_coords, label_contraction_library, img_obj=triangle_img_obj, 
    img_on_click={"True": triangle_image_2, "False": triangle_image_1}, selected=False, 
    on_select= show_contraction_library)

###############################################
#Brailler COnnected Section
###################################################

Brailler_connected_image = load_img("EPICS BCI Code/Brailler_Connected_Icon.png", size=(100,100))
brailler_icon, brailler_img_obj = create_image_canvas(root, 100, 100, 0, 0, 'nw', Brailler_connected_image, location=(50, 130))
label_sub_title_1 = create_label(root, 'w', txt="Brailler Connected",  font_txt="Roboto Condensed", font_size=25, bold='normal', italic='roman', backround='white', location=(165, 180))
brailler_circle = create_interactive_icon(brailler_icon, label_sub_title_1, (49, 52), 41)


online_dot = load_img("EPICS BCI Code/green_circle.png", size=(40,40))
dot_icon = create_label(root, 'w', img=online_dot, bd_width=0, location=(440, 180))


######################################################################
#Device Management Section
######################################################################

home_image = load_img("EPICS BCI Code/Home_icon.png", size=(105,110))
home_icon, home_img_obj = create_image_canvas(root, 105, 110, 0, 0, 'center', home_image, location=(100, 440))
label_sub_title_2 = create_label(root, 'w', txt="Device Management",  font_txt="Roboto Condensed", font_size=25, bold='normal', italic='roman', backround='white', location=(165, 437))
home_circle = create_interactive_icon(home_icon, label_sub_title_2, (52, 54), 41)

#############################################################
#Settings Section
##############################################################
settings_image = load_img("EPICS BCI Code/settings_icon.png", size=(113,100))
settings_icon, settings_img_obj = create_image_canvas(root, 113, 100, 0, 0, 'center', settings_image, location=(100, 590))
label_sub_title_3 = create_label(root, 'w', txt="Settings",  font_txt="Roboto Condensed", font_size=25, bold='normal', italic='roman', backround='white', location=(165, 587))
settings_circle = create_interactive_icon(settings_icon, label_sub_title_3, (54, 49), 41)


##############################################
#DIsplay box when Live Feed Button Selected
###############################################

#Create text box for live display
text_frame_height = 500-72-60
text_frame = tk.Frame(live_feed_frame, bg="white")
text_frame.place(x=10, y=60, width=450, height=text_frame_height)

#Scrollbar first (right side)
scrollbar = tk.Scrollbar(text_frame, orient="vertical")
scrollbar.pack(side="right", fill="y", padx=(0, 6))

# Text box second (takes remaining space)
text_display = tk.Text(
    text_frame,
    wrap="word",
    font=("Roboto Condensed", 14),
    bg="white",
    bd=0,
    highlightthickness=0,
    relief="flat",
    pady=5
)
text_display.pack(side="left", fill="both", expand=True)

# Link scroll
scrollbar.config(command=text_display.yview)
text_display.config(yscrollcommand=scrollbar.set)


live_text = ""
last_len= 0

text_file_path = "brailler_output.txt"
braille_file_path = "braille_binary.txt"

def simulate_brailler_output():
    """Simulate text arriving from Brailler device."""
    char = random.choice(["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"," ", " ", " "," ", " "])

    # Append to the file
    with open(text_file_path, "a", encoding="utf-8") as f:
        f.write(char)

    # Schedule next write
    root.after(150, simulate_brailler_output)

simulate_brailler_output()


def simulate_braille_binary_output():
    """Simulate Braille binary sequences using only valid codes in the translations dictionary."""
    if not translations:
        return  # safety check

    # Pick a random valid braille code from the dictionary keys
    binary_seq = random.choice(list(translations.keys()))
    symbol = translations[binary_seq]

    # Append it to the file with a space (to separate sequences)
    with open(braille_file_path, "a", encoding="utf-8") as f:
        f.write(symbol)

    # Schedule next write
    root.after(150, simulate_braille_binary_output)

# Start simulating
simulate_braille_binary_output()


def update_live_feed(force_full_refresh=False):
    """Continuously update the text display."""
    global last_len, current_mode
   
    # Choose file depending on mode
    if current_mode == "live":
        file_path = "brailler_output.txt"
    elif current_mode == "braille":
        file_path = "braille_binary.txt"


    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
    except FileNotFoundError:
        content = ""

    new_len = len(content)

    
    if new_len > last_len or force_full_refresh:
        new_text = content[last_len:new_len] if not force_full_refresh else content
        if force_full_refresh:
            text_display.delete("1.0", tk.END)
        text_display.insert(tk.END, new_text)

    last_len = new_len
    

    #Determines if user is at the bottom of the page, and keeps them there if so
    bottom = text_display.yview()[1]
    if bottom >= 0.92:   # user is already at bottom
        text_display.see(tk.END)

    
    # Schedule next update after 150 ms
    root.after(500, update_live_feed)

update_live_feed()  # Start the loop

#Buttons at the bottom of the frame

def new_file_action():
    #Erasing everything on the 
    with open(braille_file_path, "w") as f:
        f.write("")
    
    with open(text_file_path, "w") as f:
        f.write("")

    text_display.config(state="normal")
    text_display.delete("1.0", tk.END)

    global last_len
    last_len = 0

def export_file_action():
    try:
        # Pick save location
        export_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if not export_path:   # user canceled
            return

        # Read current brailler file
        with open(file_path, "r", encoding="utf-8") as f:
            data = f.read()

        # Write to exported file
        with open(export_path, "w", encoding="utf-8") as f:
            f.write(data)

        print("Export complete →", export_path)

    except Exception as e:
        print("Export failed:", e)

button_canvas = tk.Canvas(live_feed_frame, width=464, height=72, bg="#FFFFFF", highlightthickness=0)
button_canvas.place(x=0, y=422)

new_file_img = load_img("EPICS BCI Code/New_file_button.png", size=(120, 35))
new_file_icon = make_interactive_image(button_canvas, new_file_img, 20, 18, on_click=new_file_action)

export_text_file_img = load_img("EPICS BCI Code/export_text_file_button.png", size=(161, 37))
export_text_file_icon = make_interactive_image(button_canvas, export_text_file_img, 155, 15, on_click=export_file_action)


braille_selection_box_img = load_img("EPICS BCI Code/braille_selection_box_unselected.png", size=(113, 39))
braille_selection_box_img_2 = load_img("EPICS BCI Code/braille_selection_box_selected.png", size=(105, 42))
braille_selection_box_icon = make_interactive_image(button_canvas, braille_selection_box_img, 330, 15, on_click=toggle_braille_selection)



########################################################
#DIsplay box when contraction library Button Selected
#####################################################
# Contraction Library placeholder text
placeholder_text = "This function is currently being implemented."

# Create a frame for the message inside the contraction library frame
placeholder_label = tk.Label(
    contraction_library_frame,
    text=placeholder_text,
    font=("Roboto Condensed", 16, 'italic'),
    bg="white",
    wraplength=440,   # wrap text nicely inside the frame
    justify="left"
)
placeholder_label.place(x=15, y=80)  # Position below the header



root.mainloop()


