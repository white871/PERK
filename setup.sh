if [ nmcli -t -f DEVICE,STATE device | grep "^wlan:0:unavailable" ]; then
    echo "Network unavailable. Setting WLAN Country to US"
    sudo raspi-config nonint do_wifi_country US
fi


echo -n "Setting up I2C..."
sudo raspi-config nonint do_i2c 0
echo "Done."

echo -n "Creating venv..."
python -m venv pyperk --system-site-packages
echo "Done."

echo "Installing PiperVoice"
pyperk/bin/python -m pip install piper-tts

echo "Installing amy-medium"
pyperk/bin/python -m piper.download_voices en_US-amy-medium

echo "Installing i2c-tools"
sudo apt-get install -y i2c-tools

echo "Packages installed. please go to root and add dtoverlay=i2s-dac in the firmware/config.txt file."
echo "The Pi will reboot now."

sudo reboot now