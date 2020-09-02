Domonic: CDN
=============

To quickly use and reference external assets when prototyping use the CDN package.

Currently there are 3 types of CDN. .js, .css and .img

Their features will be added here.

To use features from CDN they must be imported.

.. code-block :: python

	from domonic.CDN import *

Or just class you need

.. code-block :: python

	from domonic.CDN import CDN_JS


CDN_JS
----------------

.. code-block :: python

	script(_src=CDN_JS.JQUERY_3_5_1)

currently constants exist for:

- JQUERY_3_5_1
- JQUERY_UI
- UNDERSCORE
- BOOTSTRAP_4
- POPPER_1_16_1
- BOOTSTRAP_5_ALPHA
- D3_6_1_0
- MODERNIZER_2_8_3
- MOMENT_2_27_0
- PIXI_5_3_3
- SOCKET_1_4_5


CDN_CSS
----------------

.. code-block :: python

	classless_css = link(_rel="stylesheet", _href=CDN_CSS.WATER_LATEST)

currently constants exist for:

- BOOTSTRAP_5_ALPHA
- BOOTSTRAP_4
- MARX
- MVP
- WATER_LATEST
- BALLOON
- THREE_DOTS_0_2_0
- MILLIGRAM_1_3_0


CDN_IMG
----------------

CDN_IMG has a placeholder service.

.. code-block :: python

        # to change it. do this... 
        CDN_IMG.PLACEHOLDER_SERVICE = "placebear.com/g"

        img(_src=CDN_IMG.PLACEHOLDER(300,100))
        
        # optional seperator if the site uses x instead of slash between dimensions
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