import requests
from bs4 import BeautifulSoup

def get_url_paths(url, ext='', params={}):
    response = requests.get(url, params=params)
    if response.ok:
        response_text = response.text
    else:
        return response.raise_for_status()
    soup = BeautifulSoup(response_text, 'html.parser')
    #parent = [url + node.get('href') for node in soup.find_all('a') if node.get('href')]
    parent = [node.get('href') for node in soup.find_all('a') if node.get('href')]
    return parent

#url = 'http://cdimage.debian.org/debian-cd/8.2.0-live/i386/iso-hybrid'
url = 'http://174.1.51.98:4040/Full/'
ext = 'iso'
result = get_url_paths(url, ext)
print(result)