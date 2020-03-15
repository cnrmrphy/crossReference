#!/usr/local/bin/python3

import xml
import requests
import sys
import os
from bs4 import BeautifulSoup
from bs4 import CData
import re
import pandas
from pandas import DataFrame
import json
import pprint


# find number of pages
def num_pages(soup):
    return(len(list(soup.findAll("li", {"class": "paginate-page"}))))


# find the total number in watchlist
def num_movies(soup, url):
    countString = soup.findAll("h1", {"class": "section-heading"})[0].get_text()
    return(re.search(r'([\d]+)', countString).group())

        
# return dicts for each individual page
def get_film_info(url):
    
    pageText = requests.get(url)

    pageSoup = BeautifulSoup(pageText.content, 'html.parser')
    
    movies = {}

    for poster in pageSoup.findAll("li", {"class": "poster-container"}):
        title = poster.find('img', alt=True)['alt']
        filmLink = f'https://letterboxd.com' + poster.find('div', {'class': 'poster film-poster really-lazy-load'})['data-target-link']
        infoText = requests.get(filmLink)
        infoSoup = BeautifulSoup(infoText.content, 'lxml')
        data = infoSoup.find('script', {'type': 'application/ld+json'}).text.splitlines()[2]
        jsonData = json.loads(data) 
        year = jsonData['releasedEvent'][0]['startDate'] 
        directors = [person['name'] for person in jsonData['director']] 
        rating = jsonData['aggregateRating']['ratingValue']
        img = jsonData['image']
        movies[title] = {'year': year, 'directors': directors, 'rating': rating, 'link': filmLink, 'image-src': img}

    return(movies)

# unify paginations into a single dict
def unify_pages(url, pages):
    movies = {}

    for x in range(1, pages+1):
        movies.update(get_film_info(url+f'/page/{x}'))

    return(movies)



def main():
    # create watchlist url 
    user = sys.argv[1]
    URL=f'https://letterboxd.com/{user}/watchlist'

    # main soup for basic info
    rawText = requests.get(URL)
    soup = BeautifulSoup(rawText.content, 'html.parser')
    pages = num_pages(soup)
    
    print(unify_pages(URL, pages))
# main execution
if __name__ == '__main__':
    main()

    






