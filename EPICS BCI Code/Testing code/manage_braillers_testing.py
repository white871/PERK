import tkinter as tk
import math
import os
import paramiko
import json
from scp import SCPClient
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

        self.wifi_name_file = "EPICS BCI Code/Data/wifi_name.txt"
        self.device_registry_path = "EPICS BCI Code/Data/device_registry.json"
        self.device_state_path = "EPICS BCI Code/Data/device_state.json"

        self.current_brailler_label = None
        self.current_brailler_name = None
        self.brailler_status_dots = {}

        self.STATUS_RADIUS = 6
        self.STATUS_GREEN = "#93c47d"
        self.STATUS_RED = "#e06666"

        self.CLIENT_USER = "perk"
        self.CLIENT_PASS = "perk"

        self.ssh = None

        self.HOST = "perkhost.local"
        self.HOST2 = "perkhost"   # or IP
        self.USER = "perkhost"
        self.PASS = "perk"

        self.load_registry()
        self.load_state()
        self.build_header()
        self.build_brailler_list()
        self.build_popup_menu()
        self.build_bottom_actions() 

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        try:
            # try shutting down wifi hotspot before exit
            if self.ssh:
                try:
                    self.run_command("nmcli connection down perk-hotspot")
                except:
                    pass

            # close ssh connection
            if self.ssh:
                self.ssh.close()
                self.ssh = None

        except Exception:
            pass

        self.root.destroy()


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

    def save_registry(self):
        with open(self.device_registry_path, "w") as f:
            json.dump(self.registry, f, indent=4)
                
    def save_state(self):
        with open(self.device_state_path, "w") as f:
            json.dump(self.state, f, indent=4)

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
            os.path.join(self.image_path, "PERK_Braille_Image_grey.png"), 
            size=(302,108)
        )

        perk_logo = create_label(
            self.root, 'nw', 
            img=self.perk_braille_img, 
            bd_width=0, 
            location=(695, 8)
        )

    def create_brailler_row(self, device_id, name, x, y):
        lbl = self.label_fn(
            self.brailler_frame,
            anchr="n",
            txt=name,
            font_txt="Roboto Condensed",
            font_size=18,
            bold="normal",
            backround=self.bg,
            location=(x, y)
        )

        lbl.config(cursor="hand2")
        lbl.bind("<Button-1>", lambda e: self.on_brailler_click(lbl, name, device_id))

        dot_canvas = tk.Canvas(
            self.brailler_frame,
            width=self.STATUS_RADIUS * 2,
            height=self.STATUS_RADIUS * 2,
            bg=self.bg,
            highlightthickness=0
        )
        dot_canvas.place(x=x + 120, y=y +10, anchor="nw")

        dot = dot_canvas.create_oval(
            0, 0,
            self.STATUS_RADIUS * 2,
            self.STATUS_RADIUS * 2,
            fill=self.STATUS_RED,
            outline=""
        )

        self.brailler_status_dots[device_id] = (dot_canvas, dot)

        self.set_brailler_status(device_id, "UNREACHABLE")

        return lbl

# Brailler list
    def build_brailler_list(self):
        self.brailler_frame = tk.Frame(
            self.root,
            bg=self.bg,
            highlightbackground=self.fg,   # border color
            highlightthickness=2           # border thickness
        )
        self.brailler_frame.place(x=80, y=240, width=890, height=280)
                
        start_y = 240
        bottom_limit = 500   # where bottom buttons start
        available_height = bottom_limit - start_y

        max_columns = 3
        total_rows = math.ceil(len(self.registry) / max_columns)

        row_height = available_height / total_rows  

        window_width = 890
        left_margin = 20
        right_margin = 20
        usable_width = window_width - left_margin - right_margin
        column_width = usable_width / max_columns

        #########EDIT HERE######## make it so it only populates this list once the start process is created
        for i, (device_id, info) in enumerate(self.registry.items()):
            name = info.get("name", device_id)

            row = i // max_columns
            col = i % max_columns

            x = col * column_width + 0.5 * column_width -10
            y = row * row_height + 20 

            self.create_brailler_row(device_id, name, x, y)

        # self.root.after(100, self.refresh_ui)

    def add_brailler_to_ui(self, device_id):
        if device_id not in self.registry:
            return


        # already exists in UI
        if device_id in self.brailler_status_dots:
            return

        index = len(self.brailler_status_dots)

        max_columns = 3
        start_y = 250
        left_margin = 110
        window_width = 1250
        column_width = (window_width - 220) / max_columns
        row_height = 100  # simple fixed spacing (important fix)

        row = index // max_columns
        col = index % max_columns

        x = left_margin + col * column_width
        y = start_y + row * row_height

        name = self.registry[device_id]["name"]

        self.create_brailler_row(device_id, name, x, y)    

