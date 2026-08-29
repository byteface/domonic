"""
BeautifulSlop compatibility example.

Use a Beautiful Soup style API while keeping real domonic nodes underneath.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from domonic.bs4 import BeautifulSlop


markup = """
<article id="post">
  <h1>Sloppy, but useful</h1>
  <p>Read <a href="/docs" class="external">the docs</a>.</p>
  <aside>Remove me</aside>
</article>
"""

soup = BeautifulSlop(markup, "html.parser")

for link in soup.find_all("a", class_="external"):
    print(link.get("href"))

aside = soup.find("aside")
aside.decompose()

badge = soup.new_tag("span", class_="badge")
badge.append("patched")
soup.find("h1").insert_after(badge)

print(soup.select_one("article > span").text)
print(soup.querySelector("article").getAttribute("id"))
print(soup)
