import requests, json, random, sys, time
import matplotlib.pyplot as plt
import numpy as np
from requests import Session

from skrunkly.weather import Weather
from skrunkly.markets import Markets

# Read the json config
with open('config.json') as h:
  config = json.load(h)

discord = config['discord'] # discord config
weather = config['weather'] # weather config
markets = config['markets'] # markets config, basically coinmarketcap

if __name__ == "__main__":
  if len(sys.argv) > 1:
    if sys.argv[1] == "--weather":
      Weather().get_weather(weather['key'], weather['city'], weather['days'], weather['alerts'])
    elif sys.argv[1] == "--crypto":
      Markets().get_market(markets['key'], markets['currencies'], markets['cryptocurrencies'])
    elif sys.argv[1] == "--help":
      print("Usage: python main.py [--weather, --help]")
    else:
      print("Invalid argument. Use --help for help.")
  else:
    print("No arguments. Use --help for help.")