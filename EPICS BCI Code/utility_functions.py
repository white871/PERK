import tkinter as tk
from PIL import Image, ImageTk

triangle_buttons = []
circle_buttons = []

def load_img(path, size=(80,80)):
    img = Image.open(path)
    img = img.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

def create_label(root, anchr,txt=None,img=None,font_txt="Roboto Condensed",
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

def create_inverted_label(root, anchr, txt=None, img=None, font_txt="Roboto Condensed", font_size=16, bold="normal", italic="roman", backround="black", bd_width=0, location=(0, 0)):
    if img==None:
        label = tk.Label(root, text=txt, fg="white", font=(font_txt, font_size, bold, italic), bg=backround)
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
        'Deselect all others, select this one, and update images.'

        # Remove destroyed widgets first
        global triangle_buttons
        triangle_buttons = [
            btn for btn in triangle_buttons
            if btn["label"].winfo_exists()
        ]

        for btn in triangle_buttons:
            if btn["tri"] == triangle_id:
                btn["selected"] = True

                if btn["label"].winfo_exists():
                    btn["label"].config(font=("Roboto Condensed", 20, 'bold', 'roman'))

                if btn["img_obj"] and btn["img_on_click"]:
                    canvas.itemconfig(btn["img_obj"], image=btn["img_on_click"]["True"])

                if on_select:
                    on_select()

            else:
                btn["selected"] = False

                if btn["label"].winfo_exists():
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
    circle_center, circle_radius, inverted=False, on_select=None):
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
            if inverted == False:
                canvas.itemconfig(circle_id, outline="gray", width=4)
            elif inverted == True:
                canvas.itemconfig(circle_id, outline="white", width=3)
            label.config(font=("Roboto Condensed", 25, 'bold', 'italic'))
        else:
            if inverted == False:
                canvas.itemconfig(circle_id, outline="", width=2)
            elif inverted == True:
                canvas.itemconfig(circle_id, outline="", width=2)
            label.config(font=("Roboto Condensed", 25, 'normal', 'roman'))

    # Click
    def on_click(event):
        if cursor_in_circle(event):
            if on_select:
                on_select()

    # Bind events
    canvas.bind("<Motion>", hover_motion)
    canvas.bind("<Button-1>", on_click)
    
    def sublabel_on_enter(event):
        if inverted == False:
            canvas.itemconfig(circle_id, outline="gray", width=4)
        elif inverted == True:
            canvas.itemconfig(circle_id, outline="white", width=4)
        
        label.config(font=("Roboto Condensed", 25, 'bold', 'italic'))

    def sublabel_on_leave(event):
        if inverted == False:
            canvas.itemconfig(circle_id, outline="", width=2)
        elif inverted == True:
            canvas.itemconfig(circle_id, outline="", width=2)

        label.config(font=("Roboto Condensed", 25, 'normal', 'roman'))

    def sublabel_on_click(event):
        if on_select:
            on_select()
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

def create_display_frame_header(parent, text, anchor, coords=(0,0),font=("Roboto Condensed", 22, 'bold'), bg="#FFFFFF", fg="#000000", line_color="#000000"):
    label = tk.Label(parent, text=text, font=font, bg=bg, fg=fg)
    label.place(x=coords[0], y=coords[1], anchor=anchor)
    
    line_canvas = tk.Canvas(parent, bg=line_color, highlightthickness=0)
    line_canvas.place(x=10, y=50, width=445, height=1)

    return label, line_canvas

def create_display_frame(parent, rel_fill = (1, 1), bg="#FFFFFF", start_display=False, inverted=False):
    if inverted ==False:
        frame = tk.Frame(parent, bg=bg)
    elif inverted== True:
        frame = tk.Frame(parent, bg=bg, highlightbackground="#FFFFFF", highlightthickness=2, relief="solid", bd=0)
    frame.place(relwidth=rel_fill[0], relheight=rel_fill[1])
    if start_display:
        frame.tkraise()
    return frame

