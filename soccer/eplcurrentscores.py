from bs4 import BeautifulSoup
import requests, os

__author__ = "@gwuah"

def scrape_from_livescore() :
  print('Fetching markup from livescores.com ..')

  # try catching all possible http errors
  try :
    livescore_html = requests.get('https://www.livescores.com/soccer/england/premier-league/')
  except Exception as e :
    return print('An error occured as: ', e)

  print("Feeding markup to beautiful soup .. \n")
  parsed_markup = BeautifulSoup(livescore_html.text, 'html.parser')

  # dictionary to contain score
  scores = []

  # scrape needed data from the parsed markup
  for element in parsed_markup.find_all("div", "row-gray") :

    match_name_element = element.find(attrs={"class": "scorelink"})

    if match_name_element is not None :

      # this means the match is about to be played

      home_team = '-'.join(element.find("div", "tright").get_text().strip().split(" "))
      away_team = '-'.join(element.find(attrs={"class": "ply name"}).get_text().strip().split(" "))

      match_name = match_name_element.get('href').split('/')[4]
      home_team_score = element.find("div", "sco").get_text().split("-")[0].strip()
      away_team_score = element.find("div", "sco").get_text().split("-")[1].strip()

      scores.append("{} %s vs {} %s".format(home_team, away_team) % (home_team_score, away_team_score))

  return '\n'.join(scores)

eplLatest = scrape_from_livescore()