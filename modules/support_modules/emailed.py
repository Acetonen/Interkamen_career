#!/usr/bin/env python3
"""Email file"""

from __future__ import annotations

import imaplib
import smtplib
import socket
import re

import email
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email.mime.image import MIMEImage
from email import encoders

from typing import List, Union
from pathlib import PurePath
from modules.support_modules.standart_functions import BasicFunctions


class EmailSender(BasicFunctions):
    """
    Class to working with e-mails.
    """
    def __init__(self):
        self.email_prop_path = super().get_root_path() / 'data' / 'email_prop'
        self.email_prop = super().load_data(self.email_prop_path)
        if not self.email_prop:
            self.email_prop = {
                'email': '',
                'password': '',
                'resivers list': [],
            }
            super().dump_data(self.email_prop_path, self.email_prop)

        self.login = self.email_prop['email']
        self.password = self.email_prop['password']
        self.destroy_data = None

    @classmethod
    def _try_connect(
            cls,
            connect_reason: Union[
                'EmailSender._send_mail',
                'EmailSender._read_mail',
            ],
            *recivers: List[str],
            **mail_parts,
    ):
        """Try to connect to server to send or read emails."""
        unsucsesse = None
        try:
            connect_reason(*recivers, **mail_parts)
        except (smtplib.SMTPAuthenticationError, imaplib.IMAP4.error):
            unsucsesse = "\033[91mcan't login in e-mail.\033[0m"
        except socket.gaierror:
            unsucsesse = "\033[91mcan't sent e-mail, no connection.\033[0m"
        except ConnectionResetError:
            unsucsesse = "\033[91me-mail connection reset.\033[0m"
        return unsucsesse

    @classmethod
    def __find_command_to_destruct(cls, msg: 'email.message_from_bytes'):
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

    def _delete_resiver(self, prop: str):
        """Delete  resiver from send list"""
        print("choose resiver to delete:")
        mail = super().choise_from_list(self.email_prop[prop],
                                        none_option=True)
        super().clear_screen()
        if mail:
            self.email_prop[prop].remove(mail)
            print(mail + "\033[91m - deleted\033[0m")

    def _add_message(self):
        """Add message to career status."""
        message = input("Input message: ")
        self.email_prop["status message"] = message

    def _change_email(self, prop: str):
        """Change e-mail adress."""
        new_email = super().check_correct_email()
        if new_email and prop == 'email':
            self.email_prop['email'] = new_email
            print("\033[92memail changed.\033[0m")
        elif (new_email and
              prop == 'resivers list' or
              prop == "career status recivers"):
            self.email_prop[prop].append(new_email)
            print("\033[92memail add.\033[0m")

    def _change_password(self, prop: str):
        """Change e-mail password."""
        new_password = input("enter new password: ")
        self.email_prop[prop] = new_password
        super().clear_screen()
        print("\033[92mpassword changed.\033[0m")

    def _send_mail(
            self,
            recivers: List[str],
            *,
            subject: str,
            message: str = '',
            add_html: str = None,
            html_img: PurePath = None,
            add_file: PurePath = None,
    ):
        """Compose and send email with provided info and attachments."""
        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = COMMASPACE.join(self.email_prop[recivers])
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
        msg.attach(MIMEText(message))
        part = MIMEBase('application', "octet-stream")

        if add_file:
            self._add_file_to_email(msg, part, add_file)

        if add_html:
            self._add_html_to_email(msg, add_html, html_img)

        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login(self.login, self.password)
        smtp.sendmail(self.login, self.email_prop[recivers], msg.as_string())
        smtp.quit()

    @classmethod
    def _add_file_to_email(
            cls,
            msg: MIMEMultipart,
            part: MIMEBase,
            add_file: PurePath,
    ):
        """Add file to html."""
        with open(add_file, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            'attachment; filename="{}"'.format(add_file.name))
        msg.attach(part)

    @classmethod
    def _add_html_to_email(
            cls, msg: MIMEMultipart,
            add_html: str,
            html_img: PurePath,
    ):
        """Add HTML to email."""
        # We reference the image in the IMG SRC attribute by the
        # ID we give it below
        # <b>Some <i>HTML</i> text</b> and an image.<br>\
        # <img src="cid:image1"><br>Nifty!
        msg_html = MIMEText(add_html, 'html')
        msg.attach(msg_html)
        if html_img:
            with open(html_img, 'rb') as image:
                msg_image = MIMEImage(image.read())
            # Define the image's ID as referenced above
            msg_image.add_header('Content-ID', '<image1>')
            msg.attach(msg_image)

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

    def edit_main_propeties(self):
        """Edit email settings."""
        while True:
            print("Program main email props:\n\
    login   : {}\n\
    password: {}\n\
    Send to:".format(self.email_prop['email'], self.email_prop['password']))
            for mail in self.email_prop['resivers list']:
                print('\t', mail)

            action_dict = {
                'change login':
                lambda arg='email': self._change_email(arg),
                'change password':
                lambda arg='password': self._change_password(arg),
                'add resiver':
                lambda arg='resivers list': self._change_email(arg),
                'delete resiver':
                lambda arg='resivers list': self._delete_resiver(arg),
                'exit': 'break',
            }
            print("\nChoose action:")
            action = super().choise_from_list(action_dict)
            if action in ['exit', '']:
                break
            else:
                action_dict[action]()
            super().dump_data(self.email_prop_path, self.email_prop)

    def edit_career_status_recivers(self):
        """Edit resiver list for dayli career status."""
        if "career status recivers" not in self.email_prop:
            self.email_prop["career status recivers"] = []
        if "status message" not in self.email_prop:
            self.email_prop["status message"] = ''
        while True:
            super().clear_screen()
            print("Daily Status Recivers:\nSend to:")
            for mail in self.email_prop["career status recivers"]:
                print('\t', mail)
            print(f'Status message: "{self.email_prop["status message"]}"')
            action_dict = {
                'add resiver': self._change_email,
                'delete resiver': self._delete_resiver,
                'add message': lambda arg: self._add_message(),
                'exit': 'break',
            }
            print("\nChoose action:")
            action_name = super().choise_from_list(action_dict)
            if action_name in ['exit', '']:
                break
            else:
                action_dict[action_name]("career status recivers")
            super().dump_data(self.email_prop_path, self.email_prop)

    def try_email(self, recivers: List[str], **mail_parts):
        """
        Try to send mail.
        """
        unsucsesse = None
        if (not self.login or not self.password or not
                self.email_prop[recivers]):
            unsucsesse = """Для получения уведомлений на почту,
настройте настройки почты в меню администратора."""
        else:
            unsucsesse = self._try_connect(
                connect_reason=self._send_mail,
                recivers=recivers,
                **mail_parts,
            )
        return unsucsesse

    def try_destroy_world(self):
        """Destroy all data."""
        self._try_connect(connect_reason=self._read_mail)
