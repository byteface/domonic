"""Observer regressions, including overlapping registrations salvaged from PR #68.

7HR4IZ3's interestedObservers algorithm combines old-value requests across
registrations: https://github.com/byteface/domonic/pull/68.
"""

import gc
import weakref

import pytest

from domonic.dom import MutationObserver, Text
from domonic.html import div, span


@pytest.fixture
def observer():
    records = []
    instance = MutationObserver(lambda batch, obs: records.extend(batch))
    yield instance, records
    instance.disconnect()


@pytest.mark.parametrize("kind", ["attributes", "characterData"])
@pytest.mark.parametrize("ancestor_first", [True, False])
@pytest.mark.parametrize("old_value_on_ancestor", [True, False])
def test_overlapping_observations_preserve_old_value(
    observer, kind, ancestor_first, old_value_on_ancestor
):
    """PR #68: one record, with oldValue from either matching registration."""
    instance, records = observer
    child = span(_id="before") if kind == "attributes" else Text("before")
    parent = div(child)
    old_option = (
        "attributeOldValue" if kind == "attributes" else "characterDataOldValue"
    )
    registrations = [
        (parent, {kind: True, "subtree": True, old_option: old_value_on_ancestor}),
        (child, {kind: True, old_option: not old_value_on_ancestor}),
    ]
    for target, options in registrations if ancestor_first else reversed(registrations):
        instance.observe(target, options)
    if kind == "attributes":
        child.setAttribute("id", "after")
    else:
        child.data = "after"
    assert len(records) == 1
    assert records[0].target is child
    assert records[0].type == kind
    assert records[0].oldValue == "before"


@pytest.mark.parametrize(
    "ancestor_options",
    [
        {"attributes": True, "attributeOldValue": True},
        {
            "attributes": True,
            "subtree": True,
            "attributeOldValue": True,
            "attributeFilter": ["class"],
        },
    ],
)
def test_nonmatching_ancestor_does_not_expose_old_value(observer, ancestor_options):
    instance, records = observer
    child = span(_id="before")
    parent = div(child)
    instance.observe(parent, ancestor_options)
    instance.observe(child, {"attributes": True})
    child.setAttribute("id", "after")
    assert len(records) == 1
    assert records[0].oldValue is None


@pytest.mark.parametrize(
    "options",
    [
        {},
        {"childList": True, "attributes": False, "attributeOldValue": True},
        {"childList": True, "attributes": False, "attributeFilter": []},
        {"childList": True, "characterData": False, "characterDataOldValue": True},
    ],
)
def test_invalid_options_preserve_existing_registration(observer, options):
    instance, records = observer
    target = div()
    instance.observe(target, {"attributes": True})
    with pytest.raises(TypeError):
        instance.observe(target, options)
    target.setAttribute("id", "still-observed")
    assert len(records) == 1


@pytest.mark.parametrize(
    "options",
    [
        {"attributeOldValue": False},
        {"attributeOldValue": True},
        {"attributeFilter": ["id"]},
        {"characterDataOldValue": False},
        {"characterDataOldValue": True},
    ],
)
def test_present_options_enable_omitted_mutation_type(observer, options):
    instance, records = observer
    character_data = "characterDataOldValue" in options
    target = Text("before") if character_data else div(_id="before")
    instance.observe(target, options)
    if character_data:
        target.data = "after"
    else:
        target.setAttribute("id", "after")
    assert len(records) == 1
    wants_old = options.get("attributeOldValue") or options.get("characterDataOldValue")
    assert records[0].oldValue == ("before" if wants_old else None)


def test_disconnect_releases_observer_and_allows_reuse(observer):
    instance, records = observer
    target = div()
    instance.observe(target, {"attributes": True})
    instance.disconnect()
    target.setAttribute("id", "ignored")
    assert records == []
    instance.observe(target, {"attributes": True})
    instance.observe(target, {"attributes": True})
    target.setAttribute("id", "observed")
    assert len(records) == 1


@pytest.mark.parametrize("observe_first", [False, True])
def test_inactive_observers_are_collectable(observe_first):
    instance = MutationObserver(lambda records, obs: None)
    if observe_first:
        instance.observe(div(), {"childList": True})
        instance.disconnect()
    reference = weakref.ref(instance)
    del instance
    gc.collect()
    assert reference() is None
