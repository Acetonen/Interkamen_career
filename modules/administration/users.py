#!/usr/bin/env python3
"""
This module work with User class and access.

"""

import getpass
from typing import List
import bcrypt
from modules.support_modules.standart_functions import BasicFunctions
from modules.administration.logger_cfg import Logs


LOGGER = Logs().give_logger(__name__)


class User(dict, BasicFunctions):
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
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

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


class Users(BasicFunctions):
    """Users warking with program."""

    access_list = ['admin', 'boss', 'master', 'mechanic', 'info']

    def __init__(self, user):
        self.data_path = super().get_root_path() / 'data' / 'users_base'
        self.user = user
        self.users_base = super().load_data(self.data_path)

    def __repr__(self):
        output = ['']
        for login in self.users_base:
            for parametr in self.users_base[login]:
                output.append(
                    parametr + ':' + self.users_base[login][parametr])
            output.append('\n')
        return ' '.join(output)

    def _delete_user(self, user: User):
        """Delete user from database"""
        user_deleted = False
        if user.accesse == 'admin' and self._check_only_admin():
            print("If 'admin' user alone you can't delete him.")
        elif super().confirm_deletion(user.login):
            self.users_base.pop(user.login, None)
            super().dump_data(self.data_path, self.users_base)
            user_deleted = True
            LOGGER.warning(
                f"User '{self.user['login']}' delete user '{user['login']}'")
        input('\n[ENTER] - выйти')
        return user_deleted

    def _check_only_admin(self):
        """Check if admin user only one in base"""
        check = False
        admin_counter = 0
        for login in self.users_base:
            if self.users_base[login].accesse == 'admin':
                admin_counter += 1
        if admin_counter == 1:
            check = True
        return check

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
        print("Input number of user to edit:")
        choosen_user = super().choise_from_list(
            self.users_base, none_option=True)
        super().clear_screen()
        while choosen_user:
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
            super().clear_screen()

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

    def check_login_password(self, login, password):
        """Check user login and password."""
        sucsesse_login = False
        password = password.encode('utf-8')
        if (login in self.users_base and
                bcrypt.checkpw(password, self.users_base[login].password)):
            sucsesse_login = True
        else:
            print("Неправильные имя пользователя или пароль.")
        return sucsesse_login

    def try_to_enter_program(self):
        """
        Take user login/password input and return current user privilege
        """
        user_in = None
        while True:
            login = input("Имя пользователя: ")
            password = getpass.getpass("Введите пароль: ")
            sucsesse_login = self.check_login_password(login, password)
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

    def get_users_emails(self, user_type=None) -> List[str]:
        """Give users emails by user type."""
        if user_type:
            emails_list = [
                self.users_base[user].email
                for user in self.users_base
                if self.users_base[user].email
                and self.users_base[user].accesse == user_type
            ]
        else:
            emails_list = [
                self.users_base[user].email
                for user in self.users_base
                if self.users_base[user].email
            ]
        return emails_list
