try:                                                                      
    from threading import Thread                                          
except ImportError:                                                       
    print("Se requiere el modulo threading")


from sensor import *
from Server import *
from properties import *
from controlPines import *




propiedades = properties()


servidor = Server("https://paul.fcv.org:8443/Senint2/serverB")  ##https://paul.fcv.org:8443/Senint2/serverB     ##http://172.16.66.84:8084/Senint2/serverB
umbralTemp = servidor.umbralTemp()
umbralHume = servidor.umbralHume()

alarmaSilenciosa = puertosGPIO(propiedades.AlarmaSilenciosa,"OUT", 1)
sensorDHT22 = Sensor(Adafruit_DHT.DHT22, propiedades.DHTpin)
rele = puertosGPIO(propiedades.RelePin,"OUT")
rele.desactivarAlarma()





def HiloSegundoPlano():
    alarmado = False
    conteoBien = 0
    while True:
        alarmado, conteoBien = cicloInfinito(alarmado, conteoBien)
        
def BlinkSilencioso():
    alarmaSilenciosa.blink(propiedades.NumeroParpadeosAlarmaSilenciosa, propiedades.TiempoParpadeoAlarmaSilenciosa)


def cicloInfinito(alarmado = False, conteoBien = 0):
    humedad, temperatura = sensorDHT22.LeerHumedadTemperatura()
    #print(humedad)
    #print(temperatura)
    if umbralTemp <= temperatura:
        conteoBien = 0
        if alarmado == False:
            print("Borrando archivos en alarma ON")
            alarmado = True
            if os.path.exists("0"):
                os.system("rm 0")
            if os.path.exists("1"):
                os.system("rm 1")     
        print("HOLA")
        if os.path.exists("0") == False:                
            rele.activarAlarma()
            servidor.sendGet("?T=" + str(temperatura) + "&H="+str(humedad))
            time.sleep(30)
        print("¡Se calentó el chuzo!")        
        Thread(target=BlinkSilencioso).start()    
    else:
        if alarmado == True:
            alarmado = False
            print("Borrando archivos en alarma Off")
            if os.path.exists("0"):
                os.system("rm 0")
            if os.path.exists("1"):
                os.system("rm 1")
        if alarmado == True:
            umbralReducido = umbralTemp - 0.5
            if umbralReducido <= temperatura:   
                conteoBien = conteoBien + 1
                if os.path.exists("1") == False:
                    rele.desactivarAlarma()
                print("Todo bien normalizando alarma")
                alarmado = False
        else:
            conteoBien = conteoBien + 1
            if conteoBien >= 480:
                conteoBien = 0
                servidor.sendGet("?T=" + str(temperatura) + "&H="+str(humedad))
            if os.path.exists("1") == False:
                rele.desactivarAlarma()
            print("Todo bien")
            alarmado = False
        
        
        
    time.sleep(30)
    return alarmado, conteoBien


Thread(target=HiloSegundoPlano).start()

