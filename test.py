#!/usr/local/bin/python3

import requests


code = requests.get('https://ipinfo.io/country').text.strip()

print(code)