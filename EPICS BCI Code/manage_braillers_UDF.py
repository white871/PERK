import tkinter as tk
from tkinter import filedialog
import tkinter.font as tkfont
from PIL import Image, ImageTk, ImageOps
import random
from utility_functions import load_img, create_label, create_inverted_label, create_image_canvas, create_triangle_button, create_interactive_icon, create_display_frame_header, create_display_frame, make_interactive_image

def load_manage_braillers_page(root, app):
    
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
        "Ayona's Brailler", "Felix's Brailler", "Joe's Brailler", 
        "Mary's Brailler", "Jane's Brailler", "Josh's Brailler", 
        "Chloe's Brailler", "Ashley's Brailler", "Gina's Brailler"
        ]

    # Main window
    root.configure(bg="#FFFFFF")

    # Header
    title_header_canvas = tk.Canvas(root, width=1035, height=110, background="#eeeeee", highlightthickness=0, relief="solid", bd=2)
    title_header_canvas.place(x=5, y=5, anchor="nw")

    title = create_label(root, 'nw', txt="PERK Brailler Digital Interface",  font_txt="Roboto Condensed", font_size=37, bold='bold', italic='roman', backround='#eeeeee', location=(50, 30))

    perk_braille_img = load_img("EPICS BCI Code\\Images\\PERK_braille_Image_grey.png", size=(302,110))
    perk_logo = create_label(root, 'nw', img=perk_braille_img, bd_width=0, location=(695, 6))

    # Manage Braillers row
    home_image = load_img("EPICS BCI Code\\Images\\Home_icon.png", size=(95, 100))
    home_icon, home_img_obj = create_image_canvas(root, 95, 100, 0, 0, 'center', home_image, location=(90, 185))
    Braillers_logo = create_label(root, anchr="nw", txt="Manage Braillers",font_txt="Roboto Condensed",font_size=25,bold="bold",backround="white",location=(140, 165))
    home_circle = create_interactive_icon(home_icon, Braillers_logo, (47, 50), 38, on_select=lambda: on_brailler_click())


    pair_all_image = load_img("EPICS BCI Code\\Images\\pair_all_button.png", size=(105, 44))
    pair_all_button = make_interactive_image(root, pair_all_image, 890, 160, on_click=None)

    
    # Brailler list 
    start_x = 110
    start_y = 250
    x_gap = 350
    y_gap = 60
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
    set_brailler_status("Mary's Brailler", False)
    set_brailler_status("Jane's Brailler", True)
    set_brailler_status("Josh's Brailler", False)
    set_brailler_status("Chloe's Brailler", True)
    set_brailler_status("Ashley's Brailler", False)
    set_brailler_status("Gina's Brailler", True)

    # Bottom actions
    bluetooth_image = load_img("EPICS BCI Code\\Images\\Bluetooth_icon.png", size=(110, 98))
    bluetooth_icon, bluetooth_img_obj = create_image_canvas(root, 110, 98, 0, 0, 'center', bluetooth_image, location=(90, 620))
    pairing_label = create_label(root, anchr="sw",txt="Start Pairing Process",font_txt="Roboto Condensed",font_size=25,bold="normal",backround="white",location=(140, 640))
    bluetooth_circle = create_interactive_icon(bluetooth_icon, pairing_label, (52, 50), 38, on_select=None)

    gear_icon = load_img("EPICS BCI Code\\Images\\settings_icon.png", size=(75, 75))
    gear_label = create_label(root,anchr="se",img=gear_icon,location=(855, 650))

    settings_label = create_label(root,anchr="se",txt="Settings",font_txt="Roboto Condensed",font_size=25,bold="normal",backround="white",location=(970, 640))

    #Brailler popup stuff
    current_brailler_label=None

    brailler_popup=create_display_frame(root, rel_fill=(0,0),bg="#eeeeee",start_display=False)

    brailler_popup.place(x=50, y=530, width=950, height=50)
    brailler_popup.place_forget()

    brailler_popup.config(highlightbackground="black", highlightthickness=1)

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
