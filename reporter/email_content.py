from datetime import datetime
import pandas as pd

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List

"""
A python module that prepares email content
"""

def prepare_mime_message(report:pd.DataFrame, gmail_user:str, subscribers:List[str]) -> MIMEMultipart:
    """
    creates a MIMEMultipart object that contains email content
    |---+ inputs
        |--- gmail_user[str]: Gmail account which sends the email
        |--- subscribers[list[str]]: Email accounts who will receive the email
    
    """
    message = MIMEMultipart("alternative")
    message["Subject"] = "ATILGAN Labs - Market Report"
    message["From"] = gmail_user
    message["To"] = ", ".join(subscribers)

    plain_text_part = MIMEText(prepare_text(), "plain")
    html_part = MIMEText(prepare_html(report), "html")

    message.attach(plain_text_part)
    message.attach(html_part)
    return message

def prepare_text():
    return """\
    ATILGAN Labs cryptocurrency market updates for {datetime.today()}
    """

def prepare_html(table):
    return f"""\
    <html>
    <style>
        .tablestyle {{
            border: 1px solid black;
            border-collapse: collapse;
            width: 100%;
            }}

            .tablestyle th, .tablestyle td {{
            border: 1px solid black;
            padding: 5px;
            text-align: center;
            }}
    </style>
    <body>
        <h2>Daily Market Overview {datetime.today()}</h2>
        {table.to_html(classes='tablestyle')}
    </body>
    </html>
    """