import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime


ano = datetime.now().strftime('%Y')
mes = datetime.now().strftime('%m')
dia = datetime.now().strftime('%d')
hora = datetime.now().strftime('%H')

url1 = sys.argv[1]


def check_parameters(parameters2):
    if len(parameters2) == 2:
        pass
    else:
        print('Argumentos equivocados')
        sys.exit(1)


def get_arcos(url2):
    response = requests.get('http://' + url2)
    if response.ok:
        response_text = response.text
    else:
        return response.raise_for_status()
    soup = BeautifulSoup(response_text, 'html.parser')
    arcos1 = [node.get('href')[:-1] for node in soup.find_all('a') if node.get('href')]
    return arcos1
    

def verify_arcos(url2, arcos3):
    lista_arcos = [ 0, '' ]
    for i in arcos3:
        response = requests.get('http://' + url2 + i + "/" + ano + "/" + mes + "/" + dia)
        #response = requests.get('http://' + url2 + i + "/" + ano + "/" + mes + "/" + dia + "/" + hora) # Comprobar si existen fotos de la hora actual
        if response.status_code != 200:
            lista_arcos[0] += 1
            lista_arcos[1] = lista_arcos[1] + i + ', '
    lista_arcos[1] = lista_arcos[1][:-2]
    return lista_arcos


def main(lista_arcos3):
    if lista_arcos3[0] == 0:
        print("OK: Todos los arcos tienen fotos")
        sys.exit(0)
    elif lista_arcos3[0] <= 12:
        print("WARNING: " + str(lista_arcos3[0]) + " Arcos tienen fotos:" + lista_arcos3[1])
        sys.exit(1)
    else:
        print("CRITICAL: " + str(lista_arcos3[0]) + " Arcos no tienen fotos:" + lista_arcos3[1])
        sys.exit(2)


if __name__ == '__main__':
    check_parameters(sys.argv)
    arcos2 = get_arcos(url1)
    lista_arcos2 = verify_arcos(url1, arcos2)
    main(lista_arcos2)