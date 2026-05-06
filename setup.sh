
unzip Perk_RPI.zip
rm Perk_RPI.zip
echo "Done."

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

echo -n 'Enabling i2s...'
echo 'dtoverlay=i2s-dac' | sudo tee -a /boot/firmware/config.txt
sudo sed -i 's/^#dtparam=i2s=on/dtparam=i2s=on/' /boot/firmware/config.txt
echo 'Done.' 

echo "Pi Ready!."
echo "The Pi will reboot now."

sudo reboot now