#!/usr/local/bin/python3

from geopy import geocoders
import geocoder
import requests
import geopy
import os
import json
import inquirer



def add_country(filename='config.json', countries='countries.json'):
    loc = geocoder.ip('me').latlng
    
    code = requests.get(f'http://api.geonames.org/countryCode?lat={loc[0]}&lng={loc[1]}&username=steemer').text.strip()

    with open(filename, 'r') as f:
        data = json.load(f)
        data["COUNTRY"] = code
    
    os.remove(filename)

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def add_user(filename='config.json'):
    
    username = input('Enter your Letterboxd username: ')

    with open(filename, 'r') as f:
        data = json.load(f)
        data["USER"] = username 

    os.remove(filename)

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def add_services(filename='config.json'):
    serviceQ = [
        inquirer.Checkbox('SERVICES',
            message='Select all the streaming services you would like to search: ',
            choices=['Netflix', 'Amazon Prime Video', 'Amazon Instant Video', 'Apple TV+', 'Google Play', 'iTunes', 'YouTube Premium', 'Disney Plus', 'Hulu', 'Atom Tickets', 'CBS', 'DC Universe', 'HBO', 'Discovery Channel', 'Fandango Movies', 'Fox', 'NBC', 'Nickelodeon'],
            ),
        ]
    serviceA=inquirer.prompt(serviceQ)
    services=serviceA['SERVICES']

    with open(filename, 'r') as f:
        data = json.load(f)
        data["SERVICES"] = services 

    os.remove(filename)

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


