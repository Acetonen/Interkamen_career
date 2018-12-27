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
from typing import Dict, List
from modules.support_modules.hi import INTERKAMEN
from modules.support_modules.backup import check_last_backup_date
from modules.support_modules.standart_functions import BasicFunctions as BasF
from modules.support_modules.reminder import Reminder
from modules.support_modules.news import News

from modules.administration.accesse_options import Accesse
from modules.administration.users import Users
from modules.administration.logger_cfg import Logs


def main(current_user: Dict[str, str]):
    """Main flow."""
    Logs().emailed_error_log()
    logger = Logs().give_logger(__name__)
    logger.warning(f"User '{current_user['login']}' enter program")
    menu_list = []
    menu_nesting = []
    menu_header = ['\033[1m \t', '\033[4m ГЛАВНОЕ МЕНЮ \033[0m', '\n \033[0m']
    usr_acs = current_user['accesse']
    show_news(usr_acs)
    check_last_backup_date(current_user)
    Users(None).try_to_destroy()
    program_menu = get_main_or_sub_menu(usr_acs, menu_list, None)

    while True:
        print_menu(usr_acs, menu_header, menu_nesting, program_menu)
        user_choise = input("\nВыберете действие: ")
        BasF.clear_screen()

        if not BasF.check_number_in_range(user_choise, program_menu):
            continue

        user_choise = int(user_choise) - 1  # User choise == Index

        # Enter sub-menu.
        if '-->' in menu_list[user_choise][0]:
            menu_header[1] = menu_list[user_choise][0].split(' ')[1]
            menu_nesting.append(menu_list[user_choise][0])
            program_menu = get_main_or_sub_menu(
                usr_acs, menu_list,
                sub_menu=menu_list[user_choise][0]
            )
            continue

        # Exit sub-menu.
        elif '<--' in menu_list[user_choise][0]:
            menu_nesting = menu_nesting[:-1]  # Go one menu up.
            if menu_nesting:
                menu_header[1] = menu_nesting[-1].split(' ')[1]
                program_menu = get_main_or_sub_menu(
                    usr_acs, menu_list,
                    sub_menu=menu_nesting[-1]
                )
            else:
                menu_header[1] = '\033[4m ГЛАВНОЕ МЕНЮ \033[0m'
                program_menu = get_main_or_sub_menu(
                    usr_acs, menu_list)

        # Exit program.
        elif menu_list[user_choise][1] == 'exit program':
            sys.exit()

        # Make action.
        else:
            action = menu_list[user_choise][1]
            action(current_user)
            input('\n[нажмите ENTER]')  # Show menu on screen.
            BasF.clear_screen()
        current_user = Users(current_user).sync_user()


def login_program():
    """Login to program and loged 'enter'"""
    print(INTERKAMEN)
    current_user = None
    while current_user is None:
        current_user = Users(None).try_to_enter_program()
    BasF().clear_screen()
    print(INTERKAMEN)
    return current_user


def show_news(usr_acs: str):
    """Try to show news."""
    if usr_acs != 'info':
        News().show_new_news(usr_acs)
        BasF().clear_screen()
        print(INTERKAMEN)


def print_menu(usr_acs: str,
               menu_header: str,
               menu_nesting: List[str],
               program_menu: Dict[str, str]):
    """Print program menu."""
    separator = "\033[36m------------------------------\033[0m"
    print(Reminder().give_remind(usr_acs) + '\n' + separator + '\n')
    if menu_nesting:
        print(''.join(menu_nesting), '\n')
    print(' '.join(menu_header))
    for index, item in enumerate(program_menu, 1):
        print("[{}] - {}".format(index, item))
    print()
    print(separator)


def get_main_or_sub_menu(usr_acs: str,
                         menu_list: List[str],
                         sub_menu: str = False) -> Dict[str, str]:
    """create main or sub-menu if sub_menu=True"""
    if sub_menu:
        program_menu = Accesse(usr_acs).get_sub_menu(sub_menu)
    else:
        program_menu = Accesse(usr_acs).get_menu_dict()
    del menu_list[:]
    menu_list.extend(list(program_menu.items()))
    return program_menu


if __name__ == '__main__':
    CURRENT_USER = login_program()
    try:
        main(CURRENT_USER)
    except Exception:
        Logs().loged_error(CURRENT_USER)
