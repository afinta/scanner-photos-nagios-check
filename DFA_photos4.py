import sys
from datetime import datetime
import argparse
import requests
from bs4 import BeautifulSoup


ano = datetime.now().strftime("%Y")
mes = datetime.now().strftime("%m")
dia = datetime.now().strftime("%d")
hora = datetime.now().strftime("%H")

parser = argparse.ArgumentParser()
parser.add_argument("--url", type=str, required=True)
parser.add_argument("-w", type=int, required=True)
parser.add_argument("-c", type=int, required=True)
args = parser.parse_args()


def get_arcos_list(url2):
    try:
        response = requests.get(url2, timeout=30)
        response.raise_for_status()  # Salta para codigos 400 y 500 y lleva al ultimo except
    except requests.exceptions.Timeout:
        print("La web no ha respondido en 30 segundos")
        sys.exit(1)
    except requests.exceptions.TooManyRedirects:
        print("Too many redirects")
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        # catastrophic error. bail.
        #raise SystemExit(err) from err
        print(err)
        sys.exit(2)
    soup = BeautifulSoup(response.text, "html.parser")
    arcos1 = [node.get("href")[:-1] for node in soup.find_all("a") if node.get("href")]
    return arcos1


def get_arcos_photos(url2, arcos3):
    arcos_photos = [
        0,
        "",
    ]  # numero de arcos sin fotos y string de los nombres de arcos sin fotos.
    for i in arcos3:
        try:
            response = requests.get(
                url2 + i + "/" + ano + "/" + mes + "/" + dia, timeout=30
            )
            response.raise_for_status()  # Salta para codigos 400 y 500 y lleva al ultimo except
        except requests.exceptions.Timeout:
            print("La web no ha respondido en 30 segundos")
            sys.exit(1)
        except requests.exceptions.TooManyRedirects:
            print("Too many redirects")
            sys.exit(1)
        except requests.exceptions.HTTPError:
            if (
                response.status_code == 404
            ):  # no existe la carpeta de fotos del dia anterior.
                arcos_photos[0] += 1
                arcos_photos[1] = arcos_photos[1] + i + ", "
        except requests.exceptions.RequestException as err2:
            # catastrophic error. bail.
            #raise SystemExit(err2) from err2
            print(err)
            sys.exit(2)
    arcos_photos[1] = arcos_photos[1][:-2]
    return arcos_photos


def print_results(lista_arcos3):
    if lista_arcos3[0] < args.w:
        print("OK: Todos los arcos tienen fotos")
        sys.exit(0)
    elif lista_arcos3[0] >= args.w and lista_arcos3[0] < args.c:
        print(
            "WARNING: "
            + str(lista_arcos3[0])
            + " Arcos no tienen fotos:"
            + lista_arcos3[1]
        )
        sys.exit(1)
    elif lista_arcos3[0] >= args.c:
        print(
            "CRITICAL: "
            + str(lista_arcos3[0])
            + " Arcos no tienen fotos:"
            + lista_arcos3[1]
        )
        sys.exit(2)


def main():
    # verify_connection(args.url)
    arcos2 = get_arcos_list(args.url)
    lista_arcos2 = get_arcos_photos(args.url, arcos2)
    print_results(lista_arcos2)


if __name__ == "__main__":
    main()
