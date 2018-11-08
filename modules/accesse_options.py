#!usr/bin/env python3
"""
This module give to program choise tree and meny depend on user access.

Classes: Accesse: 'create_list',
                  'get_menue_list',
                  'get_actions_list'
                  'get_actions_with_input'
                  'get_sub_menu'
"""

from modules.log_class import Logs
from modules.users import Users


class Accesse:
    """Give to program 'choise tree' and 'meny' depend on user access"""
    def __init__(self, accesse='mechanic'):

        self.actions = {
            'в': 'exit program',
            'п': lambda arg: Users().change_user_password(arg),
            'c': lambda *arg: Users().create_new_user(),
            'e': lambda *arg: Users().edit_user(),
            'p': lambda *arg: Users().print_all_users(),
            's': lambda *arg: Logs().search_in_logs(),
            'a': lambda *arg: Logs().show_all_logs(),
            'd': lambda *arg: Logs().delete_all_logs(),
            'u': '--> [users menu]',
            'l': '--> [log menu]',
            'г': '<-- [Главное меню]'
            }

        self.sub_menus = {
            '\033[91m--> [log menu]\033[0m': {
                's': 'search in logs',
                'd': 'delete logs from all users',
                'a': 'show all users logs'},
            '\033[91m--> [users menu]\033[0m': {
                'c': 'create new user',
                'e': 'edit user',
                'p': 'show all users'}
            }

        self.sub_standart_options = {
            'в': 'Выйти из программы',
            'м': 'Показать меню программы',
            'г': '<-- [Главное меню]'
            }

        self.menu_options = {
            'basic': {'в': 'Выйти из программы',
                      'п': 'Поменять пароль',
                      'м': 'Показать меню программы'},
            'mechanic': {},
            'master': {},
            'boss': {},
            'admin': {'u': '--> [users menu]',
                      'l': '--> [log menu]',
                      'z': '-----------------'}
            }

        # Make admin menu red.
        for key in self.menu_options['admin']:
            self.menu_options['admin'][key] = (
                '\033[91m' + self.menu_options['admin'][key] + '\033[0m')

        self.menu_list = self.create_list(accesse, self.menu_options)

    @classmethod
    def create_list(cls, accesse, options_list):
        """Create accesse and options menus"""
        options_list['mechanic'].update(options_list['basic'])
        options_list['master'].update(options_list['basic'])
        options_list['boss'].update(options_list['master'])
        options_list['boss'].update(options_list['mechanic'])
        options_list['admin'].update(options_list['boss'])

        options_list.pop('basic', None)
        return options_list[accesse]

    def get_sub_menu(self, sub_menu_name):
        """Return submenu"""
        self.sub_menus[sub_menu_name].update(
            self.sub_standart_options.items())
        return self.sub_menus[sub_menu_name]

    def get_menu_dict(self):
        """Give menue list"""
        return self.menu_list

    def get_actions_dict(self, menu_list):
        """Give menue list"""
        actions_list = {key: action for (key, action) in self.actions.items()
                        if key in menu_list}
        return actions_list
