# Imports

import os
import json
import time

import tweepy

import threading

import modules.requester as requester

# Global variables

_config = None

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
            info["name"],
            "",
            info["location"],
            info["description"]
        )

# Main functions

def like_tag(tagName, limit=25):
    print(f"[LikeTag]: Beginning search on tag {tagName}...")

    for tweet in tweepy.Cursor(_twitterApi.search, str(tagName), include_entities=True).items(limit):
        try:
            status = _twitterApi.get_status(tweet.id)
            print(f"[LikeTag]: Checking tweet {tweet.id} on tag {tagName}")

            if (status.favorited == False):
                tweet.favorite()

                time.sleep(1)

        except tweepy.TweepError as err:
            print(f"Failed to perform like functions on tweet {tweet.id}: {err.reason}")
        except StopIteration:
            break
    
    print(f"[LikeTag]: Finished search on tag {tagName}")

def check_place_updated(placeId):
    print("[CheckUpdated]: Starting updated check...")

    updated_places = requester.get_place_data(placeId)

    print("[CheckUpdated]: Finished updated check")

    index_count = len(updated_places)
    if (index_count >= 1):
        for placeData in updated_places:
            # should contain place id, name, and branch (dev/main)

            place_id = placeData["id"]
            place_name = placeData["name"]
            branch = placeData["branch"]

            game_link = f"https://www.roblox.com/games/{place_id}/"

            _twitterApi.update_status(f"{place_name} has been updated.\n\nBranch: {branch}\nLink:{game_link}")

    print(f"[CheckUpdated]: Posted {index_count} statuses relating to updated places")

# Loop functions

def loop_like_tags():
    print("[LikeTag_Loop]: Starting...")

    while True:
        print("[LikeTag_Loop]: Beginning like check...")

        for tag in config["like_tags"]["tags"]:
            like_tag(f"#{tag}", config["like_tags"]["max_posts"])
        
        print("[LikeTag_Loop]: Finished like check")
        time.sleep(config["like_tags"]["check_interval"] * 60)

def loop_check_places_updated():
    print("[CheckUpdated_Loop]: Starting...")

    while True:
        print("[CheckUpdated_Loop]: Beginning like check...")

        check_place_updated(config["place_updates"]["main"])
        time.sleep(10)
        check_place_updated(config["place_updates"]["development"])
        
        print("[CheckUpdated_Loop]: Finished like check")
        time.sleep(config["place_updates"]["check_interval"] * 60)

# Startup

if __name__ == "__main__":
    updateBotInfo()

    # Load config variable from data file
    with open("src/data/config.json", "r") as _configFile:
        config = json.load(_configFile)

    # Bot main stuff

    thread_like_tags = threading.Thread(target = loop_like_tags)
    thread_like_tags.setDaemon(True)
    thread_like_tags.start()

    thread_check_places = threading.Thread(target = loop_check_places_updated)
    thread_check_places.setDaemon(True)
    thread_check_places.start()

    while True: # Keeps the main function alive :D
        pass