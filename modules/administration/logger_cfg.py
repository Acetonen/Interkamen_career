#!/usr/bin/env python3
"""Logging setup."""

import os
import socket
import smtplib
import time
import logging
import logging.handlers
from modules.support_modules.emailed import EmailSender
from modules.support_modules.standart_functions import BasicFunctions


class Logs(BasicFunctions):
    """Setup different handlers to logs."""

    def __init__(self):
        self.log_path = super().get_root_path() / 'data' / 'file.log'
        self.error_log_path = super().get_root_path() / 'data' / 'error.log'

    @classmethod
    def send_error_to_email(cls):
        """Send error log to email."""
        handler = logging.handlers.SMTPHandler(
            mailhost=('smtp.gmail.com', 587),
            fromaddr=EmailSender().login,
            toaddrs=['acetonen@gmail.com'],
            subject='ERROR',
            credentials=(EmailSender().login, EmailSender().password),
            secure=(),
        )
        handler.setLevel(logging.ERROR)
        log_format = logging.Formatter(
            '[%(asctime)s] %(filename)s [LINE:%(lineno)d]# %(levelname)-8s'
            + '%(message)s'
        )
        handler.setFormatter(log_format)
        return handler

    def save_info_to_file(self):
        """Save info log to file."""
        handler = logging.FileHandler(self.log_path)
        handler.setLevel(logging.WARNING)
        log_format = logging.Formatter('[%(asctime)s] %(message)s')
        handler.setFormatter(log_format)
        return handler

    def save_error_to_file(self):
        """Save error log to file."""
        handler = logging.FileHandler(self.error_log_path)
        handler.setLevel(logging.ERROR)
        log_format = logging.Formatter(
            '[%(asctime)s] %(filename)s [LINE:%(lineno)d]# %(levelname)-8s'
            + '\n%(message)s'
        )
        handler.setFormatter(log_format)
        return handler

    def loged_error(self, current_user):
        """Make error log."""
        err_logger = logging.getLogger("ERR")
        super().clear_screen()
        print(
            "\033[91mВНИМАНИЕ! Произошла ошибка преведшая к завершению "
            "программы \nПожалуйста, не закрывайте окно, лог ошибки "
            "отправляется администратору...\033[0m")
        try:
            smtp = smtplib.SMTP('smtp.gmail.com', 587)
            smtp.starttls()
            smtp.login(EmailSender().login, EmailSender().password)
        except (smtplib.SMTPAuthenticationError,
                socket.gaierror,
                ConnectionResetError):
            err_logger.addHandler(self.save_error_to_file())
            connection_problem = True
        else:
            err_logger.addHandler(self.send_error_to_email())
            connection_problem = False
        finally:
            err_logger.exception(f"User '{current_user['login']}' make error:")
            if connection_problem:
                print("\033[93m\nПроблемы с подключением к интернету."
                      "\nЛог сохранен в файл и будет отправлен при "
                      "восстановлении подключения.\033[0m")
            else:
                print("\033[92m\nЛог отправлен, спасибо за ожидание.\033[0m")
            print("\nПрограмма закроется автоматически через 5 секунд.")
        time.sleep(5)

    def emailed_error_log(self):
        """Try to emailed error log file if exist."""
        if self.error_log_path.exists():
            with open(self.error_log_path, 'r', encoding='utf-8') as file:
                log = file.read()
            unsucsesse = EmailSender().try_email(
                recivers='resivers list',
                subject="ERROR",
                message=log,
            )
            if unsucsesse:
                print(unsucsesse)
                time.sleep(5)
            else:
                os.remove(self.error_log_path)

    def give_logger(self, name):
        "give logger to module."
        logger = logging.getLogger(name)
        logger.addHandler(self.save_info_to_file())
        return logger
