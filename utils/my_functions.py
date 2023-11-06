def add_user_to(users_list:list) -> None:

    """
    add object to list
    :param users_list: list - user list
    :return: None
    """
    name = input('podaj imię?')
    posts = input('dodaj liczbę postów')
    users_list.append({'name': name, 'posts': posts})

def remove_user_from(users_list: list) -> None:
    """
    remove object from list
    :param users_list: list -> user list
    :return: None
    """
    tmp_list = []
    name = input('podaj imię użytkownika do usunięcia: ')
    for user in users_list:
        if user["name"]== name:
            tmp_list.append(user)
    print('Znaleziono użytkowników:')
    print('0: Usuń wszytskich znalezionych użytkowników')
    for numerek, user_to_be_remowed in enumerate(tmp_list):
        print(f'{numerek+1}. {user_to_be_remowed}')
    numer = int(input(f'Wybierz numer użytkownika do usunięcia:'))
    if numer == 0:
        for user in users_list:
            users_list.remove(user)
    else:
        users_list.remove(tmp_list[numer-1])

def show_users_from(users_list:list)->None:
    for user in users_list:
        print(f'Twój znajomy {user["name"]} dodał {user["posts"]}')


def gui(users_list: list) -> None:
    while True:
        print(f' MENU: \n'
              f'0: Zakończ program \n'
              f'1: Wyświetl użytkowników \n'
              f'2: Dodaj użytkownika \n'
              f'3: Usuń użytkownika \n'
              f'4: Modyfikuj użytkownika \n'
              )
        menu_option = input('Podaj funkcje do wywołania')
        print(f'Wybrano funkcje {menu_option}')

        match menu_option:
            case '0':
                print('Kończę pracę')
                break
            case '1':
                print('Wyświetlam listę użytkowników')
                show_users_from(users_list)
            case '2':
                print('Dodawanie użytkownika')
                add_user_to(users_list)
            case '3':
                print('Usuwanie użytkownika')
                remove_user_from(users_list)
            case '4':
                print('Modyfikuję użytkownika')
                print('To będzie zrobione')


gui()