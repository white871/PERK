import tkinter as tk
from tkinter import filedialog, messagebox
import tkinter.font as tkfont
from PIL import Image, ImageTk
import random
import json
from utility_functions import load_img, create_label, create_image_canvas, create_triangle_button, create_interactive_icon, make_interactive_image, create_display_frame_header, create_display_frame

root = tk.Tk()
root.geometry("1050x700")
root.resizable(False, False)

root.configure(bg="#FFFFFF")

file_path = "Data\\brailler_output.txt"

current_mode = "live"

def show_live_feed():
    live_feed_frame.tkraise()

def show_contraction_library():
    contraction_library_frame.tkraise()

def toggle_braille_selection():
    global current_mode, file_path

    if current_mode == "live":
        current_mode = "braille"
        file_path = "Data\\braille_binary.txt"
        braille_selection_box_icon.config(image=braille_selection_box_img_2)
        text_display.config(font=("Cascadia Mono", 20))
    else:
        current_mode = "live"
        file_path = "Data\\brailler_output.txt"
        braille_selection_box_icon.config(image=braille_selection_box_img)
        text_display.config(font=("Roboto Condensed", 14))

    update_live_feed(force_full_refresh=True)

translations_path = "EPICS BCI Code\\Data\\translations.txt"

with open(translations_path, "r", encoding="utf-8") as f:
    translations = json.load(f)

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
display_container.place(x=530, y=145, width=470, height=500)

live_feed_frame = create_display_frame(display_container, start_display=True)
live_feed_label, line_canvas =  create_display_frame_header(live_feed_frame, "Live Text Feed", 'n', coords=(470/2, 10))

contraction_library_frame = create_display_frame(display_container)
contraction_library_label, line_canvas =  create_display_frame_header(contraction_library_frame, "Contraction Library", 'n', coords=(470/2, 10))

#######################################################
#Creating images and canvas for triangle selection box
######################################################
triangle_image_1 = load_img("EPICS BCI Code\\Images\\triangles_icon.png", size=(60,115))
triangle_image_2 = load_img("EPICS BCI Code\\Images\\triangles_icon_flipped.png", size=(60,115))

triangle_canvas, triangle_img_obj = create_image_canvas(root, 60, 115, 0, 0, 'nw', triangle_image_1, location=(155, 235))

triangle_buttons = []  # global list of all triangle buttons

########################################################
#Live Feed Button
#################################################################
label_live_text_feed = create_label(root, 'w', txt="Live Text Feed",  font_txt="Roboto Condensed", font_size=20, bold='bold', italic='roman', backround='white', location=(224, 261))
triangle_live_feed_coords = (12, 9, 12, 46, 48, 28)

triangle_live_feed = create_triangle_button(
    triangle_canvas, triangle_live_feed_coords, label_live_text_feed, img_obj=triangle_img_obj, 
    img_on_click={"True": triangle_image_1, "False": triangle_image_2}, selected=True,
    on_select= show_live_feed)

########################################################
#Contraction Library Button
#################################################################
triangle_contraction_library_coords = (12, 68, 12, 105, 48, 87)
label_contraction_library = create_label(root, 'w', txt="Contraction Library",  font_txt="Roboto Condensed", font_size=20, bold='normal', italic='roman', backround='white', location=(224, 322))

triangle_contraction_library = create_triangle_button(
    triangle_canvas, triangle_contraction_library_coords, label_contraction_library, img_obj=triangle_img_obj, 
    img_on_click={"True": triangle_image_2, "False": triangle_image_1}, selected=False, 
    on_select= show_contraction_library)

###############################################
#Brailler COnnected Section
###################################################
Brailler_connected_image = load_img("EPICS BCI Code\\Images\\Brailler_Connected_Icon.png", size=(100,100))
brailler_icon, brailler_img_obj = create_image_canvas(root, 100, 100, 0, 0, 'nw', Brailler_connected_image, location=(50, 135))
label_sub_title_1 = create_label(root, 'w', txt="Brailler Connected",  font_txt="Roboto Condensed", font_size=25, bold='bold', italic='roman', backround='white', location=(165, 185))

online_dot = load_img("EPICS BCI Code\\Images\\green_circle.png", size=(40,40))
dot_icon = create_label(root, 'w', img=online_dot, bd_width=0, location=(460, 185))

######################################################################
#Device Management Section
######################################################################
def home_select():
    return

