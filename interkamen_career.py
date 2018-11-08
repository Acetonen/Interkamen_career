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
    make_log(current_user['login'], 'enter')
    return current_user


def print_menu():
    """Print program menu."""
    print('\033[4m' + '\033[1m' + "\tМеню программы.\n" + '\033[0m')
    for key in sorted(PROGRAM_MENU):
        print("[{}] - {}".format(key, PROGRAM_MENU[key]))


def make_log(user_login, user_action):
    """Bump CURRENT_USER log to database"""
    Logs().create_log(user_login, user_action)


def reload_menu_and_actions(choise_exist):
    """Reload menu and actions"""
    get_main_or_sub_menu(choise_exist)
    create_action_dict()


def create_action_dict():
    """Created list of actions for current main/sub menu"""
    ACTIONS_LIST.clear()
    ACTIONS_LIST.update(
        Accesse(USR_ACS).get_actions_dict(PROGRAM_MENU).items()
        )
    ACTIONS_LIST['м'] = lambda *arg: print_menu()
    print_menu()


def get_main_or_sub_menu(choise_exst):
    """create main or sub-menu"""
    if choise_exst:
        program_menu = Accesse(USR_ACS).get_sub_menu(PROGRAM_MENU[choise_exst])
    else:
        program_menu = Accesse(USR_ACS).get_menu_dict()
    PROGRAM_MENU.clear()
    PROGRAM_MENU.update(program_menu)


if __name__ == '__main__':

    SEPARATOR = "\033[9m\033[36m                             \033[0m\n"
    ACTIONS_LIST = {}
    PROGRAM_MENU = {}
    CURRENT_USER = login_program()
    USR_ACS = CURRENT_USER['accesse']

    print()
    while True:

        # Create main menu (otput and actions dict).
        reload_menu_and_actions(None)

        while True:

            print(SEPARATOR)
            USER_CHOISE = input("[м] - Показать меню программы"
                                "\nВыберете действие:\n")
            print(SEPARATOR)

            if USER_CHOISE not in ACTIONS_LIST:
                print("Нет такого варианта.")
                continue

            # Enter sub-menu.
            elif '-->' in PROGRAM_MENU[USER_CHOISE]:
                reload_menu_and_actions(USER_CHOISE)

            # Exit sub-menu.
            elif '<--' in PROGRAM_MENU[USER_CHOISE]:
                break

            # Exit program.
            elif USER_CHOISE == 'в':
                make_log(CURRENT_USER['login'], USER_CHOISE)
                sys.exit()

            # Make action.
            else:
                ACTION = ACTIONS_LIST[USER_CHOISE]
                ACTION(CURRENT_USER)

            CURRENT_USER = Users().sync_user(CURRENT_USER['login'])
            make_log(CURRENT_USER['login'], USER_CHOISE)
