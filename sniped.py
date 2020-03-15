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


#find the total number in watchlist
countString = soup.findAll("h1", {"class": "section-heading"})[0].get_text()
count = re.search(r'([\d]+)', countString).group()

        
# function to return dicts for each individual page
def get_film_info(url):
    
    pageText = requests.get(url)

    pageSoup = BeautifulSoup(pageText.content, 'html.parser')
    
    movies = {}

    for poster in pageSoup.findAll("li", {"class": "poster-container"}):
        title = poster.find('img', alt=True)['alt']
        filmLink = f'https://letterboxd.com' + poster.find('div', {'class': 'poster film-poster really-lazy-load'})['data-target-link']
        img = poster.find('img')['src']

        movies[title] = {'link': filmLink, 'image-src': img}

    return(movies)

#function to unify paginations into a single dict
def unify_pages(url, pages):
    movies = {}

    for x in range(1, pages+1):
        movies.update(get_film_info(url+f'/page/{x}'))

    return(movies)

print(unify_pages(URL, pages))

#for x in range(1, pages+1):
#    print(get_film_info(URL+f'/page/{x}'))