#Brailler click
    def on_brailler_click(self, label, name, device_id):
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
        self.popup.place(x=80, y=540, width=890, height=50)
        self.popup.tkraise()
        self.current_brailler_label = label
        self.current_brailler_id = device_id
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
            highlightthickness=2
        )

        button_names= "Live Feed", "Contractions", "Remove Device", "Rename Device"
        x_positions=[30, 220, 450, 700]

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
            if name == "Contractions":
                lbl.bind("<Button-1>", lambda e: self.open_contractions())   
            if name == "Remove Device":
                lbl.bind("<Button-1>", lambda e: self.remove_device()) 
            if name == "Rename Device":
                lbl.bind("<Button-1>", lambda e: self.rename_device())     

    def open_contractions(self):
        if self.inverted:
            self.app.show_text_page_inverted(
                self.current_brailler_name,
                open_tab="contractions"
            )
        else:
            self.app.show_text_page(
                self.current_brailler_name,
                open_tab="contractions"
            )

    def remove_device(self):
        device_id = self.current_brailler_id

        if not device_id:
            return
        
        # Remove from registry
        if device_id in self.registry:
            del self.registry[device_id]

        # Remove from state
        if device_id in self.state:
            del self.state[device_id]

        # Remove status dot from UI
        if device_id in self.brailler_status_dots:
            canvas, _ = self.brailler_status_dots[device_id]
            canvas.destroy()
            del self.brailler_status_dots[device_id]

        # Remove label from UI
        if self.current_brailler_label:
            self.current_brailler_label.destroy()

        # Clear current selection
        self.current_brailler_label = None
        self.current_brailler_id = None
        self.current_brailler_name = None

        # Hide popup
        self.popup.place_forget()

        # Save changes
        self.save_registry()
        self.save_state()

        self.brailler_frame.destroy()
        self.build_brailler_list()


#Status management
    def set_brailler_status(self, device_id, status):
        if device_id not in self.brailler_status_dots:
            return

        canvas, dot = self.brailler_status_dots[device_id]
       
        connected = (status == "REACHABLE")

        color = self.STATUS_GREEN if connected else self.STATUS_RED
        
        canvas.itemconfig(dot, fill=color)
    

    def refresh_ui(self):

        self.scan_and_update_devices()

        for device_id in self.registry:
            status = self.state.get(device_id, {}).get("status", "UNREACHABLE")
            self.set_brailler_status(device_id, status)

    def scan_and_update_devices(self):
        for device_id in self.registry:
            if device_id not in self.state:
                self.state[device_id] = {}

            self.state[device_id]["status"] = "UNREACHABLE"

        self.run_command("nmap -sn 192.168.4.0/24") # Or use fping

        scan_cmd = "ip neigh show dev wlan0"
        out = self.run_command(scan_cmd)
        self.create_error_popup(out)

        for line in out.splitlines():
            parts = line.split()

            if len(parts) < 3:
                continue

            ip = parts[0]
            status = parts[-1]

            if status == "REACHABLE":
                try:

                    out = self.run_command(f"scp perk@{ip}:~/name.txt {ip}_name.txt")

                    self.create_error_popup(out)

                    # Step 2 (your PC pulls from host Pi)
                    scp = SCPClient(self.ssh.get_transport())
                    scp.get(f"{ip}_name.txt", f"{ip}_name.txt")

                    # read it
                    with open(f"{ip}_name.txt", "r") as f:
                        device_id = f.read().strip()

                    if not device_id:
                        self.create_error_popup("No device ID available")
                        return

                    self.state[device_id] = {
                        "ip": ip,
                        "status": "REACHABLE"
                    }

                    if device_id not in self.registry:
                        self.registry[device_id] = {
                            "name": device_id
                        }
                    
                        self.add_brailler_to_ui(device_id)

                except (paramiko.SSHException, FileNotFoundError, Exception):
                    # ignore devices that don't respond
                    self.create_error_popup("SSH to client pi failed")
                    continue

        else:
            # Mark as unreachable in the UI dots
            for dev_id, info in self.state.items():
                if info.get("ip") == ip:
                    self.state[dev_id]["status"] = "UNREACHABLE"

        self.save_state()
        self.save_registry()

