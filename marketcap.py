import pprint
from coinmarketcap import Market


def get_btc_change():
    coinmarketcap = Market()
    try:
        market_data = coinmarketcap.ticker(start=0, limit=3, convert='EUR')
        # pprint.pprint(market_data)
        daily_percentage_change = market_data['data']['1']['quotes']['USD']['percent_change_24h']
        return daily_percentage_change
    except:
        print('Problem with func get_btc_change()')
        raise
