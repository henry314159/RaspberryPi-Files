# RaspberryPi Files
Python script to be run on Raspberry Pi for our PAPi competition submission.

Once the pi is on run this command to connect to it:
```
ssh pi@raspberrypi
```
Once you are in the Raspberry Pi's command line:
```
sudo apt-get install bluez python3-bluez -y
```
Then see [this](https://bluedot.readthedocs.io/en/latest/pairpiandroid.html) quick tutorial on how to pair your android device to the Raspberry Pi.
Now run these commands:
```
sudo raspi-config nonint do_i2c 0
sudo pip install pimoroni-bme280
git clone https://github.com/henry314159/RaspberryPi-Files.git
sudo hciconfig hci0 piscan
```
