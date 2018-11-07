#!usr/bin/env python3
"""
This program provides control of all data and statistic of Career Interkamen.

Functions: print_menu()
           loged_and_sync_current_user(user_action)
"""

import sys
from modules.access_options import Accesse
from modules.users import Users
from modules.log_class import Logs


def print_menu():
    """Print program menu."""
    print('\033[4m' + '\033[1m' + "\n\tМеню программы.\n" + '\033[0m')
    for key in sorted(PROGRAM_MENU):
        print("[{}] - {}".format(key, PROGRAM_MENU[key]))


def loged_and_sync_current_user(user_action):
    """Bump CURRENT_USER log to database"""
    Logs().create_log(CURRENT_USER['login'], user_action)
    Users().sync_user(CURRENT_USER)


if __name__ == '__main__':

    CURRENT_USER = None
    while CURRENT_USER is None:
        CURRENT_USER = Users().try_to_enter_program()
    loged_and_sync_current_user('enter')

    ACTIONS_LIST = Accesse(CURRENT_USER['accesse']).get_actions_list()
    ACTIONS_LIST['м'] = print_menu

    PROGRAM_MENU = Accesse(CURRENT_USER['accesse']).get_menue_list()
    print_menu()

    while True:
        USER_CHOISE = input("\n[м] - Показать меню программы"
                            "\nВыберете действие:\n")
        print()
        if USER_CHOISE not in ACTIONS_LIST:
            print("Нет такого варианта.")
            continue
        elif USER_CHOISE == 'в':
            loged_and_sync_current_user(USER_CHOISE)
            sys.exit()

        ACTIONS_LIST[USER_CHOISE]()
        loged_and_sync_current_user(USER_CHOISE)
