#!/usr/bin/env python3
"""
This module work with User class and access.

"""


import getpass
from modules.support_modules.absolyte_path_module import AbsolytePath
from modules.support_modules.standart_functions import BasicFunctions


class Users(BasicFunctions):
    """Users warking with program."""

    data_path = AbsolytePath('users_base').get_absolyte_path()
    access_list = ['admin', 'boss', 'master', 'mechanic']

    def __init__(self):
        self.users_base = super().load_data(self.data_path)

    def __str__(self):
        output = ['']
        for login in self.users_base:
            for parametr in self.users_base[login]:
                output.append(
                    parametr + ':' + self.users_base[login][parametr])
            output.append('\n')
        return ' '.join(output)

    @classmethod
    def print_user(cls, user):
        """Print one user"""
        print("name:{name}\nlogin:{login}\n\
password:{password}\naccesse:{accesse}\n".format(**user))

    def create_new_user(self):
        """Create new user and save him in databese"""
        name = input("Input username: ")
        while True:
            login = input("Input login: ")
            if login in self.users_base:
                print("Login alredy exist, try enother.")
            else:
                break
        password = input("Input password: ")
        print("Choose access by number:")
        access = super().choise_from_list(self.access_list)
        self.users_base[login] = {'login': login,
                                  'name': name,
                                  'accesse': access,
                                  'password': password}
        log = f"\033[92m user '{login}' created. \033[0m"
        print(log)
        super().save_log_to_temp_file(log)
        super().dump_data(self.data_path, self.users_base)

    def edit_user(self):
        """
        Change user parametrs.
        """

        print("Input number of user to edit:")
        choosen_user = super().choise_from_list(
            self.users_base, none_option=True)
        if choosen_user:
            super().save_log_to_temp_file(choosen_user)
        super().clear_screen()
        while choosen_user:
            temp_user = self.users_base[choosen_user]
            print()
            self.print_user(self.users_base[choosen_user])
            edit_menu_dict = {'change user access': self._change_user_access,
                              'change user name': self._change_user_name,
                              'change user password': self.change_password,
                              'delete user': self._delete_user,
                              '[exit edition]': 'break'}
            print("Choose action:")
            choosen_action = super().choise_from_list(edit_menu_dict)

            print()
            if choosen_action in ['[exit edition]', '']:
                break
            are_user_deleted = edit_menu_dict[choosen_action](temp_user)
            if are_user_deleted:
                break
            self.users_base[choosen_user] = temp_user
            super().dump_data(self.data_path, self.users_base)
            super().clear_screen()

    def _delete_user(self, user):
        """Delete user from database"""
        user_deleted = False
        if user['accesse'] == 'admin' and self._check_only_admin():
            print("If 'admin' user alone you can't delete him.")
        elif super().confirm_deletion(user['login']):
            self.users_base.pop(user['login'], None)
            super().dump_data(self.data_path, self.users_base)
            user_deleted = True
            log = "\033[91m user '{}' - deleted. \033[0m".format(user['login'])
            super().save_log_to_temp_file(log)
        return user_deleted

    def _check_only_admin(self):
        """Check if admin user only one in base"""
        check = False
        admin_counter = 0
        for login in self.users_base:
            if self.users_base[login]['accesse'] == 'admin':
                admin_counter += 1
        if admin_counter == 1:
            check = True
        return check

    def _change_user_access(self, user):
        """Change_user_access"""
        print("Choose new accesse:")
        new_accesse = super().choise_from_list(self.access_list)
        user['accesse'] = new_accesse
        super().save_log_to_temp_file(' change access')

    def _change_user_name(self, user):
        """Change user name"""
        new_name = input("Input new user name: ")
        user['name'] = new_name
        super().save_log_to_temp_file(f' change name -> {new_name} ')

    def change_password(self, user):
        """Changing password"""
        old_password = input("Введите старый пароль: ")
        if old_password == user['password']:
            new_password = getpass.getpass("Введите новый пароль: ")
            repeat_password = getpass.getpass("Повторите новый пароль: ")
            if new_password == repeat_password:
                user['password'] = new_password
                self.users_base[user['login']] = user
                super().dump_data(self.data_path, self.users_base)
                print("Новый пароль сохранен.")
                super().save_log_to_temp_file(' change password')
            else:
                print("Введенные пароли не совпадают.")
        else:
            print("Неправильный пароль.")

    def try_to_enter_program(self):
        """
        Take user login/password input and return current user privilege
        """
        user_in = None
        login = input("Имя пользователя: ")
        if login in self.users_base:
            while True:
                password = getpass.getpass("Введите пароль: ")
                if self.users_base[login]['password'] == password:
                    user_in = self.users_base[login]
                    break
                else:
                    print("Неправильный пароль, попробуйте еще раз.")
        else:
            print("Такого пользователя не существует.")
        return user_in

    def sync_user(self, user_login):
        """Sync current user with base"""
        self.users_base = super().load_data(self.data_path)
        return self.users_base[user_login]

    def show_all_users(self):
        """Print all users from base"""
        for login in self.users_base:
            self.print_user(self.users_base[login])

    def get_all_users_list(self):
        """Get all users list"""
        users_list = [user for user in self.users_base]
        return users_list
