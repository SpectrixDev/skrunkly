import requests, random, json
import matplotlib.pyplot as plt
import numpy as np

# Read the json config
with open('config.json') as h:
  config = json.load(h)

dc = config['discord'] # discord config


class Weather():
    def __init__(self):
        pass

    def get_weather(self, key, city, days, alerts):
        # Get the weather data in json format
        weatherUrl = f'http://api.weatherapi.com/v1/forecast.json?key={key}&q={city}&days={days}&aqi=no&alerts={alerts}'
        weather_response = requests.get(weatherUrl)
        weather = weather_response.json()

        # Make the rain chance more readible.
        if weather['forecast']['forecastday'][0]['day']['daily_chance_of_rain'] == 0:
            rainChance = 'None predicted'
        else:
            rainChance = f"{weather['forecast']['forecastday'][0]['day']['daily_chance_of_rain']}%"

        if weather['forecast']['forecastday'][1]['day']['daily_chance_of_rain'] == 0:
            tomorrowRainChance = 'no'
        else:
            tomorrowRainChance = f"a {weather['forecast']['forecastday'][1]['day']['daily_chance_of_rain']}%"

        # Plot the day's 24 hour weather data, in 1 hour intervals.
        plt.figure(figsize=(12,8))
        for i in range(23):
            plt.plot([i, i+1], [weather['forecast']['forecastday'][0]['hour'][i]['temp_c'], weather['forecast']['forecastday'][0]['hour'][i+1]['temp_c']], '-', color='red')
            plt.ylabel('Temperature (°C)')
            plt.xlabel('Time (hours)')
            plt.xticks(np.arange(0, 24, 1))
            plt.title(f'{weather["location"]["name"]} weather for {weather["forecast"]["forecastday"][0]["date"]}')
        plt.savefig('DailyWeatherGraph.png')

        # Upload image to imgur
        try:
            imgur_response = requests.post('https://api.imgur.com/3/image', headers={'Authorization': f'Client-ID {config["imgurClientID"]}'}, files={'image': open('DailyWeatherGraph.png', 'rb')})
            imgur_json = imgur_response.json()
            imgur_url = imgur_json['data']['link']
        except Exception as e:
            print("Error upload imgur image:\n", e)
            print(imgur_json)
            imgur_url = ""
        
        # Prepare the message

        weatherDescription = (f"ℹ **Conditions:** {weather['forecast']['forecastday'][0]['day']['condition']['text']}\n\n"+
                            f"🌞 **High:** {weather['forecast']['forecastday'][0]['day']['maxtemp_c']} °C\n\n"+
                            f"🌚 **Low:** {weather['forecast']['forecastday'][0]['day']['mintemp_c']} °C\n\n"+
                            f"🌡 **Current:** {weather['current']['temp_c']} °C\n\n"+
                            f"🍃 **Max Wind:** {weather['forecast']['forecastday'][0]['day']['maxwind_kph']} km/h\n\n"+
                            f"♨️ **Humidity:** {weather['forecast']['forecastday'][0]['day']['avghumidity']}%\n\n"+
                            f"☔ **Chance of rain:** {rainChance}\n\n"+
                            f"🌅 **Sunrise:** {weather['forecast']['forecastday'][0]['astro']['sunrise']}\n\n"+
                            f"🌇 **Sunset:** {weather['forecast']['forecastday'][0]['astro']['sunset']}\n\n"+
                            f"⛱ **UV index:** {weather['forecast']['forecastday'][0]['day']['uv']}\n\n")

        # See if we need to include snow conditions              
        if weather['forecast']['forecastday'][0]['day']['daily_chance_of_snow'] > 0:
            weatherDescription+=f"• **❄ Chance of snow** {weather['forecast']['forecastday'][0]['day']['daily_chance_of_snow']}%\n"
        # See if we need to include alerts
        if weather['alerts']['alert']:
            try:
                weatherDescription+=f"• 🚨**Alerts:** {weather['alerts']['alert'][0]}\n"
            except:
                weatherDescription+=f"• 🚨**Alerts:** Apparently there's alerts in your area, check a weather app.\n"

        weatherDescription+=(f"\n📅 **Tomorrow**: {weather['forecast']['forecastday'][1]['day']['condition']['text']} " +
                            f"with a high of {weather['forecast']['forecastday'][1]['day']['maxtemp_c']} °C with {tomorrowRainChance} chance of rain\n\n")
        data={
            "username": "The Skrunkly",
            "avatar_url": "https://cdn.discordapp.com/attachments/478201257417244675/974380313046286356/TheSkrunkly.png",
            "content": ("Good morning, <@"+dc["ownerID"]+">!"),
            "embeds": [
            {
                "author": {
                "name": "Daily Rundown",
                "url": "https://calendar.google.com/calendar/u/0/r",
                "icon_url": 'http://'+((weather["forecast"]["forecastday"][0]["day"]["condition"]["icon"])[2:])
                },

                "title": "Today's weather",
                "url": "https://accuweather.com/",
                "description": weatherDescription,

                "color": ''.join(str(random.randint(0,9)) for i in range(7)),
                "thumbnail": {
                "url": imgur_url,
                }
            }
            ]
        }

        webhook = dc["webhookUrl"]
        requests.post(webhook, json=data)

