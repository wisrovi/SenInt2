import RPi.GPIO as GPIO
import time
import os  
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class puertosGPIO:    
    def __init__(self, pin, modo,default=1):
        self.pin = pin
        self.default = default
        if modo=="OUT":                        
            GPIO.setup(self.pin,GPIO.OUT)
            if self.default==0:
                self.desactivarAlarma()
            
    def blink(self,ciclos, tiempo):
        if self.default==1:
            #print( "Ejecucion iniciada...")
            iteracion = 0
            while iteracion < ciclos: ## Segundos que durara la funcion
                GPIO.output(self.pin, True)
                #print("prende")
                time.sleep(tiempo) ## Esperamos 1 segundo
                GPIO.output(self.pin, False)
                #print("apaga")
                time.sleep(tiempo) ## Esperamos 1 segundo
                iteracion = iteracion + 1
            #print("Ejecucion finalizada")
        else:
            print("Este pin no tiene la opcion de BLINK, para darle esta opcion, configurelo con 'default=1' ")
            
    def finalizoGPIO():
        GPIO.cleanup() ## Hago una limpieza de los GPIO
    
    def activarAlarma(self):
        os.system("gpio -g mode %d out" % self.pin)
        
    def desactivarAlarma(self):
        os.system("gpio -g mode %d in" % self.pin)
        
    def inactivarAlarma(self):
        os.system("gpio -g mode %d off" % self.pin)
        
