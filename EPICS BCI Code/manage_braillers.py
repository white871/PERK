import tkinter as tk
import math
from utility_functions import load_img, create_label, create_inverted_label, create_image_canvas, create_interactive_icon, create_display_frame, make_interactive_image

class ManageBraillersViewBase:
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

        self.wifi_name_file = self.app.writeable_path("Data/wifi_name.txt")

        self.current_brailler_label = None
        self.current_brailler_name = None
        self.brailler_status_dots = {}

        self.STATUS_RADIUS = 6
        self.STATUS_GREEN = "#93c47d"
        self.STATUS_RED = "#e06666"

        self.braillers = [
            "Mark's Brailler", "Nash's Brailler", "Lucy's Brailler",
            "Diana's Brailler", "Mohammad's Brailler", "Sarvesh's Brailler",
            "Ayona's Brailler", "Felix's Brailler", "Joe's Brailler", 
            "Mary's Brailler", "Jane's Brailler", "Josh's Brailler", 
            "Chloe's Brailler", "Ashley's Brailler", "Gina's Brailler"
        ]

        self.build_header()
        self.build_brailler_list()
        self.build_popup_menu()
        self.build_bottom_actions()
        self.initialize_status()

#Header
    def build_header(self):
        title_header_canvas = tk.Canvas(
            self.root, 
            width=1035, height=110, 
            background=self.header_bg, 
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
            bold='bold', italic='roman', 
            backround=self.header_bg, 
            location=(50, 30)
        )

        self.perk_braille_img = load_img(
            self.app.resource_path(self.image_path + "PERK_Braille_Image_grey.png"), 
            size=(302,110)
        )

        perk_logo = create_label(
            self.root, 'nw', 
            img=self.perk_braille_img, 
            bd_width=0, 
            location=(695, 6)
        )

# Brailler list
    def build_brailler_list(self):
        start_y = 250
        bottom_limit = 550   # where bottom buttons start
        available_height = bottom_limit - start_y

        max_columns = 3
        total_rows = math.ceil(len(self.braillers) / max_columns)

        row_height = available_height / total_rows  

        window_width = 1250
        left_margin = 110
        right_margin = 110
        usable_width = window_width - left_margin - right_margin
        column_width = usable_width / max_columns

        for i, name in enumerate(self.braillers):
            row = i // max_columns
            col = i % max_columns

            x = left_margin + col * column_width
            y = start_y + row * row_height

            lbl = self.label_fn(
                self.root,
                anchr="nw",
                txt=name,
                font_txt="Roboto Condensed",
                font_size=18,
                bold="normal",
                backround=self.bg,
                location=(x, y)
            )

            lbl.is_bold = False
            lbl.config(cursor="hand2")
            lbl.bind("<Button-1>", lambda e, l=lbl, n=name: self.on_brailler_click(l, n))

            dot_canvas = tk.Canvas(
                self.root,
                width=self.STATUS_RADIUS * 2,
                height=self.STATUS_RADIUS * 2,
                bg=self.bg,
                highlightthickness=0
            )
            dot_canvas.place(x=x - 20, y=y + 5, anchor="nw")

            dot = dot_canvas.create_oval(
                0,0,
                self.STATUS_RADIUS * 2,
                self.STATUS_RADIUS * 2,
                outline=""
            )

            self.brailler_status_dots[name] = (dot_canvas, dot)

#Brailler click
    def on_brailler_click(self, label, name):
        # If clicking the same label → unbold + hide popup
        if self.current_brailler_label == label:
            label.config(font=("Roboto Condensed", 18, "normal", "roman"))
            self.popup.place_forget()
            self.current_brailler_label = None
            return

        # If clicking a different brailler
        if self.current_brailler_label:
            self.current_brailler_label.config(
                font=("Roboto Condensed", 18, "normal", "roman")
            )

        # Bold new one
        label.config(font=("Roboto Condensed", 18, "bold"))
        self.popup.place(x=50, y=540, width=950, height=50)
        self.popup.tkraise()
        self.current_brailler_label = label
        self.current_brailler_name = name

