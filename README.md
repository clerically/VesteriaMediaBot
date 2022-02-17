# Vesteria Media Bot (VTC Bot)
hi this is mark speaking to you at 11:00 PM
this was NOT fun to create but heyyyyyyyyyyyyyy it exists now so. yea.

## Features

- Automatically likes and retweets posts with media (images, links?) on the #Vesteria tag
- Posts tweets when places are updated (it's actually like up to 10 minutes after because API limits)

## Installation

This assumes you already have created a Twitter bot (not yet? you should go [make one](https://developer.twitter.com/en), they're fun)
Create a file called `keys.json` in the `src/data` directory following this format:

```json
{
    "consumer": {
        "key": "YOUR_CONSUMER_KEY_HERE",
        "secret": "YOUR_CONSUMER_SECRET_HERE"
    },

    "access": {
        "token": "YOUR_TOKEN_HERE",
        "secret": "YOUR_ACCESS_SECRET_HERE"
    }
}
```

## Notes/Other

This is absolutely a monstrosity of code and I hate looking at it. I did this in a speedrun of 2.5 hours and I regret only half of it.

Regardless of my whining and what I said a minute ago, I did actually enjoy working on this because it gave me time to work on my Python skills as well as get more acquainted with Roblox's API - which is something that I *should have* done in the first place before trying to webscrape data that wasn't even actually there.

Anyways, thanks for reading.
Mark 👋