from domonic import *
from domonic.dom import MutationObserver, MutationRecord

node = div(
  p("Hello WOrld")
)

def on_mutation(records: list[MutationRecord]):
  print(records)

observer = MutationObserver(on_mutation, interval=0)
observer.observe(
  node, subtree=True, childList=True, attributes=True,
  attributeFilter=None, attributeOldValue=True,
  characterData=True, characterDataOldValue=True
)

p.appendChild(a("CLick Me", _href="/home"))

p.innerHTML = "Hello Wordl!!"

p.remove()
