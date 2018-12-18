import os
import datetime
from os.path import isfile, join   

class Util:
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
