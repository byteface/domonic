# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '../..')

import requests

from domonic import domonic
from domonic.utils import Utils
from domonic.html import *
from domonic.terminal import *

sites = ["bankofamerica.com","amazon.com","news.ycombinator.com","en.wikipedia.org","youtube.com","facebook.com","twitter.com","fandom.com","pinterest.com","imdb.com","reddit.com","craigslist.org","google.com","instagram.com","walmart.com","apple.com","mail.yahoo.com","indeed.com","steampowered.com","britannica.com","zillow.com","investopedia.com","speedtest.net","spotify.com","cdc.gov","dictionary.com","weather.com","ups.com","verizon.com","wowhead.com","macys.com","ign.com","cbssports.com","webmd.com","genius.com","expedia.com","yelp.com","tripadvisor.com","netflix.com","cnn.com","target.com","glassdoor.com","bulbagarden.net","paypal.com","realtor.com","macys.com","ebay.com","urbandictionary.com","nbcnews.com","microsoft.com","mayoclinic.org","nih.gov","live.com","quora.com","fedex.com","finance.yahoo.com","msn.com","att.com","bbc.com","khanacademy.org","linkedin.com","foxnews.com","ebay.com","healthline.com","yahoo.com","espn.com","gamepedia.com","irs.gov","steampowered.com","mapquest.com","allrecipes.com","aol.com","rottentomatoes.com","ca.gov","play.google.com","cnet.com","roblox.com","businessinsider.com","usatoday.com","medicalnewstoday.com","washingtonpost.com","cdc.gov","chase.com","hulu.com","xfinity.com","forbes.com","nbcnews.com","capitalone.com","ny.gov","adobe.com","irs.gov","nytimes.com","etsy.com","yahoo.com"]

# NOTE - nesting level limits in python
# https://bugs.python.org/issue33149 
# https://bugs.python.org/issue3971

import sys
sys.setrecursionlimit(5000) # beefs the recursion limit for big pages (not a solution for DEEP pages)

from sys import exc_info
from traceback import format_exception

for SITE in sites:
    try:
        r = requests.get("https://"+SITE)
        page = domonic.parseString(r.content.decode("utf-8"))
        print(page)
    except Exception as e:    
        print('Failed to dl page', e)
