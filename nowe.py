from bs4 import BeautifulSoup
from dotenv import load_dotenv
from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String
import os
import requests
import folium
from dane import users_list
import sqlalchemy.orm
from dml import db_params

# user = {"city": 'Hrubieszów', "name": "Agata", "nick": "AAA", "posts":1_00_000}

load_dotenv()
engine = sqlalchemy.create_engine(db_params)
connection = engine.connect()
Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()
Base = sqlalchemy.orm.declarative_base()

def get_coordinates_of(city:str)->list[float,float]:

    adres_URL = f'https://pl.wikipedia.org/wiki/{city}'
    response = requests.get(url=adres_URL)
    response_html = BeautifulSoup(response.text, 'html.parser')



    response_html_latitude = response_html.select('.latitude')[1].text
    response_html_latitude = float(response_html_latitude.replace(',','.'))
    response_html_longitude = response_html.select('.longitude')[1].text
    response_html_longitude = float(response_html_longitude.replace(',','.'))

    return [response_html_latitude, response_html_longitude]
def add_user_to(users_list:list) -> None:
    """
    add objcet to list
    :param users_list: lista  - user list
    :return: None
    """

    name = input('podaj imie ?')
    posts = input('podaj liczbe postow ?')
    users_list.append({'name':name,'posts':posts})

def remove_user_from(users_list: list) -> None:
    """
    remove object from list
    :param users_list: user list
    :return: None
    """
    tmp_list = []
    name = input('podaj imie uzytkownika do usuniecia: ')
    for user in users_list:
        if user["name"] == name:
            print(f'znaleziono uzytkownika {user}')
            tmp_list.append(user)
    print('znaleziono uzytkownikow:')
    print('0: Usun wszytskich znalezionych uzytkownikow')
    for numerek, user_to_be_removed in enumerate(tmp_list):
        print(f'{numerek + 1}. {user_to_be_removed}')
    numer = int(input(f'wybierz numer uzytkownika do usuniecia: '))
    if numer == 0:
        for user in users_list:
            if user['name'] == name:
                users_list.remove(user)
    else:
        users_list.remove(tmp_list[numer - 1])

def show_users_from(users_list:list)->None:
    for user in users_list:
        print(f'twoj znajomy {user["name"]} dodal {user["posts"]}')

def update_user(users_list: list[dict, dict]) -> None:
    nick_of_user = input('podaj nick użytkownika do modyfikacji')
    print(nick_of_user)
    for user in users_list:
        if user['nick'] == nick_of_user:
            print('Znaleziono!!!!')
            user['name'] = input('podaj nowe imie: ')
            user['nick'] = input('podaj nowa ksywke: ')
            user['posts'] = int(input('podaj liczbę postów: '))
def get_map_one_user(user) -> None:
    city = get_coordinates_of(user['city'])
    map = folium.Map(
        location=city,
        tiles='OpenStreetMap',
        zoom_start=15,
    )
    folium.Marker(
        location=city,
        popup=f'Tu rządzi: {user["name"]},'
              f'postów: {user["posts"]}'
    ).add_to(map)
    map.save(f'mapka_{user["name"]}.html')

def get_map_of(users) -> None:
        map = folium.Map(
            location=[52.3, 21.0],
            tiles="OpenStreetMap",
            zoom_start=7,
        )
        for user in users:
            folium.Marker(
                location=get_coordinates_of(city=user['city']),
                popup=f'Użytkownik: {user["name"]} \n'                  
                      f'Liczba postów {user["posts"]}'
            ).add_to(map)
        map.save('mapkaaaaa.html')
def pogoda(town:str):
    url = f"https://danepubliczne.imgw.pl/api/data/synop/station/{town}"
    return requests.get(url).json()

###################### SQL ###############################

class User(Base):
    __tablename__ = 'main_table'

    id = Column(Integer(),primary_key=True)
    posts = Column(Integer(), nullable=True)
    name = Column(String(100), nullable=True)
    nick = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    location = Column('geom', Geometry(geometry_type='POINT', srid=4326), nullable=True)

def aktualiacja(lista, db_params):
    engine = sqlalchemy.create_engine(db_params)
    connection = engine.connect()
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()

    users_list: list =[]
    for user in lista:
        city = get_coordinates_of(user['city'])
        users_list.append(
            User(
                name=user['name'],
                posts=user['posts'],
                nick=user['nick'],
                city=user['city'],
                location=f'POINT({city[1]} {city[0]})'
            )
        )
    session.add_all(users_list)
    session.commit()

