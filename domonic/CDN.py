"""
    domonic.CDN
    ====================================
    Refs to some useful .js and .css libs.

    use for prototyping. wget anything in later and create your own local references once ur happy

    TODO - integrity/cross origin/module?

    WARNING/NOTE - dont use. this isn't released or documented. just ideas atm...

"""

# class CDN_TEXT(object):
# lorem ipusm generator
# fake names


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
    PLACEHOLDER_SERVICE = "loremflickr.com"

    @staticmethod
    def PLACEHOLDER(width=100, height=100, HTTP="", seperator='/'):
        """
        to update do CDN_IMG.PLACEHOLDER_SERVICE = "placebear.com/g"
        usage : img(_src=CDN_IMG.PLACEHOLDER(300,100))
        default HTTP is none, to let the browser decide
        # use optional seperator if the site uses x instead of slash
        img(_src=CDN_IMG.PLACEHOLDER(300,100,'x'))
        """
        return f"{HTTP}://{CDN_IMG.PLACEHOLDER_SERVICE}/{width}{seperator}{height}"


class CDN_JS(object):
    """
    You will need to append the lib version number if you add any libs here
    # obvious candidates... https://github.com/sorrycc/awesome-javascript
    """
    JQUERY_3_5_1 = "https://code.jquery.com/jquery-3.5.1.min.js"
    JQUERY_UI = "https://code.jquery.com/ui/1.12.0/jquery-ui.min.js"
    UNDERSCORE = "https://cdn.jsdelivr.net/npm/underscore@1.11.0/underscore-min.js"
    BOOTSTRAP_4 = "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"
    POPPER_1_16_1 = "https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"
    BOOTSTRAP_5_ALPHA = "https://stackpath.bootstrapcdn.com/bootstrap/5.0.0-alpha1/js/bootstrap.min.js"
    D3_6_1_0 = "https://cdnjs.cloudflare.com/ajax/libs/d3/6.1.0/d3.min.js"
    MODERNIZER_2_8_3 = "https://cdnjs.cloudflare.com/ajax/libs/modernizr/2.8.3/modernizr.min.js"
    MOMENT_2_27_0 = "https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.27.0/moment.min.js"
    PIXI_5_3_3 = "https://cdnjs.cloudflare.com/ajax/libs/pixi.js/5.3.3/pixi.min.js"
    SOCKET_1_4_5 = "https://cdnjs.cloudflare.com/ajax/libs/socket.io/1.4.5/socket.io.min.js"
    X3DOM = "https://www.x3dom.org/download/x3dom.js"
    AFRAME_1_2 = "https://aframe.io/releases/1.2.0/aframe.min.js"
    BRYTHON_3_9_5 = "https://cdnjs.cloudflare.com/ajax/libs/brython/3.9.5/brython.min.js"
    # def find_on_cdn():
    # https://cdn.jsdelivr.net/npm/
    # https://cdnjs.cloudflare.com/ajax/libs/
    # def dl(self, path=None):  # download
    # if path none domonic.JS_MASTER < strip off name to get default assets folder if non passed


class CDN_CSS(object):
    """
    Preferably use version numbers if available. user LATEST if it always gets the latest
    """
    BOOTSTRAP_5_ALPHA = "https://stackpath.bootstrapcdn.com/bootstrap/5.0.0-alpha1/js/bootstrap.min.js"
    BOOTSTRAP_4 = "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"
    MARX = "https://unpkg.com/marx-css/css/marx.min.css"  # version?
    MVP = "https://unpkg.com/mvp.css"  # version?
    WATER_LATEST = "https://cdn.jsdelivr.net/gh/kognise/water.css@latest/water.min.css"  # note 'latest' in cdn url
    BALLOON = "https://unpkg.com/balloon-css/balloon.min.css"
    THREE_DOTS_0_2_0 = "https://cdnjs.cloudflare.com/ajax/libs/three-dots/0.2.0/three-dots.min.css"
    MILLIGRAM_1_3_0 = "https://cdnjs.cloudflare.com/ajax/libs/milligram/1.3.0/milligram.css"
    X3DOM = "https://www.x3dom.org/download/x3dom.css"
    FONTAWESOME_5_7_1 = "https://use.fontawesome.com/releases/v5.7.1/css/all.css"
    MDI_5_4_55 = "https://cdn.materialdesignicons.com/5.4.55/css/materialdesignicons.min.css"  # icons
    # find_on_cdn():
    # https://unpkg.com/
    # https://cdnjs.cloudflare.com/ajax/libs/

    # def dl(self, path=domonic.JS_MASTER):  # download


class CDN_FONT(object):
    @staticmethod
    def google(family):
        return "http://fonts.googleapis.com/css?family=" + '+'.join(family)
