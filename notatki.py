from bs4 import BeautifulSoup
import requests

nazwy_miejscowosci = ['Kraków','Mińsk Mazowiecki', 'Szczecin']
def get_coordinates_of(city:str)->list[float,float]:

    adres_URL = f'https://pl.wikipedia.org/wiki/{city}'
    response = requests.get(url=adres_URL)
    response_html = BeautifulSoup(response.text, 'html.parser')



    response_html_latitude = response_html.select('.latitude')[1].text
    response_html_latitude = float(response_html_latitude.replace(',','.'))
    response_html_longitude = response_html.select('.longitude')[1].text
    response_html_longitude = float(response_html_longitude.replace(',','.'))

    return [response_html_latitude, response_html_longitude]

for item in nazwy_miejscowosci:
    print(get_coordinates_of(item))