#Button actions
    def open_live_feed(self):
        if self.inverted:
            self.app.show_text_page_inverted(self.current_brailler_name)
        else:
            self.app.show_text_page(self.current_brailler_name)

    ###############EDIT HERE######### make it so when you rename something is passes that info to the host pi ???
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
        
        if not new_name:
            self.rename_popup.destroy()
            return
    
        device_id = self.current_brailler_id
        old_name = self.current_brailler_name

        # Update label text
        self.current_brailler_label.config(text=new_name)

        # Update registry 
        if device_id in self.registry:
            self.registry[device_id]["name"] = new_name
        else:
            # fallback safety
            self.registry[device_id] = {"name": new_name}

        self.save_registry()

        # Update current name reference
        self.current_brailler_name = new_name

        self.rename_popup.destroy()
    
    #Bottom actions
    def build_bottom_actions(self):
        # Manage Braillers row
        self.home_image = load_img(
            os.path.join(self.image_path, "Home_icon.png"), 
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
            
        self.bluetooth_image = load_img(
            os.path.join(self.image_path, "Bluetooth_icon.png"), 
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
            os.path.join(self.image_path, "settings_icon.png"), 
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

        
        self.refresh_img = load_img(
            os.path.join(self.image_path, "refresh_button.png"), 
            size=(166, 50)
        )

        new_file_icon = make_interactive_image(
            self.root, 
            self.refresh_img, 
            780, 175, 
            on_click=lambda: self.refresh_ui()
        )

    ###########EDIT HERE######## make it so when you do this it actually ssh s to the pi to start the wifi using wifi name 
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
        self.wifi_name = self.entry_var.get().strip()

        self.close_popup(self.wifi_popup)

        self.ssh = self.connect_ssh()

        # if not self.ssh:
        #    return
        
        self.setup_wifi()


        #LOTS OF STUFF HAPPENS HERE

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

    def setup_wifi(self):
        self.FULLNAME = "perk-" + self.wifi_name
        self.PASSWORD = "perk12345"

        set_up_wifi = f"sudo nmcli device wifi hotspot ssid {self.FULLNAME} password {self.PASSWORD}"
        
        out = self.run_command(set_up_wifi)

        self.create_error_popup(out)

        self.refresh_ui()

    def connect_ssh(self):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.HOST, username=self.USER, password=self.PASS)
            return ssh
        except Exception as e:
            self.create_error_popup(f"BCI Connection Failed:\n{e}")
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(self.HOST2, username=self.USER, password=self.PASS)
                return ssh
            except Exception as e:
                self.create_error_popup(f"BCI Connection Failed:\n{e}")
                return
                
        


class ManageBraillersView(ManageBraillersViewBase):
    def __init__(self, root, app, THEMES):
        super().__init__(root, app, THEMES, theme_name="light")

class ManageBraillersViewInverted(ManageBraillersViewBase):
    def __init__(self, root, app, THEMES):
        super().__init__(root, app, THEMES, theme_name="dark")