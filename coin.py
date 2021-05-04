from pycoingecko import CoinGeckoAPI
import json


cg = CoinGeckoAPI()
print("Coin Test")
cg.ping()
#print(cg.get_price(ids='bitcoin', vs_currencies='eur'))
#print(cg.get_coins_list())
#print(cg.get_coins_markets('eur'))

class Coins_market :
    "id"
    "symbol"
    "name"
    "image"
    "current_price"
    "market_cap"
    "market_cap_rank"
    "fully_diluted_valuation"
    "total_volume"
    "high_24h"
    "low_24h"
    "price_change_24h"
    "price_change_percentage_24h"
    "market_cap_change_24h"
    "market_cap_change_percentage_24h"
    "circulating_supply"
    "total_supply"
    "max_supply"
    "ath"
    "ath_change_percentage"
    "ath_date"
    "atl"
    "atl_change_percentage"
    "atl_date"
    "roi"
    "last_updated"

class Coin :
    def __init__(self,
              id,
              name,
              price,
              pourcent,
        ):
        self.id = ' '
        self.name = ' '
        self.price = ' '
        self.pourcent = ' '


def Markets (currencies='eur',ids=' '):
    print (ids)
    market= Coins_market()
    market = cg.get_coins_markets(currencies,ids)
    return (market)


#Coin_List =cg.get_coins_list()
#Coin = cg.get_coin_by_id('bitcoin')
#Coin_market = Markets()
#print(Coin)
#print(cg.get_price(ids=['bitcoin', 'litecoin', 'ethereum'], vs_currencies=['usd', 'eur']))
#print(cg.get_price(ids=['bitcoin', 'litecoin', 'ethereum'], vs_currencies=['usd', 'eur'], include_symbol='true', include_24hr_vol='true'))
def List_Coin (coin1):
    id = ''
    l =0
    coin_list = cg.get_coins_list()
    d = {}
    for coin in coin_list:
        d[coin['symbol']] = coin['id']
    for i in coin1:
        id = id + d[coin1[l]] + ','
        l = l+1
#    print (id)
    return id



#  Structure la liste des coins
Coin1 = ['link','btc','eth']
id = List_Coin(Coin1)
print(cg.get_price(ids=id, vs_currencies=['usd', 'eur']))
Market = cg.get_coins_markets('eur',ids=id)

print (Market)





    