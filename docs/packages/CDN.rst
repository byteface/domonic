CDN
=============

.. meta::
   :description: CDN constants for Python HTML generation with Bootstrap, htmx, D3, Chart.js, A-Frame, Tailwind, Font Awesome, and placeholder images.
   :keywords: Python CDN, Bootstrap Python, htmx CDN, D3 CDN, Chart.js CDN, A-Frame CDN, Tailwind CDN, Font Awesome CDN

For quick reference when prototyping you can use the CDN package.

To use a CDN class it must be imported.

.. code-block :: python

	from domonic.CDN import *

Or just classes you need...

.. code-block :: python

	from domonic.CDN import CDN_JS, CDN_CSS


CDN_JS
----------------

.. code-block :: python

	from domonic.CDN import CDN_JS
	from domonic.html import script

	script(_src=CDN_JS.JQUERY)
	script(_src=CDN_JS.HTMX)
	script(_src=CDN_JS.D3)
	script(_src=CDN_JS.CHART_JS)



CDN_CSS
----------------

.. code-block :: python

	from domonic.CDN import CDN_CSS
	from domonic.html import link

	classless_css = link(_rel="stylesheet", _href=CDN_CSS.WATER)
	bootstrap = link(_rel="stylesheet", _href=CDN_CSS.BOOTSTRAP)

Current CSS constants include:

- BOOTSTRAP
- MARX
- MVP
- WATER
- BALLOON
- THREE_DOTS
- MILLIGRAM
- X3DOM
- FONTAWESOME
- MDI
- TAILWIND
- SIMPLE

Current JavaScript constants include:

- JQUERY
- JQUERY_UI
- UNDERSCORE
- BOOTSTRAP
- POPPER
- D3
- MODERNIZER
- MOMENT
- PIXI
- SOCKET
- X3DOM
- AFRAME
- BRYTHON
- MATHML
- HTMX
- HTMX_2
- HTMAX
- LODASH
- AXIOS
- DAY_JS
- CHART_JS
- ANIME_JS
- VALIDATOR_JS

CDN_IMG
----------------

CDN_IMG has a placeholder service.

.. code-block :: python

        # to change it. do this... 
        CDN_IMG.PLACEHOLDER_SERVICE = "placebear.com/g"

        img(_src=CDN_IMG.PLACEHOLDER(300,100))
        
        # Optional separator if the site uses x instead of slash between dimensions.
        img(_src=CDN_IMG.PLACEHOLDER(300,100,'x')) 


# there's tons to pick from. (NOT ALL ARE HTTPS):

- http://placehold.it/350x150

- http://unsplash.it/200/300

- http://lorempixel.com/400/200

- http://dummyimage.com/600x300/000/fff

- https://dummyimage.com/420x320/ff7f7f/333333.png&text=Sample

- http://placekitten.com/200/300

- https://placeimg.com/640/480/any

- http://placebear.com/g/200/300

- https://ipsumimage.appspot.com/140x100, ff7700

- https://www.fillmurray.com/640/360

- https://baconmockup.com/640/360

- https://placebeard.it/640x360

- https://www.placecage.com/640/360

- https://www.stevensegallery.com/640/360

- https://fakeimg.pl/640x360

- https://fakeimg.pl/420x320/ff0000,128/333333,255/?text=Sample&font=lobster

- https://picsum.photos/640/360

- https://via.placeholder.com/420x320/ff7f7f/333333?text=Sample

- https://keywordimg.com/420x320/random

- http://www.dummysrc.com/430x320.png/22c5fc/17202A


.. automodule:: domonic.CDN
    :members:
    :noindex:

.. automodule:: domonic.utils
    :members:
    :noindex:

.. automodule:: domonic.decorators
    :members:
    :noindex:
