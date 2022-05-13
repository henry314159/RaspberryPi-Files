# Import modules for time, access to sensor and bluetooth
import RPi.GPIO as GPIO          
from time import sleep
from smbus import SMBus
from bme280 import BME280
import bluetooth
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Init for motors
in1 = 24
in2 = 23
in3 = 17
in4 = 27
en1 = 25
en2 = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en1,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p1=GPIO.PWM(en1,1000)

GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
p2=GPIO.PWM(en2,1000)

p1.start(50)
p2.start(50)

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

# Create differential input between channel 0 and 1
#chan = AnalogIn(ads, ADS.P0, ADS.P1)



# Setup for bluetooth
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee" # default uuid

bluetooth.advertise_service(server_sock, "SampleServer", service_id=uuid,
                            service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE],
                            )

# Initialise the BME280
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus,i2c_addr=0x77)

# Get data and discard to avoid garbage first reading
temperature = bme280.get_temperature()
pressure = bme280.get_pressure()
humidity = bme280.get_humidity()
sleep(1)

while True:
    print("Waiting for connection on RFCOMM channel %d" % port)
    client_sock, client_info = server_sock.accept()
    print("Accepted connection from ", client_info)
    
    try:
        x= client_sock.recv(1024)
        if len(x)== 0:
            exit()
        x=str(x)[-2]
        print("received %s" % x)
        
        if x=='l':
            print("left")
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
            GPIO.output(in3,GPIO.HIGH)
            GPIO.output(in4,GPIO.LOW)

        elif x=='r':
            print("right")
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in4,GPIO.HIGH)

        elif x=='s':
            print("stop")
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.LOW)
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in4,GPIO.LOW)

        elif x=='f':
            print("forward")
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
            GPIO.output(in3,GPIO.HIGH)
            GPIO.output(in4,GPIO.LOW)        

        elif x=='b':
            print("backward")
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in4,GPIO.HIGH)

        elif x=='m':
            print("medium")
            p1.ChangeDutyCycle(50)
            p2.ChangeDutyCycle(50)

        elif x=='h':
            print("high")
            p1.ChangeDutyCycle(100)
            p2.ChangeDutyCycle(100)
     
        elif x=='e':
            GPIO.cleanup()
            exit()


        temperature = bme280.get_temperature()
        pressure = bme280.get_pressure()
        humidity = bme280.get_humidity()
        moisture = "wet"
        if chan.voltage > 1.9:
            moisture = "moist"
        if chan.voltage > 3:
            moisture = "dry"
        client_sock.send('{:05.2f} {:05.2f} {:05.2f} '.format(temperature, pressure, humidity)+moisture+'!')
        print("sending %s" % '{:05.2f}°C {:05.2f}hPa {:05.2f}% '.format(temperature, pressure, humidity)+moisture)

    except IOError:
        pass

    except KeyboardInterrupt:

        print("disconnected")

        client_sock.close()
        server_sock.close()
        print("all done")
        exit()

    sleep(0.2)
    

