"""
    domonic.CDN
    ====================================
    For quick reference when prototyping
"""

class CDN_JS:
    """
    JavaScript libraries
    """

    JQUERY: str = "https://code.jquery.com/jquery-3.6.4.min.js"
    JQUERY_UI: str = "https://code.jquery.com/ui/1.13.2/jquery-ui.min.js"
    UNDERSCORE: str = "https://cdn.jsdelivr.net/npm/underscore@1.13.6/underscore-min.js"
    BOOTSTRAP: str = "https://stackpath.bootstrapcdn.com/bootstrap/5.3.0/js/bootstrap.min.js"
    # BOOTSTRAP: str = "https://stackpath.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
    POPPER: str = "https://cdn.jsdelivr.net/npm/popper.js@2.11.7/dist/umd/popper.min.js"
    D3: str = "https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.4/d3.min.js"
    MODERNIZER: str = "https://cdnjs.cloudflare.com/ajax/libs/modernizr/3.11.7/modernizr.min.js"
    MOMENT: str = "https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.29.4/moment.min.js"
    PIXI: str = "https://cdnjs.cloudflare.com/ajax/libs/pixi.js/7.1.0/pixi.min.js"
    SOCKET: str = "https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.6.1/socket.io.min.js"
    X3DOM: str = "https://www.x3dom.org/download/x3dom.js"
    AFRAME: str = "https://aframe.io/releases/1.3.0/aframe.min.js"
    BRYTHON: str = "https://cdnjs.cloudflare.com/ajax/libs/brython/3.11.1/brython.min.js"
    MATHML: str = "https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-mml-chtml.min.js"
    HTMX: str = "https://unpkg.com/htmx.org@1.9.0"
    LODASH: str = "https://cdn.jsdelivr.net/npm/lodash@4.17.21/lodash.min.js"
    AXIOS: str = "https://cdn.jsdelivr.net/npm/axios@0.21.1/dist/axios.min.js"
    DAY_JS: str = "https://cdn.jsdelivr.net/npm/dayjs@1.10.4/dayjs.min.js"
    CHART_JS: str = "https://cdn.jsdelivr.net/npm/chart.js@2.9.4/dist/Chart.min.js"
    ANIME_JS: str = "https://cdn.jsdelivr.net/npm/animejs@3.2.1/lib/anime.min.js"
    VALIDATOR_JS: str = "https://cdn.jsdelivr.net/npm/validator@13.6.0/validator.min.js"

class CDN_CSS:
    """
    CSS Libraries
    """

    BOOTSTRAP: str = "https://stackpath.bootstrapcdn.com/bootstrap/5.3.0/css/bootstrap.min.css"
    MARX: str = "https://unpkg.com/marx-css/css/marx.min.css"
    MVP: str = "https://unpkg.com/mvp.css"
    WATER: str = "https://cdn.jsdelivr.net/gh/kognise/water.css@latest/water.min.css"
    BALLOON: str = "https://unpkg.com/balloon-css/balloon.min.css"
    THREE_DOTS: str = "https://cdnjs.cloudflare.com/ajax/libs/three-dots/0.2.0/three-dots.min.css"
    MILLIGRAM: str = "https://cdnjs.cloudflare.com/ajax/libs/milligram/1.3.0/milligram.css"
    X3DOM: str = "https://www.x3dom.org/download/x3dom.css"
    FONTAWESOME: str = "https://use.fontawesome.com/releases/v5.7.1/css/all.css"
    MDI: str = "https://cdn.materialdesignicons.com/5.4.55/css/materialdesignicons.min.css"
    TAILWIND: str = "https://unpkg.com/tailwindcss@^2.2.15/dist/tailwind.min.css"
    SIMPLE: str = "https://cdn.simplecss.org/simple.min.css"


class CDN_IMG:
    """CDN images"""

    # - icons
    # - UI - emojis

    """
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
    """
    PLACEHOLDER_SERVICE: str = "loremflickr.com"

    @staticmethod
    def PLACEHOLDER(width: int = 100, height: int = 100, HTTP: str = "", seperator: str = "/") -> str:
        """
        to update do CDN_IMG.PLACEHOLDER_SERVICE = "placebear.com/g"
        usage : img(_src=CDN_IMG.PLACEHOLDER(300,100))
        default HTTP is none, to let the browser decide
        # use optional seperator if the site uses x instead of slash
        img(_src=CDN_IMG.PLACEHOLDER(300,100,'x'))
        """
        return f"{HTTP}://{CDN_IMG.PLACEHOLDER_SERVICE}/{width}{seperator}{height}"


class CDN_FONT:
    @staticmethod
    def google(family: str) -> str:
        """pass a font family name and returns the url"""
        return "https://fonts.googleapis.com/css?family=" + "+".join(family)

    # @staticmethod
    # def font_awesome(version='5.7.1'):
    #     return f"https://use.fontawesome.com/releases/v{version}/css/all.css"


# class CDN_TEXT:
# lorem ipusm generator
# fake names, addresses

# class CDN_VIDEO:
# class CDN_AUDIO:
