#!/usr/local/bin/python3

import xml
import requests
import re
import json
from justwatch import JustWatch
from os import path


# return the object that contains raw info about all providers
def search_object():
    basepath = path.dirname(__file__)
    filepath = path.abspath(path.join(basepath, "..", "..", "config_files", "config.json"))
    country = json.loads(open(filepath).read())["COUNTRY"]
    just_watch=JustWatch(country=country)

    return(just_watch.get_providers())

# load a json file with a map of provider ids to provider names
def load_idData(providers):
    idData = {str(provider['id']): provider['clear_name'] for provider in providers}
    filename = "idData.json"
    basepath = path.dirname(__file__)
    filepath = path.abspath(path.join(basepath, "..", "providers", filename))
    with open(filepath, 'w') as file:
       json.dump(idData, file)

def load_provData(providers):
    providerData = {provider['clear_name']: str(provider['id']) for provider in providers}
    filename = "providerData.json"
    basepath = path.dirname(__file__)
    filepath = path.abspath(path.join(basepath, "..", "providers", filename))
    with open(filepath, 'w') as file:
       json.dump(providerData, file)
def main():
    providers = search_object() 

    load_idData(providers)
    load_provData(providers)




    

if __name__ == '__main__':
    main()
