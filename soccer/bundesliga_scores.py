# Live Bundesliga Score from Past 7 Days
import sys
import requests
from bs4 import BeautifulSoup

# import urllib2
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

url = "http://www.livescores.com/soccer/germany/bundesliga/results/7-days/"

page  = urlopen(url)
soup = BeautifulSoup(page, "lxml")

games = soup.findAll("div", {"class":"row-gray"})

width = 35

def BundesligaScores():

  scores = []

  for game in games:
    g = game.text
    g = g.replace('FC Bayern München', 'Bayern')
    g = g.replace('Borussia Moenchengladbach', 'Moenchengladbach')
    g = g.replace('RasenBallsport Leipzig', 'Leipzig')
    g = g.replace('SC Paderborn 07', 'Paderborn')
    g = g.replace('Fortuna Düsseldorf', 'Düsseldorf')
    g = g.replace('Bayer Leverkusen', 'Leverkusen')
    g = g.replace('Borussia Dortmund', 'Dortmund')
    g = g.replace('Werder Bremen', 'Bremen')
    g = g.replace('Eintracht Frankfurt', 'Frankfurt')
    scores.append(g)

  # output
  if len(scores) == 0:
    return("I didn't find any score at {0}".format(url))
  else:
    return('*' * (width + 4) + "{0}".format("\n".join(scores)) + '*' * (width + 4))

bundesligascores = BundesligaScores()
# print (bundesligascores)
