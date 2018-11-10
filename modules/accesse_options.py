#!usr/bin/env python3
"""
This module give to program choise tree and meny depend on user access.

Classes: Accesse: 'create_list',
                  'get_menue_list',
                  'get_actions_list'
                  'get_actions_with_input'
                  'get_sub_menu'
"""

from collections import OrderedDict
from modules.log_class import Logs
from modules.users import Users
from modules.workers_module import AllWorkers


class Accesse:
    """Give to program 'choise tree' and 'meny' depend on user access"""
    def __init__(self, accesse='mechanic'):

        self.sub_menus = OrderedDict
        self.sub_menus = {
            '\033[91m--> [log_menu] \033[0m': {
                'search in logs': lambda *arg: Logs().search_in_logs(),
                'delete all logs': lambda *arg: Logs().delete_all_logs(),
                'show all logs': lambda *arg: Logs().show_all_logs(),
                },
            '\033[91m--> [users_menu] \033[0m': {
                'create new user': lambda *arg: Users().create_new_user(),
                'edit user': lambda *arg: Users().edit_user(),
                'show all users': lambda *arg: Users().show_all_users()
                },
            '--> [Работники] ': {
                'Новый работник': lambda *arg: AllWorkers().add_new_worker(),
                'Все работники': lambda *arg: AllWorkers().print_all_workers(),
                'Редактировать данные': lambda *arg: AllWorkers().edit_worker()
                }
            }

        self.sub_standart_options = {
            '<-- [Главное меню]': 'возврат в главное меню',
            '\033[93mВыйти из программы\033[0m': 'exit program',
            }

        self.menu_options = {
            'basic': {
                'Поменять пароль': lambda arg: Users().change_password(arg),
                '\033[93mВыйти из программы\033[0m': 'exit program'
                },
            'mechanic': {},
            'master': {},
            'boss': {'--> [Работники] ': 'sub-menu'},
            'admin': {'\033[91m--> [users_menu] \033[0m': 'sub-menu',
                      '\033[91m--> [log_menu] \033[0m': 'sub-menu',
                      '\033[91m-----------------\033[0m': 'separator'}
            }
        self.menu_list = self.create_list(accesse, self.menu_options)

    @classmethod
    def create_list(cls, accesse, options_list):
        """Create accesse and options menus"""
        options_list['mechanic'].update(options_list['basic'])
        options_list['boss'].update(options_list['master'])
        options_list['boss'].update(options_list['mechanic'])
        options_list['admin'].update(options_list['boss'])
        options_list['master'].update(options_list['basic'])
        return options_list[accesse]

    def get_sub_menu(self, sub_menu_name):
        """Return sub-menu"""
        self.sub_menus[sub_menu_name].update(self.sub_standart_options)
        return self.sub_menus[sub_menu_name]

    def get_menu_dict(self):
        """Give menu dict"""
        return self.menu_list
