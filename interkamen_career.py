#!usr/bin/env python3
"""
This program provides control of all data and statistic of Career Interkamen.
"""

import sys
import shelve
from modules import users, access_options
from modules.absolyte_path_module import USERS_PATH


def print_menu():
    """Print program menu."""
    print('\033[4m' + '\033[1m' + "\n\tМеню программы.\n" + '\033[0m')
    for key in sorted(PROGRAM_MENU):
        print("[{}] - {}".format(key, PROGRAM_MENU[key]))


def loged_and_sync_current_user(user_action):
    """Bump CURRENT_USER log to database"""
    users.create_log(CURRENT_USER, user_action)
    with shelve.open(USERS_PATH) as users_base:
        users_base[CURRENT_USER.login] = CURRENT_USER


if __name__ == '__main__':

    CURRENT_USER = None
    while CURRENT_USER is None:
        CURRENT_USER = users.try_to_enter_program()
    loged_and_sync_current_user('enter')

    OPTIONS_LIST = access_options.create_options_list(CURRENT_USER)
    OPTIONS_LIST['м'] = (print_menu, )

    PROGRAM_MENU = access_options.create_menu_list(CURRENT_USER.get_access())
    print_menu()

    while True:
        USER_CHOISE = input("\n[м] - Показать меню программы"
                            "\nВыберете действие:\n")
        print()
        if USER_CHOISE not in OPTIONS_LIST:
            print("Нет такого варианта.")
            continue
        elif USER_CHOISE == 'в':
            loged_and_sync_current_user(USER_CHOISE)
            sys.exit()

        for action in OPTIONS_LIST[USER_CHOISE]:
            action()
        loged_and_sync_current_user(USER_CHOISE)
