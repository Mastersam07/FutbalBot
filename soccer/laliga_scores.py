# Live MLS Score from Past 7 Days
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

url = "http://www.livescores.com/soccer/spain/primera-division/results/7-days/"

width = 35

page  = urlopen(url)
soup = BeautifulSoup(page, "lxml")

games = soup.findAll("div", {"class":"row-gray"})

def LaligaScores():

  scores = []

  for game in games:
    g = game.text
    g = g.replace('RCD Espanyol', 'Espanyol')
    g = g.replace('Athletic Bilbao', 'Ath. Bilbao')
    g = g.replace('Deportivo Alaves', 'Deportivo')
    scores.append(g)

  # output
  if len(scores) == 0:
    return("I didn't find any score at {0}".format(url))
  else:
    return('*' * (width + 4) + "{0}".format("\n".join(scores)) + '*' * (width + 4))

laligacores = LaligaScores()
#print (l)
