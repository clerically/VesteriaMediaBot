# Imports

import os
import json
import time

import tweepy

import threading

import modules.requester as requester

# Global variables

config = None
info = None

# Loop checks

started_likes = False
started_updates = False

# Twitter authentication

_twitterAuth = None
_twitterApi = None

botUser = None

with open("src/data/keys.json", "r") as _keyFile:
    keys = json.load(_keyFile)

    _twitterAuth = tweepy.OAuthHandler(keys["consumer"]["key"], keys["consumer"]["secret"])
    _twitterAuth.set_access_token(keys["access"]["token"], keys["access"]["secret"])

    _twitterApi = tweepy.API(_twitterAuth)
    botUser = _twitterApi.me()

# Bot utility functions

def updateBotInfo():
    with open("src/data/info.json", "r") as _infoFile:
        info = json.load(_infoFile)

        _twitterApi.update_profile(
            str.replace(info["name"], "%VERSION%", info["version"]),
            "",
            info["location"],
            info["description"]
        )

def log(message):
    try:
        _twitterApi.send_direct_message(
            config["twitter"]["owner_id"],
            message
        )
    except:
        print(message)

def is_value_matching(input, value):
    if (input == value):
        return True
    return False

# Main functions

def like_tag(tagName, limit=25):
    for tweet in tweepy.Cursor(_twitterApi.search, str(tagName), include_entities=True).items(limit):
        try:
            status = _twitterApi.get_status(tweet.id)

            if (status.favorited == False):
                tweet.favorite()

                time.sleep(1)

        except tweepy.TweepError as err:
            log(f"Failed to perform like functions on tweet {tweet.id}: {err.reason}")
        except StopIteration:
            break

def check_place_updated(placeId):
    updated_places = requester.get_place_data(placeId)

    index_count = len(updated_places)
    if (index_count >= 1):
        for placeData in updated_places:
            # should contain place id, name, and branch (dev/main)

            place_id = placeData["id"]
            place_name = placeData["name"]
            branch = placeData["branch"]

            game_link = f"https://www.roblox.com/games/{place_id}/"

            _twitterApi.update_status(f"{place_name} has been updated.\n\nBranch: {branch}\nLink:{game_link}")

        log(f"[CheckUpdated]: Posted {index_count} status(es) relating to updated places")

# Loop functions

def loop_like_tags():
    log("[LikeTag_Loop]: Started")
    started_likes = True

    while True:
        for tag in config["like_tags"]["tags"]:
            like_tag(f"#{tag}", config["like_tags"]["max_posts"])
        
        time.sleep(config["like_tags"]["check_interval"] * 60)

def loop_check_places_updated():
    log("[CheckUpdated_Loop]: Started")
    started_updates = True

    while True:

        check_place_updated(config["place_updates"]["main"])
        time.sleep(10)
        check_place_updated(config["place_updates"]["development"])
        
        time.sleep(config["place_updates"]["check_interval"] * 60)

# Startup

if __name__ == "__main__":
    updateBotInfo()

    # Load configs from data files
    with open("src/data/config.json", "r") as _configFile:
        config = json.load(_configFile)

    with open("src/data/info.json", "r") as _infoFile:
        info = json.load(_infoFile)

    # Bot main stuff

    thread_like_tags = threading.Thread(target = loop_like_tags)
    thread_like_tags.setDaemon(True)
    thread_like_tags.start()

    thread_check_places = threading.Thread(target = loop_check_places_updated)
    thread_check_places.setDaemon(True)
    thread_check_places.start()

    botVersion = info["version"]
    log(f"Bot started successfully. Active version: {botVersion}")

    while True: # Keeps the main function alive :D
        pass