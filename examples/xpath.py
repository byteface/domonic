import sys
sys.path.insert(0, '..')

from domonic.dom import Text
from domonic.i18n.sw import *
import elementpath  # requires elementpath package

ukurasa = html(
	kichwa(
		hati(),
		mtindo()
	),
	mwili(
		div(Text('Salamu, Dunia')),
		div(Text('test'))
	)
)

# print(f'{ukurasa}')

# elementpath.select(ukurasa, '/html/*')
# print( elementpath.select(ukurasa, '/html') )

from xml.etree import ElementTree
root = ElementTree.XML(str(ukurasa))

print(root)
elementpath.select(root, '//div')

print( elementpath.select(root, '//div') )
print( "test:", str(elementpath.select(ukurasa, '//div[text()="test"]')[0]) )

# impressive. needs more testing