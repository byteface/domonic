"""Insertion must refresh descendants and preserve lifecycle transitions."""

from domonic.dom import Document
from domonic.html import div, span


def test_append_ownership_and_callbacks_across_document_transitions():
    events = []

    class TrackedSpan(span):
        def adoptedCallback(self, old, new):
            events.append(('adopted', old, new))

        def connectedCallback(self):
            events.append(('connected',))

        def disconnectedCallback(self):
            events.append(('disconnected',))

    first, second = Document(), Document()
    left, right, elsewhere = div(), div(), div()
    first.appendChild(left)
    first.appendChild(right)
    second.appendChild(elsewhere)
    leaf = TrackedSpan()
    subtree = div(leaf)

    left.append(subtree)
    assert events == [('connected',)]
    assert leaf.ownerDocument is first
    assert leaf.isConnected

    events.clear()
    right.append(subtree)
    assert events == [('disconnected',), ('connected',)]
    assert leaf.ownerDocument is first

    events.clear()
    elsewhere.append(subtree)
    assert events == [('disconnected',), ('adopted', first, second), ('connected',)]
    assert leaf.ownerDocument is second
    assert leaf.parentNode is subtree

    events.clear()
    detached = div()
    detached.append(subtree)
    assert events == [('disconnected',), ('adopted', second, None)]
    assert leaf.ownerDocument is None
    assert not leaf.isConnected