#Popup menu

    def build_popup_menu(self):
        self.popup=create_display_frame(
            self.root, 
            rel_fill=(0,0),
            bg=self.bg,
            start_display=False,
            border_color=self.fg
        )

        self.popup.config(
            highlightbackground=self.hbg,
            highlightthickness=self.hth
        )

        button_names= "Live Feed", "Disconnect Brailler", "Pair Device", "Rename Device"
        x_positions=[60, 250, 530, 730]

        for name, x in zip(button_names, x_positions):
            lbl= self.label_fn(
                self.popup, 
                anchr="nw",
                txt=name, 
                font_txt="Roboto Condensed", 
                font_size=18, 
                bold="normal", 
                backround=self.bg,
                location=(x, 5)
                )
            lbl.config(cursor="hand2")

            if name == "Live Feed":
                lbl.bind("<Button-1>", lambda e: self.open_live_feed())    
            if name == "Disconnect Brailler":
                lbl.bind("<Button-1>", lambda e: self.disconnect_brailler())   
            if name == "Pair Device":
                lbl.bind("<Button-1>", lambda e: self.pair_brailler()) 
            if name == "Rename Device":
                lbl.bind("<Button-1>", lambda e: self.rename_device())     

#Status management
    def set_brailler_status(self, name, connected):
        if name not in self.brailler_status_dots:
            return

        canvas, dot = self.brailler_status_dots[name]
        color = self.STATUS_GREEN if connected else self.STATUS_RED
        canvas.itemconfig(dot, fill=color)
    
    def initialize_status(self):
        self.set_brailler_status("Mark's Brailler", False)
        self.set_brailler_status("Nash's Brailler", False)
        self.set_brailler_status("Ayona's Brailler", True)
        self.set_brailler_status("Joe's Brailler", False)
        self.set_brailler_status("Lucy's Brailler", True)
        self.set_brailler_status("Diana's Brailler", False)
        self.set_brailler_status("Mohammad's Brailler", True)
        self.set_brailler_status("Sarvesh's Brailler", True)
        self.set_brailler_status("Felix's Brailler", False)
        self.set_brailler_status("Mary's Brailler", False)
        self.set_brailler_status("Jane's Brailler", True)
        self.set_brailler_status("Josh's Brailler", False)
        self.set_brailler_status("Chloe's Brailler", True)
        self.set_brailler_status("Ashley's Brailler", False)
        self.set_brailler_status("Gina's Brailler", True)

#Button actions
    def open_live_feed(self):
        if self.inverted:
            self.app.show_text_page_inverted(self.current_brailler_name)
        else:
            self.app.show_text_page(self.current_brailler_name)

    def disconnect_brailler(self):
        self.set_brailler_status(self.current_brailler_name, False)
    
    def pair_brailler(self):
        self.set_brailler_status(self.current_brailler_name, True)

