#!usr/bin/env python3
"""
This program provides control of all data and statistic of Career Interkamen.

Functions: 'print_menu'
           'make_log'
           'create_action_dict'
           'login_program'
           'reload_menu_and_actions'
           'create_action_dict'
           'get_main_or_sub_menu'
"""

import sys
from collections import OrderedDict
from modules.hi import INTERKAMEN
from modules.accesse_options import Accesse
from modules.users import Users
from modules.log_class import Logs


def login_program():
    """Login to program and loged 'enter'"""
    print(INTERKAMEN)
    current_user = None
    while current_user is None:
        current_user = Users().try_to_enter_program()
    Logs().create_log(
        current_user['login'], '\033[94m enter program \033[0m')
    return current_user


def print_menu():
    """Print program menu."""
    print(' '.join(MENU_HEADER))
    for index, item in enumerate(PROGRAM_MENU, 1):
        print("[{}] - {}".format(index, item))


def get_main_or_sub_menu(sub_menu):
    """create main or sub-menu"""
    if sub_menu:
        program_menu = Accesse(USR_ACS).get_sub_menu(sub_menu)
    else:
        program_menu = Accesse(USR_ACS).get_menu_dict()
    PROGRAM_MENU.clear()
    PROGRAM_MENU.update(program_menu)
    del MENU_LIST[:]
    MENU_LIST.extend(list(PROGRAM_MENU.items()))


def check_number_in_range(user_input, list_range):
    """Check is input a number in current range."""
    check_number = None
    if user_input.isdigit():
        check_number = int(user_input) in range(len(list_range)+1)
        if not check_number:
            print("\nВведите цифру соответствующую пункту меню.\n")
    else:
        print("\nВведите цифру соответствующую пункту меню.\n")
    return check_number


if __name__ == '__main__':

    MENU_HEADER = ['\033[1m \t', None, '\n \033[0m']
    SEPARATOR = "\033[9m\033[36m                             \033[0m\n"
    PROGRAM_MENU = OrderedDict
    PROGRAM_MENU = {}
    MENU_LIST = []
    MENU_NESTING = []
    CURRENT_USER = login_program()
    USR_ACS = CURRENT_USER['accesse']

    print()
    while True:

        # Create main menu (otput and actions dict).
        MENU_HEADER[1] = '\033[4m ГЛАВНОЕ МЕНЮ \033[0m'
        get_main_or_sub_menu(None)
        print_menu()

        while True:
            print(SEPARATOR)
            USER_CHOISE = input("[м] - Показать меню программы"
                                "\nВыберете действие:\n")
            print(SEPARATOR)

            if USER_CHOISE == 'м':
                print_menu()
                continue

            if not check_number_in_range(USER_CHOISE, PROGRAM_MENU):
                continue

            USER_CHOISE = int(USER_CHOISE) - 1

            # Enter sub-menu.
            if '-->' in MENU_LIST[USER_CHOISE][0]:
                MENU_HEADER[1] = MENU_LIST[USER_CHOISE][0].split(' ')[1]
                MENU_NESTING.append(MENU_LIST[USER_CHOISE][0])
                get_main_or_sub_menu(MENU_LIST[USER_CHOISE][0])
                print_menu()
                continue

            # Exit sub-menu.
            elif '<--' in MENU_LIST[USER_CHOISE][0]:
                MENU_NESTING = MENU_NESTING[:-1]
                if MENU_NESTING:
                    MENU_HEADER[1] = MENU_NESTING[-1].split(' ')[1]
                    get_main_or_sub_menu(MENU_NESTING[-1])
                    print_menu()
                else:
                    break

            # Exit program.
            elif MENU_LIST[USER_CHOISE][1] == 'exit program':
                Logs().create_log(
                    CURRENT_USER['login'], MENU_LIST[USER_CHOISE][0])
                sys.exit()

            # Make action.
            else:
                ACTION = MENU_LIST[USER_CHOISE][1]
                ACTION(CURRENT_USER)

            CURRENT_USER = Users().sync_user(CURRENT_USER['login'])
            Logs().create_log(
                CURRENT_USER['login'], MENU_LIST[USER_CHOISE][0])
