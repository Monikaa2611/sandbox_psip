from dane import users_list
from utils import gui, baza
from dml import db_params
from hoy import baza_to_zmienna, GUI


# gui(baza(db_params))
GUI(baza_to_zmienna(db_params))



