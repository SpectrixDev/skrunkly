import requests, random, json
from requests import Session

# Read the json config
with open('config.json') as h:
  config = json.load(h)

discord = config['discord'] # discord config

class Markets:
    def __init__(self):
        pass
    
    def get_market(self, key, currencies, cryptocurrencies):
        # Get the crypto prices for BTC, ETH and SOL in both dollar, pound and zar.
        url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion'
        priceList = []
        cryptoMessage = ''
        # Get cryptocurrency prices for each of the currencies in the array above.
        # Note: The API has a daily limit of 333 requests a day 10k a month
        for currency in currencies:
            cryptoMessage+=f"\n**{currency}:**\n"
            for cryptocurrency in cryptocurrencies:
                payload = {
                    'amount': 1,
                    'convert': currency,
                    'symbol': cryptocurrency
                    }
                headers = {
                    'Accepts': 'application/json',  
                    'X-CMC_PRO_API_KEY': key
                    }
                response = requests.get(url, params=payload, headers=headers)
                data = response.json()
                cryptoMessage+=f"{(data['data']['symbol'])}:  {str(round(float(data['data']['quote'][currency]['price']), 2))} {currency}\n"
                priceList.append(float(data['data']['quote'][currency]['price']))
        # Figure out the current exchange rate roughly using the crypto priecs for the lulz, cuz why not do funny math just cuz life is too short not to
        # Mega spaghetti code, except it makes sense and I don't wanna make it more readable hahahaha
        poundtozar = round((priceList[6]/priceList[0]+priceList[7]/priceList[1]+priceList[8]/priceList[2])/3, 2)
        usdtozar = round((priceList[6]/priceList[3]+priceList[7]/priceList[4]+priceList[8]/priceList[5])/3, 2)
        poundtousd = round((priceList[0]/priceList[3]+priceList[1]/priceList[4]+priceList[2]/priceList[5])/3, 2)

        discordEmbed={
            "username": "The Skrunkly",
            "avatar_url": "https://cdn.discordapp.com/attachments/478201257417244675/974380313046286356/TheSkrunkly.png",
            "embeds": [
            {
                "author": {
                "name": "Daily Rundown",
                "url": "https://calendar.google.com/calendar/u/0/r",
                "icon_url": "https://is5-ssl.mzstatic.com/image/thumb/Purple115/v4/6f/c6/78/6fc67811-c13b-a812-048d-3b1155a58449/source/256x256bb.jpg"
                },

                "title": "📊 Market Rundown",
                "url": "https://coingecko.com",

                "fields": [
                {
                    "name": "💳 __**Live Crypto Prices:**__",
                    "value": cryptoMessage,
                    "inline": False
                },
                {
                    "name": "💵 __**Live Fiat Prices:**__",
                    "value": f"£1 = R{usdtozar}\n£1 = ${poundtousd}\n$1 = R{poundtozar}\n",
                    "inline": False
                }
                ],

                "color": ''.join(str(random.randint(0,9)) for i in range(7)),
            }
            ]
        }
        webhook = discord["webhookUrl"]
        requests.post(webhook, json=discordEmbed)