#!/usr/local/bin/python3

import requests
from bs4 import BeautifulSoup
import re

USER='cmurph29'
URL=f'https://letterboxd.com/{USER}/watchlist/'


rawText = requests.get(URL)

soup = BeautifulSoup(rawText.content, 'html.parser')

#find the total number in watchlist
countString = soup.findAll("h1", {"class": "section-heading"})[0].get_text()
count = re.search(r'([\d]+)', countString).group()


#find all titles
posters = list(soup.findAll("li", {"class": "poster-container"}))
print(posters[0])
