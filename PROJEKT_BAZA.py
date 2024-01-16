from sqlalchemy import create_engine, Sequence, Column, Integer, String
import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from geoalchemy2 import Geometry
import folium
import requests
import bs4
from shapely import wkb
from getpass import getpass
from geopy.geocoders import Nominatim

### DB CONNECTION ###
db_params = sqlalchemy.URL.create(
    drivername='postgresql+psycopg2',
    username='postgres',
    password='1234',
    host='localhost',
    database='postgres',
    port=5432
)

engine = create_engine(db_params)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


### TABLE ###
class Cinema(Base):
    __tablename__ = "Cinema"

    id = Column(Integer(), Sequence("id_seq"), primary_key=True)
    name = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    location = Column('geom', Geometry(geometry_type='POINT', srid=4326), nullable=True)

    def __init__(self, name, city):
        self.name = name
        self.city = city
        coords = get_coords(city)
        self.location = f'POINT({coords[1]} {coords[0]})'


class Employee(Base):
    __tablename__ = "Employee"

    id = Column(Integer(), Sequence("id_seq"), primary_key=True)
    name = Column(String(100), nullable=True)
    surname = Column(String(100), nullable=True)
    cinema = Column(String(100), nullable=True)
    location = Column('geom', Geometry(geometry_type='POINT', srid=4326), nullable=True)

    def __init__(self, name, surname, cinema, address):
        self.name = name
        self.surname = surname
        self.cinema = cinema
        coords = get_coords(address)
        self.location = f'POINT({coords[1]} {coords[0]})'


class Film(Base):
    __tablename__ = "Film"

    id = Column(Integer(), Sequence("id_seq"), primary_key=True)
    name = Column(String(100), nullable=True)
    type = Column(String(100), nullable=True)
    cinema = Column(String(100), nullable=True)
    location = Column('geom', Geometry(geometry_type='POINT', srid=4326), nullable=True)

    def __init__(self, name, type, cinema, x, y):
        self.name = name
        self.type = type
        self.cinema = cinema
        self.location = f'POINT({y} {x})'


Base.metadata.create_all(engine)


### FUNCTIONAL ###
def convert_point(wkb_point):
    point = wkb.loads(str(wkb_point), hex=True)
    return (point.y, point.x)


def get_coords(address):
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode(address)

    latitude, longitude = location.latitude, location.longitude
    return latitude, longitude


def GUI():
    while True:
        print('\n6 Manage cinemas, employees and films 9\n\n'
              f'0: Exit\n'
              f'Cinemas\n'
              f'11: show cinemas\n'
              f'12: create cinema\n'
              f'13: remove cinema\n'
              f'14. update cinema\n'
              f'Employees\n'
              f'21. show all employees\n'
              f'22. show employees from once cinema\n'
              f'23. create employee\n'
              f'24. remove employee\n'
              f'25. update employee\n'
              f'Films\n'
              f'31. show films\n'
              f'32. show films from once cinema\n'
              f'33. create films\n'
              f'34. remove films\n'
              f'35. update films\n'
              f'Maps\n'
              f'41. map of all cinemas\n'
              f'42. map of all employees\n'
              f'43. map film by type \n'
              f'44. map where play film\n')
        choose = int(input('Choose funcion: '))
        print(f'Chose {choose}: \n')

        match choose:
            case 0:
                print('Close app')
                session.flush()
                engine.dispose()
                break
            case 11:
                print('List of cinemas')
                select_all_cinemas()
            case 12:
                print('Create cinema')
                insert_cinema()
            case 13:
                print('Remove cinema')
                delete_cinema()
            case 14:
                print('Update cinema')
                update_cinema()
            case 23:
                print('Create employee')
                insert_employee()
            case 21:
                print('List of all employees')
                select_all_employees()
            case 22:
                print('List of employees from once cinema')
                select_employees_from()
            case 24:
                print('Remove employee')
                delete_employee()
            case 25:
                print('Update employee')
                update_empoloyee()
            case 33:
                print('Create films')
                insert_film()
            case 31:
                print('List of films')
                select_all_film()
            case 32:
                print('List of films from once cinema')
                select_film_from()
            case 34:
                print('Remove films')
                delete_film()
            case 35:
                print('Update films')
                update_film()
            case 41:
                print('Map of all cinemas')
                map_all_cinema()
            case 43:
                print('Map of all employees')
                map_film_by_type()
            case 42:
                print('Map film by type')
                map_all_employee()
            case 44:
                print('Map where play film')
                map_where_play_film()


