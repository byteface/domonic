"""
    domonic.CDN
    ====================================
    For quick reference when prototyping you can use the CDN package.
    (Don't rely on a CDN package for production code. wget a local copy.)

    TODO - integrity/cross origin/module?
"""


class CDN_JS(object):
    """
    Preferably use version numbers if available.
    """
    JQUERY_3_5_1: str = "https://code.jquery.com/jquery-3.5.1.min.js"  #:
    JQUERY_UI: str = "https://code.jquery.com/ui/1.12.0/jquery-ui.min.js"  #:
    UNDERSCORE: str = "https://cdn.jsdelivr.net/npm/underscore@1.11.0/underscore-min.js"  #:
    BOOTSTRAP_4: str = "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"  #:
    POPPER_1_16_1: str = "https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"  #:
    BOOTSTRAP_5_ALPHA: str = "https://stackpath.bootstrapcdn.com/bootstrap/5.0.0-alpha1/js/bootstrap.min.js"  #:
    D3_6_1_0: str = "https://cdnjs.cloudflare.com/ajax/libs/d3/6.1.0/d3.min.js"  #:
    MODERNIZER_2_8_3: str = "https://cdnjs.cloudflare.com/ajax/libs/modernizr/2.8.3/modernizr.min.js"  #:
    MOMENT_2_27_0: str = "https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.27.0/moment.min.js"  #:
    PIXI_5_3_3: str = "https://cdnjs.cloudflare.com/ajax/libs/pixi.js/5.3.3/pixi.min.js"  #:
    SOCKET_1_4_5: str = "https://cdnjs.cloudflare.com/ajax/libs/socket.io/1.4.5/socket.io.min.js"  #:
    X3DOM: str = "https://www.x3dom.org/download/x3dom.js"  #:
    AFRAME_1_2: str = "https://aframe.io/releases/1.2.0/aframe.min.js"  #:
    BRYTHON_3_9_5: str = "https://cdnjs.cloudflare.com/ajax/libs/brython/3.9.5/brython.min.js"  #:
    MATHML: str = "https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config=MML_HTMLorMML"  #:
    HTMX: str = "https://unpkg.com/htmx.org@1.5.0"  #:


class CDN_CSS(object):
    """
    Preferably use version numbers if available.
    use LATEST if it always gets the latest
    """
    BOOTSTRAP_5_ALPHA: str = "https://stackpath.bootstrapcdn.com/bootstrap/5.0.0-alpha1/js/bootstrap.min.js"  #:
    BOOTSTRAP_4: str = "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"  #:
    MARX: str = "https://unpkg.com/marx-css/css/marx.min.css"  #:
    MVP: str = "https://unpkg.com/mvp.css"  #:
    WATER_LATEST: str = "https://cdn.jsdelivr.net/gh/kognise/water.css@latest/water.min.css"  #:
    BALLOON: str = "https://unpkg.com/balloon-css/balloon.min.css"  #:
    THREE_DOTS_0_2_0: str = "https://cdnjs.cloudflare.com/ajax/libs/three-dots/0.2.0/three-dots.min.css"  #:
    MILLIGRAM_1_3_0: str = "https://cdnjs.cloudflare.com/ajax/libs/milligram/1.3.0/milligram.css"  #:
    X3DOM: str = "https://www.x3dom.org/download/x3dom.css"  #:
    FONTAWESOME_5_7_1: str = "https://use.fontawesome.com/releases/v5.7.1/css/all.css"  #:
    MDI_5_4_55: str = "https://cdn.materialdesignicons.com/5.4.55/css/materialdesignicons.min.css"  #:
    TAILWIND_2_2_15: str = "https://unpkg.com/tailwindcss@^2.2.15/dist/tailwind.min.css"  #:
    SIMPLE: str = "https://cdn.simplecss.org/simple.min.css"  #:


class CDN_IMG(object):
    """ CDN images """
    # - icons
    # - UI - emojis

    '''
    # SOME EXAMPLES. NOT ALL ARE HTTPS:
    http://placehold.it/350x150
    http://unsplash.it/200/300
    http://lorempixel.com/400/200
    http://dummyimage.com/600x300/000/fff
    # https://dummyimage.com/420x320/ff7f7f/333333.png&text=Sample
    http://placekitten.com/200/300
    https://placeimg.com/640/480/any
    http://placebear.com/g/200/300
    https://ipsumimage.appspot.com/140x100, ff7700
    https://www.fillmurray.com/640/360
    https://baconmockup.com/640/360
    https://placebeard.it/640x360
    https://www.placecage.com/640/360
    https://www.stevensegallery.com/640/360
    https://fakeimg.pl/640x360
    # https://fakeimg.pl/420x320/ff0000,128/333333,255/?text=Sample&font=lobster
    https://picsum.photos/640/360
    https://via.placeholder.com/420x320/ff7f7f/333333?text=Sample
    https://keywordimg.com/420x320/random
    http://www.dummysrc.com/430x320.png/22c5fc/17202A
    '''
    PLACEHOLDER_SERVICE: str = "loremflickr.com"

    @staticmethod
    def PLACEHOLDER(width: int=100, height: int=100, HTTP: str="", seperator: str='/') -> str:
        """
        to update do CDN_IMG.PLACEHOLDER_SERVICE = "placebear.com/g"
        usage : img(_src=CDN_IMG.PLACEHOLDER(300,100))
        default HTTP is none, to let the browser decide
        # use optional seperator if the site uses x instead of slash
        img(_src=CDN_IMG.PLACEHOLDER(300,100,'x'))
        """
        return f"{HTTP}://{CDN_IMG.PLACEHOLDER_SERVICE}/{width}{seperator}{height}"


class CDN_FONT(object):

    @staticmethod
    def google(family: str) -> str:
        """ pass a font family name and returns the url """
        return "https://fonts.googleapis.com/css?family=" + '+'.join(family)

    # @staticmethod
    # def font_awesome(version='5.7.1'):
    #     return f"https://use.fontawesome.com/releases/v{version}/css/all.css"


# class CDN_TEXT(object):
# lorem ipusm generator
# fake names, addresses

# class CDN_VIDEO(object):
# class CDN_AUDIO(object):
