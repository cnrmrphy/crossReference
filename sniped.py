#!/usr/local/bin/python3

import xml
import requests
import sys
from bs4 import BeautifulSoup
import json
import inquirer
import config
from justwatch import JustWatch


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


# configure username
def config_user():
    configData = json.loads(open('config.json').read())

    if configData["USER"]:
        return(configData["USER"])
    else:
        config.add_user()
        configData = json.loads(open('config.json').read())
        return(configData["USER"])


#conigure country code
def config_country():
    configData = json.loads(open('config.json').read())
    config.add_country()
    configData = json.loads(open('config.json').read())
    return(configData["COUNTRY"])

# configure services
def config_services():
    configData = json.loads(open('config.json').read())

    if configData["SERVICES"]:
        return(configData["SERVICES"])
    else:
        config.add_services()
        configData = json.loads(open('config.json').read())
        return(configData["SERVICES"])

# returns a dict object with relevant information from api for a single movie
def search_film(movie, just_watch):
    return(just_watch.search_for_item(query=movie))

# add a movie to the reference dict:
def add_to_reference(movie, provider, reference_dict):
    if movie not in reference_dict[provider]:
        reference_dict[provider].append(movie)

# retrieve the name of a provider for given offer in api call
def get_provider(idData, offer):
    return(idData[str(offer['provider_id'])]['title'])

# add movie to provider list if not in already
def update_provider(provider, movie, reference_dict):
        if provider in reference_dict:
            if movie not in reference_dict[provider]:
                reference_dict[provider].append(movie)
        

# check every movie in titles and add to cross-reference dict the ones in the config list of services
def reference_films(titles, just_watch, reference_dict):
    for movie in titles:
        search = search_film(movie, just_watch)
        result = search['items'][0]
        if movie == result['title']:
            for offer in result['offers']:
                update_provider(get_provider(idData, offer), movie, reference_dict)


def main():

    # TODO: create ability to reconfigure based on flag or commandline prompt

    # storing config info and creating unique url for watchlist
    user = config_user()
    URL=f'https://letterboxd.com/{user}/watchlist'
    
    country = config_country()

    services = config_services()

    # empty dictionary for all the movies
    reference_dict = {service: [] for service in services}
   
    
    # main soup for basic watchlist info
    rawText = requests.get(URL)
    soup = BeautifulSoup(rawText.content, 'html.parser')
    pages = num_pages(soup)
    titles = unify_pages_list(URL, pages) 


    # main api object
    just_watch=JustWatch(country=country)
    
    # load provider/id maps
    #providerData = json.loads(open('providers.json').read())
    idData = json.loads(open('ids.json').read())


    
    reference_films(titles, just_watch, reference_dict)
    print(reference_dict)
# main execution
if __name__ == '__main__':
    main()

    

