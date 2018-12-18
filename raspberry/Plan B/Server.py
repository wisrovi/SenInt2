import requests

class Server:
    def __init__(self, url, umbralT=0, umbralH=0):
        self.url = url
        self.umbralT = umbralT
        self.umbralH = umbralH
        
    def sendGet(self, parametros, certificados = True):        
        urlEnviar = self.url + parametros
        req = ""
        if certificados:
            certificadosServidor = "ca.crt"
            req = requests.get(urlEnviar, verify=certificadosServidor)
        else:
            req = requests.get(urlEnviar)
        return req
        
    def umbralTemp(self):
        req = self.sendGet("?umbral=T")
        self.umbralT = float(req.text)
        return self.umbralT
    
    def umbralHume(self):
        req = self.sendGet("?umbral=H")
        self.umbralH = float(req.text)
        return self.umbralH