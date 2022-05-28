# -*- coding: utf-8 -*-

import sys

sys.path.insert(0, "../..")

import requests

from domonic import domonic
from domonic.utils import Utils
from domonic.html import *
from domonic.terminal import *

sites = [
    "bankofamerica.com",
    "amazon.com",
    "news.ycombinator.com",
    "en.wikipedia.org",
    "youtube.com",
    "facebook.com",
    "twitter.com",
    "fandom.com",
    "pinterest.com",
    "imdb.com",
    "reddit.com",
    "craigslist.org",
    "google.com",
    "instagram.com",
    "walmart.com",
    "apple.com",
    "mail.yahoo.com",
    "indeed.com",
    "steampowered.com",
    "britannica.com",
    "zillow.com",
    "investopedia.com",
    "speedtest.net",
    "spotify.com",
    "cdc.gov",
    "dictionary.com",
    "weather.com",
    "ups.com",
    "verizon.com",
    "wowhead.com",
    "macys.com",
    "ign.com",
    "cbssports.com",
    "webmd.com",
    "genius.com",
    "expedia.com",
    "yelp.com",
    "tripadvisor.com",
    "netflix.com",
    "cnn.com",
    "target.com",
    "glassdoor.com",
    "bulbagarden.net",
    "paypal.com",
    "realtor.com",
    "macys.com",
    "ebay.com",
    "urbandictionary.com",
    "nbcnews.com",
    "microsoft.com",
    "mayoclinic.org",
    "nih.gov",
    "live.com",
    "quora.com",
    "fedex.com",
    "finance.yahoo.com",
    "msn.com",
    "att.com",
    "bbc.com",
    "khanacademy.org",
    "linkedin.com",
    "foxnews.com",
    "ebay.com",
    "healthline.com",
    "yahoo.com",
    "espn.com",
    "gamepedia.com",
    "irs.gov",
    "steampowered.com",
    "mapquest.com",
    "allrecipes.com",
    "aol.com",
    "rottentomatoes.com",
    "ca.gov",
    "play.google.com",
    "cnet.com",
    "roblox.com",
    "businessinsider.com",
    "usatoday.com",
    "medicalnewstoday.com",
    "washingtonpost.com",
    "cdc.gov",
    "chase.com",
    "hulu.com",
    "xfinity.com",
    "forbes.com",
    "nbcnews.com",
    "capitalone.com",
    "ny.gov",
    "adobe.com",
    "irs.gov",
    "nytimes.com",
    "etsy.com",
    "yahoo.com",
]

# sites = ["bankofamerica.com"] ??
# sites = ["amazon.com"]
# sites = ["news.ycombinator.com"]
# sites = ["en.wikipedia.org"]
# sites = ["youtube.com"]
# sites = ["facebook.com"]
# sites = ["twitter.com"]
# sites = ["fandom.com"] # < json tags . not done - xxxx
# sites = ["pinterest.com"]
# sites = ["imdb.com"] # _xmlns:og=" . not done - xxxx
# sites = ["reddit.com"]
# sites = ["craigslist.org"]. NOT DONE. < max recur ["cnbc.com"]
# sites = ["google.com"]
# sites = ["instagram.com"]
# sites = ["walmart.com"]
# sites = ["apple.com"]
# sites = ["mail.yahoo.com"]
# sites = ["indeed.com"]
# sites = ["steampowered.com"] # . NOT DONE. parser stack overflow ["theguardian.com"]
# sites = ["britannica.com"]
# sites = ["zillow.com"]
# sites = ["investopedia.com"] < svg.  symbol .NOT DONE.
# sites = ["speedtest.net"]
# sites = ["spotify.com"]
# sites = ["cdc.gov"] < svg.  symbol .NOT DONE.
# sites = ["dictionary.com"] # nice
# sites = ["weather.com"]
# sites = ["ups.com"] # useful
# sites = ["verizon.com"] #.NOT DONE gzip?
# sites = ["wowhead.com"] > ? .NOT DONE.? can't see why? - need to wrap a test so it points to the err
# sites = ["macys.com"]
# sites = ["ign.com"]
# sites = ["cbssports.com"]
# sites = ["webmd.com"]
# sites = ["genius.com"] # nice
# sites = ["expedia.com"]
# sites = ["yelp.com"] . DONE / NOT DONE. strange nested tuples react-root
# sites = ["tripadvisor.com"] # niiice
# sites = ["netflix.com"] # wow
# sites = ["cnn.com"]
# sites = ["indeed.com"]
# sites = ["target.com"]
# sites = ["glassdoor.com"]
# sites = ["bulbagarden.net"] # nice
# sites = ["paypal.com"] # nice
# sites = ["realtor.com"]
# sites = ["macys.com"]

# sites = ["ebay.com"] # svg
# sites = ["urbandictionary.com"]

# sites = ["nbcnews.com"]
# sites = ["craigslist.org"]
# sites = ["capitalone.com"]

# sites = ["craigslist.org"]. NOT DONE. < max recur ["cnbc.com"]

