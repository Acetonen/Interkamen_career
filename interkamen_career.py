#!usr/bin/env python3
"""
This program provides control of all data and statistic of Career Interkamen.

Functions: 'print_menu'
           'make_log'
           'create_action_dict'
"""

import sys
from modules.hi import INTERKAMEN
from modules.accesse_options import Accesse
from modules.users import Users
from modules.log_class import Logs


def print_menu():
    """Print program menu."""
    print('\033[4m' + '\033[1m' + "\tМеню программы.\n" + '\033[0m')
    for key in sorted(PROGRAM_MENU):
        print("[{}] - {}".format(key, PROGRAM_MENU[key]))


def make_log(user_action):
    """Bump CURRENT_USER log to database"""
    Logs().create_log(CURRENT_USER['login'], user_action)


def create_action_dict():
    """Created list of actions for current main/sub menu"""
    ACTIONS_LIST.clear()
    ACTIONS_LIST.update(
        Accesse(USR_ACS).get_actions_dict(PROGRAM_MENU).items())
    ACTIONS_LIST['м'] = lambda *arg: print_menu()
    print_menu()


if __name__ == '__main__':
    print(INTERKAMEN)
    SEPARATOR = "\033[9m\033[36m                             \033[0m\n"

    CURRENT_USER = None
    while CURRENT_USER is None:
        CURRENT_USER = Users().try_to_enter_program()
    make_log('enter')
    USR_ACS = CURRENT_USER['accesse']

    print()
    while True:

        # Create main menu (otput and actions dict).
        PROGRAM_MENU = Accesse(USR_ACS).get_menu_dict()
        ACTIONS_LIST = {}
        create_action_dict()

        while True:

            print(SEPARATOR)
            USER_CHOISE = input("[м] - Показать меню программы"
                                "\nВыберете действие:\n")
            print(SEPARATOR)

            if USER_CHOISE not in ACTIONS_LIST:
                print("Нет такого варианта.")
                continue

            ITEM = PROGRAM_MENU[USER_CHOISE]

            # Enter sub-menu.
            if '-->' in ITEM:
                PROGRAM_MENU = Accesse(USR_ACS).get_sub_menu(ITEM)
                create_action_dict()

            # Exit sub-menu.
            elif '<--' in ITEM:
                break

            # Exit program.
            elif USER_CHOISE == 'в':
                make_log(USER_CHOISE)
                sys.exit()

            # Make action.
            else:
                ACTION = ACTIONS_LIST[USER_CHOISE]
                ACTION(CURRENT_USER)

            CURRENT_USER = Users().sync_user(CURRENT_USER['login'])
            make_log(USER_CHOISE)
