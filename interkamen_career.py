#!usr/bin/env python3
"""
This program provides control of all data and statistic of Career Interkamen.
"""

import shelve
from modules import users, access
from modules.absolyte_path_module import USERS_PATH


def print_menu():
    """Print program menu."""
    print('\033[4m' + '\033[1m' + "\n\tМеню программы.\n" + '\033[0m')
    for key in sorted(PROGRAM_MENU):
        print("[{}] - {}".format(key, PROGRAM_MENU[key]))


def sync_current_user():
    """Bump CURRENT_USER log to database"""
    with shelve.open(USERS_PATH) as users_base:
        users_base[CURRENT_USER.login] = CURRENT_USER


if __name__ == '__main__':

    CURRENT_USER = None
    while CURRENT_USER is None:
        CURRENT_USER = users.try_to_enter_program()
    CURRENT_USER.bump_log('enter in program')

    OPTIONS_LIST = access.create_options_list(
        CURRENT_USER.get_access(), CURRENT_USER)
    OPTIONS_LIST['м'] = (print_menu, )

    LOG_LIST = access.LOG_LIST

    PROGRAM_MENU = access.create_menu_list(CURRENT_USER.get_access())
    print_menu()

    while True:
        USER_CHOISE = input("\n[м] - Показать меню программы"
                            "\nВыберете действие:\n")
        print()
        if USER_CHOISE not in OPTIONS_LIST:
            print("Нет такого варианта.")
            continue
        CURRENT_USER.bump_log(LOG_LIST[USER_CHOISE])
        for action in OPTIONS_LIST[USER_CHOISE]:
            action()

        sync_current_user()
