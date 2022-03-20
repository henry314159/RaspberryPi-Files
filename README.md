# RaspberryPi Files

Python script to be run on Raspberry Pi for our PAPi competition submission.

Once the pi is on run this command in command prompt to connect to it:
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
cd RaspberryPi-Files/
sudo python setup.py
```

# Common Errors

If you get an error like this: 
<span style="color:red">"bluetooth.btcommon.BluetoothError: no advertisable device"</span>
simply run `sudo hciconfig hci0 piscan` again as it has just been timed out.

If you get an error like this:
<span style="color:red">"bluetooth.btcommon.BluetoothError: [Errno 2] No such file or directory"</span>
run `sudo nano /etc/systemd/system/dbus-org.bluez.service` then change the line that looks like this:
ExecStart=/usr/lib/bluetooth/bluetoothd
to something like this:
ExecStart=/usr/lib/bluetooth/bluetoothd -C

If everything seems to be working, but the 'PI DATA' part of the app keeps crashing, try to follow [this](https://thepihut.com/blogs/raspberry-pi-tutorials/19668676-renaming-your-raspberry-pi-the-hostname) tutorial to change the hostname of the Raspberry Pi to 'raspberrypi-0'.
