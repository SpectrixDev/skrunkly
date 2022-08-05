import requests, json, random, sys, time, matplotlib
import matplotlib.pyplot as plt
import numpy as np
from requests import Session

from modules.weather import Weather
from modules.markets import Markets

# Read the json config
with open('config.json') as h:
  config = json.load(h)

discord = config['discord'] # discord config
weather = config['weather'] # weather config
markets = config['markets'] # markets config, basically coinmarketcap

if __name__ == "__main__":
  matplotlib.use('Agg') # This is to make matplotlib work on a server, making it not load up GTK (for use with raspberry pi running ubuntu)
  if len(sys.argv) > 1:
    if sys.argv[1] == "--weather":
      Weather().get_weather(weather['key'], weather['city'], weather['days'], weather['alerts'], discord, config["imgurClientID"])
    elif sys.argv[1] == "--markets":
      Markets().get_market(markets['key'], markets['currencies'], markets['cryptocurrencies'], discord)
    elif sys.argv[1] == "--help":
      print("Usage: python main.py [--weather, --help]")
    else:
      print("Invalid argument. Use --help for help.")
  else:
    print("No arguments. Use --help for help.")