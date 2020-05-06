#!/usr/local/bin/python3

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
    
    code = requests.get('https://ipinfo.io/country').text.strip()
    
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
    providers = list(json.loads(open('config_files/providers/providerData.json', 'r').read()).keys())
    services = []
    cont = True
    word = input("Enter a service you would like to search: ")
    while cont:
        if word != "done":
            matches = get_close_matches(word, providers)
            if matches:
                if matches[0] == word:
                    services.append(word)
                elif len(matches) > 0:                
                    matches.append("None")
                    questions = [
                        inquirer.List('service',
                            message="Did you mean?",
                            choices=matches,
                        ),
                    ]                   
                    word = inquirer.prompt(questions)
                    if not word == "None":
                        services.append(word['service'])
                    else:
                        print("Not a valid service")
            else:
                print('Not a valid service')
        else:
            cont = False
            continue
        word = input("Enter another service, or enter \"done\" to continue: ")

    with open(filename, 'r') as f:
        data = json.load(f)
        data["SERVICES"].extend(services)

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

# print out to the user all services they have previously configured that are available in their current location
def filter_services(filename, configData):
    providers = list(json.loads(open('config_files/providers/providerData.json', 'r').read()).keys())
    #referencing all avilable providers in the user's country from api
    user_services = [service for service in configData['SERVICES'] if service in providers] 

    print('Current Preferred Services List:')
    for service in user_services:
        print(f'\t{service}')
    print()

# let the user review their list of preferred services
def configure_current_services(filename):
    options = [
        inquirer.Checkbox('configs',
                            message='Select any of the following options, or select \'Continue\' to proceed without making changes:',
                            choices=['Add service(s)', 'Remove service(s)', 'Clear all services', 'Continue'],
                          ),
    ]

    choices = inquirer.prompt(options)['configs']
    if 'Clear all services' in choices:
        with open(filename, 'r') as f:
            data = json.load(f)
            data["SERVICES"] = []

        os.remove(filename)

        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

        add_services(filename)
    else: 
        if 'Add service(s)' in choices:
            add_services(filename)
        if 'Remove service(s)' in choices:
            delete_existing_service(filename)

# let the user pick a service from their config file to delete
def delete_existing_service(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    options = [
        inquirer.Checkbox('deleted',
                            message='Select to delete any of your services',
                            choices = data["SERVICES"],
                        ),
    ]
    choices = inquirer.prompt(options)['deleted']
    for service in choices:
        data["SERVICES"].remove(service)
    
    os.remove(filename)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

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
        configData = json.loads(open(filename).read())
    filter_services(filename, configData)
    configure_current_services(filename)
    configData = json.loads(open(filename).read())
    filter_services(filename, configData)
    

if __name__ == '__main__':
    main()
