# Live EPL Score from Past 7 Days
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

url = "http://www.livescores.com/soccer/england/premier-league/results/7-days/"

page  = urlopen(url)
soup = BeautifulSoup(page, "lxml")

games = soup.findAll("div", {"class":"row-gray"})

width = 28

def EPLScores():

  scores = []

  for game in games:
    g = game.text
    g = g.replace('AFC Bournemouth', 'Bournemouth')
    g = g.replace('Brighton & Hove Albion', 'Brighton')
    g = g.replace('Wolverhampton Wanderers', 'Wolverhampton')
    g = g.replace('Leicester City', 'Leicester')
    g = g.replace('Tottenham Hotspur', 'Tottenham')
    g = g.replace('United', 'Utd')
    g = g.replace('Manchester', 'Man.')
    scores.append(g)

  # output
  if len(scores) == 0:
    return("I didn't find any score at {0}".format(url))
  else:
    return('*' * (width + 4) + "{0}".format("\n".join(scores)) + '*' * (width + 4))

n = EPLScores()
#print (n)
