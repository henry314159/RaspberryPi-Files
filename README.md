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

Now enable i2c connection on the Raspberry Pi using [this](https://www.mathworks.com/help/supportpkg/raspberrypiio/ref/enablei2c.html) tutorial.

Now run these commands:
```
sudo pip install pimoroni-bme280
git clone https://github.com/henry314159/RaspberryPi-Files.git
sudo hciconfig hci0 piscan
cd RaspberryPi-Files/
sudo python setup.py
```

# Optional experimentation

If you want to make the setup.py script run on boot, edit the rc.local file by adding the following lines:
```
#!bin/bash
sleep 10
sudo hciconfig hci0 piscan
sleep 5
sudo python RaspberryPi-Files/setup.py

exit 0
```
The sleep commands are intended to allow the user time to connect to the raspberry pi with their device, and to allow the raspberry pi time to initialise bluetooth.

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
