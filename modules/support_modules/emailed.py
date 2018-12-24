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
from email.mime.image import MIMEImage
from email import encoders

from modules.support_modules.standart_functions import BasicFunctions
from modules.support_modules.absolyte_path_module import AbsPath


class EmailSender(BasicFunctions):
    """
    Class to working with e-mails.
    """
    email_prop_path = AbsPath.get_path('data', 'email_prop')

    def __init__(self):
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
    def _try_connect(cls, connect_reason, recivers=None, **mail_parts):
        """Try to connect to server to send or read emails."""
        unsucsesse = None
        try:
            if recivers:
                connect_reason(recivers, **mail_parts)
            else:
                connect_reason()
        except smtplib.SMTPAuthenticationError:
            unsucsesse = "\033[91mcan't login in e-mail.\033[0m"
        except socket.gaierror:
            unsucsesse = "\033[91mcan't sent e-mail, no connection.\033[0m"
        except ConnectionResetError:
            unsucsesse = "\033[91me-mail connection reset.\033[0m"
        return unsucsesse

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

    def _delete_resiver(self, prop):
        """Delete  resiver from send list"""
        print("choose resiver to delete:")
        mail = super().choise_from_list(self.email_prop[prop],
                                        none_option=True)
        super().clear_screen()
        if mail:
            self.email_prop[prop].remove(mail)
            print(mail + "\033[91m - deleted\033[0m")

    def _change_email(self, prop):
        """Change e-mail adress."""
        new_email = input("enter new email: ")
        match = re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",
                         new_email)
        super().clear_screen()
        if not match:
            print('\033[91mbad Syntax in\033[0m ' + new_email)
        elif prop == 'email':
            self.email_prop['email'] = new_email
            print("\033[92memail changed.\033[0m")
        elif (prop == 'resivers list' or
              prop == "career status recivers"):
            self.email_prop[prop].append(new_email)
            print("\033[92memail add.\033[0m")

    def _change_password(self, prop):
        """Change e-mail password."""
        new_password = input("enter new password: ")
        self.email_prop[prop] = new_password
        super().clear_screen()
        print("\033[92mpassword changed.\033[0m")

    def _send_mail(
            self,
            recivers,
            *,
            subject,
            message='',
            add_html=None,
            html_img=None,
            add_file=None,
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
    def _add_file_to_email(cls, msg, part, add_file):
        """Add file to html."""
        with open(add_file, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            'attachment; filename="{}"'.format(op.basename(add_file)))
        msg.attach(part)

    @classmethod
    def _add_html_to_email(cls, msg, add_html, html_img):
        """Add HTNL to email."""
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
                'change login': (self._change_email, 'email'),
                'change password': (self._change_password, 'password'),
                'add resiver': (self._change_email, 'resivers list'),
                'delete resiver': (self._delete_resiver, 'resivers list'),
                'exit': 'break',
            }
            print("\nChoose action:")
            action_name = super().choise_from_list(action_dict)
            if action_name in ['exit', '']:
                break
            else:
                action = action_dict[action_name][0]
                argument = action_dict[action_name][1]
                action(argument)
            super().dump_data(self.email_prop_path, self.email_prop)

    def edit_career_status_recivers(self):
        """Edit resiver list for dayli career status."""
        if "career status recivers" not in self.email_prop:
            self.email_prop["career status recivers"] = []
        while True:
            print("Daily Status Recivers:\nSend to:")
            for mail in self.email_prop["career status recivers"]:
                print('\t', mail)
            action_dict = {
                'add resiver':
                (self._change_email, "career status recivers"),
                'delete resiver':
                (self._delete_resiver, "career status recivers"),
                'exit': 'break',
            }
            print("\nChoose action:")
            action_name = super().choise_from_list(action_dict)
            if action_name in ['exit', '']:
                break
            else:
                action = action_dict[action_name][0]
                argument = action_dict[action_name][1]
                action(argument)
            super().dump_data(self.email_prop_path, self.email_prop)

    def try_email(self, recivers, **mail_parts):
        """
        Try to send mail.
        recivers - list of emails.
        subject - string.
        message - string, default - ''
        add_html - HTML doc, default - None
        html_img - HTML img, default - None
        add_file - file attachment, default - None
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
