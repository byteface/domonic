"""
    domonic.CDN
    ====================================
    For quick reference when prototyping
"""


class CDN_JS:
    """
    JavaScript libraries
    """

    JQUERY: str = "https://code.jquery.com/jquery-4.0.0.min.js"
    JQUERY_UI: str = "https://code.jquery.com/ui/1.14.2/jquery-ui.min.js"
    UNDERSCORE: str = "https://cdn.jsdelivr.net/npm/underscore@1.13.8/underscore-umd-min.js"
    BOOTSTRAP: str = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"
    POPPER: str = "https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js"
    D3: str = "https://cdn.jsdelivr.net/npm/d3@7.9.0/dist/d3.min.js"
    # Modernizr 3.x no longer publishes a generic browser build; keep the last public default build.
    MODERNIZR: str = "https://cdnjs.cloudflare.com/ajax/libs/modernizr/2.8.3/modernizr.min.js"
    MODERNIZER: str = MODERNIZR
    MOMENT: str = "https://cdn.jsdelivr.net/npm/moment@2.30.1/min/moment.min.js"
    PIXI: str = "https://cdn.jsdelivr.net/npm/pixi.js@8.20.0/dist/pixi.min.js"
    SOCKET: str = "https://cdn.jsdelivr.net/npm/socket.io-client@4.8.3/dist/socket.io.min.js"
    X3DOM: str = "https://www.x3dom.org/download/x3dom.js"
    AFRAME: str = "https://cdn.jsdelivr.net/npm/aframe@1.8.0/dist/aframe-v1.8.0.min.js"
    BRYTHON: str = "https://cdn.jsdelivr.net/npm/brython@3.14.3/brython.min.js"
    MATHML: str = "https://cdn.jsdelivr.net/npm/mathjax@4.1.3/tex-mml-chtml.min.js"
    HTMX: str = "https://unpkg.com/htmx.org@2.0.10"
    LODASH: str = "https://cdn.jsdelivr.net/npm/lodash@4.18.1/lodash.min.js"
    AXIOS: str = "https://cdn.jsdelivr.net/npm/axios@1.19.0/dist/axios.min.js"
    DAY_JS: str = "https://cdn.jsdelivr.net/npm/dayjs@1.11.23/dayjs.min.js"
    CHART_JS: str = "https://cdn.jsdelivr.net/npm/chart.js@4.5.1/dist/chart.umd.min.js"
    ANIME_JS: str = "https://cdn.jsdelivr.net/npm/animejs@4.5.0/dist/bundles/anime.umd.min.js"
    VALIDATOR_JS: str = "https://cdn.jsdelivr.net/npm/validator@13.15.35/validator.min.js"
    TAILWIND: str = "https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4.3.3/dist/index.global.js"
    CODEMIRROR: str = "https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.20/codemirror.min.js"
    CODEMIRROR_PYTHON: str = "https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.20/mode/python/python.min.js"


class CDN_CSS:
    """
    CSS Libraries
    """

    BOOTSTRAP: str = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css"
    MARX: str = "https://cdn.jsdelivr.net/npm/marx-css@5.3.0/css/marx.min.css"
    MVP: str = "https://cdn.jsdelivr.net/npm/mvp.css@1.17.3/mvp.css"
    WATER: str = "https://cdn.jsdelivr.net/npm/water.css@2.1.1/out/water.min.css"
    BALLOON: str = "https://cdn.jsdelivr.net/npm/balloon-css@1.2.0/balloon.min.css"
    THREE_DOTS: str = "https://cdn.jsdelivr.net/npm/three-dots@0.3.2/dist/three-dots.min.css"
    MILLIGRAM: str = "https://cdn.jsdelivr.net/npm/milligram@1.4.1/dist/milligram.min.css"
    X3DOM: str = "https://www.x3dom.org/download/x3dom.css"
    FONTAWESOME: str = "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@7.3.1/css/all.min.css"
    MDI: str = "https://cdn.jsdelivr.net/npm/@mdi/font@7.4.47/css/materialdesignicons.min.css"
    TAILWIND: str = "https://cdn.jsdelivr.net/npm/tailwindcss@4.3.3/index.css"
    SIMPLE: str = "https://cdn.jsdelivr.net/npm/simpledotcss@2.3.7/simple.min.css"
    CODEMIRROR: str = "https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.20/codemirror.min.css"
    CODEMIRROR_MONOKAI: str = "https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.20/theme/monokai.min.css"


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
    def PLACEHOLDER(
        width: int = 100,
        height: int = 100,
        HTTP: str = "",
        seperator: str = "/",
        separator: str | None = None,
    ) -> str:
        """
        to update do CDN_IMG.PLACEHOLDER_SERVICE = "placebear.com/g"
        usage : img(_src=CDN_IMG.PLACEHOLDER(300,100))
        default HTTP is none, to let the browser decide
        # use optional separator if the site uses x instead of slash
        img(_src=CDN_IMG.PLACEHOLDER(300, 100, separator="x"))
        """
        if separator is not None:
            seperator = separator
        protocol = f"{HTTP.rstrip(':/')}:" if HTTP else ""
        return f"{protocol}//{CDN_IMG.PLACEHOLDER_SERVICE}/{width}{seperator}{height}"


class CDN_FONT:
    @staticmethod
    def google(family: str | list[str] | tuple[str, ...]) -> str:
        """pass a font family name and returns the url"""
        if isinstance(family, str):
            family = [family]
        return "https://fonts.googleapis.com/css?family=" + "|".join(
            str(font).strip().replace(" ", "+") for font in family
        )

    # @staticmethod
    # def font_awesome(version='7.3.1'):
    #     return f"https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@{version}/css/all.min.css"


# class CDN_TEXT:
# lorem ipusm generator
# fake names, addresses

# class CDN_VIDEO:
# class CDN_AUDIO:
