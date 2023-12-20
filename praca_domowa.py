from dane import users_list
from bs4 import BeautifulSoup
import requests
import folium
import sqlalchemy.orm
from dotenv import load_dotenv
from geoalchemy2 import Geometry
import os
from sqlalchemy import Column, Integer, String
from dml import db_params

load_dotenv()
engine = sqlalchemy.create_engine(db_params)
connection = engine.connect()
Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()
Base = sqlalchemy.orm.declarative_base()

def get_coordinates_of(city:str)->list[float,float]:
    adres_URL = f'https://pl.wikipedia.org/wiki/{city}'

    response = requests.get(url=adres_URL)
    response_htlm = BeautifulSoup(response.text, 'html.parser')

    res_h_lat = response_htlm.select('.latitude')[1].text
    res_h_lat = float(res_h_lat.replace(',', '.'))

    res_h_lon = response_htlm.select('.longitude')[1].text
    res_h_lon = float(res_h_lon.replace(',', '.'))

    return [res_h_lat, res_h_lon]

class User(Base):
    __tablename__ = 'lista_uzytkownikow'

    id = Column(Integer(), primary_key=True)
    posts = Column(Integer(), nullable=True)
    name = Column(String(100), nullable=True)
    nick = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    location = Column('geom', Geometry(geometry_type='POINT', srid=4326), nullable=True)

def GUI(users_list):
    while True:
        print(f'MENU: \n'
              F'0: Zakoncz program \n'
              F'1: Wyswietl uzytkownikow \n'
              F'2: dodaj uzytkownikow \n'
              F'3: Usun uzytkownika \n'
              F'4: Modyfikuj uzytkownika\n'
              F'5: Rysuj mapę z podanym użytkownikiem\n'
              F'6: Rysuj mapę ze wszytskimi użytownikami\n'
              f'7. Utwórz tabele\n'
              f'8. Usuń dane\n'
              f'9. Utwórz tabele z danymi \n')
        menu_option = int(input('Podaj funkcje do wywolania'))
        print(f' Wybrano funkcje {menu_option}')

        match menu_option:
            case 0:
                print('koncze prace')
                break
            case 1:
                print('wyswietlam liste')
                show_users_from(db_params)
            case 2:
                print('dodawanie')
                add_user_to(users_list, db_params)
            case 3:
                print('usuwanie')
                remove_user_from(users_list, db_params)
            case 4:
                print('modyfikacja')
                update_user(users_list, db_params)
            case '5':
                print('Rysyję mapę z użytkownikiem')
                user = input('podaj nazwę użytkownika do modyfikacji ')
                for item in users_list:
                    if item['nick'] == user:
                        get_map_one_user(item)
            case '6':
                print('Rysyję mapę ze wszystkimi użytkownikami ')
                get_map_of(users_list)
            case 7:
                print('Utworzono tabele')
                create_table(db_params)
            case 8:
                print('Usunięto dane')
                delate_data(db_params)
            case 9:
                print('Utworzono tabele z danymi')
                create_tandd(db_params)

def show_users_from(db_params):
    engine = sqlalchemy.create_engine(db_params)
    connection = engine.connect()
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()
    lista_uzytkownikow = session.query(User).all()

    for user in lista_uzytkownikow:
        print(f"Użytkownik {user.name} zamieszkujacy {user.city} utworzyl {user.posts} postow")

def add_user_to(lissta, db_params):
    engine = sqlalchemy.create_engine(db_params)
    connection = engine.connect()

    name = input('Podaj imie: ')
    nick = input('Podaj nick: ')
    post = int(input('Liczba postow: '))
    miasto = input('Podaj nazwe miejscowosci: ')
    lissta.append({"name": name, "nick": nick, "posts": post, 'city': miasto})
    xy = get_coordinates_of(miasto)
    sql_query = sqlalchemy.text(f"INSERT INTO public.lista_uzytkownikow(name, nick, city, posts, geom) VALUES ('{name}', '{nick}', '{miasto}', '{post}', 'POINT({xy[1]} {xy[0]})');")

    connection.execute(sql_query)
    connection.commit()

