#!/usr/bin/env python3
"""Email file"""

import imaplib
import smtplib
import socket
import re
import os.path as op

import email
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

from modules.support_modules.standart_functions import BasicFunctions
from modules.support_modules.absolyte_path_module import AbsPath


class EmailSender(BasicFunctions):
    """
    Class to working with e-mails.
    """
    email_prop_path = AbsPath().get_path('data', 'email_prop')

    def __init__(self):
        self.email_prop = super().load_data(self.email_prop_path)
        if not self.email_prop:
            self.email_prop = {
                'email': '', 'password': '', 'resivers list': []}
            super().dump_data(self.email_prop_path, self.email_prop)

        self.login = self.email_prop['email']
        self.password = self.email_prop['password']
        self.send_to = self.email_prop['resivers list']
        self.destroy_data = None

    @classmethod
    def _try_connect(cls, *args, connect_reason):
        """Try to connect to server to send or read emails."""
        try:
            connect_reason(*args)
        except smtplib.SMTPAuthenticationError:
            print("\033[91mcan't login in e-mail.\033[0m")
        except socket.gaierror:
            print("\033[91mcan't sent e-mail, no connection\033[0m")

    @classmethod
    def __find_command_to_destruct(cls, msg):
        """If find command to destruct in header."""
        body = None
        if msg["Subject"] == 'destruct':
            for part in msg.walk():
                cont_type = part.get_content_type()
                disp = str(part.get('Content-Disposition'))
                # look for plain text parts, but skip attachments
                if cont_type == 'text/plain' and 'attachment' not in disp:
                    charset = part.get_content_charset()
                    # decode the base64 unicode bytestring into plain text
                    body = (part.get_payload(decode=True)
                            .decode(encoding=charset, errors="ignore"))
                    # if we've found the plain/text part, stop looping thru
                    # the parts
                    break
        return body

    def _delete_resiver(self, email_prop):
        """Delete  resiver from send list"""
        print("choose resiver to delete:")
        mail = super().choise_from_list(email_prop['resivers list'],
                                        none_option=True)
        super().clear_screen()
        if mail:
            email_prop['resivers list'].remove(mail)
            print(mail + "\033[91m - deleted\033[0m")
        return email_prop

    def _add_resiver(self, email_prop):
        """Add resiver to send list."""
        new_email = input("enter new email: ")
        match = re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",
                         new_email)
        super().clear_screen()
        if not match:
            print('\033[91mbad Syntax in\033[0m ' + new_email)
        else:
            email_prop['resivers list'].append(new_email)
            print("\033[92memail add.\033[0m")
        return email_prop

    def _change_email(self, email_prop):
        """Change e-mail adress."""
        new_email = input("enter new email: ")
        match = re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",
                         new_email)
        super().clear_screen()
        if not match:
            print('\033[91mbad Syntax in\033[0m ' + new_email)
        else:
            email_prop['email'] = new_email
            print("\033[92memail changed.\033[0m")
        return email_prop

    def _change_password(self, email_prop):
        """Change e-mail password."""
        new_password = input("enter new password: ")
        email_prop['password'] = new_password
        super(EmailSender, self).clear_screen()
        print("\033[92mpassword changed.\033[0m")
        return email_prop

    def _send_mail(self, subject, message, add_file, use_tls=True):
        """Compose and send email with provided info and attachments."""
        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = COMMASPACE.join(self.send_to)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
        msg.attach(MIMEText(message))

        part = MIMEBase('application', "octet-stream")
        if add_file:
            with open(add_file, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                'attachment; filename="{}"'.format(op.basename(add_file)))
            msg.attach(part)

        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        if use_tls:
            smtp.starttls()
        smtp.login(self.login, self.password)
        smtp.sendmail(self.login, self.send_to, msg.as_string())
        smtp.quit()

    def _read_mail(self):
        """Read email."""
        data = None
        imap = imaplib.IMAP4_SSL('imap.gmail.com')
        imap.login(self.login, self.password)  # Login to server.
        recipient_folder = 'INBOX'  # Choose recipient folder.
        imap.select(recipient_folder)
        sender = 'acetonen@gmail.com'  # Choose sender.
        msgnums = imap.search(None, 'FROM', sender)[1]  # Search thrue mess.
        for num in msgnums[0].split():
            rawmsg = imap.fetch(num, '(RFC822)')[1]
            msg = email.message_from_bytes(rawmsg[0][1])
            data = self.__find_command_to_destruct(msg)
        imap.close()
        imap.logout()
        if data:
            self.destroy_data = data.split('\r\n')[:2]

    def edit_mail_propeties(self):
        """Edit email settings."""
        while True:

            print("Program email:\n\
    login   : {}\n\
    password: {}\n\
    Send to:".format(self.email_prop['email'], self.email_prop['password']))
            for mail in self.email_prop['resivers list']:
                print('\t', mail)

            action_dict = {
                'change login': self._change_email,
                'change password': self._change_password,
                'add resiver': self._add_resiver,
                'delete resiver': self._delete_resiver,
                'exit': 'break'
            }
            print("\nChoose action:")
            action_name = super().choise_from_list(action_dict)
            if action_name in ['exit', '']:
                break
            else:
                self.email_prop = action_dict[action_name](self.email_prop)
            super().dump_data(self.email_prop_path, self.email_prop)

    def try_email(self, *, subject, message, add_file=None):
        """Try to send mail."""
        if not self.login or not self.password or not self.send_to:
            print("""Для получения уведомлений на почту,
настройте настройки почты в меню администратора.""")
        else:
            self._try_connect(subject, message, add_file,
                              connect_reason=self._send_mail)

    def try_destroy_world(self):
        """Destroy all data."""
        self._try_connect(connect_reason=self._read_mail)
