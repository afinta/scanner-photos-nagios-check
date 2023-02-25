import requests
import sys
from datetime import datetime

ano = datetime.now().strftime('%Y')
mes = datetime.now().strftime('%m')
dia = datetime.now().strftime('%d')
hora = datetime.now().strftime('%H')

# Arcos de Llegadas
arcos = {
    "DFA410261": "174.1.98.11",
    "DFA420261": "174.1.98.12",
    "DFA430261": "174.1.98.13",
    "DFA440261": "174.1.98.14",
    "DFA450231": "174.1.98.15",
    "DFA460311": "174.1.98.16",
    "DFA470491": "174.1.98.17",
    "DFA480461": "174.1.98.18",
    "DFA210051": "174.1.98.21",
    "DFA220011": "174.1.98.22",
    "DFA230011": "174.1.98.23",
    "DFA240011": "174.1.98.24",
    "DFA250011": "174.1.98.25",
    "DFA260041": "174.1.98.26",
    "DFA270011": "174.1.98.27",
    "DFA280031": "174.1.98.28",
}

NoPhotos = 0
ArcosMalos = ""

for i in arcos:
    response = requests.get("http://174.1.51.98:4040/Full/" + i + "/" + ano + "/" + mes + "/" + dia)
    if response.status_code != 200:
        NoPhotos +=1
        ArcosMalos = ArcosMalos + i + ", "

# Quitar la ultima coma y espacio
ArcosMalos = ArcosMalos[:-2]

if NoPhotos == 0:
    print("OK: Todos los arcos de llegadas tienen fotos")
    sys.exit(0)
elif NoPhotos <= 12:
    print("WARNING: " + str(NoPhotos) + " Arcos de llegadas no tienen fotos:" + ArcosMalos)
    sys.exit(1)
else:
    print("CRITICAL: " + str(NoPhotos) + " Arcos de llegadas no tienen fotos:" + ArcosMalos)
    sys.exit(2)