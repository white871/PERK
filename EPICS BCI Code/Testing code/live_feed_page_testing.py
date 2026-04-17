import tkinter as tk
from tkinter import filedialog, messagebox
import random
import json
import os
from utility_functions import load_img, create_label, create_inverted_label, create_image_canvas, create_triangle_button, create_interactive_icon, make_interactive_image, create_display_frame_header, create_display_frame

class IndividualBraillerViewBase:

    def __init__(self, root, app, brailler_name, THEMES, open_tab, ssh, theme_name="light"):
        self.root = root
        self.app = app
        self.brailler_name = brailler_name
        self.current_tab = open_tab

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

        #STATE MODIFIERS
        self.current_mode = "live"
        self.last_len = 0
        self.ssh = ssh

        self.device_registry_path = "EPICS BCI Code/Data/device_registry.json"
        self.device_state_path = "EPICS BCI Code/Data/device_state.json"
        self.text_file_path = "EPICS BCI Code/Data/brailler_output.txt"
        self.braille_file_path = "EPICS BCI Code/Data/braille_binary.txt"
        self.translations_path = "EPICS BCI Code/Data/translations.txt"
        self.enabled_contractions_path = "EPICS BCI Code/Data/enabled_contractions.txt"

        self.load_registry()
        self.load_state()

        self.brailler_id = None
        for dev_id, info in self.registry.items():
            if info.get("name") == brailler_name:
                self.brailler_id = dev_id
                break

        self.ip = self.state[self.brailler_id].get("ip")

        self.after_id1 = None
        self.after_id2 = None
        self.after_id3 = None

        #LOAD DATA
        self.load_translations()
        self.load_enabled_contractions()

        #BUILD UI
        self.build_header()
        self.build_main_frames()
        self.build_navigation_buttons()
        self.build_live_feed()
        self.build_contraction_library()

        # Start background loops
        self.simulate_brailler_output()
        self.simulate_braille_binary_output()
        self.update_live_feed()

        self.sync_triangle_state()

    def load_registry(self):
        try:
            with open(self.device_registry_path, "r") as f:
                self.registry = json.load(f)
        except:
            self.registry = {}

    def load_state(self):
        try:
            with open(self.device_state_path, "r") as f:
                 self.state = json.load(f)
        except:
            self.state = {}


    def load_translations(self):
        try:
            with open(self.translations_path, "r", encoding="utf-8") as f:
                self.translations = json.load(f)
        except FileNotFoundError:
            self.translations = {}

    def load_enabled_contractions(self):
        try:
            with open(self.enabled_contractions_path, "r", encoding="utf-8") as f:
                self.enabled_contractions = json.load(f)
        except FileNotFoundError:
            self.enabled_contractions = {}

    def build_header(self):
        title_header_canvas = tk.Canvas(
            self.root,
            width=1035,
            height=110,
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
            bold='bold',
            italic='roman',
            backround=self.header_bg,
            location=(50, 30)
        )

        self.perk_braille_img = load_img(
            os.path.join(self.image_path, "PERK_Braille_Image_grey.png"), 
            size=(302,108)
        )
    
        perk_logo = self.label_fn(
            self.root, 'nw', 
            img=self.perk_braille_img, 
            bd_width=0, 
            location=(695, 8)
        )
    
    def show_live_feed(self):
        self.current_tab = "live_feed"
        self.sync_triangle_state()

    def show_contraction_library(self):
        self.current_tab = "contractions"
        self.sync_triangle_state()

    def toggle_braille_selection(self):

        if self.current_mode == "live":
            self.current_mode = "braille"
            self.braille_selection_box_icon.config(image=self.braille_selection_box_img_2)
            self.text_display.config(font=("Cascadia Mono", 20))
        else:
            self.current_mode = "live"
            self.braille_selection_box_icon.config(image=self.braille_selection_box_img)
            self.text_display.config(font=("Roboto Condensed", 14))

        self.update_live_feed(force_full_refresh=True)

    
    def update_live_feed(self, force_full_refresh=False):
        """Continuously update the text display."""
    
        if not self.text_display.winfo_exists():
            # Stop the loop if widget is destroyed
            return

        # Choose file depending on mode
        if self.current_mode == "live":
            current_contents = self.text_content
        elif self.current_mode == "braille":
            current_contents = self.braille_content

        ###################################################
        #####################################################
        #EDIT HERE#### add function to get file from pi###############

        new_len = len(current_contents)

        if new_len > self.last_len or force_full_refresh:
            if not force_full_refresh:
                new_text = current_contents[self.last_len:new_len]
            else:
                new_text = current_contents
                self.text_display.delete("1.0", tk.END)
            self.text_display.insert(tk.END, new_text)

        if self.current_mode == "braille":
            current_contents = self.binToBraille(current_contents)

        self.last_len = new_len

        #Determines if user is at the bottom of the page, and keeps them there if so
        bottom = self.text_display.yview()[1]
        if bottom >= 0.92:   # user is already at bottom
            self.text_display.see(tk.END)
        
        # Schedule next update after 150 ms
        self.after_id3 = self.root.after(500, self.update_live_feed)

      
    def binToBraille(self, bin_data):
        out = ""

        # Split by whitespace/newlines
        chunks = bin_data.split()

        for chunk in chunks:
            if chunk in self.translations:
                out += self.translations[chunk]
            elif chunk == "":
                out += " "
            else:
                # Unknown pattern (optional debug)
                pass

        return out

    
    def run_command(self, command):

        if self.ssh is None:
            self.create_error_popup("SSH is not connected.")
            return ""
        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()

        if error:
            self.create_error_popup(error)
        return output

    ####################EDIT HERE ##############remove these two functions that simulate output  
    def simulate_brailler_output(self):
        # """Simulate text arriving from Brailler device."""
        # char = random.choice(
        #     ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p",
        #      "q","r","s","t","u","v","w","x","y","z"," ", " ", " "," ", " "]
        # )

        # # Append to the file
        # with open(self.text_file_path, "a", encoding="utf-8") as f:
        #     f.write(char)

        cmd = f"sshpass -p 'perk' ssh -o StrictHostKeyChecking=no perk@{self.ip} 'cat ~/transliterateOutput.txt'"
        self.text_content= self.run_command(cmd)

        if self.braille_content == None:
            self.root.after_cancel(self.after_id1)
            print("Connection lost. Stopping updates.")

        # Schedule next write
        self.after_id1 = self.root.after(300, self.simulate_brailler_output)

    def simulate_braille_binary_output(self):
        # """Simulate Braille binary sequences using only valid codes in the translations dictionary."""
        # if not self.translations:
        #     return  # safety check

        # # Pick a random valid braille code from the dictionary keys
        # binary_seq = random.choice(list(self.translations.keys()))
        # symbol = self.translations[binary_seq]

        # # Append it to the file with a space (to separate sequences)
        # with open(self.braille_file_path, "a", encoding="utf-8") as f:
        #     f.write(symbol)

        cmd = f"sshpass -p 'perk' ssh -o StrictHostKeyChecking=no perk@{self.ip} 'cat ~/outputBin.txt'"
        self.braille_content= self.run_command(cmd)

        if self.braille_content == None:
            self.root.after_cancel(self.after_id2)
            print("Connection lost. Stopping updates.")

        # Schedule next write
        self.after_id2 = self.root.after(300, self.simulate_braille_binary_output)

    ###############EDIT HERE ############ somehow make it so new file action also clears file on client raspberry pi
    def new_file_action(self):
        #Making sure the user intended to click the new file button
        confirm = messagebox.askyesno(
            title="Confirm New File", 
            message="Are you sure you want to erase the text? \nYou cannot retrieve it once you confirm."
        )

        if not confirm:
            return #user clicked no
        
        #Erasing everything on the 
        with open(self.braille_file_path, "w") as f:
            f.write("")
        
        with open(self.text_file_path, "w") as f:
            f.write("")

        self.text_display.config(state="normal")
        self.text_display.delete("1.0", tk.END)

        self.last_len = 0

    def export_file_action(self):
        try:
            # Pick save location
            export_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            
            if not export_path:   # user canceled
                return

            # Read current brailler file
            data = self.text_display.get("1.0", tk.END)

            # Write to exported file
            with open(export_path, "w", encoding="utf-8") as f:
                f.write(data)

            print("Export complete →", export_path)

        except Exception as e:
            messagebox.showerror("Export Failed", f"Error: {e}")

    def build_main_frames(self):
        display_container = tk.Frame(
            self.root, 
            bg=self.bg, 
            bd=0, 
            highlightthickness=0
        )
        display_container.place(x=530, y=145, width=470, height=500)

        self.live_feed_frame = create_display_frame(
            display_container,
            bg=self.bg,
            start_display=True,
            border_color=self.fg
        )
        
        live_feed_label, line_canvas =  create_display_frame_header(
            self.live_feed_frame, 
            "Live Text Feed", 'n', 
            coords=(470/2, 10),
            bg=self.bg,
            fg=self.fg,
            line_color=self.fg
        )

        self.contraction_library_frame = create_display_frame(
            display_container,
            bg=self.bg,
            border_color=self.fg
        )
        
        contraction_library_label, line_canvas =  create_display_frame_header(
            self.contraction_library_frame, 
            "Contraction Library", 'n', 
            coords=(470/2, 10),
            bg=self.bg,
            fg=self.fg,
            line_color=self.fg
        )

    def cancel_loops(self):
        for after_id in [self.after_id1, self.after_id2, self.after_id3]:
            if after_id:
                self.root.after_cancel(after_id)

    def home_select(self):
        self.cancel_loops()
        if self.inverted:
            self.app.show_manage_braillers_inverted()
        else:
            self.app.show_manage_braillers()
    
    def settings_select(self):
        self.cancel_loops()
        if self.inverted:
            self.app.show_settings_inverted()
        else:
            self.app.show_settings()

    def build_navigation_buttons(self):
        self.triangle_image_1 = load_img(
            os.path.join(self.image_path, "triangles_icon.png"), 
            size=(60,115)
        )

        self.triangle_image_2 = load_img(
            os.path.join(self.image_path, "triangles_icon_flipped.png"), 
            size=(60,115)
        )

        self.triangle_canvas, triangle_img_obj = create_image_canvas(
            self.root, 
            60, 115, 0, 0, 
            'nw', self.triangle_image_1, 
            location=(155, 235)
        )

        self.triangle_buttons = []  # global list of all triangle buttons

        label_live_text_feed = self.label_fn(
            self.root, 'w', 
            txt="Live Text Feed",  
            font_txt="Roboto Condensed", 
            font_size=20, 
            bold='bold', italic='roman', 
            backround=self.bg, 
            location=(224, 261)
        )

        triangle_live_feed_coords = (12, 9, 12, 46, 48, 28)

        self.triangle_live_feed = create_triangle_button(
            self.triangle_canvas, 
            triangle_live_feed_coords, 
            label_live_text_feed, 
            target_frame = self.live_feed_frame,
            img_obj=triangle_img_obj, 
            img_on_click={"True": self.triangle_image_1, "False": self.triangle_image_2}, 
            selected=(self.current_tab == "live_feed"),
            on_select= self.show_live_feed
        )

        label_contraction_library = self.label_fn(
            self.root, 'w', 
            txt="Contraction Library",  
            font_txt="Roboto Condensed", 
            font_size=20, 
            bold='normal', italic='roman', 
            backround=self.bg, 
            location=(224, 322)
        )

        triangle_contraction_library_coords = (12, 68, 12, 105, 48, 87)

        self.triangle_contraction_library = create_triangle_button(
            self.triangle_canvas, 
            triangle_contraction_library_coords, 
            label_contraction_library, 
            target_frame = self.contraction_library_frame,
            img_obj=triangle_img_obj, 
            img_on_click={"True": self.triangle_image_2, "False": self.triangle_image_1}, 
            selected=(self.current_tab == "contractions"), 
            on_select= self.show_contraction_library
        )

        self.Brailler_connected_image = load_img(
            os.path.join(self.image_path, "Brailler_Connected_Icon.png"), 
            size=(100,100)
        )

        brailler_icon, brailler_img_obj = create_image_canvas(
            self.root, 
            100, 100, 0, 0, 
            'nw', self.Brailler_connected_image, 
            location=(50, 135)
        )

        label_sub_title_1 = self.label_fn(
            self.root, 'w', 
            txt=self.brailler_name,  
            font_txt="Roboto Condensed", 
            font_size=25, 
            bold='bold', italic='roman', 
            backround=self.bg, 
            location=(165, 185)
        )

        self.online_dot = load_img(
            os.path.join(self.image_path, "green_circle.png"), 
            size=(40,40)
        )

        dot_icon = self.label_fn(
            self.root, 'w', 
            img=self.online_dot, 
            bd_width=0, 
            location=(460, 185)
        )

        
        self.home_image = load_img(
            os.path.join(self.image_path, "Home_icon.png"), 
            size=(105,110)
        )

        home_icon, home_img_obj = create_image_canvas(
            self.root, 
            105, 110, 0, 0, 
            'center', self.home_image, 
            location=(100, 445)
        )

        label_sub_title_2 = self.label_fn(
            self.root, 'w', 
            txt="Device Management",  
            font_txt="Roboto Condensed", 
            font_size=25, 
            bold='normal', italic='roman', 
            backround=self.bg, 
            location=(165, 442)
        )

        self.home_circle = create_interactive_icon(
            home_icon, 
            label_sub_title_2, 
            (52, 54), 41, 
            on_select=self.home_select
        )

        self.settings_image = load_img(
            os.path.join(self.image_path, "settings_icon.png"), 
            size=(113,100)
        )

        settings_icon, settings_img_obj = create_image_canvas(
            self.root, 
            113, 100, 0, 0, 
            'center', self.settings_image, 
            location=(100, 595)
        )

        label_sub_title_3 = self.label_fn(
            self.root, 'w', 
            txt="Settings",  
            font_txt="Roboto Condensed", 
            font_size=25, 
            bold='normal', italic='roman', 
            backround=self.bg, 
            location=(165, 592)
        )

        self.settings_circle = create_interactive_icon(
            settings_icon, 
            label_sub_title_3, 
            (54, 49), 41, 
            on_select=self.settings_select
        )

    def sync_triangle_state(self):
        if self.current_tab == "live_feed":
            self.triangle_live_feed.select(True)
            self.triangle_contraction_library.select(False)
    
        elif self.current_tab == "contractions":
            self.triangle_live_feed.select(False)
            self.triangle_contraction_library.select(True)
          
    def build_live_feed(self):
        text_frame_height = 500-72-60

        text_frame = tk.Frame(
            self.live_feed_frame, 
            bg=self.bg
        )
        text_frame.place(x=10, y=60, width=450, height=text_frame_height)

        #Scrollbar first (right side)
        scrollbar = tk.Scrollbar(
            text_frame, 
            orient="vertical"
        )
        scrollbar.pack(side="right", fill="y", padx=(5, 6))

        # Text box second (takes remaining space)
        self.text_display = tk.Text(
            text_frame,
            wrap="word",
            font=("Roboto Condensed", 14),
            fg=self.fg,
            bg=self.bg, 
            bd=0,
            highlightthickness=0,
            relief="flat",
            pady=5
        )
        self.text_display.pack(side="left", fill="both", expand=True)

        # Link scroll
        scrollbar.config(command=self.text_display.yview)
        self.text_display.config(yscrollcommand=scrollbar.set)
   
        button_canvas = tk.Canvas(
            self.live_feed_frame, 
            width=460, height=66, 
            bg=self.bg, 
            highlightthickness=0
        )
        button_canvas.place(x=0, y=422)

        self.new_file_img = load_img(
            os.path.join(self.image_path, "New_file_button.png"), 
            size=(120, 35)
        )

        new_file_icon = make_interactive_image(
            button_canvas, 
            self.new_file_img, 
            20, 18, 
            on_click=self.new_file_action
        )

        self.export_text_file_img = load_img(
            os.path.join(self.image_path, "export_text_file_button.png"), 
            size=(161, 37)
        )

        export_text_file_icon = make_interactive_image(
            button_canvas, 
            self.export_text_file_img, 
            155, 15, 
            on_click=self.export_file_action
        )

        self.braille_selection_box_img = load_img(
            os.path.join(self.image_path, "braille_selection_box_unselected.png"), 
            size=(113, 39)
        )

        self.braille_selection_box_img_2 = load_img(
            os.path.join(self.image_path, "braille_selection_box_selected.png"), 
            size=(105, 42)
        )

        self.braille_selection_box_icon = make_interactive_image(
            button_canvas, 
            self.braille_selection_box_img, 
            330, 15, 
            on_click=self.toggle_braille_selection
        )

    def update_enabled(self, contraction, var):
        self.enabled_contractions[contraction]['enabled'] = var.get()
        # Optionally, write back to file
        with open(self.enabled_contractions_path, "w", encoding="utf-8") as f:
            json.dump(self.enabled_contractions, f, indent=4, ensure_ascii=False)

    def on_search_focus_in(self, event):
        if self.search_var.get() == self.placeholder_text:
            self.search_var.set("")
            self.search_entry.config(fg=self.fg)

    def on_search_focus_out(self, event):
        if self.search_var.get().strip() == "":
            self.search_var.set(self.placeholder_text)
            self.search_entry.config(fg=self.fg)

            self.search_entry.selection_clear()
            self.root.focus()  # move focus somewhere else, here root

    def _on_mousewheel(self, event):
        # For Windows, event.delta is multiples of 120
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")


    def build_contraction_library(self):
        #Search bar for contraction library
        self.search_var = tk.StringVar()
        self.placeholder_text = "Search here:"
        self.search_var.set(self.placeholder_text)  # placeholder


        self.search_entry = tk.Entry(
            self.contraction_library_frame,
            textvariable=self.search_var,
            font=("Roboto Condensed", 16),
            fg=self.fg,
            bg=self.bg,
            highlightbackground=self.hbg,
            highlightthickness=self.hth,
            bd=1,
            relief="solid"
        )
        self.search_entry.place(x=10, y=63, width=315, height=60)

        self.search_entry.bind("<FocusIn>", self.on_search_focus_in)
        self.search_entry.bind("<FocusOut>", self.on_search_focus_out)

        self.contraction_library_frame.bind("<Button-1>", self.on_search_focus_out)

        # Scrollable frame for contraction list
        contraction_list_frame = tk.Frame(
            self.contraction_library_frame, 
            bg=self.bg
        )
        contraction_list_frame.place(x=15, y=130, width=435, height=350)

        self.canvas = tk.Canvas(
            contraction_list_frame, 
            bg=self.bg, 
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            contraction_list_frame, 
            orient="vertical", 
            command=self.canvas.yview
        )

        self.scrollable_frame = tk.Frame(
            self.canvas, 
            bg=self.bg
        )
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window(
            (0, 0), 
            window=self.scrollable_frame, 
            anchor="nw"
        )
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.canvas.bind("<MouseWheel>", self._on_mousewheel)


        contraction_labels = []
        self.contraction_vars = {}  # To keep track of each checkbox variable
        self.original_contractions_order = sorted(
            self.enabled_contractions.keys(), 
            key=str.lower
        )
        self.contraction_labels_dict = {}

        for contraction in self.original_contractions_order:
            data = self.enabled_contractions[contraction]
            var = tk.IntVar(value=data['enabled'])
            self.contraction_vars[contraction] = var

            # Checkbox with label showing contraction + braille
            cb = tk.Checkbutton(
                self.scrollable_frame,
                text=f"{contraction.capitalize()}   ({data['braille']})",
                variable=var,
                onvalue=1,
                offvalue=0,
                anchor="w",
                fg=self.fg,
                bg=self.bg,
                selectcolor=self.bg,
                highlightbackground=self.hbg,
                highlightthickness=self.hth,
                font=("Roboto Condensed", 14),
                command=lambda c=contraction, v=var: self.update_enabled(c, v)
            )
            cb.pack(fill="x", padx=5, pady=2)

            contraction_labels.append((var, cb, contraction))
            self.contraction_labels_dict[contraction] = (var, cb, contraction)

            
        select_all_btn = tk.Button(
            self.contraction_library_frame,
            text="Select All",
            font=("Roboto Condensed", 14),
            fg=self.fg,
            bg=self.bg,
            highlightbackground=self.hbg,
            highlightthickness=self.hth,
            command=self.select_all_contractions
        )
        select_all_btn.place(x=331, y=63, width=120, height=28)

        deselect_all_btn = tk.Button(
            self.contraction_library_frame,
            text="Deselect All",
            font=("Roboto Condensed", 14),
            fg=self.fg,
            bg=self.bg,
            highlightbackground=self.hbg,
            highlightthickness=self.hth,
            command=self.deselect_all_contractions
        )
        deselect_all_btn.place(x=331, y=95, width=120, height=28)

        # Bind the search_var so it updates automatically
        self.search_var.trace_add("write", self.update_contraction_display)

    def update_contraction_display(self, *args):
        search_term = self.search_var.get().lower().strip()

        # Hide all checkboxes first
        for contraction in self.original_contractions_order:
            var, chk, name = self.contraction_labels_dict[contraction]
            chk.pack_forget()

        # Determine which contractions to show
        if search_term == "" or search_term == self.placeholder_text.lower():
            # Show all in alphabetical order
            for contraction in sorted(self.original_contractions_order, key=str.lower):
                var, chk, name = self.contraction_labels_dict[contraction]
                chk.pack(fill="x", padx=5, pady=2)
            self.canvas.yview_moveto(0)
            return

        # Otherwise, filter dynamically
        filtered_contractions = [
            contraction for contraction in self.original_contractions_order
            if search_term in contraction.lower()
        ]

        filtered_contractions.sort(key=str.lower)

        first_match_widget = None
        for contraction in filtered_contractions:
            var, chk, name = self.contraction_labels_dict[contraction]
            chk.pack(fill="x", padx=5, pady=2)
            if not first_match_widget:
                first_match_widget = chk

        # Scroll to first match if exists
        if first_match_widget:
            self.canvas.update_idletasks()
            self.canvas.yview_moveto(first_match_widget.winfo_y() / self.scrollable_frame.winfo_height())
        else:
            self.canvas.yview_moveto(0)

    def select_all_contractions(self):
        for contraction, var in self.contraction_vars.items():
            var.set(1)
            self.enabled_contractions[contraction]['enabled'] = 1

        # Save once (not per checkbox)
        with open(self.enabled_contractions_path, "w", encoding="utf-8") as f:
            json.dump(self.enabled_contractions, f, indent=4, ensure_ascii=False)


    def deselect_all_contractions(self):
        for contraction, var in self.contraction_vars.items():
            var.set(0)
            self.enabled_contractions[contraction]['enabled'] = 0

        # Save once
        with open(self.enabled_contractions_path, "w", encoding="utf-8") as f:
            json.dump(self.enabled_contractions, f, indent=4, ensure_ascii=False)

    
    def create_error_popup(self, text):
        error_popup = tk.Toplevel(self.root)
        error_popup.title("Error or Output")
        error_popup.geometry("400x200")
        error_popup.grab_set()  # Make it modal
        error_popup.configure(bg=self.bg)

        max_width = 400

        error_label = tk.Label(
            error_popup,
            text=text,
            font=("Roboto Condensed", 14),
            bg=self.bg,
            fg=self.fg,
            wraplength=max_width-40,
            justify="left",
            padx=20,
            pady=20
        )
        error_label.pack(expand=True, fill="both")  # top padding, small gap below

        okay_button = tk.Button(
            error_popup, 
            text="Okay", 
            font=("Roboto Condensed", 12),
            bg=self.bg,
            fg=self.fg, 
            command=error_popup.destroy
        )
        okay_button.pack(pady=(0,10))



class IndividualBraillerView(IndividualBraillerViewBase):
    def __init__(self, root, app, brailler_name, THEMES, open_tab, ssh):
        super().__init__(root, app, brailler_name, THEMES, open_tab, ssh, theme_name="light")

class IndividualBraillerViewInverted(IndividualBraillerViewBase):
    def __init__(self, root, app, brailler_name, THEMES, open_tab, ssh):
        super().__init__(root, app, brailler_name, THEMES, open_tab, ssh, theme_name="dark")