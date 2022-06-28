from domonic.html import *

# TODO - finish example using every tag

# mycss = inlcude('static/css/mystyle.css')
# myjs = inlcude('static/js/script.js')

repo = "http://www.github.com/byteface/domonic"
css = ".titleStyle{color:lime;}"
js = "setTimeout( function(){alert('python is fun!')}, 2000 );"

output = html(
    head(
        title("domonic", _id="title"),
        link(
            _rel="stylesheet",
            _type="text/css",
            _href="https://cdnjs.cloudflare.com/ajax/libs/milligram/1.3.0/milligram.css",
        ),
        style(css),
        script(js),
    ),
    body(
        header(
            a(
                img(
                    _width="149",
                    _height="149",
                    _src="https://github.blog/wp-content/uploads/2008/12/forkme_right_white_ffffff.png?resize=149%2C149",
                    _class="attachment-full size-full",
                    _alt="Fork me on GitHub",
                    _style="float:right;",
                    **{"_data-recalc-dims": "1"},
                ),
                _href=repo,
            )
        ),
        article(
            h1("domonic!", _class="titleStyle"),
            # h2(":)"),h3(":)"),h4(":)"),h5(":)"),h6(":)"),
            div("This webpage was created with ", a("domonic", _href=repo)),
            code("python3 -m pip install domonic"),
            # code("pip3 install domonic"),
            a(" go to the repo >>", _href=repo, _style="font-size:15px;"),
            br(),
            br(),
            nav("Nav:", a("Go back to here again", _href=""), "|", a("repo", _href=repo)),
            br(),
            img(_src="http://placekitten.com/400/400", _alt="some text", _title="some text"),
            br(),
            ol("".join([f'{li("some item")}' for thing in range(5)])),
            table(
                tr(th("A"), th("B"), th("C")),
                tr(td("test"), td("test"), td("test")),
                tr(td("test"), td("test"), td("test")),
                _style="width:100%",
            ),
            span("spaf", _style="color:fuchsia"),
        ),
        section(
            figure(
                img(_src="http://placekitten.com/200/200", _alt="some text", _title="some text"),
                br(),
            ),
            figcaption("a cat"),
            br(),
            dl(dt("coffee"), dd("hot drink"), dt("milk"), dd("cold drink")),
            form(
                label("this is a label:", _for="some_input"),
                br(),
                input(_id="some_input", _name="some_input", _type="text", _placeholder="cool"),
                br(),
                input(" yer or no?", _type="radio"),
                br(),
                input(_value="send", _type="button"),
                comment("This webpage was created with 'domonic'"),
            ),
        ),
        iframe("test", _data_test="test", _src="https://www.google.com"),
        noscript("Your browser does not support javascript"),
        footer(
            address("Where: Earth"),
            select(option("test1", _value="test1"), option("test2", _value="test2"), option("test3", _value="test3")),
            button("cool button"),
            sup("sup!"),
            sub("sub!"),
            textarea("test"),
            details(summary(small("domonic 2020."))),
        ),
        p(var("a"), "(", var("b"), "+", var("c"), ")=", var("ab"), "+", var("ac")),
        tbody("test"),
        thead("test"),
        tfoot("test"),
        aside("test"),
        hgroup("test"),
        pre("test"),
        em("test"),
        s("test"),
        cite("test"),
        q("test"),
        dfn("test"),
        abbr("test"),
        var("test"),
        samp("test"),
        kbd("test"),
        i("test"),
        b("test"),
        u("test"),
        mark("test"),
        ruby("test"),
        rt("test"),
        rp("test"),
        bdi("test"),
        bdo("test"),
        ins("test"),
        video("test"),
        audio("test"),
        canvas("test"),
        caption("test"),
        colgroup("test"),
        fieldset("test"),
        legend("test"),
        datalist("test"),
        optgroup("test"),
        option("test"),
        output("test"),  # shite -----
        progress("test"),
        meter("test"),
        menu("test"),
        font("test", **{"_data-test": "test"}),
        # map("test"),
        # del("test"),
        # object("test"),
        # time("test"),
    ),
    _lang="",
)


# def dom_console_log_test():
#     mydom = dom.document(output)
#     mydom.console.log("test")


# print( "output.baseURI:", output.baseURI )
# print( "output.body:", output.body )
# print( "output.forms:", output.forms )
# print( "output.images:", output.images )
# print( "output.scripts:", output.scripts )
# print( "output.title:", output.title )
print("output._get_tags:", output._get_tags("li"))
print("output._get_tags:", output._get_tags("input"))
print("output._get_tags:", output._get_tags("div"))
print("output._get_tags:", output._get_tags("style"))


# TODO - add some methods to do cool stuff

# print(output[0])

# for each in output:
#   print(each)

# print(output.content)
# print(output.attributes)

# print(output.args)
# print(output.kwargs)

# print(output.args[1].args[1].args[0])

# print(output.content[1].content[1].content[0])
# print(output.content[1].content[2].attributes[0])

print(render(output))

# TODO - prettify by using newlines in returned content to save installing this?
# from html5print import HTMLBeautifier
# render(HTMLBeautifier.beautify(render(output), 4), 'index.html')
