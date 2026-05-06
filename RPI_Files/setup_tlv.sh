ADDR=0x18
BUS=1

write() {
    sudo i2cset -y $BUS $ADDR $1 $2
}
write 0x00 0x00 # Ensure reg is on page 0

write 0x01 0x01 # Reset Software
sleep 0.1
# Clock Gen
write 0x04 0x07 # PLL_CLK = BCLK, CODEC = PLL_CLK

# PLL Values - 44100 hz
write 0x05 0x93 # Power and set P & R (1, 3)
write 0x06 0x0A # J value (10)
write 0x07 0x00
write 0x08 0x00

write 0x0B 0x85 # NDAC Power, = 5
write 0x0C 0x83 # MDAC Power, = 3
write 0x0D 0x00 # DOSR (Upper)
write 0x0E 0x80 # DOSR (Lower), = 128

write 0x1B 0x00 # Codec config, I2s slave, 16-bit

# DAC Datapath
write 0x3F 0xFA # Power both channels, set to L+R / 2
write 0x40 0x00 # Unmute DAC channels, ind. volume control
write 0x41 0xD4 # -22db Left - EDIT FOR VOLUME CONTROL
write 0x42 0xD4 # -22db Right - EDIT FOR VOLUME CONTROL

#write 0x74 0x80 # Set ADC for pot. vol control

write 0x00 0x01 # Pg 1

# Speaker Config
#write 0x20 0x86 # Speaker Driver on
#write 0x23 0x44 # DAC Channels to mixer amps
#write 0x26 0x80 # Left analog volume to speaker
#write 0x2A 0x04 # Unmute driver
#write 0x2e 0x0b
#write 0x1F 0xC4 #Headphone driver on
#write 0x23 0x44 # Dac to mixer
#write 0x24 0x80 # Analog to headphones
#write 0x25 0x80
#write 0x28 0x06 # Unmute headphones
#write 0x29 0x06
