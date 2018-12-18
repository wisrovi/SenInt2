import os
import datetime
from os.path import isfile, join   

def BlinkSilencioso():
    alarmaSilenciosa.blink(propiedades.NumeroParpadeosAlarmaSilenciosa, propiedades.TiempoParpadeoAlarmaSilenciosa)

class Util:
    
    def __init__(self, servidor, segundoEnviadoDatosServidorSistemaNormal, rele):
        self.servidor = servidor
        self.segundoEnviadoDatosServidorSistemaNormal = segundoEnviadoDatosServidorSistemaNormal
        self.rele = rele
        
    def MostrarLogConsola(self, datos):        
        comandoGuardar = 'echo "%s" >> /var/log/senint2.log ' %(datos)
        os.system(comandoGuardar)
        print(datos)
    
    def LlenarLogAuditoria(self, datos):        
        dateTimeActual = datetime.datetime.now()
        infoGuardar = '%s --> %s \n' %(str(dateTimeActual), datos)
        f=open("logAuditoria.bin",'a')
        f.write(infoGuardar)
        f.close()
        self.MostrarLogConsola(infoGuardar)
    
    def evaluarDatos(self, dato, conteo, banderaAlarma, umbral, tolerancia, etiqueta = 'T'):
        if umbral <= dato:
            conteo = 0
            if banderaAlarma == False:
                self.LlenarLogAuditoria("Borrando archivos en alarma ON")
                banderaAlarma = True
                if os.path.exists("0"):
                    os.system("rm 0")
                if os.path.exists("1"):
                    os.system("rm 1")     
            if os.path.exists("0") == False:                
                self.rele.activarAlarma()
                self.LlenarLogAuditoria("Enviando datos al servidor, sistema alarmado")
                self.servidor.sendGet("?"+ etiqueta + "=" + str(dato))
                time.sleep(30)
            self.LlenarLogAuditoria("¡Se calentó el chuzo!")        
            Thread(target=BlinkSilencioso).start()
        else:
            if banderaAlarma == True:
                banderaAlarma = False
                self.LlenarLogAuditoria("Borrando archivos en alarma Off")
                if os.path.exists("0"):
                    os.system("rm 0")
                if os.path.exists("1"):
                    os.system("rm 1")
            if banderaAlarma == True:
                umbralReducido = umbral - tolerancia
                if umbralReducido <= dato:   
                    conteo = conteo + 1
                    if os.path.exists("1") == False:
                        self.rele.desactivarAlarma()
                    self.LlenarLogAuditoria("Todo bien normalizando alarma")
                    banderaAlarma = False
            else:
                conteo = conteo + 1
                if conteo == 1:
                    self.LlenarLogAuditoria("Enviando datos al servidor, sistema normal")
                    self.servidor.sendGet("?"+ etiqueta + "=" + str(dato))
                if conteo >= self.segundoEnviadoDatosServidorSistemaNormal:
                    conteo = 0
                if os.path.exists("1") == False:
                    self.rele.desactivarAlarma()
                datoImprimir = "Todo bien %s  %s " %(etiqueta, str(self.segundoEnviadoDatosServidorSistemaNormal - conteo))
                self.LlenarLogAuditoria(datoImprimir)
                banderaAlarma = False
        return conteo, banderaAlarma
