import tkinter as tk
from tkinter import filedialog
import tkinter.font as tkfont
from PIL import Image, ImageTk, ImageOps
import random
from utility_functions import load_img, create_label, create_image_canvas, create_triangle_button, create_interactive_icon, create_display_frame_header, create_display_frame

root = tk.Tk()


# Set geometry
root.geometry("1050x700")
root.resizable(False, False)
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
        "img_on_click": img_on_click,
        "on_select": on_select
    }

    circle_buttons.append(button_state)

    
    def update_selection():
        for btn in circle_buttons:
            if btn["circle"] == circle_id:
                btn["selected"] = True
                btn["label"].config(
                    font=("Roboto Condensed", 25, "bold", "roman")
                )
                if btn["img_obj"] and btn["img_on_click"]:
                    canvas.itemconfig(btn["img_obj"], image=filter_images[btn["img_on_click"][btn["selected"]]]) #WHAT
                if on_select:
                    on_select()
            else:
                btn["selected"] = False
                btn["label"].config(
                    font=("Roboto Condensed", 25, "normal", "roman")
                )
                if btn["img_obj"] and btn["img_on_click"]:
                    canvas.itemconfig(btn["img_obj"], image=filter_images[btn["img_on_click"][btn["selected"]]])

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
    canvas.tag_bind(circle_id, "<Motion>", hover_motion)
    canvas.tag_bind(circle_id, "<Button-1>", on_click_circle)
    
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
    "default": load_img("EPICS BCI Code/Images/circles_icon1.png", size=(39,85)),
    "inverted": load_img("EPICS BCI Code/Images/circles_icon2.png", size=(39,85)),
}
default_image = {
    True: "default",
    False: "inverted"
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
    return

########################################################
#Default Section
###################################################
#default_image = filter_images["default"]
default_image = {True: "default", False: "inverted"}
default_label =  create_label(filters_frame, 'w', txt="Default",  font_txt="Roboto Condensed", font_size=25, bold='normal', italic='roman', backround='white', location=(60,90))
default_circle = create_circle_button(preview_canvas, (20,23), 12, default_label, canvas_img_obj, default_image, selected=True, on_select=default_filter_load)

########################################################
#Inverted Section
###################################################
#inverted_image = filter_images["inverted"]
inverted_image = {"True": "inverted", "False": "default"}
inverted_label =  create_label(filters_frame, 'w', txt="Inverted",  font_txt="Roboto Condensed", font_size=25, bold='normal', italic='roman', backround='white', location=(60,130))
inverted_circle = create_circle_button(preview_canvas, (20, 65.4), 12, inverted_label, canvas_img_obj, inverted_image, selected=False, on_select=inverted_filter_load)

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