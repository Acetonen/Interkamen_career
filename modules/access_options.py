#!usr/bin/env python3
"""
This module give to program choise tree and meny depend on user access.

Classes: Accesse: 'create_list',
                  'get_menue_list',
                  'get_actions_list'
                  'get_actions_with_input'
"""

from modules.log_class import Logs
from modules.users import Users


class Accesse:
    """Give to program 'choise tree' and 'meny' depend on user access"""
    def __init__(self, accesse):

        action_options = {
            'basic': {'в': None,
                      'п': Users().change_user_password},
            'mechanic': {},
            'master': {},
            'admin': {'c': Users().create_new_user,
                      'e': Users().edit_user,
                      's': Users().print_all_users,
                      'l': Logs().search_in_logs,
                      'a': Logs().show_all_logs,
                      'w': Logs().delete_all_logs}}

        menue_options = {
            'basic': {'в': 'Выйти из программы',
                      'п': 'Поменять пароль'},
            'mechanic': {},
            'master': {},
            'admin': {'c': 'create new user',
                      'e': 'edit user',
                      's': 'show all users',
                      'l': 'search in logs',
                      'a': 'show all users logs',
                      'w': 'delete logs from all useers',
                      'z': '----------------------------'}}

        # Make admin menu red.
        for key in menue_options['admin']:
            menue_options['admin'][key] = (
                '\033[91m' + menue_options['admin'][key] + '\033[0m')

        self.menue_list = self.create_list(accesse, menue_options)
        self.actions_list = self.create_list(accesse, action_options)
        self.actions_that_need_input = ['п']

    @classmethod
    def create_list(cls, accesse, options_list):
        """Create accesse and options menues"""
        options_list['mechanic'].update(options_list['basic'])
        options_list['master'].update(options_list['basic'])
        options_list['admin'].update(options_list['master'])
        options_list['admin'].update(options_list['mechanic'])

        options_list.pop('basic', None)
        return options_list[accesse]

    def get_menue_list(self):
        """Give menue list"""
        return self.menue_list

    def get_actions_list(self):
        """Give menue list"""
        return self.actions_list

    def get_input_actions(self):
        """Give menue list"""
        actions = [
            x for x in self.actions_that_need_input if x in self.actions_list]
        return actions
