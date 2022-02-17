# Basically a straight rip of my GamePlaceTracker file with slight modifications

from mmap import ALLOCATIONGRANULARITY
import os
import sys
import time

import json

import requests

from datetime import datetime
from dateutil import parser as dateparser

config = None
    
# Load config variable from data file
with open("src/data/config.json", "r") as _configFile:
    config = json.load(_configFile)

def jstamp_to_epoch(jstamp):
    # "Jstamp" values are like: 2022-02-12T20:25:43.707Z

    date_time_obj = dateparser.parse(jstamp)
    return int(date_time_obj.timestamp())


def get_place_data(gameId):
    # Universe (game holder) id

    get_universeId = requests.get("https://api.roblox.com/universes/get-universe-containing-place", params = {"placeid": gameId})
    universeId = -1

    if (get_universeId.status_code == 200):
        universeId = get_universeId.json()["UniverseId"]
    else:
        print(f"CRITICAL ERROR: Invalid universe id get status code ({get_universeId.status_code}), terminating process...")
        sys.exit()

    # Universe places

    get_universePlaces = requests.get(f"https://develop.roblox.com/v1/universes/{universeId}/places", params = {"sortOrder": "Asc", "limit": 100})
    universePlaces = {}

    if (get_universePlaces.status_code == 200):
        universePlaces = get_universePlaces.json()["data"]
    else:
        print(f"CRITICAL ERROR: Invalid universe places get status code ({get_universeId.status_code}), terminating process...")
        sys.exit()

    # Insert place data stuff into data directory folde

    updated_places = []

    for place in universePlaces:
        # Place (and universe creator) data

        place_name = place["name"]
        place_id = str(place["id"])

        branch = None
        if (gameId == config["place_updates"]["development"]):
            branch = "development"
        if (gameId == config["place_updates"]["main"]):
            branch = "main"

        place_file_path = f"src/data/cache/{branch}/{place_id}.txt"

        raw_api_data = requests.get(f"https://api.roblox.com/marketplace/productinfo?assetId={place_id}")
        apiData = None

        if (raw_api_data.status_code == 200):
            apiData = raw_api_data.json()
        
        if (apiData != None):
            updated_timestamp = jstamp_to_epoch(apiData["Updated"])

            if (os.path.exists(place_file_path)):
                oldTimestamp = int(float(open(place_file_path, "r").read())) # Should always be timestamp
                newTimestamp = int(float(updated_timestamp))

                if (newTimestamp > oldTimestamp):
                    return_data = {
                        "id": place_id,
                        "name": place_name,
                        "branch": str.capitalize(branch)
                    }

                    updated_places.append(return_data)
            
            with open(place_file_path, "w") as _placeFile:
                _placeFile.write(str(updated_timestamp))
        
    return updated_places