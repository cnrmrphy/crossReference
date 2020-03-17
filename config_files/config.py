#!/usr/local/bin/python3

from geopy import geocoders
import geocoder
import requests
import geopy
import os
import json
import inquirer



def add_country(filename='config_files/config.json'):
    loc = geocoder.ip('me').latlng
    
    code = requests.get(f'http://api.geonames.org/countryCode?lat={loc[0]}&lng={loc[1]}&username=steemer').text.strip()

    with open(filename, 'r') as f:
        data = json.load(f)
        data["COUNTRY"] = code
    
    os.remove(filename)

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def add_user(filename='config_files/config.json'):
    
    username = input('Enter your Letterboxd username: ')

    with open(filename, 'r') as f:
        data = json.load(f)
        data["USER"] = username 

    os.remove(filename)

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def add_services(filename='config_files/config.json'):
    serviceQ = [
        inquirer.Checkbox('SERVICES',
            message='Select all the services you would like to search',
            choices=['Netflix', 'Amazon Prime Video', 'Amazon Instant Video', 'Apple TV Plus', 'Kanopy', 'Google Play', 'Amazon Video', 'TCM', 'Mubi', 'Criterion Channel', 'iTunes', 'YouTube Premium', 'Disney Plus', 'Hulu', 'HBO Now', 'Atom Tickets', 'CBS', 'DC Universe', 'HBO Go', 'Discovery Channel', 'Fandango Movies', 'Fox', 'NBC', 'Nickelodeon'],
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

def clear_config(filename='config_files/config.json'):
    with open(filename, 'r') as f:
        data = json.load(f)
        for key in data:
            if type(data[key])==list:
                data[key] = []
            else:
                data[key] = ""

    os.remove(filename)

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def main():
    configData = json.loads(open('config_files/config.json').read())
    if not configData["USER"]:
        add_user()
    add_country()
    if not configData["SERVICES"]:
        add_services()
    

if __name__ == '__main__':
    main()