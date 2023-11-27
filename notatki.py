from bs4 import BeautifulSoup
import requests
import folium

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

#zwrócić mapę z pinezką odnoszącą się do nazwy użytkownika podanego z klawiatury

#zwróci mapę z wszystkimi użytkownikami z danej listy (znajom
city= get_coordinates_of(city='Zamość')
map = folium.Map(
    location=city,
    tiles="OpenStreetMap",
    zoom_start=15
)
for item in nazwy_miejscowosci:
    folium.Marker(
        location=get_coordinates_of(city=item),
        popup='GEOINFORMATYKA RZĄDZI OU YEAAAH'

    ).add_to(map)
map.save('mapka.html')