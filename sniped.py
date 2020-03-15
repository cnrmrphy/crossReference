#!/usr/local/bin/python3

import requests
from bs4 import BeautifulSoup
import re
import pandas
from pandas import DataFrame

USER='cmurph29'
URL=f'https://letterboxd.com/{USER}/watchlist'

rawText = requests.get(URL)

#print(rawText.text)

soup = BeautifulSoup(rawText.content, 'html.parser')

#find number of pages
pages = len(list(soup.findAll("li", {"class": "paginate-page"})))

#true soup calls template
for x in range(1, pages+1):
    print(URL+f'/page/{x}')


#find the total number in watchlist
countString = soup.findAll("h1", {"class": "section-heading"})[0].get_text()
count = re.search(r'([\d]+)', countString).group()


#grabbing all movies 
postersObj = soup.findAll("li", {"class": "poster-container"})
posters = list(postersObj)




