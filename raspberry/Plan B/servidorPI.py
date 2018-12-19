from flask import Flask, request
import os

from perifericos import *
from Util import *
servidor = Server("https://paul.fcv.org:8443/Senint2/serverB")

app = Flask(__name__)

def procesoApagarAlarma():
    rele.desactivarAlarma()
    
def procesoPrenderAlarma():
    rele.activarAlarma()
    
propiedades = properties()
claseUtil = Util(servidor, propiedades.NumeroSegundosSinAlarma, rele)
log = LogAuditoria()
    
@app.route('/Alarma1/ON', methods=['GET', 'POST'])
def Alarma1_ON():
    rele.activarAlarma()
    if os.path.exists("0"):
        os.system("rm 0")
    os.system("touch 1")
    log.LlenarLogAuditoria("Prendiendo alarma desde el servidor.")
    return '/Alarma1/ON'

@app.route('/Alarma1/OFF', methods=['GET', 'POST'])
def Alarma1_OFF():
    rele.desactivarAlarma()
    if os.path.exists("1"):
        os.system("rm 1")
    os.system("touch 0")
    log.LlenarLogAuditoria("Apagando alarma desde el servidor.")
    return '/Alarma1/OFF'

@app.route('/Correo', methods=['GET', 'POST'])
def Correo():    
    humedad, temperatura = sensorDHT22.LeerHumedadTemperatura()
    servidor.sendGet("?T=" + str(temperatura) + "&H="+str(humedad))
    log.LlenarLogAuditoria("Forzando Envio datos desde el servidor")
    return 'Correo'

@app.route('/Sensor', methods=['GET', 'POST'])
def Sensor():
    humedad, temperatura = sensorDHT22.LeerHumedadTemperatura()
    texto = 'H=%s&T=%s' %(str(humedad), str(temperatura))
    log.LlenarLogAuditoria("Leyendo sensor desde el servidor.")
    return texto

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    # Check if a valid image file was uploaded        
    if request.method == 'POST':
        claseUtil.MostrarLogConsola("solicitud POST")
        datoControl = request.form['namePost']
        if datoControl[:1] == "F":
            procesoApagarAlarma()
        if datoControl[:1] == "T":
            procesoPrenderAlarma()
            
    if request.method == 'GET':
        username = request.cookies.get('username')
        claseUtil.LlenarLogAuditoria("solicitud GET")
        datoControl = request.form['namePost']
        if datoControl[:1] == "F":
            procesoApagarAlarma()
        if datoControl[:1] == "T":
            procesoPrenderAlarma()            
        claseUtil.LlenarLogAuditoria(type(username))
    return '''
    <!doctype html>
	<h1>Servidor SENINT2</h1>
    '''

log.LlenarLogAuditoria("******************* Servidor iniciado *******************")
	
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2019, debug=True)