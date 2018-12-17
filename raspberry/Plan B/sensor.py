from properties import *
#https://github.com/adafruit/Adafruit_Python_DHT
#sudo apt-get update
#sudo apt-get install python3-pip
#sudo python3 -m pip install --upgrade pip setuptools wheel
#sudo pip3 install Adafruit_DHT
#git clone https://github.com/adafruit/Adafruit_Python_DHT.git
#cd Adafruit_Python_DHT
#sudo python3 setup.py install



import Adafruit_DHT


class Sensor:
    def __init__(self, sensor, pin):
        self.sensor = sensor       
        self.pin = pin       
        
    def LeerHumedadTemperatura(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
        if humidity is not None and temperature is not None:
            temperatura = float(format(temperature,'0.3f'))
            humedad = float(format(humidity,'0.3f'))
            return humedad, temperatura
        else:
            return 0,0
            print('Failed to get reading. Try again!')
