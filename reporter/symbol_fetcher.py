import asyncio
from itertools import islice
import pandas as pd

def remove_missing_symbols(market_prices, min_len):
    """
    Remove symbols if they have less then 'min_len' data points
    """
    
    market_prices = market_prices.groupby("symbol").filter(
        lambda x: len(x) >= min_len
    )
    return market_prices


class AsyncSymbolFetcher(object):
    def __init__(self, async_client):
        self._client = async_client

    async def _fetch(self, quote_asset, excluded_symbols = ['BUSD', 'USDC', 'EUR', 'DAI', 'AUD']):
        exchange_info = await self._client.get_exchange_info()
        symbols = exchange_info["symbols"]

        active_symbols = list(
            filter(lambda x: x["status"] == "TRADING" and 
                            x["quoteAsset"] == quote_asset and
                            x["baseAsset"] not in excluded_symbols, 
                symbols)
        )
        return active_symbols
    
    def fetch(self, quote_asset):
        loop = asyncio.get_event_loop()

        async def _pipeline():
            await self._client.create()
            symbols = await self._fetch(quote_asset)
            await self._client.close_connection()
            return symbols

        results = loop.run_until_complete(_pipeline())
        return results
