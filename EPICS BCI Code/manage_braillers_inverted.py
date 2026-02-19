import tkinter as tk
from tkinter import filedialog
import tkinter.font as tkfont
from PIL import Image, ImageTk, ImageOps
import random
import math
from utility_functions import load_img, create_label, create_inverted_label, create_image_canvas, create_interactive_icon, create_display_frame, make_interactive_image

def load_manage_braillers_page_inverted(root, app):
    current_brailler_label = None
    current_brailler_name = None

    #Brailler popup stuff
    brailler_popup=create_display_frame(
        root, 
        rel_fill=(0,0),
        bg="#000000",
        start_display=False
    )

    brailler_popup.config(
        highlightbackground="white",
        highlightthickness=1
    )

    popup_buttons=[]
    button_names= "Live Feed", "Disconnect Brailler", "Pair Device", "Rename Device"
    x_positions=[60, 250, 530, 730]


    def on_brailler_click(label, name):
        nonlocal current_brailler_label, current_brailler_name

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
        current_brailler_name = current_brailler_label["text"]

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
    root.configure(bg="#000000")

    # Header
    title_header_canvas = tk.Canvas(root, width=1035, height=110, background="#000000", highlightbackground="#FFFFFF", highlightthickness=1, relief="solid", bd=2)
    title_header_canvas.place(x=5, y=5, anchor="nw")

    title = create_inverted_label(root, 'nw', txt="PERK Brailler Digital Interface",  font_txt="Roboto Condensed", font_size=37, bold='bold', italic='roman', backround='#000000', location=(50, 30))

    perk_braille_img = load_img("EPICS BCI Code\\Images\\Inverted Images\\PERK_Braille_Image_inverted.png", size=(302,110))
    perk_logo = create_label(root, 'nw', img=perk_braille_img, bd_width=0, location=(695, 6))

    # Manage Braillers row
    home_image = load_img("EPICS BCI Code\\Images\\Inverted Images\\Home_icon_inverted.png", size=(95, 100))
    home_icon, home_img_obj = create_image_canvas(root, 95, 100, 0, 0, 'center', home_image, location=(90, 185))
    Braillers_logo = create_inverted_label(root, anchr="nw", txt="Manage Braillers",font_txt="Roboto Condensed",font_size=25,bold="bold",backround="black",location=(140, 165))

    pair_all_image = load_img("EPICS BCI Code\\Images\\Inverted Images\\pair_all_button_inverted.png", size=(105, 44))
    pair_all_button = make_interactive_image(root, pair_all_image, 890, 160, on_click=None)

        
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

        lbl = create_inverted_label(
            root,
            anchr="nw",
            txt=name,
            font_txt="Roboto Condensed",
            font_size=18,
            bold="normal",
            backround="black",
            location=(x, y)
        )

        lbl.is_bold = False
        lbl.config(cursor="hand2")
        lbl.bind("<Button-1>", lambda e, l=lbl, n=name: on_brailler_click(l, n))

        dot_canvas = tk.Canvas(
            root,
            width=STATUS_RADIUS * 2,
            height=STATUS_RADIUS * 2,
            bg="black",
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

    def on_settings_click():
        app.show_settings()

    # Bottom actions
    bluetooth_image = load_img("EPICS BCI Code\\Images\\Inverted Images\\Bluetooth_icon_inverted.png", size=(110, 98))
    bluetooth_icon, bluetooth_img_obj = create_image_canvas(root, 110, 98, 0, 0, 'center', bluetooth_image, location=(90, 645))
    pairing_label = create_inverted_label(root, anchr="sw",txt="Start Pairing Process",font_txt="Roboto Condensed",font_size=25,bold="normal",backround="black",location=(140, 665))
    bluetooth_circle = create_interactive_icon(bluetooth_icon, pairing_label, (52, 50), 38, True, on_select=None)

    settings_image = load_img("EPICS BCI Code\\Images\\Inverted Images\\settings_icon_inverted.png", size=(105, 97))
    settings_icon, settings_img_obj = create_image_canvas(root, 105, 97, 0, 0, 'center', settings_image, location=(805, 645))
    settings_label = create_inverted_label(root, anchr="se",txt="Settings",font_txt="Roboto Condensed",font_size=25,bold="normal",backround="black",location=(970, 665))
    settings_circle = create_interactive_icon(settings_icon, settings_label, (51, 48), 38, True, on_select=lambda: on_settings_click())

    def on_live_feed_click():
        app.show_text_page_inverted(current_brailler_name)

    def disconnect_brailler():
        set_brailler_status(current_brailler_name, False)

    def pair_brailler():
        set_brailler_status(current_brailler_name, True)

    def rename_device():
         # Create a small popup window
        popup = tk.Toplevel(root)
        popup.title("Rename Device")
        popup.geometry("300x120")
        popup.resizable(False, False)
        popup.grab_set()  # Make it modal

         # Create the entry variable and widget
        entry_var = tk.StringVar()
        entry = tk.Entry(popup, textvariable=entry_var, font=("Roboto Condensed", 14))
        entry.pack(pady=10)
        entry.focus_set()


        def submit_rename():
            nonlocal current_brailler_name
            new_name = entry_var.get().strip()
            if new_name:
                # Update label text
                current_brailler_label.config(text=new_name)
                
                # Update brailler status dictionary
                if current_brailler_name in brailler_status_dots:
                    brailler_status_dots[new_name] = brailler_status_dots.pop(current_brailler_name)
                
                # Update current name reference
                current_brailler_name = new_name

            popup.destroy()

        submit_btn = tk.Button(popup, text="Rename", font=("Roboto Condensed", 12), command=submit_rename)
        submit_btn.pack(pady=5)

    for name, x in zip(button_names, x_positions):
        lbl=create_inverted_label(
            brailler_popup, 
            anchr="nw",
            txt=name, 
            font_txt="Roboto Condensed", 
            font_size=18, 
            bold="normal", 
            backround="#000000",
            location=(x, 5)
            )
        lbl.config(cursor="hand2")
        popup_buttons.append(lbl)

        if name == "Live Feed":
            lbl.bind("<Button-1>", lambda e, f=on_live_feed_click: f())

        if name == "Disconnect Brailler":
            lbl.bind("<Button-1>", lambda e, f=disconnect_brailler: f())

        if name == "Pair Device":
            lbl.bind("<Button-1>", lambda e, f=pair_brailler: f())

        if name == "Rename Device":
            lbl.bind("<Button-1>", lambda e, f=rename_device: f())


    root.mainloop()
