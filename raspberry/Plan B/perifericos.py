try:                                                                      
    from threading import Thread                                          
except ImportError:                                                       
    LlenarLogAuditoria("Se requiere el modulo threading")


from sensor import *
from Server import *
from properties import *
from controlPines import *
from Util import *
claseUtil = Util()



propiedades = properties()


servidor = Server("https://paul.fcv.org:8443/Senint2/serverB")  ##https://paul.fcv.org:8443/Senint2/serverB     ##http://172.16.66.84:8084/Senint2/serverB
umbralTemp = servidor.umbralTemp()
umbralHume = servidor.umbralHume()

alarmaSilenciosa = puertosGPIO(propiedades.AlarmaSilenciosa,"OUT", 1)
sensorDHT22 = Sensor(Adafruit_DHT.DHT22, propiedades.DHTpin)
rele = puertosGPIO(propiedades.RelePin,"OUT")
rele.desactivarAlarma()
segundoEnviadoDatosServidorSistemaNormal = propiedades.NumeroSegundosSinAlarma




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
            claseUtil.LlenarLogAuditoria("Borrando archivos en alarma ON")
            alarmado = True
            if os.path.exists("0"):
                os.system("rm 0")
            if os.path.exists("1"):
                os.system("rm 1")     
        claseUtil.MostrarLogConsola("HOLA")
        if os.path.exists("0") == False:                
            rele.activarAlarma()
            claseUtil.LlenarLogAuditoria("Enviando datos al servidor, sistema alarmado")
            servidor.sendGet("?T=" + str(temperatura) + "&H="+str(humedad))
            time.sleep(30)
        claseUtil.LlenarLogAuditoria("¡Se calentó el chuzo!")        
        Thread(target=BlinkSilencioso).start()    
    else:
        if alarmado == True:
            alarmado = False
            claseUtil.LlenarLogAuditoria("Borrando archivos en alarma Off")
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
                claseUtil.LlenarLogAuditoria("Todo bien normalizando alarma")
                alarmado = False
        else:
            conteoBien = conteoBien + 1
            if conteoBien == 1:
                claseUtil.LlenarLogAuditoria("Enviando datos al servidor, sistema normal")
                servidor.sendGet("?T=" + str(temperatura) + "&H="+str(humedad))
            if conteoBien >= segundoEnviadoDatosServidorSistemaNormal:
                conteoBien = 0
            if os.path.exists("1") == False:
                rele.desactivarAlarma()
            datoImprimir = "Todo bien %s " %(str(segundoEnviadoDatosServidorSistemaNormal - conteoBien))
            claseUtil.LlenarLogAuditoria(datoImprimir)
            alarmado = False
        
        
        
    time.sleep(30)
    return alarmado, conteoBien

claseUtil.LlenarLogAuditoria("******************* Perifericos iniciados *******************")
Thread(target=HiloSegundoPlano).start()

