"""    
    test_domonic 
    ~~~~~~~~~~~~~~~~
    
    unit tests for domonic
    
    # TODO - tests for all bs5 pages

"""

import unittest
# import requests
# from mock import patch

from domonic.javascript import Math
from domonic.javascript import Global
from domonic.javascript import Window
from domonic.javascript import Date

from domonic import *

class domonicTestCase(unittest.TestCase):

    # def test_domonic_parse(self):
        # page = domonic.parse("<html><body>'some content'</body></html>")
        # page = domonic.parse("<html><body></body></html>")
        # print(page)

    def test_domonic_get(self):
        print("test_domonic_get-----------=-----------=-----------=-----------=-----------=-----------=-----------=")
        # page = domonic.get("http://eventual.technology")
        # page = domonic.get("https://v5.getbootstrap.com/docs/5.0/examples/checkout/")
        # page = domonic.get("https://v5.getbootstrap.com/docs/5.0/examples/carousel/?#")
        # page = domonic.get("https://v5.getbootstrap.com/docs/5.0/examples/dashboard/#")

        # print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        # print(render(page))
        # dir(page)


    def test_domonic_render(self):
        test = html(
            head(
            meta( _charset="utf-8"),
            # meta( **{"http-equiv":"X-UA-Compatible"}, content="IE=edge"),
            title("eventual.technology"),
            meta( _name="viewport", _content="width=device-width, initial-scale=1"),
            meta( _name="description", _content="eventual technology" ),
            meta( _name="keywords", _content="website, html5, javascript, python, software, aws" ),
            meta( _name="author", _content="eventual.technology" ),
            meta( _property="og:title", _content="eventual technology"),
            meta( _property="og:image", _content=""),
            meta( _property="og:url", _content=""),
            meta( _property="og:site_name", _content="eventual.technology"),
            meta( _property="og:description", _content=""),
            meta( _name="twitter:title", _content="eventual technology" ),
            meta( _name="twitter:image", _content="" ),
            meta( _name="twitter:url", _content="eventual.technology" ),
            meta( _name="twitter:card", _content="" )
            ),
            body(
                header(
                    h1(a( _href="mailto:mike@eventual.technology")),
                    h2("07535784121")
                ),
                footer(
                    img( _class="logo", _src="static/img/logo.svg", _alt="eventual technology")
                )

            )
        )
        # print(render(test))
        pass


    def test_domonic_render_head(self):
        '''
        test = head(
            meta( _charset="utf-8"),
            # meta( **{"http-equiv":"X-UA-Compatible"}, content="IE=edge"),
            title("byteface"),
            meta( _name="viewport", _content="width=device-width, initial-scale=1"),
            meta( _name="description", _content="eventual technology" ),
            meta( _name="keywords", _content="website, html5, javascript, python, software, aws" ),
            meta( _name="author", _content="" ),

            meta( _property="og:title", _content=""),
            meta( _property="og:image", _content=""),
            meta( _property="og:url", _content=""),
            meta( _property="og:site_name", _content=""),
            meta( _property="og:description", _content=""),
            meta( _property="og:type", _content="" ),
            
            meta( _name="twitter:title", _content="" ),
            meta( _name="twitter:imag:src", _content="" ),
            meta( _name="twitter:url", _content="" ),
            meta( _name="twitter:card", _content="" ),
            meta( _name="twitter:site", _content="" ),
            meta( _name="twitter:description", _content="" ),
  
            # link( _rel="dns-prefetch", _href="https://github.githubassets.com" )
            # TOOD - list of 'classless'
            # link( _crossorigin="anonymous", _media="all", _integrity="sha512-1234", _rel="stylesheet", _href="styles.css" )
            # link( rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="GitHub")

            meta( _property="fb:app_id", _content=""),
            meta( _name="google-site-verification", _content="" ),
            meta( _name="google-analytics", _content="" ),
            meta( _name="hostname", _content="site.com"),
            link( _rel="icon", _class="js-site-favicon", _type="image/png", _href="favicon.svg" ),
            meta( _name="theme-color", _content="#1e2327" ),
            link( _rel="manifest", _href="/manifest.json", _crossOrigin="use-credentials" ),
            meta( _property="profile:username", _content="byteface" )
        )
        '''
        # print(render(test))
        pass


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
                link(_href="/docs/5.0/dist/css/bootstrap.min.css", _rel="stylesheet", _integrity="sha384-12345", _crossorigin="anonymous"),
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
            body(_class="bg-light").html( #, _html= # TODO - make an attribute to do the same
                div(_class="container").html( 
                    div(_class="py-5 text-center").html(
                        img(_class="d-block mx-auto mb-4", 
                            _src="/docs/5.0/assets/brand/bootstrap-solid.svg", 
                            _alt="", 
                            _width="72", 
                            _height="72"
                            ),
                        h2("Checkout form"),
                        p( "Below is an example form built entirely with Bootstrap’s form controls. \
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



if __name__ == '__main__':
    unittest.main()
