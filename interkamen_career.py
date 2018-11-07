#!usr/bin/env python3
"""
This program provides control of all data and statistic of Career Interkamen.

Functions: 'print_menu'
           'make_log'
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


def make_log(user_action):
    """Bump CURRENT_USER log to database"""
    Logs().create_log(CURRENT_USER['login'], user_action)


if __name__ == '__main__':

    CURRENT_USER = None
    while CURRENT_USER is None:
        CURRENT_USER = Users().try_to_enter_program()
    make_log('enter')

    ACTIONS_LIST = Accesse(CURRENT_USER['accesse']).get_actions_list()
    ACTIONS_LIST['м'] = print_menu
    ACTIONS_WITH_INPUT = Accesse(CURRENT_USER['accesse']).get_input_actions()
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
            make_log(USER_CHOISE)
            sys.exit()
        elif USER_CHOISE in ACTIONS_WITH_INPUT:
            ACTIONS_LIST[USER_CHOISE](CURRENT_USER)
        else:
            ACTIONS_LIST[USER_CHOISE]()
        CURRENT_USER = Users().sync_user(CURRENT_USER['login'])
        make_log(USER_CHOISE)
