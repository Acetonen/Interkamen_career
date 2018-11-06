#!usr/bin/env python3
"""This module give to program choise tree and meny depend on user access"""

from modules import users

LOG_LIST = {'enter': '\033[94m enter in program \033[0m',
            'c': 'create new user',
            'd': 'delete user',
            's': 'show all users',
            'п': 'change password',
            'l': 'show logs',
            'a': 'show all users logs',
            'w': 'delete logs from all useers',
            'в': '\033[94m exit program \033[0m',
            'p': 'clean log of current user',
            'м': 'Показать меню программы'}


def create_options_list(current_user):
    """Create list of options depend on user access"""
    basic_options = {'в': None,
                     'п': (current_user.change_password, )}
    mechanic_options = {}
    master_options = {}
    admin_options = {'c': (users.create_new_user, ),
                     'd': (users.delete_user, ),
                     's': (users.show_all_users, ),
                     'l': (current_user.print_log, ),
                     'a': (users.show_all_logs, ),
                     'w': (users.delete_all_logs, current_user.clean_log),
                     'p': (current_user.clean_log, )}

    mechanic_options.update(basic_options)
    master_options.update(basic_options)
    admin_options.update(master_options)
    admin_options.update(mechanic_options)
    access_list = {'admin': admin_options,
                   'master': master_options,
                   'mechanic': mechanic_options}
    options_list = access_list[current_user.get_access()]
    return options_list


def create_menu_list(access):
    """Create list of menu depend on user access"""
    basic_menu = {'в': 'Выйти из программы',
                  'п': 'Поменять пароль'}
    mechanic_menu = {}
    master_menu = {}
    admin_menu = {'c': 'create new user',
                  'd': 'delete user',
                  's': 'show all users',
                  'l': 'show logs',
                  'a': 'show all users logs',
                  'w': 'delete logs from all useers',
                  'p': 'clean log of current user',
                  'z': '----------------------------'}

    for key in admin_menu:
        admin_menu[key] = '\033[91m' + admin_menu[key] + '\033[0m'

    mechanic_menu.update(basic_menu)
    master_menu.update(basic_menu)
    admin_menu.update(master_menu)
    admin_menu.update(mechanic_menu)
    access_list = {'admin': admin_menu,
                   'master': master_menu,
                   'mechanic': mechanic_menu}
    menu_list = access_list[access]
    return menu_list
