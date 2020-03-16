#!/usr/local/bin/python3

import xml
import requests
import sys
from bs4 import BeautifulSoup
import json
import inquirer
import config


# find number of pages
def num_pages(soup):
    return(len(list(soup.findAll("li", {"class": "paginate-page"}))))


# find the total number in watchlist
def num_movies(soup, url):
    countString = soup.findAll("h1", {"class": "section-heading"})[0].get_text()
    return(re.search(r'([\d]+)', countString).group())

       
# basic calls that don't make hella requests, just gets film title
def get_film_title(url):
    pageText = requests.get(url)

    pageSoup = BeautifulSoup(pageText.content, 'html.parser')

    #makes a list of the alt text for every poster img, only way to get the titles from this url
    return([poster.find('img', alt=True)['alt'] for poster in pageSoup.findAll('li', {'class': 'poster-container'})])
# return dicts for each film on a given page 
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
# unify paginations into a single list
def unify_pages_list(url, pages):
    # wild ass list comp here lmao
    
    return([a for x in range(1, pages+1) for a in get_film_title(url+f'/page/{x}')]) 
# unify paginations into a single dict
def unify_pages_dict(url, pages):
    movies = {}

    for x in range(1, pages+1):
        movies.update(get_film_info(url+f'/page/{x}'))

    return(movies)

# yield tuples of overlap
def tuple_API(titles, COUNTRY, SERVICES, apiURL, HEADERS):
    for title in titles:
        querystring = {'term': title, 'country': COUNTRY}
        response = json.loads(requests.request('GET', apiURL, headers=HEADERS, params=querystring).text)
        for name in response['results']:
            movie = name['name']
            if name['name'] == title:
                for result in name['locations']:
                    if result['display_name'] in SERVICES:
                        yield result['display_name'], movie
# yield dictionary per streaming service
def make_dict(titles, COUNTRY, SERVICES, apiURL, HEADERS):
    big_dict = {service: [] for service in SERVICES}

    for twosome in tuple_API(titles, COUNTRY, SERVICES, apiURL, HEADERS):
        if twosome[1] not in big_dict[twosome[0]]:
            big_dict[twosome[0]].append(twosome[1])
    
    return(big_dict)

# format output
def printout(big_dict):
    for service, movies in big_dict.items():
        print('Movies on '+service + ': ' + ', '.join(movies) + '\n') 
        
# call api to find the 
def main():
    # create watchlist url 

    # configure username
    configData = json.loads(open('config.json').read())
    
    if configData["USER"]:
        user = configData["USER"]
    else:
        config.add_user()
        configData = json.loads(open('config.json').read())
        user = configData["USER"]

    URL=f'https://letterboxd.com/{user}/watchlist'


    # configure country code
    if configData["COUNTRY"]:
        country = configData["COUNTRY"]
    else:
        config.add_country()
        configData = json.loads(open('config.json').read())
        country = configData["COUNTRY"]

    # configure services
    if configData["SERVICES"]:
        services = configData["SERVICES"] 
    else:
        config.add_services()
        configData = json.loads(open('config.json').read())
        services = configData["SERVICES"]

    # main soup for basic info

    #rawText = requests.get(URL)
    #soup = BeautifulSoup(rawText.content, 'html.parser')
    #pages = num_pages(soup)
    
    #titles = unify_pages_list(URL, pages)
    


# main execution
if __name__ == '__main__':
    main()

    

