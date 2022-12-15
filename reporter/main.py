import os
from dotenv import load_dotenv
import pandas as pd

from email_agent import EmailSender
from email_content import prepare_mime_message
from price_fetcher import AsyncPriceFetcher
from symbol_fetcher import AsyncSymbolFetcher

from binance.client import AsyncClient

load_dotenv()

gmail_user = os.getenv('GMAIL_USER')
gmail_password = os.getenv('GMAIL_PASSWORD')

binance_api_key = os.getenv('BINANCE_API_KEY')
binance_api_secret = os.getenv('BINANCE_API_SECRET')

subscribers = ['mkaanerkoc@gmail.com', 'duyguiremdemiryurek@gmail.com']

def fetch_symbols():
    client = AsyncClient(binance_api_key, binance_api_secret)
    symbol_fetcher = AsyncSymbolFetcher(client)
    symbols = symbol_fetcher.fetch('USDT')
    return symbols

def fetch_prices(symbols):
    client = AsyncClient(binance_api_key, binance_api_secret)
    price_fetcher = AsyncPriceFetcher(client)
    prices = price_fetcher.fetch(symbols, AsyncClient.KLINE_INTERVAL_1HOUR, '16 days ago UTC')
    print(prices)

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
    symbols = fetch_symbols()
    fetch_prices(symbols[0:2])
    report = process_pricess()
    # send_email(report)

if __name__ == '__main__':
    main()
