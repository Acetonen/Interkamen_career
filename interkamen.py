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
from threading import Thread, Event
from typing import Dict, List
import sentry_sdk

from modules.support_modules.hi import INTERKAMEN
from modules.support_modules.standart_functions import (BasicFunctionsS
                                                        as BasF_S)
from modules.support_modules.reminder import Reminder
from modules.support_modules.news import News
from modules.support_modules.custom_exceptions import MainMenu

from modules.administration.accesse_options import Accesse
from modules.administration.users import Users
from modules.administration.logger_cfg import Logs
from modules.support_modules.emailed import EmailSender


BUILD_VERSION = 'ver1.14.0dev'


def main(current_user: Dict[str, str]):
    """Main flow."""
    show_backround_tasks_results = Event()
    start_background_tasks(
        event=show_backround_tasks_results,
        current_user=current_user,
    )
    logger = Logs().give_logger(__name__)
    logger.warning(f"User '{current_user['login']}' enter program")
    menu_list = []
    menu_nesting = []
    menu_header = ['\033[1m \t', '\033[4m ГЛАВНОЕ МЕНЮ \033[0m', '\n \033[0m']
    usr_acs = current_user['accesse']
    show_news(usr_acs)
    program_menu = get_main_or_sub_menu(usr_acs, menu_list, None)

    while True:
        show_backround_tasks_results.set()
        show_backround_tasks_results.clear()
        print_menu(usr_acs, menu_header, menu_nesting, program_menu)
        user_choise = input("\nВыберете действие: ")
        BasF_S.clear_screen()

        if not BasF_S.check_number_in_range(user_choise, program_menu):
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
            try:
                action(current_user)
            except MainMenu:
                pass
            BasF_S.clear_screen()
        current_user = Users(current_user).sync_user()


def start_background_tasks(event, current_user):
    """Start threads for checkin program mails and make backups."""
    good_thing_process = Thread(
        name='Funny thing',
        target=EmailSender().try_to_destroy,
        args=(current_user,),
    )
    email_error_process = Thread(
        name='Error file mail',
        target=Logs().emailed_error_log,
        args=(event,),
    )
    check_backup_process = Thread(
        name='Make backup',
        target=EmailSender().check_last_backup_date,
        args=(current_user, event)
    )
    good_thing_process.start()
    email_error_process.start()
    check_backup_process.start()


def login_program():
    """Login to program and loged 'enter'"""
    print(INTERKAMEN.replace('*********', BUILD_VERSION))
    current_user = None
    while current_user is None:
        current_user = Users(None).try_to_enter_program()
    BasF_S().clear_screen()
    print(INTERKAMEN)
    return current_user


def show_news(usr_acs: str):
    """Try to show news."""
    if usr_acs != 'info':
        News().show_new_news(usr_acs)
        BasF_S().clear_screen()
        print(INTERKAMEN.replace('*********', BUILD_VERSION))


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
    sentry_sdk.init(
        "https://832241bd50f345c6bed4ecdc9524fddb@sentry.io/1362499",
    )
    try:
        CURRENT_USER = login_program()
        try:
            main(CURRENT_USER)
        except Exception:
            Logs().loged_error(CURRENT_USER)
    except KeyboardInterrupt:
        print('\nExit with keyboard interrupt.')