### CINEMA ###
def insert_cinema():
    name = input('Cinema name: ')
    city = input('City address: ')
    add = Cinema(name, city)

    session.add(add)
    session.commit()


def select_all_cinemas():
    cinemas_from_db = session.query(Cinema).all()
    if cinemas_from_db == []:
        print('no data available')
    else:
        for id, cinema in enumerate(cinemas_from_db):
            print(f'{id + 1}. {cinema.name} - {cinema.city}')


def delete_cinema():
    closure = input('Name the cinema to be closed down: ')
    cinemas_from_db = session.query(Cinema).filter(Cinema.name == closure)

    for cinema in cinemas_from_db:
        if cinema.name == closure:
            print(f'{cinema.name} cinema closed down')

            session.delete(cinema)

    employees_from_db = session.query(Employee).filter(Employee.cinema == closure)

    for empoloyee in employees_from_db:
        if empoloyee.cinema == closure:
            print(f'{empoloyee.name} was fired')

            session.delete(empoloyee)

    films_from_db = session.query(Film).filter(Film.cinema == closure)

    for film in films_from_db:
        if film.cinema == closure:
            print(f'{film.name} from {closure} was delate')

            session.delete(film)

    session.commit()


def update_cinema():
    modify = input('Name the cinema to be modified: ')
    cinemas_from_db = session.query(Cinema).all()
    for cinema in cinemas_from_db:
        if cinema.name == modify:
            cinema.name = input('New name: ')
            ccity = input('New city location: ')
            cinema.city = ccity
            coords = get_coords(ccity)
            cinema.location = f'POINT({coords[1]} {coords[0]})'
    session.commit()


### EMPLOYEE ###
def insert_employee():
    name = input('Employee name: ')
    surname = input('Employee surname: ')
    cinema = input('Cinema where he/she/it works: ')
    address = input("Employee's address: ")
    add = Employee(name, surname, cinema, address)
    session.add(add)
    session.commit()


def select_all_employees():
    employees_from_db = session.query(Employee).all()
    if employees_from_db == []:
        print('no data available')
    else:
        for id, employee in enumerate(employees_from_db):
            print(f'{id + 1}. {employee.name} working in {employee.cinema}')


def select_employees_from():
    cinema = input('Cinema to screen its employees: ')
    employees_from_db = session.query(Employee).filter(Employee.cinema == cinema)
    if employees_from_db == []:
        print('no data available')
    else:
        for id, employee in enumerate(employees_from_db):
            print(f'{id + 1}. {employee.name}')


def delete_employee():
    fired = input('Surname of employee to be fired: ')
    employees_from_db = session.query(Employee).filter(Employee.surname == fired)

    fired_list = []

    for employee in employees_from_db:
        if employee.name == fired:
            fired_list.append(employee.surname)
    print('Such workers were found:')
    print('0. fired all')

    for id, to_be_fired in enumerate(fired_list):
        print(id + 1, to_be_fired)
    number = int(input('Select an employee to be fired: '))

    if number == 0:
        for employee in fired_list:
            session.delete(employee)
    else:
        aa = fired_list[number - 1]
        session.delete(aa)

    session.commit()


def update_empoloyee():
    edit = input('Surname of employee to edit: ')
    employees_from_db = session.query(Employee).filter(Employee.surname == edit)

    edit_list = []

    if len(edit_list) > 1:

        for empoloyee in employees_from_db:
            if empoloyee.surname == edit:
                edit_list.append(empoloyee)
        print('Such workers were found:')

        for id, to_be_edt in enumerate(edit_list):
            print(f"{id + 1}. {to_be_edt.name} {to_be_edt.surname}")
        number = int(input('Select an employee to be edit: '))

        emp = edit_list[number - 1]
        emp.name = input('New employee name: ')
        emp.surname = input('New employee surname: ')
        emp.cinema = input('New cinema where he/she/it works: ')
        address = input('New address: ')
        coords = get_coords(address)
        emp.location = f'POINT({coords[1]} {coords[0]})'
    else:
        for empoloyee in employees_from_db:
            empoloyee.name = input('New employee name: ')
            empoloyee.surname = input('New employee surname: ')
            empoloyee.cinema = input('New cinema where he/she/it works: ')
            address = input('New address: ')
            coords = get_coords(address)
            empoloyee.location = f'POINT({coords[1]} {coords[0]})'
    session.commit()


### FILM ###
def insert_film():
    name = input("Film's tittle: ")
    cinema = input('Cinema where to watch: ')
    type = input('Type of film: ')
    x = int(input('Latitude: '))
    y = int(input("Longitude: "))
    add = Film(name, type, cinema, x, y)
    session.add(add)
    session.commit()


