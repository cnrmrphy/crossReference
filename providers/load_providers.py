#!/usr/local/bin/python3

import xml
import requests
import re
import json
from justwatch import JustWatch



# return the object that contains raw info about all providers
def search_object():
    country = json.loads(open('../config_files/config.json').read())["COUNTRY"]
    just_watch=JustWatch(country=country)

    return(just_watch.get_providers())

# load a json file with a map of provider ids to provider names
def load_idData(providers):
    idData = {str(provider['id']): provider['clear_name'] for provider in providers}

    with open('idData.json', 'w') as file:
        json.dump(idData, file)

def load_provData(providers):
    providerData = {provider['clear_name']: str(provider['id']) for provider in providers}

    with open('providerData.json', 'w') as file:
        json.dump(providerData, file)
def main():
    providers = search_object() 

    load_idData(providers)
    load_provData(providers)




    

if __name__ == '__main__':
    main()