def remove_user_from(lissta, db_params):
    engine = sqlalchemy.create_engine(db_params)
    connection = engine.connect()

    listt = []
    name = input('Wybierz uzytkownika do usuniecia :')
    for user in lissta:
        if user['name'] == name:
            listt.append(user)
    print('Znaleziono:')
    print('0 Usun wszytskich uzytkownikow')
    for numerek, user_to_be_removed in enumerate(listt):
        print(numerek + 1, user_to_be_removed)
    numer = int(input('Wybierz uzytkownika do usuniecia: '))
    if numer == 0:
        for user in listt:
            lissta.remove(user)
            print(user)
            print(type(user))
            sql_query = sqlalchemy.text(f"DELETE FROM public.lista_uzytkownikow WHERE name = '{user['name']}';")
    else:
        null = listt[numer - 1]
        lissta.remove(null)
        print(type(null))
        print(null['city'])
        sql_query = sqlalchemy.text(f"DELETE FROM public.lista_uzytkownikow WHERE nick = '{null['nick']}';")

    connection.execute(sql_query)
    connection.commit()

def update_user(lissta, db_params):
    engine = sqlalchemy.create_engine(db_params)
    connection = engine.connect()

    user_nick = input('Podaj nick użytkownika do modyfikacji ')
    print(f'Wpisano {user_nick}')
    for user in lissta:
        if user['nick'] == user_nick:
            print('znaleziono')
            nowe_imie = input('Podaj nowe imię ')
            user['name'] = nowe_imie
            nowy_nick = input('Podaj nowy nick ')
            user['nick'] = nowy_nick
            nowa_liczba = input('Podaj nową ilość postów ')
            user['posts'] = nowa_liczba
            nowe_mias = input('Podaj nową nazwe miasta' )
            user['city'] = nowe_mias
            xy = get_coordinates_of(nowe_mias)

    sql_query = sqlalchemy.text(
        f"UPDATE public.lista_uzytkownikow SET name='{nowe_imie}', posts='{nowa_liczba}', nick='{nowy_nick}', city='{nowe_mias}', geom='POINT({xy[1]} {xy[0]})' WHERE nick='{user_nick}';")

    connection.execute(sql_query)
    connection.commit()

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

def create_table(db_params):
    engine = sqlalchemy.create_engine(db_params)
    Base = sqlalchemy.orm.declarative_base()

    class User(Base):
        __tablename__ = 'lista_uzytkownikow'

        id = Column(Integer(), primary_key=True)
        posts = Column(Integer(), nullable=True)
        name = Column(String(100), nullable=True)
        nick = Column(String(100), nullable=True)
        city = Column(String(100), nullable=True)
        location = Column('geom', Geometry(geometry_type='POINT', srid=4326), nullable=True)

    Base.metadata.create_all(engine)

def delate_data(db_params):
    engine = sqlalchemy.create_engine(db_params)
    connection = engine.connect()

    sql_query = sqlalchemy.text(f"DELETE FROM public.lista_uzytkownikow WHERE name != 'XXX';")

    connection.execute(sql_query)
    connection.commit()

def create_tandd(db_params):
    engine = sqlalchemy.create_engine(db_params)
    connection = engine.connect()
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()

    Base = sqlalchemy.orm.declarative_base()

    class User(Base):
        __tablename__ = 'lista_uzytkownikow'

        id = Column(Integer(), primary_key=True)
        posts = Column(Integer(), nullable=True)
        name = Column(String(100), nullable=True)
        nick = Column(String(100), nullable=True)
        city = Column(String(100), nullable=True)
        location = Column('geom', Geometry(geometry_type='POINT', srid=4326), nullable=True)

    Base.metadata.create_all(engine)

    lista_uz: list = []

    for user in users_list:
        xy = get_coordinates_of(user['city'])
        lista_uz.append(
            User(
                name=user['name'],
                posts=user['posts'],
                nick=user['nick'],
                city=user['city'],
                location=f'POINT({xy[1]} {xy[0]})'
            )
        )
    session.add_all(lista_uz)
    session.commit()

def data(db_params):
    engine = sqlalchemy.create_engine(db_params)
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()

    data_1 = []
    lista_uzytkownikow_db = session.query(User).all()

    for user in lista_uzytkownikow_db:
        name = user.name
        nick = user.nick
        post = user.posts
        city = user.city
        data_1.append({"name": name, "nick": nick, "posts": post, 'city': city})

    return data_1

GUI(data(db_params))
