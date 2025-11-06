# PERK
This is the software repository for the PERK project under the RPVI team for Purdue's design program EPICS. <br>
In this README, brief descriptions on each directory, guides for building the executible, and updating the scripts for the Raspberry Pi are provided. <br>
This repository also serves as backup to the Raspberry Pi's files, please ensure that the Python scripts for the Pi on both the repository and on the Pi are consistent with each other. <br>

## Setting Up a New Pi
### Installing Raspberry Pi OS
- If setting up a Raspberry Pi 4 is required, download the Pi imager here: https://www.raspberrypi.com/software/. You also need a blank micro-SD card to install the Pi OS on.
- Set both the hostname and password to "Perk", SSH MUST be enabled. To use the Pi, you need a HDMI to microHDMI cable and a mouse and keyboard, and a USB-C cable to power the Pi.
### Enabling USB-Gadget
- To allow the Pi to work with the executible, the executible must be able to SSH into the Pi using the power USB-C port.
- First, go to boot/firmware/config.txt, ensure the line "dtoverlay=dwc2" is in the file
- Then, go to boot/firmware/cmdline.txt, add "module-line=dwc2,g_ether" after "rootwait"
- Reboot the Pi. Type "sudo reboot now" in terminal to properly do this.
- When the OS is rebooted, type in "ifconfig -a". If a "usb0" interface does not show up, type "sudo modprobe g_ether", run "ifconfig -a" again.
- If the usb0 interface disappears after rebooting, edit the /etc/modules file, add "dwc2" and "g_ether".
- Your computer should detect an "Ethernet Gadget" (Check device manager for windows under "Network Adapters", or "Network" on MacOS).
- You can now ssh into the Pi without an internet connection. Open up terminal and type "ssh perk@raspberrypi.local".
### Enabling I2S
- To use the speaker, you must enable the I2S protocol in the config file. Uncomment "dtparam=i2s=on" and "dtparam=audio=on"
- Finally, add "dtoverlay = hifiberry-dacplus"
- Reboot the Pi
- Keep in mind that pins 18, 19, 38, and 40 are now occupied for this protocol. Avoid using these pins for other external devices.

