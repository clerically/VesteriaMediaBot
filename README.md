# Vesteria Media Bot (VTC Bot)
hi this is mark speaking to you at 11:00 PM
this was NOT fun to create but heyyyyyyyyyyyyyy it exists now so. yea.

i will be updating this sporadically throughout 2022 or whenever I am bored, it's kind of a cool project but doesn't really serve a functional purpose (yet at least since the bot has 0 following at the moment)

## Features

- Automatically likes and retweets posts with media (images, links?) on the #Vesteria tag
- Posts tweets when places are updated (it's actually like up to 10 minutes after because API limits)

## Installation

Pip module requirements:

- requests
- tweepy

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

You can just modify the `info.json` file in the same directory to configure your bot's bio.

**PLEASE FOR THE LOVE OF ALL THAT IS SACRED,** change the "owner_id" config in `info.json` to your Twitter id. If you don't know it, you can use a site like [this](https://tweeterid.com/) to get it for you.
## Notes/Other

This is absolutely a monstrosity of code and I hate looking at it. I did this in a speedrun of 2.5 hours and I regret only half of it.

Regardless of my whining and what I said a minute ago, I did actually enjoy working on this because it gave me time to work on my Python skills as well as get more acquainted with Roblox's API - which is something that I *should have* done in the first place before trying to webscrape data that wasn't even actually there.

If you have any issues, please make sure to make a GitHub issue instead of just complaining to me and I'll be happy to look into it.

Anyways, thanks for reading & have fun.
Mark 👋