"""Grouped select_one must return the earliest descendant in document order."""

import pytest
from bs4 import BeautifulSoup

from domonic.bs4 import BeautifulSlop


@pytest.mark.parametrize('selector', [
    'ul, tbody, #content, body',
    '#later, #early',
    '.missing, .hit',
    '[data-label="a, b"], #later',
    'aside, footer',
    'section > p, #later',
    'p:last-child, #early',
])
def test_grouped_select_one_matches_bs4(selector):
    markup = ('<html><body><section><p id="early" class="hit" '
              'data-label="a, b">first</p><p id="later">last</p>'
              '</section></body></html>')
    expected = BeautifulSoup(markup, 'html.parser').select_one(selector)
    actual = BeautifulSlop(markup, 'html.parser').select_one(selector)
    assert (actual.name if actual is not None else None) == (
        expected.name if expected is not None else None)
    assert (actual.get('id') if actual is not None else None) == (
        expected.get('id') if expected is not None else None)


def test_grouped_select_one_excludes_context_and_siblings():
    soup = BeautifulSlop('<div id="outside"></div><section id="context">'
                         '<p id="inside"></p></section>', 'html.parser')
    context = soup.find('section')
    assert context.select_one('#outside, section') is None
    assert context.select_one('#outside, p').get('id') == 'inside'
