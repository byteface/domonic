import sys

sys.path.insert(0, "..")

# mac:
# brew install chromedriver
# xattr -d com.apple.quarantine /usr/local/bin/chromedriver
# pip install selenium

from selenium import webdriver

from domonic import domonic

browser = webdriver.Chrome()
browser.get("http://google.com")
page = domonic.parseString(browser.page_source)


# test xpath
print(page.evaluate("//a/@href", page))


# test css
for link in page.querySelectorAll("a"):
    # print(link)
    print(link.href)
