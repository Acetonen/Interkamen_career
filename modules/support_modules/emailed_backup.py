#!/usr/bin/env python3
"""Email backup file"""

import smtplib
import os.path as op
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders


def send_mail(path, use_tls=True):
    """Compose and send email with provided info and attachments."""
    msg = MIMEMultipart()
    msg['From'] = 'acetonen2@gmail.com'
    msg['To'] = 'acetonen@gmail.com'
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = 'Backup for InterkamenCorp'
    msg.attach(MIMEText('Backup for InterkamenCorp'))

    part = MIMEBase('application', "octet-stream")
    with open(path, 'rb') as file:
        part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',
                    'attachment; filename="{}"'.format(op.basename(path)))
    msg.attach(part)

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    if use_tls:
        smtp.starttls()
    smtp.login('acetonen2@gmail.com', 'Kovalev2')
    smtp.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp.quit()
