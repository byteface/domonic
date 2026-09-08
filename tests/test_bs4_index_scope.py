"""Root tag indexes must not broaden subtree searches."""

from domonic.bs4 import BeautifulSlop


def test_body_search_excludes_head_matches_with_warm_root_index():
    soup = BeautifulSlop(
        "<html><head><title>head</title></head><body><p>body</p></body></html>",
        "html.parser",
    )
    soup.find_all("title")
    body = soup.find("body")
    assert body.find_all("title") == []
    assert body.find_all("body") == []
    assert [p.text for p in body.find_all("p")] == ["body"]


def test_document_child_search_excludes_siblings_after_append():
    soup = BeautifulSlop(
        "<html><head></head><body><p>existing</p></body></html>", "html.parser"
    )
    head, body = soup.find("head"), soup.find("body")
    soup.find_all("p")
    tag = soup.new_tag("p")
    tag.string = "added"
    body.append(tag)
    assert head.find_all("p") == []
    assert [p.text for p in body.find_all("p")] == ["existing", "added"]
