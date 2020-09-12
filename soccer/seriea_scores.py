# Live Serie A Score from Past 7 Days
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

url = "http://www.livescores.com/soccer/italy/serie-a/results/7-days/"

page  = urlopen(url)
soup = BeautifulSoup(page, "lxml")

games = soup.findAll("div", {"class":"row-gray"})

width = 35

def SerieaScores():

  scores = []

  for game in games:
    scores.append(game.text)

  # output
  if len(scores) == 0:
    return("I didn't find any score at {0}".format(url))
  else:
    return('*' * (width + 4) + "{0}".format("\n".join(scores)) + '*' * (width + 4))

serieascores = SerieaScores()
# print (serieascores)
