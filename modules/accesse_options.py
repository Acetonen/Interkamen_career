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

        self.actions = {'в': 'exit program',
                        'п': Users().change_user_password,
                        'c': Users().create_new_user,
                        'e': Users().edit_user,
                        'p': Users().print_all_users,
                        's': Logs().search_in_logs,
                        'a': Logs().show_all_logs,
                        'd': Logs().delete_all_logs,
                        'l': '--> log menu',
                        'г': '<-- Главное меню'}

        self.sub_menues = {
            '\033[91m--> log menu\033[0m': {
                's': 'search in logs',
                'd': 'delete logs from all users',
                'a': 'show all users logs',
                'в': 'Выйти из программы',
                'г': '<-- Главное меню'}}

        self.menu_options = {
            'basic': {'в': 'Выйти из программы',
                      'п': 'Поменять пароль'},
            'mechanic': {},
            'master': {},
            'boss': {},
            'admin': {'c': 'create new user',
                      'e': 'edit user',
                      's': 'show all users',
                      'l': '--> log menu',
                      'z': '-----------------'}}

        # Make admin menu red.
        for key in self.menu_options['admin']:
            self.menu_options['admin'][key] = (
                '\033[91m' + self.menu_options['admin'][key] + '\033[0m')

        self.menu_list = self.create_list(accesse, self.menu_options)
        self.actions_that_need_input = ['п']

    @classmethod
    def create_list(cls, accesse, options_list):
        """Create accesse and options menues"""
        options_list['mechanic'].update(options_list['basic'])
        options_list['master'].update(options_list['basic'])
        options_list['boss'].update(options_list['master'])
        options_list['boss'].update(options_list['mechanic'])
        options_list['admin'].update(options_list['boss'])

        options_list.pop('basic', None)
        return options_list[accesse]

    def get_sub_menu(self, sub_menu_name):
        """Return submenu"""
        return self.sub_menues[sub_menu_name]

    def get_menu_dict(self):
        """Give menue list"""
        return self.menu_list

    def get_actions_dict(self, menu_list):
        """Give menue list"""
        actions_list = {key: action for (key, action) in self.actions.items()
                        if key in menu_list}
        return actions_list

    def get_input_actions(self, menu_list):
        """Give menue list"""
        actions = self.get_actions_dict(menu_list)
        inp_actions = [x for x in self.actions_that_need_input if x in actions]
        return inp_actions
