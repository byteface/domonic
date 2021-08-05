"""
    test_domonic
    ~~~~~~~~~~~~
    - unit tests for domonic
    # TODO - tests for all bs5 pages
"""

import unittest
# import requests
# from mock import patch

from domonic import domonic

from domonic.html import *
from domonic.decorators import silence


class TestCase(unittest.TestCase):

    def test_hello_world(self):
        assert str(html(body(h1('Hello World!')))) == \
            '''<html><body><h1>Hello World!</h1></body></html>'''

    def test_html_attributes(self):
        assert str(div(_id='mydiv', _class='test', **{"_aria-label": True}, **{"_data-name": True}, _onclick="alert('hi');")) == \
            '''<div id="mydiv" class="test" aria-label="True" data-name="True" onclick="alert('hi');"></div>'''

        myel = div(_id='mydiv', _class='test', **{"_aria-label": True}, **{"_data-name": True}, _onclick="alert('hi');")
        assert myel.id == "mydiv"
        assert myel._id == "mydiv"
        assert myel._class == "test"
        assert myel.onclick == "alert('hi');"

    def test_create_element(self):
        # print(create_element('custom_el', div('some content'), _id="test"))
        assert str(create_element('custom_el', div('some content'), _id="test")) == \
            '''<custom_el id="test"><div>some content</div></custom_el>'''

    # @silence
    def test_domonic_parse(self):
        page = domonic.parse("<html><body>'some content'</body></html>") # TODO - single comma
        page = domonic.parse("<html><body></body></html>")
        print(page)

    @silence
    def test_domonic_get(self):
        print("test_domonic_get-----------=-----------=-----------=-----------=-----------=-----------=-----------=")
        page = domonic.get("http://eventual.technology")
        page = domonic.get("https://v5.getbootstrap.com/docs/5.0/examples/checkout/")
        page = domonic.get("https://v5.getbootstrap.com/docs/5.0/examples/carousel/?#")
        page = domonic.get("https://v5.getbootstrap.com/docs/5.0/examples/dashboard/#")
        page = domonic.get("https://www.google.com")
        page = domonic.get("https://www.facebook.com")
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print(render(page))
        pass

    @silence
    def test_domonic_render(self):
        test = html(
            head(
            meta(_charset="utf-8"),
            # meta(**{"http-equiv": "X-UA-Compatible"},, _content="IE=edge"),
            title("eventual.technology"),
            meta(_name="viewport", _content="width=device-width, initial-scale=1"),
            meta(_name="description", _content="eventual technology"),
            meta(_name="keywords", _content="website, html5, javascript, python, software, aws"),
            meta(_name="author", _content="eventual.technology"),
            meta(_property="og:title", _content="eventual technology"),
            meta(_property="og:image", _content=""),
            meta(_property="og:url", _content=""),
            meta(_property="og:site_name", _content="eventual.technology"),
            meta(_property="og:description", _content=""),
            meta(_name="twitter:title", _content="eventual technology"),
            meta(_name="twitter:image", _content=""),
            meta(_name="twitter:url", _content="eventual.technology"),
            meta(_name="twitter:card", _content="")
            ),
            body(
                header(
                    h1(a(_href="mailto:mike@eventual.technology")),
                    h2("07535784121")
                ),
                footer(
                    img(_class="logo", _src="static/img/logo.svg", _alt="eventual technology")
                )

            )
        )
        # print(render(test))
        pass

    @silence
    def test_domonic_render_head(self):
        test = head(
            meta(_charset="utf-8"),
            # meta(**{"http-equiv": "X-UA-Compatible"},, _content="IE=edge"),
            title("byteface"),
            meta(_name="viewport", _content="width=device-width, initial-scale=1"),
            meta(_name="description", _content="eventual technology"),
            meta(_name="keywords", _content="website, html5, javascript, python, software, aws"),
            meta(_name="author", _content=""),

            meta(_property="og:title", _content=""),
            meta(_property="og:image", _content=""),
            meta(_property="og:url", _content=""),
            meta(_property="og:site_name", _content=""),
            meta(_property="og:description", _content=""),
            meta(_property="og:type", _content=""),

            meta(_name="twitter:title", _content=""),
            meta(_name="twitter:imag:src", _content=""),
            meta(_name="twitter:url", _content=""),
            meta(_name="twitter:card", _content=""),
            meta(_name="twitter:site", _content=""),
            meta(_name="twitter:description", _content=""),

            # link(_rel="dns-prefetch", _href="https://github.githubassets.com")
            # TOOD - list of 'classless'
            # link(_crossorigin="anonymous", _media="all", _integrity="sha512-1234", _rel="stylesheet", _href="styles.css")
            # link(_rel="search", _type="application/opensearchdescription+xml" href="/opensearch.xml" title="GitHub")

            meta(_property="fb:app_id", _content=""),
            meta(_name="google-site-verification", _content=""),
            meta(_name="google-analytics", _content=""),
            meta(_name="hostname", _content="site.com"),
            link(_rel="icon", _class="js-site-favicon", _type="image/png", _href="favicon.svg"),
            meta(_name="theme-color", _content="#1e2327"),
            link(_rel="manifest", _href="/manifest.json", _crossOrigin="use-credentials"),
            meta(_property="profile:username", _content="byteface")
        )
        print(render(test))
        pass

    @silence
    def test_domonic_render_bs5_checkout(self):
        test = html(
            head().html(
                meta(_charset="utf-8"),
                meta(_name="viewport", _content="width=device-width, initial-scale=1"),
                meta(_name="description", _content=""),
                meta(_name="author", _content="Mark Otto, Jacob Thornton, and Bootstrap contributors"),
                meta(_name="generator", _content="Hugo 0.72.0"),
                title("Checkout example · Bootstrap"),
                link(_rel="canonical", _href="https://v5.getbootstrap.com/docs/5.0/examples/checkout/"),
                link(_href="/docs/5.0/dist/css/bootstrap.min.css", _rel="stylesheet", __integrity="sha384-12345", __crossorigin="anonymous"),
                link(_rel="apple-touch-icon", _href="/docs/5.0/assets/img/favicons/apple-touch-icon.png", _sizes="180x180"),
                link(_rel="icon", _href="/docs/5.0/assets/img/favicons/favicon-32x32.png", _sizes="32x32", _type="image/png"),
                link(_rel="icon", _href="/docs/5.0/assets/img/favicons/favicon-16x16.png", _sizes="16x16", _type="image/png"),
                link(_rel="manifest", _href="/docs/5.0/assets/img/favicons/manifest.json"),
                link(_rel="mask-icon", _href="/docs/5.0/assets/img/favicons/safari-pinned-tab.svg", _color="#7952b3"),
                link(_rel="icon", _href="/docs/5.0/assets/img/favicons/favicon.ico"),
                meta(_name="theme-color", _content="#7952b3"),
                style("""
                .bd-placeholder-img {
                    font-size: 1.125rem;
                    text-anchor: middle;
                    -webkit-user-select: none;
                    -moz-user-select: none;
                    -ms-user-select: none;
                    user-select: none;
                }
                @media (min-width: 768px) {
                .bd-placeholder-img-lg {
                    font-size: 3.5rem;
                }
                }
                """),
                link(_href="form-validation.css", _rel="stylesheet"),
            ),
            body(_class="bg-light").html(  #, _html= # TODO - make an attribute to do the same
                div(_class="container").html(
                    div(_class="py-5 text-center").html(
                        img(_class="d-block mx-auto mb-4",
                            _src="/docs/5.0/assets/brand/bootstrap-solid.svg",
                            _alt="", _width="72", _height="72"
                            ),
                        h2("Checkout form"),
                        p("Below is an example form built entirely with Bootstrap’s form controls. \
                            Each required form group has a validation state that can be triggered \
                            by attempting to submit the form without completing it.",
                            _class="lead")
                    ),
                    div(_class="row g-3").html(
                        div(_class="col-md-5 col-lg-4 order-md-last").html(
                            h4(_class="d-flex justify-content-between align-items-center mb-3").html(
                                span("Your cart", _class="text-muted"),
                                span("3", _class="badge bg-secondary rounded-pill"),
                            ),
                            ul(_class="list-group mb-3").html(
                                li(_class="list-group-item d-flex justify-content-between lh-sm").html(
                                    div(
                                        h6("Product name", _class="my-0"),
                                        small("Brief description", _class="text-muted"),
                                    ),
                                    span("$12", _class="text-muted")
                                ),
                                li(_class="list-group-item d-flex justify-content-between lh-sm").html(
                                    div(
                                        h6("Second product", _class="my-0"),
                                        small("Brief description", _class="text-muted"),
                                    ),
                                    span("$8", _class="text-muted")
                                ),
                                li(_class="list-group-item d-flex justify-content-between lh-sm").html(
                                    div(
                                        h6("Third item", _class="my-0"),
                                        small("Brief description", _class="text-muted"),
                                        ),
                                    span("$5", _class="text-muted")
                                ),
                                li(_class="list-group-item d-flex justify-content-between bg-light").html(
                                    div(_class="text-success").html(
                                        h6("Promo code", _class="my-0"),
                                        small("EXAMPLECODE"),
                                        ),
                                    span("−$5", _class="text-success")
                                ),
                                li(_class="list-group-item d-flex justify-content-between").html(
                                    span("Total (USD)"),
                                    strong("$20")
                                )
                            ),
                            form(_class="card p-2").html(
                                div(_class="input-group").html(
                                    input(_type="text", _class="form-control", _placeholder="Promo code"),
                                    button("Redeem", _type="submit", _class="btn btn-secondary")
                                )
                            )
                        ),
                        div(_class="col-md-7 col-lg-8").html(
                            h4("Billing address", _class="mb-3"),
                            form(_class="needs-validation", _novalidate=True).html(
                                div(_class="row g-3").html(
                                    div(_class="col-sm-6").html(
                                        label("First name", _for="firstName", _class="form-label"),
                                        input(_type="text", _class="form-control", _id="firstName", _placeholder="", _value="", _required=True),
                                        div("Valid first name is required.", _class="invalid-feedback")
                                    ),
                                    div(_class="col-sm-6").html(
                                        label("Last name", _for="lastName", _class="form-label"),
                                        input(_type="text", _class="form-control", _id="lastName", _placeholder="", _value="", _required=True),
                                        div("Valid last name is required.", _class="invalid-feedback")
                                    ),
                                    div(_class="col-12").html(
                                        label("Username", _for="username", _class="form-label"),
                                        div(_class="input-group").html(
                                            span("@", _class="input-group-text"),
                                            input(_type="text", _class="form-control", _id="username", _placeholder="Username", _required=True),
                                            div("Your username is required.", _class="invalid-feedback")
                                        )
                                    ),
                                    div(_class="col-12").html(
                                        label("Email Optional", _for="email", _class="form-label"),
                                        input(_type="email", _class="form-control", _id="email", _placeholder="you@example.com"),
                                        div("Please enter a valid email address for shipping updates.", _class="invalid-feedback")
                                    ),
                                    div(_class="col-12").html(
                                        label("Address", _for="address", _class="form-label"),
                                        input(_type="text", _class="form-control", _id="address", _placeholder="1234 Main St", _required=True),
                                        div("Please enter your shipping address.", _class="invalid-feedback")
                                    ),
                                    div(_class="col-12").html(
                                        label("Address 2 Optional", _for="address2", _class="form-label"),
                                        input(_type="text", _class="form-control", _id="address2", _placeholder="Apartment or suite")
                                    ),
                                    div(_class="col-md-5").html(
                                        label("Country", _for="country", _class="form-label"),
                                        select(_class="form-select", _id="country", _required=True).html(
                                            option("Choose...", _value=""),
                                            option("United States"),
                                        ),
                                        div("Please select a valid country.", _class="invalid-feedback")
                                    ),
                                    div(_class="col-md-4").html(
                                        label("State", _for="state", _class="form-label"),
                                        select(_class="form-select", _id="state", _required=True).html(
                                            option("Choose...", _value=""),
                                            option("California"),
                                        ),
                                        div("Please provide a valid state.", _class="invalid-feedback")
                                    ),
                                    div(_class="col-md-3").html(
                                        label("Zip", _for="zip", _class="form-label"),
                                        input(_type="text", _class="form-control", _id="zip", _placeholder="", _required=True),
                                        div("Zip code required.", _class="invalid-feedback")
                                    )
                                ),
                                hr(_class="my-4"),
                                div(_class="form-check").html(
                                    input(_type="checkbox", _class="form-check-input", _id="same-address"),
                                    label("Shipping address is the same as my billing address", _class="form-check-label", _for="same-address"),
                                ),
                                div(_class="form-check").html(
                                    input(_type="checkbox", _class="form-check-input", _id="save-info"),
                                    label("Save this information for next time", _class="form-check-label", _for="save-info"),
                                ),
                                hr(_class="my-4"),
                                h4("Payment", _class="mb-3"),
                                div(_class="my-3").html(
                                    div(_class="form-check").html(
                                        input(_id="credit", _name="paymentMethod", _type="radio", _class="form-check-input", _checked=True, _required=True),
                                        label("Credit card", _class="form-check-label", _for="credit"),
                                    ),
                                    div(_class="form-check").html(
                                        input(_id="debit", _name="paymentMethod", _type="radio", _class="form-check-input", _required=True),
                                        label("Debit card", _class="form-check-label", _for="debit"),
                                    ),
                                    div(_class="form-check").html(
                                        input(_id="paypal", _name="paymentMethod", _type="radio", _class="form-check-input", _required=True),
                                        label("PayPal", _class="form-check-label", _for="paypal"),
                                    )
                                ),
                                div(_class="row gy-3").html(
                                    div(_class="col-md-6").html(
                                        label("Name on card", _for="cc-name", _class="form-label"),
                                        input(_type="text", _class="form-control", _id="cc-name", _placeholder="", _required=True),
                                        small("Full name as displayed on card", _class="text-muted"),
                                        div("Name on card is required", _class="invalid-feedback")
                                    ),
                                    div(_class="col-md-6").html(
                                        label("Credit card number", _for="cc-number", _class="form-label"),
                                        input(_type="text", _class="form-control", _id="cc-number", _placeholder="", _required=True),
                                        div("Credit card number is required", _class="invalid-feedback")
                                    ),
                                    div(_class="col-md-3").html(
                                        label("Expiration", _for="cc-expiration", _class="form-label"),
                                        input(_type="text", _class="form-control", _id="cc-expiration", _placeholder="", _required=True),
                                        div("Expiration date required", _class="invalid-feedback")
                                    ),
                                    div(_class="col-md-3").html(
                                        label("CVV", _for="cc-cvv", _class="form-label"),
                                        input(_type="text", _class="form-control", _id="cc-cvv", _placeholder="", _required=True),
                                        div("Security code required", _class="invalid-feedback")
                                    )
                                ),
                                hr(_class="my-4"),
                                button("Continue to checkout", _class="btn btn-primary btn-lg btn-block", _type="submit")
                            )
                        )
                    ),
                    footer(_class="my-5 pt-5 text-muted text-center text-small").html(
                        p("&copy; 2020 Company Name", _class="mb-1"),
                        ul(_class="list-inline").html(
                            li(a("Privacy", _href="#"), _class="list-inline-item"),
                            li(a("Terms", _href="#"), _class="list-inline-item"),
                            li(a("Support", _href="#"), _class="list-inline-item")
                        )
                    ),
                    script(_src="/docs/5.0/dist/js/bootstrap.bundle.min.js", _integrity="sha384-12345", _crossorigin="anonymous"),
                    script(_src="form-validation.js")
                )
            )
        )

        # print(render(test,'bs5_test_checkout.html'))
        print(render(test))
        pass

    @silence
    def test_domonic_render_bs5_carousel(self):
        test = html(_lang="en").html(
            head(
                meta(_charset="utf-8"),
                meta(_name="viewport", _content="_width=device-width, initial-scale=1"),
                meta(_name="description", _content=""),
                meta(_name="author", _content="Mark Otto, Jacob Thornton, and Bootstrap contributors"),
                meta(_name="generator", _content="Hugo 0.72.0"),
                title("Carousel Template · Bootstrap"),
                link(_rel="canonical", _href="https://v5.getbootstrap.com/docs/5.0/examples/carousel/"),
                link(_href="/docs/5.0/dist/css/bootstrap.min.css", _rel="stylesheet", _integrity="sha384-1234", _crossorigin="anonymous"),
                link(_rel="apple-touch-icon", _href="/docs/5.0/assets/img/favicons/apple-touch-icon.png", _sizes="180x180"),
                link(_rel="icon", _href="/docs/5.0/assets/img/favicons/favicon-32x32.png", _sizes="32x32", _type="image/png"),
                link(_rel="icon", _href="/docs/5.0/assets/img/favicons/favicon-16x16.png", _sizes="16x16", _type="image/png"),
                link(_rel="manifest", _href="/docs/5.0/assets/img/favicons/manifest.json"),
                link(_rel="mask-icon", _href="/docs/5.0/assets/img/favicons/safari-pinned-tab.svg", _color="#7952b3"),
                link(_rel="icon", _href="/docs/5.0/assets/img/favicons/favicon.ico"),
                meta(_name="theme-color", _content="#7952b3"),
                style("""
                .bd-placeholder-img {
                    font-size: 1.125rem;
                    text-anchor: middle;
                    -webkit-user-select: none;
                    -moz-user-select: none;
                    -ms-user-select: none;
                    user-select: none;
                }
                @media (min-width: 768px) {
                    .bd-placeholder-img-lg {
                    font-size: 3.5rem;
                    }
                }
                """),
                link(_href="carousel.css", _rel="stylesheet"),
            ),
            body(
                header(
                    nav(_class="navbar navbar-expand-md navbar-dark fixed-top bg-dark").html(
                        div(_class="container-fluid").html(
                            a("Carousel", _class="navbar-brand", _href="#"),
                            button(span(_class="navbar-toggler-icon"), _class="navbar-toggler", _type="button", **{"_data-toggle": "collapse"}, **{"_data-target": "#navbarCollapse"}, **{"_aria-controls": "navbarCollapse"}, **{"_aria-expanded": "false"}, **{"_aria-label": "Toggle navigation"})
                        ),
                        div(_class="collapse navbar-collapse", _id="navbarCollapse").html(
                                ul(_class="navbar-nav mr-auto mb-2 mb-md-0").html(
                                    li(a("Home", _class="nav-link", **{"_aria-current": "page"}, _href="#"), _class="nav-item active"),
                                    li(a("Link", _class="nav-link", _href="#"), _class="nav-item"),
                                    li(a("Disabled", _class="nav-link disabled", _href="#", _tabindex="-1", **{"_aria-disabled": "true"}),
                                    _class="nav-item"
                                    )
                                ),
                                form(_class="d-flex").html(
                                    input(button("Search", _class="btn btn-outline-success", _type="submit"),
                                    _class="form-control mr-2", _type="search", _placeholder="Search", **{"_aria-label": "Search"},
                                )
                            )
                        )
                    )
                ),
                main(
                    div(_id="myCarousel", _class="carousel slide", **{"_data-ride": "carousel"}).html(
                    ol(_class="carousel-indicators").html(
                        li(**{"_data-target": "#myCarousel"}, **{"_data-slide-to": "0"}, _class="active"),
                        li(**{"_data-target": "#myCarousel"}, **{"_data-slide-to": "1"}),
                        li(**{"_data-target": "#myCarousel"}, **{"_data-slide-to": "2"})
                    ),
                    div(_class="carousel-inner").html(
                    div(_class="carousel-item active").html(
                        """<svg _class="bd-placeholder-img", _width="100%", _height="100%" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice", _role="img" focusable="false",<rect _width="100%", _height="100%" fill="#777")</svg>""",
                        div(_class="container").html(
                            div(_class="carousel-caption text-left").html(
                                h1("Example headline."),
                                p("Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit."),
                                p(a("Sign up today", _class="btn btn-lg btn-primary", _href="#", _role="button"))
                            )
                        )
                    ),
                    div(_class="carousel-item").html(
                        """<svg _class="bd-placeholder-img", _width="100%", _height="100%" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice", _role="img" focusable="false",<rect _width="100%", _height="100%" fill="#777")</svg>""",
                        div(_class="container").html(
                            div(_class="carousel-caption").html(
                                h1("Another example headline."),
                                p("Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit."),
                                p(a("Learn more", _class="btn btn-lg btn-primary", _href="#", _role="button"))
                            )
                        )
                    ),
                    div(_class="carousel-item").html(
                        """<svg _class="bd-placeholder-img", _width="100%", _height="100%" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice", _role="img" focusable="false",<rect _width="100%", _height="100%" fill="#777")</svg>""",
                        div(_class="container").html(
                            div(_class="carousel-caption text-right").html(
                                h1("One more for good measure."),
                                p("Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit."),
                                p(a("Browse gallery", _class="btn btn-lg btn-primary", _href="#", _role="button"))
                            )
                        )
                    )
                    ),
                    a(_class="carousel-control-prev", _href="#myCarousel", _role="button", **{"_data-slide": "prev"}).html(
                        span(**{"_aria-hidden": "true"}, _class="carousel-control-prev-icon"),
                        span("Previous", _class="sr-only")
                    ),
                    a(_class="carousel-control-next", _href="#myCarousel", _role="button", **{"_data-slide": "next"}).html(
                        span(_class="carousel-control-next-icon", **{"_aria-hidden": "true"}),
                        span("Next", _class="sr-only")
                    )
                ),
                div(_class="container marketing").html(
                    div(_class="row").html(
                    div(_class="col-lg-4").html(
                        """<svg _class="bd-placeholder-img rounded-circle", _width="140", _height="140" xmlns="http://www.w3.org/2000/svg" aria-label="Placeholder: 140x140" preserveAspectRatio="xMidYMid slice", _role="img" focusable="false",title(Placeholder)<rect _width="100%", _height="100%" fill="#777")<text x="50%" y="50%" fill="#777" dy=".3em">140x140</text></svg>""",
                        h2("Heading"),
                        p("Donec sed odio dui. Etiam porta sem malesuada magna mollis euismod. Nullam id dolor id nibh ultricies vehicula ut id elit. Morbi leo risus, porta ac consectetur ac, vestibulum at eros. Praesent commodo cursus magna."),
                        p(a("View details &raquo;", _class="btn btn-secondary", _href="#", _role="button"))
                    ),
                    div(_class="col-lg-4").html(
                        """<svg _class="bd-placeholder-img rounded-circle", _width="140", _height="140" xmlns="http://www.w3.org/2000/svg" aria-label="Placeholder: 140x140" preserveAspectRatio="xMidYMid slice", _role="img" focusable="false",title(Placeholder)<rect _width="100%", _height="100%" fill="#777")<text x="50%" y="50%" fill="#777" dy=".3em">140x140</text></svg>""",
                        h2("Heading"),
                        p("Duis mollis, est non commodo luctus, nisi erat porttitor ligula, eget lacinia odio sem nec elit. Cras mattis consectetur purus sit amet fermentum. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh."),
                        p(a("View details &raquo;", _class="btn btn-secondary", _href="#", _role="button"))
                    ),
                    div(_class="col-lg-4").html(
                        """<svg _class="bd-placeholder-img rounded-circle", _width="140", _height="140" xmlns="http://www.w3.org/2000/svg" aria-label="Placeholder: 140x140" preserveAspectRatio="xMidYMid slice", _role="img" focusable="false",title(Placeholder)<rect _width="100%", _height="100%" fill="#777")<text x="50%" y="50%" fill="#777" dy=".3em">140x140</text></svg>""",
                        h2("Heading"),
                        p("Donec sed odio dui. Cras justo odio, dapibus ac facilisis in, egestas eget quam. Vestibulum id ligula porta felis euismod semper. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus."),
                        p(a("View details &raquo;", _class="btn btn-secondary", _href="#", _role="button")
                    ),
                    hr(_class="featurette-divider"),
                    div(_class="row featurette").html(
                        div(_class="col-md-7").html(
                            h2("First featurette heading.", span(_class="text-muted"), "It’ll blow your mind.", _class="featurette-heading"),
                            p("Donec ullamcorper nulla non metus auctor fringilla. Vestibulum id ligula porta felis euismod semper. Praesent commodo cursus magna, vel scelerisque nisl consectetur. Fusce dapibus, tellus ac cursus commodo.",
                            _class="lead")
                        ),
                        div("""<svg _class="bd-placeholder-img bd-placeholder-img-lg featurette-image img-fluid mx-auto", _width="500", _height="500" xmlns="http://www.w3.org/2000/svg" aria-label="Placeholder: 500x500" preserveAspectRatio="xMidYMid slice", _role="img" focusable="false",title(Placeholder)<rect _width="100%", _height="100%" fill="#eee")<text x="50%" y="50%" fill="#aaa" dy=".3em">500x500</text></svg>""",
                            _class="col-md-5"
                        )
                    ),
                    hr(_class="featurette-divider"),
                    div(_class="row featurette").html(
                        div(_class="col-md-7 order-md-2").html(
                            h2("Oh yeah, it’s that good.", span(_class="text-muted"), "See for yourself.", _class="featurette-heading")),
                            p("Donec ullamcorper nulla non metus auctor fringilla. Vestibulum id ligula porta felis euismod semper. Praesent commodo cursus magna, vel scelerisque nisl consectetur. Fusce dapibus, tellus ac cursus commodo.", _class="lead")
                        ),
                        div(_class="col-md-5 order-md-1").html(
                            """<svg _class="bd-placeholder-img bd-placeholder-img-lg featurette-image img-fluid mx-auto", _width="500", _height="500" xmlns="http://www.w3.org/2000/svg" aria-label="Placeholder: 500x500" preserveAspectRatio="xMidYMid slice", _role="img" focusable="false",title(Placeholder)<rect _width="100%", _height="100%" fill="#eee")<text x="50%" y="50%" fill="#aaa" dy=".3em">500x500</text></svg>"""
                        )
                    ),
                    hr(_class="featurette-divider"),
                    div(_class="row featurette").html(
                    div(_class="col-md-7").html(
                        h2("Checkmate.", "And lastly, this one.", span(_class="text-muted"), _class="featurette-heading"),
                        p("Donec ullamcorper nulla non metus auctor fringilla. Vestibulum id ligula porta felis euismod semper. Praesent commodo cursus magna, vel scelerisque nisl consectetur. Fusce dapibus, tellus ac cursus commodo.",
                        _class="lead")
                    ),
                    div("""<svg _class="bd-placeholder-img bd-placeholder-img-lg featurette-image img-fluid mx-auto", _width="500", _height="500" xmlns="http://www.w3.org/2000/svg" aria-label="Placeholder: 500x500" preserveAspectRatio="xMidYMid slice", _role="img" focusable="false",title(Placeholder)<rect _width="100%", _height="100%" fill="#eee")<text x="50%" y="50%" fill="#aaa" dy=".3em">500x500</text></svg>""",
                        _class="col-md-5"
                        )
                    ),
                    hr(_class="featurette-divider"),
                    footer(_class="container").html(
                        p("Back to top", a(_href="#"), _class="float-right"),
                        p("&copy; 2017-2020 Company, Inc. &middot;", a("Privacy", _href="#"), "&middot;", a("Terms", _href="#"))
                    )
                    ),
                    script(_src="/docs/5.0/dist/js/bootstrap.bundle.min.js", _integrity="sha384-12345", _crossorigin="anonymous")
                    )
                )
            )
        )
        # print(render(test,'bs5_test_carousel.html'))
        print(render(test))
        pass


    @silence
    def test_domonic_render_bs5_dashboard(self):
        root = html(_lang="en")
        test = root.html(
            head(
                meta(_charset="utf-8"),
                meta(_name="viewport", _content="width=device-width, initial-scale=1"),
                meta(_name="description", _content=""),
                meta(_name="author", _content="Mark Otto, Jacob Thornton, and Bootstrap contributors"),
                meta(_name="generator", _content="Hugo 0.72.0"),
                title("Dashboard Template · Bootstrap"),
                link(_rel="canonical", _href="https://v5.getbootstrap.com/docs/5.0/examples/dashboard/"),
                link(_href="/docs/5.0/dist/css/bootstrap.min.css", _rel="stylesheet", _integrity="sha384-1234", _crossorigin="anonymous"),
                link(_rel="apple-touch-icon", _href="/docs/5.0/assets/img/favicons/apple-touch-icon.png", _sizes="180x180"),
                link(_rel="icon", _href="/docs/5.0/assets/img/favicons/favicon-32x32.png", _sizes="32x32", _type="image/png"),
                link(_rel="icon", _href="/docs/5.0/assets/img/favicons/favicon-16x16.png", _sizes="16x16", _type="image/png"),
                link(_rel="manifest", _href="/docs/5.0/assets/img/favicons/manifest.json"),
                link(_rel="mask-icon", _href="/docs/5.0/assets/img/favicons/safari-pinned-tab.svg", _color="#7952b3"),
                link(_rel="icon", _href="/docs/5.0/assets/img/favicons/favicon.ico"),
                meta(_name="theme-color", _content="#7952b3"),
                style("""
                .bd-placeholder-img {
                    font-size: 1.125rem;
                    text-anchor: middle;
                    -webkit-user-select: none;
                    -moz-user-select: none;
                    -ms-user-select: none;
                    user-select: none;
                }
                @media (min-width: 768px) {
                .bd-placeholder-img-lg {
                    font-size: 3.5rem;
                }
                }
                """),
                link(_href="dashboard.css", _rel="stylesheet"),
            ),
            body(
                nav(_class="navbar navbar-dark sticky-top bg-dark flex-md-nowrap p-0 shadow").html(
                    a("Company name", _class="navbar-brand col-md-3 col-lg-2 mr-0 px-3", _href="#"),
                    button(span(_class="navbar-toggler-icon"), 
                        _class="navbar-toggler position-absolute d-md-none collapsed",
                        _type="button", 
                        **{"_data-toggle": "collapse"}, 
                        **{"_data-target": "#sidebarMenu"}, 
                        **{"_aria-controls": "sidebarMenu"}, 
                        **{"_aria-expanded": "false"}, 
                        **{"_aria-label": "Toggle navigation"}
                    ),
                    input(_class="form-control form-control-dark w-100", _type="text", _placeholder="Search", **{"_aria-label": "Search"}).html(
                        ul(_class="navbar-nav px-3").html(
                            li(a("Sign out",_class="nav-link", _href="#"), _class="nav-item text-nowrap")
                        )
                    ),
                    div(_class="container-fluid").html(
                    div(_class="row").html(
                        nav(_id="sidebarMenu", _class="col-md-3 col-lg-2 d-md-block bg-light sidebar collapse").html(
                            div(_class="position-sticky pt-3").html(
                                ul(_class="nav flex-column").html(
                                    li(
                                        a(span(**{"_data-feather": "home"}), "Dashboard", _class="nav-link active", **{"_aria-current": "page"}, _href="#"),
                                        _class="nav-item"
                                    ),
                                    li(
                                        a(span(**{"_data-feather": "file"}), "Orders", _class="nav-link", _href="#"),
                                        _class="nav-item"
                                    ),
                                    li(
                                        a(span(**{"_data-feather": "shopping-cart"}), "Products", _class="nav-link", _href="#"),
                                        _class="nav-item"
                                    ),
                                    li(
                                        a(span(**{"_data-feather": "users"}), "Customers", _class="nav-link", _href="#"),
                                        _class="nav-item"
                                    ),
                                    li(
                                        a(span(**{"_data-feather": "bar-chart-2"}), "Reports", _class="nav-link", _href="#"),
                                        _class="nav-item"
                                    ),
                                    li(
                                        a(span(**{"_data-feather": "layers"}),"Integrations",_class="nav-link", _href="#"),
                                        _class="nav-item"
                                    )
                                )
                            ),
                            h6(_class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-muted").html(
                            span("Saved reports"),
                                a(span(**{"_data-feather": "plus-circle"}, **{"_aria-label": "Add a new report"}),
                                    _class="link-secondary", _href="#")
                                )
                            ),
                            ul(_class="nav flex-column mb-2").html(
                                li(
                                    a(span(**{"_data-feather": "file-text"}), "Current month", _class="nav-link", _href="#"),
                                    _class="nav-item"
                                ),
                                li(
                                    a(span(**{"_data-feather": "file-text"}), "Last quarter", _class="nav-link", _href="#"),
                                    _class="nav-item"
                                ),
                                li(
                                    a(span(**{"_data-feather": "file-text"}), "Social engagement", _class="nav-link", _href="#"),
                                    _class="nav-item"
                                ),
                                li(
                                    a(span(**{"_data-feather": "file-text"}), "Year-end sale", _class="nav-link", _href="#"),
                                    _class="nav-item"
                                )
                            )
                        )
                    ),
                    main(_class="col-md-9 ml-sm-auto col-lg-10 px-md-4").html(
                        div(_class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom").html(
                            h1("Dashboard", _class="h2"),
                            div(_class="btn-toolbar mb-2 mb-md-0").html(
                                div(_class="btn-group mr-2").html(
                                    button("Share", _type="button", _class="btn btn-sm btn-outline-secondary"),
                                    button("Export", _type="button", _class="btn btn-sm btn-outline-secondary")
                                ),
                                button(span(**{"_data-feather": "calendar"}), "This week", _type="button", _class="btn btn-sm btn-outline-secondary dropdown-toggle")
                            )
                        ),
                        canvas(_class="my-4 w-100", _id="myChart", _width="900", _height="380"),
                        h2("Section title"),
                        div(_class="table-responsive").html(
                            table(_class="table table-striped table-sm").html(
                                thead(
                                    tr(
                                        th("  #"),
                                        th("Header"),
                                        th("Header"),
                                        th("Header"),
                                        th("Header")
                                        )
                                    ),
                                tbody(
                                    tr(
                                        td("1, 001"),
                                        td("Lorem"),
                                        td("ipsum"),
                                        td("dolor"),
                                        td("sit")
                                    ),
                                    tr(
                                        td("1, 002"),
                                        td("amet"),
                                        td("consectetur"),
                                        td("adipiscing"),
                                        td("elit")
                                    ),
                                    tr(
                                        td("1, 003"),
                                        td("Integer"),
                                        td("nec"),
                                        td("odio"),
                                        td("Praesent")
                                    ),
                                    tr(
                                        td("1, 003"),
                                        td("libero"),
                                        td("Sed"),
                                        td("cursus"),
                                        td("ante")
                                    ),
                                    tr(
                                        td("1, 004"),
                                        td("dapibus"),
                                        td("diam"),
                                        td("Sed"),
                                        td("nisi")
                                    ),
                                    tr(
                                        td("1, 005"),
                                        td("Nulla"),
                                        td("quis"),
                                        td("sem"),
                                        td("at")
                                    ),
                                    tr(
                                        td("1, 006"),
                                        td("nibh"),
                                        td("elementum"),
                                        td("imperdiet"),
                                        td("Duis")
                                    ),
                                    tr(
                                        td("1, 007"),
                                        td("sagittis"),
                                        td("ipsum"),
                                        td("Praesent"),
                                        td("mauris")
                                    ),
                                    tr(
                                        td("1, 008"),
                                        td("Fusce"),
                                        td("nec"),
                                        td("tellus"),
                                        td("sed")
                                    ),
                                    tr(
                                        td("1, 009"),
                                        td("augue"),
                                        td("semper"),
                                        td("porta"),
                                        td("Mauris")
                                    ),
                                    tr(
                                        td("1, 010"),
                                        td("massa"),
                                        td("Vestibulum"),
                                        td("lacinia"),
                                        td("arcu")
                                    ),
                                    tr(
                                        td("1, 011"),
                                        td("eget"),
                                        td("nulla"),
                                        td("Class"),
                                        td("aptent")
                                    ),
                                    tr(
                                        td("1, 012"),
                                        td("taciti"),
                                        td("sociosqu"),
                                        td("ad"),
                                        td("litora")
                                    ),
                                    tr(
                                        td("1, 013"),
                                        td("torquent"),
                                        td("per"),
                                        td("conubia"),
                                        td("nostra")
                                    ),
                                    tr(
                                        td("1, 014"),
                                        td("per"),
                                        td("inceptos"),
                                        td("himenaeos"),
                                        td("Curabitur")
                                    ),
                                    tr(
                                        td("1, 015"),
                                        td("sodales"),
                                        td("ligula"),
                                        td(" in "),
                                        td("libero")
                                    )
                                )
                            )
                        )
                    )
                )
            ),
            script(_src="/docs/5.0/dist/js/bootstrap.bundle.min.js", _integrity="sha384-1234", _crossorigin="anonymous"),
            script(_src="https://cdnjs.cloudflare.com/ajax/libs/feather-icons/4.24.1/feather.min.js", _integrity="sha384-1234", _crossorigin="anonymous"),
            script(_src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.min.js", _integrity="sha384-1234", _crossorigin="anonymous"),
            script(_src="dashboard.js")
        )

        # print(render(test,'bs5_test_dashboard.html'))
        # print(render(test))

        # document.getElementsByTagName("div")[0].getAttributeNode("class");
        # print(test.getElementsByTagName("div") )

        # test = html().html(head(),body())
        # print(type(root))
        # print(root.getElementsByTagName("button")[0].getAttribute("class"))
        # print(render(root))
        pass


    def test_domonic_render_a_tag(self):
        atag = a(_href="https://somesite.com:8000/blog/article-one#some-hash")
        assert str(atag) == '<a href="https://somesite.com:8000/blog/article-one#some-hash"></a>'
        assert "https://somesite.com:8000/blog/article-one#some-hash" == atag.href
        assert 'https' == atag.protocol
        assert '8000' == str(atag.port)
        atag.protocol = "http"
        assert 'http' == atag.protocol
        assert "http://somesite.com:8000/blog/article-one#some-hash" == atag.href
        atag.port = 8983
        assert '8983' == str(atag.port)
        assert "http://somesite.com:8983/blog/article-one#some-hash" == atag.href
        assert 'somesite.com' == atag.hostname
        # print('host:',atag.host)


    def test_domonic_render_a_tag_query_params(self):
        # from domonic import a, render
        urls = [
        'example.com/stuff?things=morestuff',
        'https://example.com/stuff?things=morestuff',
        'https://example.com/stuff',
        'https://www.example.com/stuff?thing',
        'https://www.example.com/?stuff'
        ]
        for url in urls:
            print( 'zz',url)
            print( 'zz2',render(a(_href=url)) )
            assert f'''{render(a(_href=url))}''' == f'''<a href="{url}"></a>'''

        # a tag no href TODO
        # print( render(a(_name="test")) )




if __name__ == '__main__':
    unittest.main()
