from dane import users_list





def update_users(users_list: list[dict,dict]) -> None:
    nick_of_users = input('podaj nick uzytkownika do modyfikacji')
    print(nick_of_users)
    for users in users_list:
        if users['nick'] == nick_of_users:
           print('Znaleziono !!')
           users['name'] = input('podaj nowe imie: ')
           users['nick'] = input('podaj nowa ksywe: ')
           users['posts'] = int(input('podaj liczbe postow: '))

update_users(users_list)
for users in users_list:
    print(users)


