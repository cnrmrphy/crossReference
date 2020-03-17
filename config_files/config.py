#!/usr/local/bin/python3

from geopy import geocoders
import geocoder
import requests
import geopy
import os
import json
import inquirer
# to test this script directly switch the following comments:
#from providers import load_providers
from config_files.providers import load_providers
from difflib import get_close_matches


def add_country(filename):
    loc = geocoder.ip('me').latlng
    
    code = requests.get(f'http://api.geonames.org/countryCode?lat={loc[0]}&lng={loc[1]}&username=steemer').text.strip()

    with open(filename, 'r') as f:
        data = json.load(f)
        data["COUNTRY"] = code
    
    os.remove(filename)

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

#def load_providers()
def add_user(filename):
    
    username = input('Enter your Letterboxd username: ')

    with open(filename, 'r') as f:
        data = json.load(f)
        data["USER"] = username 

    os.remove(filename)

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def add_services(filename):
    # serviceQ = [
    #     inquirer.Checkbox('SERVICES',
    #         message='Select all the services you would like to search',
    #         choices=['Netflix', 'Amazon Prime Video', 'Amazon Instant Video', 'Apple TV Plus', 'Kanopy', 'Google Play', 'Amazon Video', 'TCM', 'Mubi', 'Criterion Channel', 'iTunes', 'YouTube Premium', 'Disney Plus', 'Hulu', 'HBO Now', 'Atom Tickets', 'CBS', 'DC Universe', 'HBO Go', 'Discovery Channel', 'Fandango Movies', 'Fox', 'NBC', 'Nickelodeon'],
    #         ),
    #     ]
    # serviceA=inquirer.prompt(serviceQ)
    # services=serviceA['SERVICES']
    providers = list(json.loads(open('config_files/providers/providerData.json', 'r').read()).keys())
    services = []
    cont = True
    word = input("Enter a service you would like to search: ")
    while cont:
        if word != "done":
            matches = get_close_matches(word, providers)
            print(matches)
            services.append(word)
        else:
            cont = False
            continue
        word = input("Enter another serice, or enter \"done\" to quit: ")
    print(services)    


    with open(filename, 'r') as f:
        data = json.load(f)
        data["SERVICES"] = services 

    os.remove(filename)

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def clear_config(filename):
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

    open('config_files/providers/idData.json', 'w').close()
    open('config_files/providers/providerData.json', 'w').close()



def main():
    # to test directly, switch the following comments 
    #filename = 'config.json'
    filename = 'config_files/config.json'
    configData = json.loads(open(filename).read())
   
    if not configData["USER"]:
        add_user(filename)
  
    add_country(filename)
    configData = json.loads(open(filename).read())
    load_providers.main()
    
    
    if not configData["SERVICES"]:
        add_services(filename)
    

if __name__ == '__main__':
    main()
