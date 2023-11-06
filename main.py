from dane import users_list

def add_user_to(users_list:list) -> None:
    # 3 razy shift enter
    """
    add object to list
    :param users_list: list - user list
    :return: None
    """
    name = input('podaj imię?')
    posts = input('dodaj liczbę postów')
    users_list.append({'name': name, 'posts': posts})

add_user_to(users_list)
add_user_to(users_list)
add_user_to(users_list)

for user in users_list:
    print(f'Twój znajomy {user["name"]} dodał {user["posts"]}')