def add_user_to_table(lista, db_params):
    engine = sqlalchemy.create_engine(db_params)
    connection = engine.connect()
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()

    Base = sqlalchemy.orm.declarative_base()

    class User(Base):
        __tablename__ = 'Lista_uzytkownikow'

        id = Column(Integer(), primary_key=True)
        posts = Column(Integer(), nullable=True)
        name = Column(String(100), nullable=True)
        nick = Column(String(100), nullable=True)
        city = Column(String(100), nullable=True)
        location = Column('geom', Geometry(geometry_type='POINT', srid=4326), nullable=True)

    Base.metadata.create_all(engine)

    users_list: list = []

    for user in lista:
        city = get_coordinates_of (user['city'])
        users_list.append(
            User(
                name=user['name'],
                posts=user['posts'],
                nick=user['nick'],
                city=user['city'],
                location=f'POINT({city[1]} {city[0]})'
            )
        )
    session.add_all(users_list)
    session.commit()

def dodaj_usera(lissta, db_params):
    engine = sqlalchemy.create_engine(db_params)
    connection = engine.connect()

    name = input('Imie: ')
    nick = input('Nick: ')
    post = int(input('Liczba postow: '))
    city = input('Miasto: ')
    lissta.append({"name": name, "nick": nick, "posts": post, 'city': city})
    local = get_coordinates_of(city)
    sql_query = sqlalchemy.text(
        f"INSERT INTO public.user_list(name, nick, city, posts, geom) VALUES ('{name}', '{nick}', '{city}', '{post}', 'POINT({local[1]} {local[0]})');")

    connection.execute(sql_query)
    connection.commit()
def zmien_dane(lista, db_params):
    engine = sqlalchemy.create_engine(db_params)
    connection = engine.connect()

    user_nick = input('Podaj nick użytkownika ')
    print(f' {user_nick}')
    for user in lista:
        if user['nick'] == user_nick:
            print('Wyszukano')
            nowe_imie = input('Podaj nowe imię użytkownika ')
            user['name'] = nowe_imie
            nowy_nick = input('Podaj nowy nick użytkownika ')
            user['nick'] = nowy_nick
            nowa_liczba_postow = input('Podaj nową liczbę postów ')
            user['posts'] = nowa_liczba_postow
            nowe_miasto = input('Podaj nową miasto ')
            user['city'] = nowe_miasto
            local = get_coordinates_of(nowe_miasto)

    sql_query = sqlalchemy.text(
        f"UPDATE public.list_of_muls SET name='{nowe_imie}', posts='{nowa_liczba_postow}', nick='{nowy_nick}', city='{nowe_miasto}', geom='POINT({local[1]} {local[0]})' WHERE nick='{user_nick}';")

    connection.execute(sql_query)
    connection.commit()


def gui(users_list) -> None:
            while True:
                print(f'MENU: \n'
                      F'0: Zakoncz program \n'
                      F'1: Wyswietl uzytkownikow \n'
                      F'2: dodaj uzytkownikow \n'
                      F'3: Usun uzytkownika \n'
                      F'4: Modyfikuj uzytkownika\n'
                      F'5: Rysuj mapę z podanym użytkownikiem\n'
                      F'6: Rysuj mapę ze wszytskimi użytownikami\n'
                      )
                menu_option = input('Podaj funkcje do wywolania')
                print(f' Wybrano funkcje {menu_option}')

                match menu_option:
                    case '0':
                        print('koncze prace')
                        break
                    case '1':
                        print('lista uzytkownikow: ')
                        show_users_from(users_list)
                    case '2':
                        print('dodaje uzytkownika: ')
                        add_user_to(users_list)
                    case '3':
                        print('usun uzytkownika: ')
                        remove_user_from(users_list)
                    case '4':
                        print('modyfikuj uzytkownika')
                        update_user(users_list)
                    case '5':
                        print('Rysyję mapę z użytkownikiem')
                        user = input('podaj nazwę użytkownika do modyfikacji ')
                        for item in users_list:
                            if item['nick'] == user:
                                get_map_one_user(item)
                    case '6':
                        print('Rysyję mapę z wszystkimi użytkownikami ')
                        get_map_of(users_list)

