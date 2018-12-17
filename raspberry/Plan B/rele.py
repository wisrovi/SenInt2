from properties import *
propiedades = properties()

from controlPines import *
rele = puertosGPIO(propiedades.RelePin,"OUT")
rele.desactivarAlarma()