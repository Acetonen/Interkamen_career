#!/usr/bin/env python3
"""
This program provides control of all data and statistic of Career Interkamen.

Functions: 'print_menu'
           'make_header'
           'login_program'
           'check_backup'
           'get_main_or_sub_menu'
"""

import sys

from modules.support_modules.hi import INTERKAMEN
from modules.support_modules.backup import check_last_backup_date
from modules.support_modules.standart_functions import BasicFunctions
from modules.support_modules.reminder import Reminder
from modules.support_modules.news import News

from modules.administration.accesse_options import Accesse
from modules.administration.users import Users
from modules.administration.log_class import Logs


def login_program():
    """Login to program and loged 'enter'"""
    print(INTERKAMEN)
    current_user = None
    while current_user is None:
        current_user = Users().try_to_enter_program()
    Logs().create_log(current_user['login'], 'enter program')
    BasicFunctions().clear_screen()
    print(INTERKAMEN)
    return current_user


def print_menu():
    """Print program menu."""
    print(Reminder().give_remind(USR_ACS) + '\n' + SEPARATOR + '\n')
    if MENU_NESTING:
        print(''.join(MENU_NESTING), '\n')
    print(' '.join(MENU_HEADER))
    for index, item in enumerate(PROGRAM_MENU, 1):
        print("[{}] - {}".format(index, item))
    print()


def get_main_or_sub_menu(sub_menu=None):
    """create main or sub-menu"""
    if sub_menu:
        program_menu = Accesse(USR_ACS).get_sub_menu(sub_menu)
    else:
        program_menu = Accesse(USR_ACS).get_menu_dict()
    PROGRAM_MENU.clear()
    PROGRAM_MENU.update(program_menu)
    del MENU_LIST[:]
    MENU_LIST.extend(list(PROGRAM_MENU.items()))


def check_backup():
    """Check if user 'admin', and make backup if positive."""
    backup = check_last_backup_date()
    if backup:
        Logs().create_log(CURRENT_USER['login'], "Backup done.")


def show_news():
    """Try to show news."""
    if USR_ACS != 'info':
        News().show_new_news(USR_ACS)
        BasicFunctions().clear_screen()
        print(INTERKAMEN)


if __name__ == '__main__':
    MENU_HEADER = ['\033[1m \t', None, '\n \033[0m']
    SEPARATOR = "\033[36m------------------------------\033[0m"
    PROGRAM_MENU = {}
    MENU_LIST = []
    MENU_NESTING = []
    Users().try_to_destroy()
    CURRENT_USER = login_program()
    USR_ACS = CURRENT_USER['accesse']
    check_backup()
    show_news()

    # Create main menu (otput and actions dict).
    MENU_HEADER[1] = '\033[4m ГЛАВНОЕ МЕНЮ \033[0m'
    get_main_or_sub_menu(None)

    while True:

        print_menu()
        print(SEPARATOR)
        USER_CHOISE = input("\nВыберете действие: ")
        BasicFunctions().clear_screen()

        if not BasicFunctions().check_number_in_range(
                USER_CHOISE, PROGRAM_MENU):
            continue

        USER_CHOISE = int(USER_CHOISE) - 1

        # Enter sub-menu.
        if '-->' in MENU_LIST[USER_CHOISE][0]:
            MENU_HEADER[1] = MENU_LIST[USER_CHOISE][0].split(' ')[1]
            MENU_NESTING.append(MENU_LIST[USER_CHOISE][0])
            get_main_or_sub_menu(sub_menu=MENU_LIST[USER_CHOISE][0])
            continue

        # Exit sub-menu.
        elif '<--' in MENU_LIST[USER_CHOISE][0]:
            MENU_NESTING = MENU_NESTING[:-1]
            if MENU_NESTING:
                MENU_HEADER[1] = MENU_NESTING[-1].split(' ')[1]
                get_main_or_sub_menu(sub_menu=MENU_NESTING[-1])
            else:
                MENU_HEADER[1] = '\033[4m ГЛАВНОЕ МЕНЮ \033[0m'
                get_main_or_sub_menu()

        # Exit program.
        elif MENU_LIST[USER_CHOISE][1] == 'exit program':
            Logs().create_log(
                CURRENT_USER['login'], 'exit program')
            sys.exit()

        # Make action.
        else:
            ACTION = MENU_LIST[USER_CHOISE][1]
            ACTION(CURRENT_USER)
            input('\n[нажмите ENTER]')
            BasicFunctions().clear_screen()
            Logs().create_log(
                CURRENT_USER['login'], MENU_LIST[USER_CHOISE][0])

        CURRENT_USER = Users().sync_user(CURRENT_USER['login'])
