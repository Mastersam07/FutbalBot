# Current MLS Table
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

w,h=9,21
teamInfo = [[0 for x in range(w)] for y in range(h)]

url = "http://www.livescores.com/soccer/spain/primera-division/"

page  = urlopen(url)
soup = BeautifulSoup(page, "lxml")

team = soup.findAll("div", {"class":"team"})
pts = soup.findAll("div", {"class":"pts"})

def LaligaTable():

  table = []

  if not team or not pts:
	  table.append("%-*s %s" % (5, "Empty table", "Empty table"))
  else:
    z = 0
    for x in range(0,21):
      teamInfo[x][0] = team[x].text
      for y in range(1, 9):
        teamInfo[x][y] = pts[z].text
        z+=1

    #Format the print
    for x in range (0, 21):
      if x == 0:
        table.append("%-*s %s" % (5, teamInfo[x][8], teamInfo[x][0]))
      if x != 0 and x < 21:
        table.append("%-*s %s" % (5, teamInfo[x][8], teamInfo[x][0]))

  return '\n'.join(table)

laligatable = LaligaTable()
#print (m)