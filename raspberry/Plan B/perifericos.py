try:                                                                      
    from threading import Thread                                          
except ImportError:                                                       
    LlenarLogAuditoria("Se requiere el modulo threading")


from sensor import *
from Server import *
from properties import *
from controlPines import *
from Util import *



propiedades = properties()


servidor = Server("https://paul.fcv.org:8443/Senint2/serverB")  ##https://paul.fcv.org:8443/Senint2/serverB     ##http://172.16.66.84:8084/Senint2/serverB
umbralTemp = servidor.umbralTemp()
umbralHume = servidor.umbralHume()


alarmaSilenciosa = puertosGPIO(propiedades.AlarmaSilenciosa,"OUT", 1)
sensorDHT22 = Sensor(Adafruit_DHT.DHT22, propiedades.DHTpin)
rele = puertosGPIO(propiedades.RelePin,"OUT")
rele.desactivarAlarma()
segundoEnviadoDatosServidorSistemaNormal = propiedades.NumeroSegundosSinAlarma


claseUtil = Util(servidor, segundoEnviadoDatosServidorSistemaNormal, rele)


def HiloSegundoPlano():
    alarmado = False
    alarmado2 = False
    conteoBien = 0
    conteoBien2 = 0
    while True:
        alarmado, conteoBien, conteoBien2, alarmado2 = cicloInfinito(alarmado, conteoBien, conteoBien2, alarmado2)
        

def cicloInfinito(alarmado = False, conteoBien = 0, conteoBien2 = 0, alarmado2 = False):
    humedad, temperatura = sensorDHT22.LeerHumedadTemperatura()
    
    conteoBien, alarmado = claseUtil.evaluarDatos(temperatura, conteoBien, alarmado, umbralTemp, 0.5 , 'T')
    conteoBien2, alarmado2 = claseUtil.evaluarDatos(humedad, conteoBien2, alarmado2, umbralHume, 5, 'H' )
               
    time.sleep(30)
    return alarmado, conteoBien, conteoBien2, alarmado2

claseUtil.LlenarLogAuditoria("******************* Perifericos iniciados *******************")
Thread(target=HiloSegundoPlano).start()

