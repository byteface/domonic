from domonic.ext.tl_ import _extract_leading_doctype


def test_extract_leading_doctype_after_comments():
    source = '<!--before--><!DOCTYPE html PUBLIC "a>public" "b>system"><p>x</p>'
    assert _extract_leading_doctype(source) == (
        '<!DOCTYPE html PUBLIC "a>public" "b>system">',
        len("<!--before-->"),
        len('<!--before--><!DOCTYPE html PUBLIC "a>public" "b>system">'),
    )


def test_extract_leading_doctype_ignores_near_miss_after_many_comments():
    source = "<!-- -->" * 200 + "<!doctypish html><p>x</p>"
    assert _extract_leading_doctype(source) is None