home_image = load_img("EPICS BCI Code\\Images\\Home_icon.png", size=(105,110))
home_icon, home_img_obj = create_image_canvas(root, 105, 110, 0, 0, 'center', home_image, location=(100, 445))
label_sub_title_2 = create_label(root, 'w', txt="Device Management",  font_txt="Roboto Condensed", font_size=25, bold='normal', italic='roman', backround='white', location=(165, 442))
home_circle = create_interactive_icon(home_icon, label_sub_title_2, (52, 54), 41, on_select=lambda: home_select())

#############################################################
#Settings Section
##############################################################
def settings_select():
    return

settings_image = load_img("EPICS BCI Code\\Images\\settings_icon.png", size=(113,100))
settings_icon, settings_img_obj = create_image_canvas(root, 113, 100, 0, 0, 'center', settings_image, location=(100, 595))
label_sub_title_3 = create_label(root, 'w', txt="Settings",  font_txt="Roboto Condensed", font_size=25, bold='normal', italic='roman', backround='white', location=(165, 592))
settings_circle = create_interactive_icon(settings_icon, label_sub_title_3, (54, 49), 41, on_select=lambda: settings_select())

##############################################
#DIsplay box when Live Feed Button Selected
###############################################
#Create text box for live display
text_frame_height = 500-72-60
text_frame = tk.Frame(live_feed_frame, bg="white")
text_frame.place(x=10, y=60, width=450, height=text_frame_height)

#Scrollbar first (right side)
scrollbar = tk.Scrollbar(text_frame, orient="vertical")
scrollbar.pack(side="right", fill="y", padx=(5, 6))

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

text_file_path = "EPICS BCI Code\\Data\\brailler_output.txt"
braille_file_path = "EPICS BCI Code\\Data\\braille_binary.txt"

after_id3 = None

def update_live_feed(force_full_refresh=False):
    """Continuously update the text display."""
    global last_len, current_mode, after_id3

    if not text_display.winfo_exists():
        # Stop the loop if widget is destroyed
        return

    # Choose file depending on mode
    if current_mode == "live":
        file_path = "EPICS BCI Code\\Data\\brailler_output.txt"
    elif current_mode == "braille":
        file_path = "EPICS BCI Code\\Data\\braille_binary.txt"

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
    after_id3 = root.after(500, update_live_feed)

update_live_feed()  # Start the loop

#Buttons at the bottom of the frame

def new_file_action():
    #Making sure the user intended to click the new file button
    confirm = messagebox.askyesno(title="Confirm New File", message="Are you sure you want to erase the text? \nYou cannot retrieve it once you confirm.")

    if not confirm:
        return #user clicked no
    
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
        data = text_display.get("1.0", tk.END)

        # Write to exported file
        with open(export_path, "w", encoding="utf-8") as f:
            f.write(data)

        print("Export complete →", export_path)

    except Exception as e:
        messagebox.showerror("Export Failed", f"Error: {e}")

button_canvas = tk.Canvas(live_feed_frame, width=464, height=72, bg="#FFFFFF", highlightthickness=0)
button_canvas.place(x=0, y=422)

new_file_img = load_img("EPICS BCI Code\\Images\\New_file_button.png", size=(120, 35))
new_file_icon = make_interactive_image(button_canvas, new_file_img, 20, 18, on_click=new_file_action)

export_text_file_img = load_img("EPICS BCI Code\\Images\\export_text_file_button.png", size=(161, 37))
export_text_file_icon = make_interactive_image(button_canvas, export_text_file_img, 155, 15, on_click=export_file_action)

braille_selection_box_img = load_img("EPICS BCI Code\\Images\\braille_selection_box_unselected.png", size=(113, 39))
braille_selection_box_img_2 = load_img("EPICS BCI Code\\Images\\braille_selection_box_selected.png", size=(105, 42))
braille_selection_box_icon = make_interactive_image(button_canvas, braille_selection_box_img, 330, 15, on_click=toggle_braille_selection)

########################################################
#DIsplay box when contraction library Button Selected
#####################################################
def update_enabled(contraction, var):
    enabled_contractions[contraction]['enabled'] = var.get()
    # Optionally, write back to file
    with open(enabled_contractions_path, "w", encoding="utf-8") as f:
        json.dump(enabled_contractions, f, indent=4, ensure_ascii=False)


enabled_contractions_path = "EPICS BCI Code\\Data\\enabled_contractions.txt"

# Load the file if it exists
try:
    with open(enabled_contractions_path, "r", encoding="utf-8") as f:
        enabled_contractions = json.load(f)
except FileNotFoundError:
    enabled_contractions = {}

#Search bar for contraction library
search_var = tk.StringVar()
placeholder_text = "Search here:"
search_var.set(placeholder_text)  # placeholder

def on_search_focus_in(event):
    if search_var.get() == placeholder_text:
        search_var.set("")
        search_entry.config(fg="black")

