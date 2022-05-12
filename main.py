import requests, json, random, sys

# Read the json config
with open('config.json') as h:
  config = json.load(h)

dc = config['discord'] # discord config

def weather(key, city, days, aqi, alerts):
  # Get the weather data in json format
  weatherUrl = f'http://api.weatherapi.com/v1/forecast.json?key={key}&q={city}&days={days}&aqi={aqi}&alerts={alerts}'
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


  # Prepare the message

  weatherDescription = (f"ℹ **Conditions:** {weather['forecast']['forecastday'][0]['day']['condition']['text']}\n\n"+
                        f"🌞 **High:** {weather['forecast']['forecastday'][0]['day']['maxtemp_c']} °C\n\n"+
                        f"🌚 **Low:** {weather['forecast']['forecastday'][0]['day']['mintemp_c']} °C\n\n"+
                        f"🍃 **Max Wind** {weather['forecast']['forecastday'][0]['day']['maxwind_kph']} km/h\n\n"+
                        f"♨️ **Humidity** {weather['forecast']['forecastday'][0]['day']['avghumidity']}%\n\n"+
                        f"☔ **Chance of rain** {rainChance}\n\n"+
                        f"🌅 **Sunrise** {weather['forecast']['forecastday'][0]['astro']['sunrise']}\n\n"+
                        f"🌇 **Sunset** {weather['forecast']['forecastday'][0]['astro']['sunset']}\n\n"+
                        f"⛱ **UV index** {weather['forecast']['forecastday'][0]['day']['uv']}\n\n")
                     
  if weather['forecast']['forecastday'][0]['day']['daily_chance_of_snow'] > 0:
    weatherDescription+=f"• **❄ Chance of snow** {weather['forecast']['forecastday'][0]['day']['daily_chance_of_snow']}%\n"

  weatherDescription+=(f"\n📅 **Tomorrow**: {weather['forecast']['forecastday'][1]['day']['condition']['text']} " +
                        f"with a high of {weather['forecast']['forecastday'][1]['day']['maxtemp_c']} °C with {tomorrowRainChance} chance of rain\n\n")

  data={
    "username": "The Skrunkly",
    "avatar_url": "https://i.imgur.com/4M34hi2.png",
    "content": ("Good morning, <@"+dc["ownerID"]+">!"),
    "embeds": [
      {
        "author": {
          "name": "Daily Rundown",
          "icon_url": "https://cdn.pixabay.com/photo/2019/01/01/14/55/calendar-3906791_640.jpg",
          "url": "https://calendar.google.com/calendar/u/0/r",
        },

        "title": "Today's weather",
        "url": "https://accuweather.com/",
        "description": weatherDescription,

        "color": ''.join(str(random.randint(0,9)) for i in range(7)),
        "thumbnail": {
          "url": "http://"+((weather["forecast"]["forecastday"][0]["day"]["condition"]["icon"])[2:])
        }
      }
    ]
  }

  webhook = dc["webhookUrl"]
  response = requests.post(webhook, json=data)

if __name__ == "__main__":
  if len(sys.argv) > 1:
    if sys.argv[1] == "--weather":
      weather(config['weather']['key'], config['weather']['city'], config['weather']['days'], config['weather']['aqi'], config['weather']['alerts'])
    elif sys.argv[1] == "--help":
      print("Usage: python main.py [--weather, --help]")
    else:
      print("Invalid argument. Use --help for help.")
  else:
    print("No arguments. Use --help for help.")