#Rename device 
    def rename_device(self):
        self.rename_popup = tk.Toplevel(self.root)
        self.rename_popup.title("Rename Device")
        self.rename_popup.geometry("300x120")
        self.rename_popup.resizable(False, False)
        self.rename_popup.grab_set()  # Make it modal
        self.rename_popup.configure(bg=self.bg)
    
        # Create the entry variable and widget
        self.entry_var = tk.StringVar()

        entry = tk.Entry(
            self.rename_popup, 
            textvariable=self.entry_var, 
            font=("Roboto Condensed", 14),
            bg=self.bg,
            fg=self.fg,
            insertbackground=self.fg
        )
        
        entry.pack(pady=10)
        entry.focus_set()
    
        rename_button = tk.Button(
            self.rename_popup, 
            text="Rename", 
            font=("Roboto Condensed", 12),
            bg=self.bg,
            fg=self.fg, 
            command=self.submit_rename
            )
        rename_button.pack(pady=5)

    def submit_rename(self):
        new_name = self.entry_var.get().strip()
        if new_name:
            # Update label text
            self.current_brailler_label.config(text=new_name)
                    
            # Update brailler status dictionary
            if self.current_brailler_name in self.brailler_status_dots:
                self.brailler_status_dots[new_name]=\
                    self.brailler_status_dots.pop(self.current_brailler_name)
            # Update current name reference
            self.current_brailler_name = new_name
    
            if self.current_brailler_name in self.braillers:
                index = self.braillers.index(self.current_brailler_name)
                self.braillers[index] = new_name
        self.rename_popup.destroy()
    
    #Bottom actions
    def build_bottom_actions(self):
        # Manage Braillers row
        self.home_image = load_img(
            self.app.resource_path(self.image_path + "Home_icon.png"), 
            size=(95, 100)
        )

        home_icon, home_img_obj = create_image_canvas(
            self.root, 
            95, 100, 0, 0, 
            'center', 
            self.home_image, 
            location=(90, 185)
        )

        Braillers_logo = self.label_fn(
            self.root, 
            anchr="nw",
            txt="Manage Braillers",
            font_txt="Roboto Condensed",
            font_size=25,
            bold="bold",
            backround=self.bg,
            location=(140, 165)
        )

        self.pair_all_image = load_img(
            self.app.resource_path(self.image_path + "pair_all_button.png"), 
            size=(105, 44)
        )
        pair_all_button = make_interactive_image(
            self.root, 
            self.pair_all_image, 
            890, 160, 
            on_click=lambda: self.pair_all()
        )   
            
        self.bluetooth_image = load_img(
            self.app.resource_path(self.image_path + "Bluetooth_icon.png"), 
            size=(110, 98)
        )

        bluetooth_icon,_=create_image_canvas(
            self.root, 
            110, 98, 0, 0, 
            'center', 
            self.bluetooth_image, 
            location=(90, 645)
        )

        pairing_label=self.label_fn(
            self.root, 
            anchr="sw",
            txt="Start Pairing Process",
            font_txt="Roboto Condensed",
            font_size=25,
            bold="normal",
            backround=self.bg,
            location=(140, 665)
        )

        create_interactive_icon(
            bluetooth_icon, 
            pairing_label, 
            (52, 50), 38,
            on_select=lambda: (
                self.wifi_enable()
            )
        )

        self.settings_image = load_img(
            self.app.resource_path(self.image_path + "settings_icon.png"), 
            size=(105, 97)
        )
        
        settings_icon,_=create_image_canvas(
            self.root, 
            105, 97, 0, 0, 
            'center', 
            self.settings_image, 
            location=(805, 645)
        )

        settings_label=self.label_fn(
            self.root, 
            anchr="se",
            txt="Settings",
            font_txt="Roboto Condensed",
            font_size=25,
            bold="normal",
            backround=self.bg,
            location=(970, 665)
        )

        create_interactive_icon(
            settings_icon, 
            settings_label, 
            (51, 48), 38, 
            on_select=lambda: (
                self.app.show_settings_inverted()
                if self.inverted
                else self.app.show_settings()
            )
        )    

    def wifi_enable(self):
        self.wifi_popup = tk.Toplevel(self.root)
        self.wifi_popup.title("Wireless Connection")
        self.wifi_popup.geometry("300x120")
        self.wifi_popup.resizable(False, False)
        self.wifi_popup.grab_set()  # Make it modal
        self.wifi_popup.configure(bg=self.bg)
    
        title_label = tk.Label(
            self.wifi_popup,
            text="Enter Your Classroom's Room Number",
            font=("Roboto Condensed", 14, "bold"),
            bg=self.bg,
            fg=self.fg
        )
        title_label.pack(pady=(10, 5))  # top padding, small gap below


        # Create the entry variable and widget
        self.entry_var = tk.StringVar()

        entry = tk.Entry(
            self.wifi_popup, 
            textvariable=self.entry_var, 
            font=("Roboto Condensed", 14),
            bg=self.bg,
            fg=self.fg,
            insertbackground=self.fg
        )
        entry.pack(pady=5)
        entry.focus_set()
    
        submit_button = tk.Button(
            self.wifi_popup, 
            text="Submit", 
            font=("Roboto Condensed", 12),
            bg=self.bg,
            fg=self.fg, 
            command=self.submit_wifi
            )
        submit_button.pack(pady=5)

    
    def submit_wifi(self):
        wifi_name = self.entry_var.get().strip()

        with open(self.wifi_name_file, "a", encoding="utf-8") as f:
            f.write(wifi_name)

        self.wifi_popup.destroy()

        #LOTS OF STUFF HAPPENS HERE

    def pair_all(self):
                for brailler in self.braillers:
                    self.set_brailler_status(brailler, True)
                return

class ManageBraillersView(ManageBraillersViewBase):
    def __init__(self, root, app, THEMES):
        super().__init__(root, app, THEMES, theme_name="light")

class ManageBraillersViewInverted(ManageBraillersViewBase):
    def __init__(self, root, app, THEMES):
        super().__init__(root, app, THEMES, theme_name="dark")