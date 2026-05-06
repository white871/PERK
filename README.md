# PERK
This is the software repository for the PERK project under the RPVI team for Purdue's design program EPICS. <br>
In this README, brief descriptions on each directory, guides for building the executible, and updating the scripts for the Raspberry Pi are provided. <br>
This repository also serves as backup to the Raspberry Pi's files, please ensure that the Python scripts for the Pi on both the repository and on the Pi are consistent with each other. <br>

## Setting Up a New Pi
### Installing Raspberry Pi OS
- If setting up a Raspberry Pi 4/ Zero 2 W is required, download the Pi imager here: https://www.raspberrypi.com/software/.
- After downloading the imager, do NOT open the imager yet. Instead, download the os image manifest and launch that instead, this will open the imager with an option needed for this project. 
- You also need a blank micro-SD card to install the Pi OS on.
- Below is what each configuration you MUST follow in each tab
- Device & OS: Select the correct model, then select Raspberry Pi OS (64-bit)
- Alternatively, if you are familiar with Linux terminals, install Pi Lite instead for faster bootup time (no desktop environment)
- Storage: It should be the SD card you inserted into your computer
- Hostname: perk (perkhost if host pi)
- Localization: Washington, D.C. for capital city; New_York for Time zone; and us for Keyboard layout (this is important, if you select the incorrect keyboard layout you most likely WILL have issues with your keyboard when typing in the Pi's terminal)
- User: perk, password: perk (For the host Pi, the user is perkhost)
- Wi-fi: Doesn't really matter, but do connect it to wifi for installing packages
- *NOTE* If you leave Wifi blank, youll have to manually enable it when working with the Pi (See https://www.raspberrypi.com/documentation/computers/configuration.html#wireless-connection)
- Remote Access: enable SSH, and select "Use password authentication"
- RPI connect doesn't matter
- Enable USB-Gadget (you'll get a warning, ignore it) <br> <br>
For more information on setting up RPI gadget mode, you can look at this guide: https://www.raspberrypi.com/news/usb-gadget-mode-in-raspberry-pi-os-ssh-over-usb/
### Host Pi (Perkhost)
- After setting up, run sudo apt-get install sshpass
- That's it!
### Setup.sh and Perk_RPI.zip (Client Pi)
- transfer setup.sh into the Pi AND Perk_RPI.zip (navigate to your directory containing setup.sh, then run "scp setup.sh perk@perk.local:~/setup.sh", then to the directory with Perk_RPI do the corresponding scp command)
- When editing ANY file in Raspberry Pi Files, you MUST compress all files into Perk_RPI before committing and pushing. Please keep the zip file updated!!
- With these two files, you can skip the below steps (besides building the exe) for setting up the client Pi.
- Run "bash setup.sh" and you should be good to go
- Next, for the program to run on boot, type "crontab -e", go to the bottom of the opened file and type "@reboot bash home/perk/bootup.sh"
### TLV320DAC3100 setup (speaker & headphones)
- Setup is simple, go into boot/firmware/config.txt and add "dtoverlay=i2s-dac"
- Uncomment 'dtparam=i2s=on'
- Enable i2c: When done with the config file, type "sudo raspi-config", and go into interfacing options and enable i2c
- Run 'sudo apt-get install -y i2c-tools'
- Install the bash script on the repository onto the Pi, run it using (bash setup_tlv) before doing anything else
- **Note, holding down the network search button switches between headphones and speaker. MAKE SURE THERE IS NO AUDIO JACK PLUGGED IN WHEN SWITCHING TO SPEAKER. It will blast your ears.**
### Max98357a setup (speaker only)
- To use this audio chip, you must enable the I2S protocol in the config file.
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
- Next, you'll need a voice. Run "python -m piper.download_voices en_US-amy-medium".
- You can look at the documentation if you want to install other voices, however I wouldn't recommend running high quality TTS models since they will take a while to load when running the audio python script. 

#### That's it for the Raspberry Pi installation! Simple, right?

#### Setting up an .exe file
- Make sure you have PyInstaller downloaded using pip install PyInstaller
- After, run this command in a terminal with the directory open: python -m PyInstaller --onefile --add-data "Data;Data" --add-data "Fonts;Fonts" --add-data "Images;Images" main.py
