#!/usr/bin/env python3
"""
This module work with User class and access.

.create_new_user() - add new user to company.

.edit_user() - edit all user propertes.

.change_password() - change user password.

.try_to_enter_program() check user login/password.

.sync_user() - sync current user with database.

.show_all_users() - print all users from base.

.get_all_users_list() - get list of all users.
"""

import getpass
from typing import List
import bcrypt
from modules.support_modules.standart_functions import (BasicFunctionsS
                                                        as BasF_S)
from modules.administration.logger_cfg import Logs


LOGGER = Logs().give_logger(__name__)


class User(dict, BasF_S):
    """User class."""
    def __init__(self, user_dict=None):
        super().__init__()
        if isinstance(user_dict, dict):
            self.update(user_dict)
        else:
            self.name = 'empty'
            self.accesse = 'info'
            self.login = 'empty'
            self.password = 'empty'
            self.email = 'empty'

    def __getattr__(self, name):
        if name in self:
            name = self[name]
        else:
            raise AttributeError("No such attribute: " + name)
        return name

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __repr__(self):
        output = (f"\nname:{self.name}\nlogin:{self.login}"
                  f"\npassword:{self.password}\naccesse:{self.accesse}"
                  f"\nemail:{self.email}")
        return output


class Users(BasF_S):
    """Users warking with program."""

    __slots__ = (
        'data_path',
        'user',
        'users_base',
    )

    access_list = ['admin', 'boss', 'master', 'mechanic', 'info']

    def __init__(self, user):
        self.user = user
        self.data_path = super().get_root_path() / 'data' / 'users_base'
        if not self.data_path.exists():
            self._create_new_users_base()
        self.users_base = super().load_data(self.data_path)

    def __repr__(self):
        output = ['']
        for login in self.users_base:
            for parametr in self.users_base[login]:
                output.append(
                    parametr + ':' + self.users_base[login][parametr])
            output.append('\n')
        return ' '.join(output)

    def _create_new_users_base(self):
        """Create new users base with new 'admin' account and key
        for encrypt database
        """
        new_key = super().create_new_key()
        password = bcrypt.hashpw(b'admin', bcrypt.gensalt())
        admin_user = {
            'name': 'Main Program Admin',
            'accesse': 'admin',
            'login': 'admin',
            'password': password,
            'email': 'empty',
            'key': new_key,
        }
        admin_user = User(admin_user)
        users_base = {'admin': admin_user}
        super().dump_data(self.data_path, users_base)

    @BasF_S.confirm_deletion_decorator
    def _check_deletion(self, user: User):
        """Delete user from database"""
        if 'key' in user:
            print("Yoy can't delete main admin user.")
            check = False
        else:
            check = True
        return check, user.login

    def _delete_user(self, user: User):
        """delete user from database."""
        user_deleted = False
        deletion_approved = self._check_deletion(user)
        if deletion_approved:
            self.users_base.pop(user.login, None)
            super().dump_data(self.data_path, self.users_base)
            user_deleted = True
            LOGGER.warning(
                f"User '{self.user['login']}' delete user '{user['login']}'")
        input('\n[ENTER] - выйти')
        return user_deleted

    def _change_user_access(self, user: User):
        """Change_user_access"""
        print("Choose new accesse:")
        new_accesse = super().choise_from_list(self.access_list)
        user.accesse = new_accesse
        LOGGER.warning(
            f"User '{self.user.login}' change access {user.login}")

    def _change_user_name(self, user: User):
        """Change user name"""
        new_name = input("Input new user name: ")
        old_name = user.name
        user.name = new_name
        LOGGER.warning(
            f"User '{self.user.login}' change name {old_name} -> {new_name}"
        )

    def _change_user_email(self, user: User):
        """Change user email"""
        new_email = super().check_correct_email()
        old_email = user.email
        user.email = new_email
        LOGGER.warning(
            f"User '{self.user.login}' change email {old_email} -> {new_email}"
        )

    def _working_with_user(self, choosen_user):
        """Edit choosen user."""
        while True:
            super().clear_screen()
            temp_user = self.users_base[choosen_user]
            print()
            print(self.users_base[choosen_user])
            edit_menu_dict = {
                'change user access': self._change_user_access,
                'change user name': self._change_user_name,
                'change user password': self.change_password,
                'delete user': self._delete_user,
                'change email': self._change_user_email,
                '[exit edition]': 'break',
            }
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

    def _try_set_new_password(self, user):
        while True:
            new_password = getpass.getpass("Введите новый пароль: ")
            if not new_password:
                break
            repeat_password = getpass.getpass("Повторите новый пароль: ")
            if new_password == repeat_password:
                new_password = new_password.encode('utf-8')
                user.password = bcrypt.hashpw(new_password, bcrypt.gensalt())
                self.users_base[user.login] = user
                super().dump_data(self.data_path, self.users_base)
                print("Новый пароль сохранен.")
                LOGGER.warning(
                    f"User '{user.login}' change password")
                input('\n[ENTER] - продолжить.')
                break
            else:
                print("Введенные пароли не совпадают.")
                input('\n[ENTER] - продолжить.')
            return new_password

    def create_new_user(self):
        """Create new user and save him in databese"""
        name = input("Input username: ")
        while True:
            login = input("Input login: ")
            if login in self.users_base:
                print("Login alredy exist, try enother.")
            elif not login:
                print("You must input login.")
            else:
                break
        password = input("Input password: ")
        password = password.encode('utf-8')
        password = bcrypt.hashpw(password, bcrypt.gensalt())
        print("Choose access by number:")
        access = super().choise_from_list(self.access_list)
        email = super().check_correct_email()
        new_user = {
            'login': login,
            'name': name,
            'accesse': access,
            'password': password,
            'email': email,
        }
        self.users_base[login] = User(new_user)
        print(f"\033[92m user '{login}' created. \033[0m")
        LOGGER.warning(
            f"User '{self.user.login}' create new user: '{login}'")
        super().dump_data(self.data_path, self.users_base)
        input('\n[ENTER] - выйти')

    def edit_user(self):
        """
        Change user parametrs.
        """
        while True:
            super().clear_screen()
            print("Input number of user to edit:")
            choosen_user = super().choise_from_list(
                self.users_base, none_option=True)
            if choosen_user:
                self._working_with_user(choosen_user)
            else:
                break

    def change_password(self, user):
        """Changing password"""
        while True:
            old_password = input("Введите старый пароль: ")
            old_password = old_password.encode('utf-8')
            if bcrypt.checkpw(old_password, user.password):
                new_password = self._try_set_new_password(user)
                if new_password:
                    break
            elif not old_password:
                break
            else:
                print("Неправильный пароль.")
                input('\n[ENTER] - продолжить.')

    def try_to_enter_program(self):
        """
        Take user login/password input and return current user privilege
        """
        user_in = None
        while True:
            login = input("Имя пользователя: ")
            password = getpass.getpass("Введите пароль: ")
            sucsesse_login = super().check_login_password(self.users_base,
                                                          login,
                                                          password)
            if sucsesse_login:
                user_in = self.users_base[login]
                break
        return user_in

    def sync_user(self):
        """Sync current user with base"""
        self.users_base = super().load_data(self.data_path)
        return self.users_base[self.user.login]

    def show_all_users(self):
        """Print all users from base"""
        for login in self.users_base:
            print(self.users_base[login])
        input('\n[ENTER] - выйти')

    def get_all_users_list(self) -> List['Users']:
        """Get all users list"""
        users_list = [user for user in self.users_base]
        return users_list
