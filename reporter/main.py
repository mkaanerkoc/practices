import os
from dotenv import load_dotenv
import pandas as pd

from email_agent import EmailSender
from email_content import prepare_mime_message

load_dotenv()

gmail_user = os.getenv('GMAIL_USER')
gmail_password = os.getenv('GMAIL_PASSWORD')

subscribers = ['mkaanerkoc@gmail.com', 'duyguiremdemiryurek@gmail.com']

def process_pricess():
    return pd.DataFrame({'name': ['BTC', 'LTC', 'ETH', 'XMR'],
                        'Crossover': [1, 1, -1, 1],
                        'Duration': [84, 56, 73, 69],
                        'Volume': [78, 88, 82, 87]})

def send_email(report):
    email_agent = EmailSender(gmail_user, gmail_password)
    message = prepare_mime_message(report, gmail_user, subscribers)
    email_agent.initialize()
    email_agent.send_email(message, subscribers)
    email_agent.close()

def main():
    #fetch_symbols()
    #fetch_prices()
    report = process_pricess()
    send_email(report)

if __name__ == '__main__':
    main()
