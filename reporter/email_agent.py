import smtplib
from email.mime.multipart import MIMEMultipart

EMAIL_HOST = 'smtp.gmail.com'


class EmailSender(object):
    def __init__(self, user:str, password:str):
        self._user = user
        self._password = password
        self._smtp_obj = smtplib.SMTP_SSL(EMAIL_HOST)

    def initialize(self):
        try:
            self._smtp_obj.login(self._user, self._password)
        except Exception as e:
            print(f'something went wrong. Exception {e}')

    def send_email(self, message: MIMEMultipart, subscribers):
        self._smtp_obj.sendmail(self._user, subscribers, message.as_string())
    
    def close(self):
        self._smtp_obj.close()