def select_all_film():
    films_from_db = session.query(Film).all()
    if films_from_db == []:
        print('no data available')
    else:
        for id, film in enumerate(films_from_db):
            print(f'{id + 1}. {film.name} - {film.type} plays in {film.cinema}')


def select_film_from():
    film = input('Cinema to screen its films: ')
    films_from_db = session.query(Film).filter(Film.cinema == film)
    if films_from_db == []:
        print('no data available')
    else:
        for id, film in enumerate(films_from_db):
            print(f'{id + 1}. {film.name}')


def delete_film():
    dell = input('Tittle of film to delete: ')
    films_from_db = session.query(Film).filter(Film.name == dell)

    del_list = []

    for film in films_from_db:
        if film.name == dell:
            del_list.append(film)
    print('Such films were found:')
    print('0. delete from all cinema')
    for number, film_to_be_removed in enumerate(del_list):
        print(number + 1, film_to_be_removed)
    number = int(input('Choose cinema, where film will delete: '))

    if number == 0:
        for user in del_list:
            session.delete(user)
    else:
        aa = del_list[number - 1]
        session.delete(aa)


def update_film():
    edit = input('Tittle of film to edit: ')
    films_from_db = session.query(Film).filter(Film.name == edit)

    edit_list = []

    if len(edit_list) > 1:

        for film in films_from_db:
            if film.name == edit:
                edit_list.append(film)
        print('Such films were found:')

        for id, to_be_edt in enumerate(edit_list):
            print(f"{id + 1}. {to_be_edt.name} {to_be_edt.cinema}")
        number = int(input('Select an film to be edit: '))

        ff = edit_list[number - 1]
        ff.name = input('New film tittle: ')
        ff.type = input('New type of film ')
        ff.cinema = input('New cinema where it plays: ')
        x = int(input('New latitude: '))
        y = int(input("New longitude: "))
        ff.location = f'POINT({y} {x})'
    else:
        for film in films_from_db:
            film.name = input('New film title: ')
            film.type = input('New type of film')
            film.cinema = input('New cinema where it plays: ')
            x = int(input('New latitude: '))
            y = int(input("New longitude: "))
            film.location = f'POINT({y} {x})'
    session.commit()


### MAPS ###
def map_all_cinema():
    map = folium.Map(location=[52.3, 21.0], tiles='OpenStreetMap', zoom_start=7)

    cinema_form_db = session.query(Cinema).all()
    for cinema in cinema_form_db:
        coords = get_coords(cinema.city)
        folium.Marker(location=coords, popup=f"{cinema.name}").add_to(map)
    print('\Printed')
    map.save(f'map_all_cinema.html')


def map_film_by_type():
    map = folium.Map(location=[52.3, 21.0], tiles='OpenStreetMap', zoom_start=7)

    choose = print('Choose type of film to print map: ')

    films_form_db = session.query(Film).filter(Film.type == choose)
    for film in films_form_db:
        coords = convert_point(film.location)
        folium.Marker(location=coords, popup=f"{film.name}").add_to(map)
    print('\Printed')
    map.save(f'map_{choose}.html')


def map_all_employee():
    map = folium.Map(location=[52.3, 21.0], tiles='OpenStreetMap', zoom_start=7)

    employees_form_db = session.query(Employee).all()
    for employee in employees_form_db:
        coords = convert_point(employee.location)
        folium.Marker(location=coords, popup=f"{employee.name}").add_to(map)
    print('\Printed')
    map.save(f'map_all_employee.html')


def map_where_play_film():
    map = folium.Map(location=[52.3, 21.0], tiles='OpenStreetMap', zoom_start=7)

    choose = print('Choose film to print map, where it plays: ')
    ff = []
    films_form_db = session.query(Film).filter(Film.name == choose)
    for film in films_form_db:
        ff.append(film.cinema)

    cinema_form_db = session.query(Cinema).filter(Cinema.name in ff)
    for cinema in cinema_form_db:
        coords = get_coords(cinema.city)
        folium.Marker(location=coords, popup=f"{cinema.name}").add_to(map)
    print('\Printed')
    map.save(f'map_cinema_play_{choose}.html')


### LOGIN ###
def login_win():
    while True:
        login = input('Enter login: ')
        password = getpass('Enter password: ')
        if (login == 'login') and (password == 'password'):
            GUI()
        else:
            print('\nNOOO\nincorrectly values!!!!\n')