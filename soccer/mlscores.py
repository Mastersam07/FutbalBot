# Live MLS Score from Past 7 Days
import requests
from bs4 import BeautifulSoup
import re
import sys
import datetime
from time import time
import re

# import urllib2
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

width = 35

def MLScores():
        url = "http://www.livescores.com/soccer/usa/mls/results/"
        page  = urlopen(url)
        soup = BeautifulSoup(page, "lxml")
        o = []
        gms = soup.findAll('div', attrs={'class':'row-gray'})
        # iterate and clean the string. real basic.
        for gm in gms:
            g = gm.getText()
            if sys.version_info[0] < 3:
                g = g.encode('utf-8')
            g = ' '.join(g.split())
            g = g.replace('Game Preview', '')
            g = g.strip()
            o.append(g)
        # output
        if len(o) == 0:
            return("I didn't find any score at {0}".format(url))
        else:
            return('*' * (width + 4) + "{0}".format("\n".join(o)) + '*' * (width + 4))

mlscores = MLScores()
#print(cfl)
