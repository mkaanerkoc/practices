import asyncio
from itertools import islice
import pandas as pd 

def chunked_iterable(iterable, chunk_size):
    """
    slices the given iterable into chunks with chunk_size size.
    
    """
    it = iter(iterable)
    while True:
        chunk = list(islice(it, chunk_size))
        if not chunk:
            break
        yield chunk

def preprocess_price_data(price_data_raw, base_asset):
    """
    converts price data into pandas.DataFrame and process columns.
    """
    price_data = pd.DataFrame(price_data_raw,
                                dtype='float',
                                columns=['open_time', 'open', 'high', 'low', 'close', 
                                        'volume', 'close_time', 'quote_volume', 
                                        'trade_count', 'taker_buy_vol', 
                                        'taker_buy_quote_vol', 'unused'])
    price_data['time'] = pd.to_datetime(price_data['open_time'], unit='ms')


    price_data = price_data.drop(columns=['open_time', 'close_time', 'taker_buy_vol', 
                                'taker_buy_quote_vol', 'unused'])

    price_data.rename(columns={'quote_volume':'volume'}, inplace=True)
    price_data[['symbol']] = base_asset
    price_data.set_index('time', inplace=True)

    return price_data

def remove_missing_symbols(market_prices):
    """
    Remove symbols with missing data between start and end date.
    """
    start, end = market_prices.index[0], market_prices.index[-1]
    ref_time = pd.date_range(start, end, freq="1H")
    market_prices = market_prices.groupby("symbol").filter(
        lambda x: len(x) == len(ref_time)
    )
    return market_prices


class AsyncPriceFetcher(object):
    MAX_WORKERS = 40
    def __init__(self, async_client):
        self._client = async_client


    async def _fetch_symbol(self, symbol, period, start, end=None):
        """
        bottom-level function that sends HTTP request to Binance and awaits on response
        """
        price_data_raw = await self._client.get_historical_klines(symbol['symbol'], 
                                                            period, start, end)
        return preprocess_price_data(price_data_raw, symbol['baseAsset'])

    async def _fetch_chunk(self, symbol_chunk, period, start, end=None):
        """
        creates a Future object for every symbol in the symbol_chunk.
        it awaits until all the Future objects returns.
        
        """
        tasks = []
        for symbol in symbol_chunk:
            task = asyncio.ensure_future(self._fetch_symbol(symbol, period, start, end))
            tasks.append(task)
        return await asyncio.gather(*tasks, return_exceptions=False)

    async def fetch(self, symbols, interval, start):
        symbol_prices = []
        # Request price data chunk by chunk
        for index, symbols_in_chunk in enumerate(chunked_iterable(symbols, self.MAX_WORKERS)):
            chunk_results = await self._fetch_chunk(
                symbols_in_chunk, interval, start
            )
            symbol_prices.extend(chunk_results)

        market_prices_online = pd.concat(symbol_prices)
        market_prices_online = remove_missing_symbols(market_prices_online)
        market_prices_online.to_csv("data/market_prices.csv")
        return market_prices_online