# can pass by removing lines I cant yet always parse properly. i.e. custom tags and multi lines strings
# sites = ["microsoft.com"]
# sites = ["mayoclinic.org"]
# sites = ["nih.gov"]
# sites = ["britannica.com"]
# sites = ["live.com"]
# sites = ["quora.com"] # huge parse no content again.
# sites = ["fedex.com"] # parse no content. looks like custom tags
# sites = ["finance.yahoo.com"]
# sites = ["msn.com"]
# sites = ["dictionary.com"]
# sites = ["indeed.com"]
# sites = ["apple.com"]
# sites = ["att.com"]
# sites = ["bbc.com"]
# sites = ["khanacademy.org"]
# sites = ["cbssports.com"]
# sites = ["linkedin.com"]
# sites = ["foxnews.com"]

# STILL NOT PARSING
# sites = ["ebay.com"] # n? - no error shown
# sites = ["healthline.com"] # n? - missing comma after custom hyphenated attrribute at end of line.
# sites = ["etsy.com"]  #n? keyword argument repeated
# sites = ["yahoo.com"] # are lass params now getting () applied??. ffs
# sites = ["espn.com"] # n? not sure
# sites = ["gamepedia.com"]# n? not sure
# sites = ["irs.gov"] # n? unexpected keyword argument.
# sites = ["steampowered.com"]
# sites = ["mapquest.com"]# n? unexpected keyword argument.

# sites = ["allrecipes.com"]
# sites = ["aol.com"] # n? s_push stack overflow. hard to test as main site is different
# sites = ["rottentomatoes.com"]
# sites = ["ca.gov"] #n? . dodgy chars at top of file
# sites = ["play.google.com"] # n? js heavy i think
# sites = ["cnet.com"] # n? overflow - json in data tag
# sites = ["roblox.com"] # do we have 3 hyphen limit on custom tags?
# sites = ["businessinsider.com"] # encoded quotes have appeared on tags pushing them into creatElement?
# sites = ["usatoday.com"]# encoded quotes have appeared. happneing a lot :(
# sites = ["medicalnewstoday.com"] #? not sure
# sites = ["washingtonpost.com"] #? not sure
# sites = ["investopedia.com"] #? not sure
# sites = ["cdc.gov"] #? keyword argument repeated (<string>, line 1007)
# sites = ["chase.com"] #? not sure
# sites = [ "hulu.com"]
# sites = ["xfinity.com"] #? not sure
# sites = ["forbes.com"] #? not sure
# sites = ["wowhead.com"] #? not sure
# sites = ["nbcnews.com"] #? not sure
# sites = ["capitalone.com"] #? not sure
# sites = ["ny.gov"] #? not sure
# sites = ["adobe.com"]
# sites = ["irs.gov"]
# sites = ["urbandictionary.com"]
# sites = ["nytimes.com"] # dodgy quotes around failed single param parse
# sites = ["etsy.com"]
# sites = ["yahoo.com"]


# NOTE - nesting level limits in python
# https://bugs.python.org/issue33149
# https://bugs.python.org/issue3971

import sys

sys.setrecursionlimit(5000)  # beefs the recursion limit for big pages (not a solution for DEEP pages)

from sys import exc_info
from traceback import format_exception

# log_file = open("fail.log","w")
# sys.stdout = log_file

for SITE in sites:
    # print("Trying::", SITE)
    # page = domonic.get("https://"+SITE)

    try:
        r = requests.get("https://" + SITE)
        # print(r.text.decode("utf-8"))
        page = domonic.parse(r.content.decode("utf-8"), remove_broken_lines=True)
    except Exception as e:
        print("Failed to dl page")

    if page is None:
        print("NO PAGE")
        continue

    render(page, "tmp/" + Utils.url2file(SITE))  # render the one before the eval

    page = domonic.evaluate(page)  # eval - tell us if we failed
    render(page, "tmp/" + Utils.url2file(SITE) + ".pyml")  # write evaulated

    try:
        outp = domonic.domonify(page)
        if type(outp) is tuple:
            outp = outp[0]
        render(outp, "tmp/" + Utils.url2file(SITE) + ".html")  # output rendered html
        print("Success! html file generated")
    except Exception as e:
        print("Failed to create html. you will have to manually fix the pyml")


print(domonic.parse("<div></div>"))
print(domonic.parse("<div><ul><li><li></ul></div>"))

# <------------------------------ should compile. i.e
# page = '''html(
#     head(
#         meta( _charset="utf-8" ),
#         meta( **{"_http-equiv":"X-UA-Compatible"}, _content="IE=edge" ),
#         title("eventual.technology"),
#         meta( _name="description", _content="" ),
#         meta( _name="viewport", _content="width=device-width, initial-scale=1" ),
#         meta( _name="robots", _content="all,follow" ),
#         link( _rel="stylesheet", _href="static/css/bootstrap.min.css" ),
#         link( _rel="stylesheet", _href="static/css/lightbox.min.css" ),
#         link( _rel="stylesheet", _href="static/css/styles.css" ),
#         link( _rel="shortcut icon", _href="favicon.png" )
#     ),
# )'''
# p = eval(page)
# print("===============")
# print(type(p))
