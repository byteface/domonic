"""
Generate the synthetic HTML fixtures used by ``scripts/benchmark_bs4.py``.

Run from the repo root::

    python scripts/make_bench_fixtures.py

The real-world fixture (``html_meaty_page.html``) is committed as-is and not
touched here. The generated fixtures are committed too so the benchmark is
reproducible without running this script, but regenerate them if you change the
shapes below.
"""

from __future__ import annotations

from pathlib import Path

BENCH_DIR = Path(__file__).resolve().parents[1] / "benchmarks"


def _wrap(title: str, body: str) -> str:
    return (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n"
        f"<meta charset=\"utf-8\">\n<title>{title}</title>\n"
        "</head>\n<body>\n" + body + "\n</body>\n</html>\n"
    )


def tiny() -> str:
    body = """
<header id="site-header">
  <nav class="primary-nav">
    <a href="/" class="nav-link">Home</a>
    <a href="/about" class="nav-link">About</a>
    <a href="/contact" class="nav-link" data-track="contact">Contact</a>
  </nav>
</header>
<main id="content">
  <article class="post" data-id="42">
    <h1>A Short Article</h1>
    <p class="lead">Intro paragraph with <a href="/x">one link</a> and <em>emphasis</em>.</p>
    <p>Second paragraph, <strong>bold</strong> and <a href="/y" rel="nofollow">another link</a>.</p>
    <ul class="tags">
      <li>alpha</li>
      <li>beta</li>
      <li>gamma</li>
    </ul>
  </article>
  <form action="/search" method="get">
    <input type="search" name="q" placeholder="Search" required>
    <button type="submit">Go</button>
  </form>
</main>
<footer id="site-footer">
  <p>&copy; 2024. <a href="/privacy">Privacy</a></p>
</footer>
"""
    return _wrap("Tiny Page", body)


def wide_flat(rows: int = 8000) -> str:
    items = "\n".join(
        f'  <li class="row {"even" if i % 2 == 0 else "odd"}" data-index="{i}">'
        f'<a href="/item/{i}" class="item-link">Item {i}</a>'
        f'<span class="meta">#{i}</span></li>'
        for i in range(rows)
    )
    body = f'<ul id="big-list" class="listing">\n{items}\n</ul>'
    return _wrap(f"Wide Flat ({rows} rows)", body)


def deep_nested(depth: int = 450) -> str:
    open_tags = "".join(
        f'<div class="level level-{i}" data-depth="{i}">' for i in range(depth)
    )
    close_tags = "</div>" * depth
    inner = (
        '<article id="needle"><h1>Deep Content</h1>'
        '<p class="lead">Text buried <a href="/deep">deep</a> in the tree.</p>'
        "</article>"
    )
    return _wrap(f"Deep Nested ({depth} levels)", open_tags + inner + close_tags)


def tables(count: int = 180, rows: int = 12, cols: int = 6) -> str:
    blocks = []
    for t in range(count):
        head = "".join(f"<th>Col {c}</th>" for c in range(cols))
        body_rows = []
        for r in range(rows):
            cells = "".join(
                f'<td class="cell r{r} c{c}">'
                f'<a href="/t/{t}/r/{r}/c/{c}">{t}-{r}-{c}</a></td>'
                for c in range(cols)
            )
            body_rows.append(f"<tr>{cells}</tr>")
        blocks.append(
            f'<section class="report" data-table="{t}">'
            f'<h2>Table {t}</h2>'
            f'<table class="data"><thead><tr>{head}</tr></thead>'
            f'<tbody>{"".join(body_rows)}</tbody></table></section>'
        )
    return _wrap(f"Tables ({count} tables)", "\n".join(blocks))


def broken() -> str:
    # Deliberately malformed: unclosed tags, mis-nested inline elements, stray
    # text, an attribute with a raw '>' , a bare '<' that is not a tag.
    body = """
<div id=main class=container>
  <p>Paragraph without a close
  <p>Another one <b>bold <i>and italic</b> still italic?</i>
  <ul>
    <li>one
    <li>two <a href="/z">link
    <li>three</a>
  </ul>
  <table>
    <tr><td>a<td>b
    <tr><td>c<td>d
  </table>
  <span data-json='{"k": "v>x", "n": 3}'>templated</span>
  5 < 3 is false &amp; 3 > 1 is true
  <img src="/pic.png" alt="pic without close"
  <section>trailing section never closed
"""
    return _wrap("Broken Markup", body)


def main() -> None:
    BENCH_DIR.mkdir(exist_ok=True)
    fixtures = {
        "html_tiny.html": tiny(),
        "html_wide_flat.html": wide_flat(),
        "html_deep_nested.html": deep_nested(),
        "html_tables.html": tables(),
        "html_broken.html": broken(),
    }
    for name, content in fixtures.items():
        path = BENCH_DIR / name
        path.write_text(content, encoding="utf-8")
        print(f"wrote {path.relative_to(BENCH_DIR.parent)}  ({len(content):,} bytes)")


if __name__ == "__main__":
    main()
