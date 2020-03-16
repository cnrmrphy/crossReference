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

    if configData["COUNTRY"]:
        return(configData["COUNTRY"])
    else:
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

# call api to find the 
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
    just_watch = JustWatch(country=country)
    # load provider/id maps
    providerData = json.loads(open('providers.json').read())
    idData = json.loads(open('ids.json').read())

    # function to check a single movie in the api
    movie = titles[0]
    search = just_watch.search_for_item(query=movie)

    # for provider in just_watch.get_providers():
    #     print(str(provider['id']) + ' '+provider['technical_name'])

    if movie == search['items'][0]['title']:
        print(f'Movie searched: {movie}; First Search Result: '+search['items'][0]['title']) 
        for offer in search['items'][0]['offers']:
            print(idData[str(offer['provider_id'])]['title']+ ' monetization type: '+offer['monetization_type'])
    else:
        print(f'{movie} Not Found')
# main execution
if __name__ == '__main__':
    main()

    

