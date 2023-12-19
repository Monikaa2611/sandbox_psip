import sqlalchemy

db_params = sqlalchemy.URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password="1234",
    host="localhost",
    database="postgres",
    port=5433

)


engine= sqlalchemy.create_engine(db_params)
connection=engine.connect()
#sql_query_1=sqlalchemy.text("INSERT INTO public.my_table(name) VALUES('kowalczyk');")
#sql_query_1=sqlalchemy.text("select * from public.my_table;")
#user=input('podaj nazwe zawodnika do usuniecia')
#sql_query_1=sqlalchemy.text(f"delete from public.my_table where name='{user}';")
# kogo_zamienic=input('podaj kogo zmienic')
# na_kogo=input('podaj na kogo zamienic')
# sql_query_1=sqlalchemy.text(f"update public.my_table set name= {na_kogo}' where name ={kogo_zamienic}';")
def dodaj_uzytkownika(user:str):
    sql_query_1=sqlalchemy.text("INSERT INTO public.my_table(name) VALUES('{user}');")
    connection.execute(sql_query_1)
    connection.commit()


def usun_uzytkownika(user:str):
    sql_query_1=sqlalchemy.text(f"delete from public.my_table where name='{user}';")
    connection.execute(sql_query_1)
    connection.commit()


def aktualizuj_uzytkownika(user_1:str, user_2:str):
    sql_query_1 = sqlalchemy.text(f"update public.my_table set name= {user_1}' where name ={user_2}';")
    connection.execute(sql_query_1)
    connection.commit()
# aktualizuj_uzytkownika(
#     user_1=input('na kogo zamienic'),
#     user_2=input('kogo zamienic'))




#connection.execute(sql_query_1)
#connection.commit()