def on_search_focus_out(event):
    if search_var.get().strip() == "":
        search_var.set(placeholder_text)
        search_entry.config(fg="gray")

        search_entry.selection_clear()
        root.focus()  # move focus somewhere else, here root

search_entry = tk.Entry(
    contraction_library_frame,
    textvariable=search_var,
    font=("Roboto Condensed", 16),
    fg="gray",
    bd=1,
    relief="solid"
)
search_entry.place(x=10, y=63, width=315, height=60)
search_entry.bind("<FocusIn>", on_search_focus_in)
search_entry.bind("<FocusOut>", on_search_focus_out)

contraction_library_frame.bind("<Button-1>", on_search_focus_out)

# Scrollable frame for contraction list
contraction_list_frame = tk.Frame(contraction_library_frame, bg="white")
contraction_list_frame.place(x=15, y=130, width=435, height=350)

canvas = tk.Canvas(contraction_list_frame, bg="white", highlightthickness=0)
scrollbar = tk.Scrollbar(contraction_list_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="white")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

def _on_mousewheel(event):
    # For Windows, event.delta is multiples of 120
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)

contraction_labels = []
contraction_vars = {}  # To keep track of each checkbox variable
original_contractions_order = sorted(enabled_contractions.keys(), key=str.lower)
contraction_labels_dict = {}

for contraction in original_contractions_order:
    data = enabled_contractions[contraction]
    var = tk.IntVar(value=data['enabled'])
    contraction_vars[contraction] = var

    # Checkbox with label showing contraction + braille
    cb = tk.Checkbutton(
        scrollable_frame,
        text=f"{contraction.capitalize()}   ({data['braille']})",
        variable=var,
        onvalue=1,
        offvalue=0,
        anchor="w",
        bg="white",
        font=("Roboto Condensed", 14),
        command=lambda c=contraction, v=var: update_enabled(c, v)
    )
    cb.pack(fill="x", padx=5, pady=2)

    contraction_labels.append((var, cb, contraction))
    contraction_labels_dict[contraction] = (var, cb, contraction)

def update_contraction_display(*args):
    search_term = search_var.get().lower().strip()

    # Hide all checkboxes first
    for contraction in original_contractions_order:
        var, chk, name = contraction_labels_dict[contraction]
        chk.pack_forget()

    # Determine which contractions to show
    if search_term == "" or search_term == placeholder_text.lower():
        # Show all in alphabetical order
        for contraction in sorted(original_contractions_order, key=str.lower):
            var, chk, name = contraction_labels_dict[contraction]
            chk.pack(fill="x", padx=5, pady=2)
        canvas.yview_moveto(0)
        return

    # Otherwise, filter dynamically
    filtered_contractions = [
        contraction for contraction in original_contractions_order
        if search_term in contraction.lower()
    ]

    filtered_contractions.sort(key=str.lower)

    first_match_widget = None
    for contraction in filtered_contractions:
        var, chk, name = contraction_labels_dict[contraction]
        chk.pack(fill="x", padx=5, pady=2)
        if not first_match_widget:
            first_match_widget = chk

    # Scroll to first match if exists
    if first_match_widget:
        canvas.update_idletasks()
        canvas.yview_moveto(first_match_widget.winfo_y() / scrollable_frame.winfo_height())
    else:
        canvas.yview_moveto(0)

def select_all_contractions():
    for contraction, var in contraction_vars.items():
        var.set(1)
        enabled_contractions[contraction]['enabled'] = 1

    # Save once (not per checkbox)
    with open(enabled_contractions_path, "w", encoding="utf-8") as f:
        json.dump(enabled_contractions, f, indent=4, ensure_ascii=False)


def deselect_all_contractions():
    for contraction, var in contraction_vars.items():
        var.set(0)
        enabled_contractions[contraction]['enabled'] = 0

    # Save once
    with open(enabled_contractions_path, "w", encoding="utf-8") as f:
        json.dump(enabled_contractions, f, indent=4, ensure_ascii=False)

select_all_btn = tk.Button(
    contraction_library_frame,
    text="Select All",
    font=("Roboto Condensed", 14),
    command=select_all_contractions
)
select_all_btn.place(x=331, y=63, width=120, height=28)

deselect_all_btn = tk.Button(
    contraction_library_frame,
    text="Deselect All",
    font=("Roboto Condensed", 14),
    command=deselect_all_contractions
)
deselect_all_btn.place(x=331, y=95, width=120, height=28)

# Bind the search_var so it updates automatically
search_var.trace_add("write", update_contraction_display)


root.mainloop()