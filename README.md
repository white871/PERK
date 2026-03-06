# PERK
This is the software repository for the PERK project under the RPVI team for Purdue's design program EPICS. <br>
In this README, brief descriptions on each directory, guides for building the executible, and updating the scripts for the Raspberry Pi are provided. <br>
This repository also serves as backup to the Raspberry Pi's files, please ensure that the Python scripts for the Pi on both the repository and on the Pi are consistent with each other. <br>

## Setting Up a New Pi
### Installing Raspberry Pi OS
- If setting up a Raspberry Pi 4 is required, download the Pi imager here: https://www.raspberrypi.com/software/.
- You also need a blank micro-SD card to install the Pi OS on.
- Below is what each configuration you MUST follow in each tab
- Device & OS: Select the correct model, then select Raspberry Pi OS (64-bit)
- Alternatively, if you are familiar with Linux terminals, install Pi Lite instead for faster bootup time (no desktop environment)
- Storage: It should be the SD card you inserted into your computer
- Hostname: perk
- Localization: Washington, D.C. for capital city; New_York for Time zone; and us for Keyboard layout (this is important, if you select the incorrect keyboard layout you most likely WILL have issues with your keyboard when typing in the Pi's terminal)
- User: perk, password: perk
- Wi-fi: Doesn't really matter, but do connect it to wifi for installing packages
- Remote Access: enable SSH, and select "Use password authentication"
- RPI connect doesn't matter <br> <br>
The proper config files should be in this repository for reference, but you can follow these steps if otherwise.
#### To allow the Pi to work with the executible, the executible must be able to SSH into the Pi using the power USB-C port.
### Enabling USB-Gadget  (SD Card)
- Note: as of 2026 with RPI Trixie, there's now a simpler way to enable USB-gadget on a Pi without accessing the OS, however the ethernet driver for windows is screwed up. 
- Access the SD card, and open "user-data" with a text editor (like notepad)
- Find the section that has "rpi:" with "enable_ssh:" below it
- <img width="244" height="58" alt="image" src="https://github.com/user-attachments/assets/46e6e9bd-0a51-4786-91c1-1d54ca724813" />
- Enter enable_usb_gadget: true
- If these steps do not work, then follow the steps below
### Enabling USB-Gadget  (OS)
- First, go to boot/firmware/config.txt, add the line "dtoverlay=dwc2" at the very bottom
- Comment out "otg_mode=1"
- Then, go to boot/firmware/cmdline.txt, add "module-line=dwc2,g_ether" after "rootwait"
- Reboot the Pi. Type "sudo reboot now" in terminal to properly do this.
- When the OS is rebooted, type in "ifconfig -a". If a "usb0" interface does not show up, type "sudo modprobe g_ether", run "ifconfig -a" again.
- If the usb0 interface disappears after rebooting, edit the /etc/modules file, add "dwc2" and "g_ether".
- Your computer should detect an "Ethernet Gadget" (Check device manager for windows under "Network Adapters", or "Network" on MacOS).
- You can now ssh into the Pi without an internet connection. Open up terminal and type "ssh perk@perk.local". If that doesn't work, try "ssh perk@perk"
For more information on setting up RPI gadget mode, you can look at this guide: https://www.raspberrypi.com/news/usb-gadget-mode-in-raspberry-pi-os-ssh-over-usb/
### Enabling I2S
- To use the speaker, you must enable the I2S protocol in the config file.
- Uncomment "dtparam=12s=on" and comment "dtparam=audio=on"
- Comment the vc4-kms-v3d dtoverlay and max_framebuffers, set disable_fw_kms_setup to 0
- Finally, add "dtoverlay = max98357a"
- Reboot the Pi
- Keep in mind that pins 18, 19, 38, and 40 are now occupied for this protocol. Avoid using these pins for other external devices.
- Next, to allow the sound architecture to recognize the i2s board to be controlled with software, go into root/etc and copy the asound.conf file. Restart, then do a speaker-test.
- Type "alsamixer" and there should be a software volume control interface for Softmaster
### Python Virtual Environment and Package Installation
- We're almost there. Now, for context, Linux doesn't like it when you try to download a python library with the entire system, so you'll have to create a virtual enviroment in order to run the TTS processes.
- First, type "python -m venv pyperk --system-site-packages", wait for it to setup, then type "source pyperk/bin/activate"
- "(pyperk)" should be preceeding perk@perk in the terminal now. You can install python packages now!
- This project uses Piper for clean TTS (https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/API_PYTHON.md), use pip install or python -m pip to install piper-tts
- Next, you'll need a voice. Run "python -m piper.download_voices en_US-amy-low".
- You can look at the documentation if you want to install other voices, however I recommend using only low quality TTS models since we're not working with a lot of processing power here.
#### That's it for the Raspberry Pi installation! Simple, right?
