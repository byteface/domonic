import sys

sys.path.insert(0, "..")

import elementpath  # requires elementpath package
import requests

from domonic import domonic
from domonic.dom import Text
from domonic.html import *
from domonic.i18n.sw import *

# ukurasa = html(
# 	kichwa(
# 		hati(),
# 		mtindo()
# 	),
# 	mwili(
# 		div(Text('Salamu, Dunia')),
# 		div(Text('test'))
# 	)
# )
# print(f'{ukurasa}')

# elementpath.select(ukurasa, '/html/*')
# print( elementpath.select(ukurasa, '/html') )

# from xml.etree import ElementTree
# root = ElementTree.XML(str(ukurasa))
# print(root)
# elementpath.select(root, '//div')
# print( elementpath.select(root, '//div') )

# print("results:", str(elementpath.select(page, '//div[text()="Salamu, Dunia"]')[0]))
# impressive. needs more testing


# sites = ["bankofamerica.com","amazon.com","news.ycombinator.com","en.wikipedia.org","youtube.com","facebook.com","twitter.com","fandom.com","pinterest.com","imdb.com","reddit.com","craigslist.org","google.com","instagram.com","walmart.com","apple.com","mail.yahoo.com","indeed.com","steampowered.com","britannica.com","zillow.com","investopedia.com","speedtest.net","spotify.com","cdc.gov","dictionary.com","weather.com","ups.com","verizon.com","wowhead.com","macys.com","ign.com","cbssports.com","webmd.com","genius.com","expedia.com","yelp.com","tripadvisor.com","netflix.com","cnn.com","target.com","glassdoor.com","bulbagarden.net","paypal.com","realtor.com","macys.com","ebay.com","urbandictionary.com","nbcnews.com","microsoft.com","mayoclinic.org","nih.gov","live.com","quora.com","fedex.com","finance.yahoo.com","msn.com","att.com","bbc.com","khanacademy.org","linkedin.com","foxnews.com","ebay.com","healthline.com","yahoo.com","espn.com","gamepedia.com","irs.gov","steampowered.com","mapquest.com","allrecipes.com","aol.com","rottentomatoes.com","ca.gov","play.google.com","cnet.com","roblox.com","businessinsider.com","usatoday.com","medicalnewstoday.com","washingtonpost.com","cdc.gov","chase.com","hulu.com","xfinity.com","forbes.com","nbcnews.com","capitalone.com","ny.gov","adobe.com","irs.gov","nytimes.com","etsy.com","yahoo.com"]

r = requests.get("https://news.ycombinator.com")
page = domonic.parseString(r.content.decode("utf-8"))
# print(page)

# print("results:", str(elementpath.select(page, '//span/a')))

# //*[@id="29950006"]/td[3]/span/a/span

# /html/body/center/table/tbody/tr[3]/td/table/tbody/tr[10]/td[3]/span/a/span

# print("results:", str(elementpath.select(page, '/html/body/center/table/tbody/tr[3]/td/table/tbody/tr[10]/td[3]/span/a/span')))

# print("results:", str(elementpath.select(page, 'html/body/center/table/tbody/tr[3]/td/table/tbody/tr[10]/td[3]/span/a/span')[0].text))

# print("results:", str(elementpath.select(page, '//*/a[@href]')))
# print("results:", str(elementpath.select(page, '//*/a/@_href')))  # ahhh. lol. right. needs the underscores

# print("results:", str(elementpath.select(page, '//*//@_class')))  # cool!

print("results:", str(page.evaluate("//*//@_class", page)))  # cool!
