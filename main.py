import csv
import pandas as pd
import numpy as np

repaired = pd.read_csv('repaired.csv') 
unrepaired = pd.read_csv('unrepaired.csv')
addresses = pd.read_csv('addresses.csv')

repaired['Google Address'] = 0
repaired['Google Result'] = 0

for index, row in repaired.iterrows():
    if pd.isnull(repaired.loc[index,'Cross Street']):
        repaired.loc[index,'Google Address'] = (repaired.loc[index,'Address'] 
            + ", " + repaired.loc[index,'Municipality'] + ", " + "MA")
    else: 
        repaired.loc[index,'Google Address'] = (repaired.loc[index,'Address']
            + " & " + repaired.loc[index,'Cross Street'] + ", " + 
            repaired.loc[index,'Municipality'] + ", " + "MA")

import googlemaps

with open('api.txt','r') as api_file:
    api_key = api_file.read()

gmaps = googlemaps.Client(key=api_key)

for index in range(2000):
    address = repaired.loc[index,'Google Address']

    if ((addresses['Google Address'] == address).any()) == False:

        geocode = gmaps.geocode(repaired.loc[index,'Google Address'])
        new_address = pd.DataFrame({'Google Address': address, 
            'Google Result': geocode})
        addresses = addresses.append(new_address)

addresses.to_csv('addresses.csv')