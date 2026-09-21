"""Tests for domonic.layout -- the CSS/layout boundary.

``layout_style()`` sits between the CSSOM cascade and a future layout engine:
it must resolve real lengths to px exactly as ``getComputedStyle`` does, but
leave percentages, ``auto``, and anything layout-dependent untouched. The
geometry hand-back (``set_layout_box``/``get_layout_box``) must leave every
existing ``Element`` geometry getter's fallback behaviour unchanged when no
layout engine has attached a box.
"""

import unittest

from domonic.dom import Document
from domonic.layout import (
    AUTO,
    Edges,
    Fr,
    Gap,
    GridLine,
    GridSpan,
    Keyword,
    Length,
    LayoutBox,
    Percent,
    Ratio,
    clear_layout_box,
    get_layout_box,
    layout_style,
    set_layout_box,
)

document = Document()


def _styled(css: str):
    el = document.createElement("div")
    el.setAttribute("style", css)
    return el


class LayoutStyleLengthsAndKeywords(unittest.TestCase):
    def test_px_length_resolves(self):
        self.assertEqual(layout_style(_styled("width: 200px")).width, Length(200.0))

    def test_layout_style_reuses_a_supplied_computed_style(self):
        # a caller that also needs the ComputedStyleDeclaration itself (for
        # something LayoutStyle excludes, e.g. paint-only colours) should be
        # able to resolve the cascade once and share it, via either the
        # layout_style(element, computed=...) parameter or the public
        # LayoutStyle.from_computed() classmethod directly.
        from domonic.layout import LayoutStyle
        from domonic.style import ComputedStyleDeclaration

        el = _styled("width: 100px; color: red")
        computed = ComputedStyleDeclaration(el)
        self.assertEqual(layout_style(el, computed=computed).width, Length(100.0))
        self.assertEqual(LayoutStyle.from_computed(computed).width, Length(100.0))

    def test_em_resolves_against_font_size(self):
        el = _styled("font-size: 20px; width: 2em")
        self.assertEqual(layout_style(el).width, Length(40.0))

    def test_ch_resolves_against_font_size(self):
        # Without a renderer-provided glyph-metrics resolver, CSS defines the
        # unavailable zero-glyph advance as 0.5em. This is the layout-facing
        # path consumed by downstream engines, not just getComputedStyle().
        self.assertEqual(layout_style(_styled("width: 20ch")).width, Length(160.0))
        self.assertEqual(
            layout_style(_styled("font-size: 20px; width: 10ch")).width,
            Length(100.0),
        )

    def test_percent_stays_symbolic(self):
        self.assertEqual(layout_style(_styled("width: 50%")).width, Percent(0.5))

    def test_auto_stays_auto(self):
        self.assertIs(layout_style(_styled("width: auto")).width, AUTO)

    def test_unset_width_is_the_initial_value_auto(self):
        self.assertIs(layout_style(_styled("")).width, AUTO)

    def test_max_width_none_is_a_keyword_not_auto(self):
        style = layout_style(_styled(""))
        self.assertEqual(style.maxWidth, Keyword("none"))
        self.assertIsNot(style.maxWidth, AUTO)

    def test_calc_of_plain_lengths_resolves(self):
        self.assertEqual(layout_style(_styled("width: calc(10px + 2em); font-size: 10px")).width, Length(30.0))

    def test_calc_mixing_in_a_percent_is_left_alone(self):
        style = layout_style(_styled("width: calc(100% - 20px)"))
        self.assertEqual(style.width, Keyword("calc(100% - 20px)"))

    def test_calc_referencing_a_custom_property_resolves(self):
        # Tailwind v4's spacing scale is exactly this shape
        # (calc(var(--spacing)*N)) on essentially every length value; the raw
        # cascaded string still has the var() reference in it here (unlike
        # getComputedStyle, which expands var() before it ever reaches a
        # calc() evaluator), so this needs the same expansion done first.
        style = layout_style(_styled("--spacing: 4px; height: calc(var(--spacing)*16)"))
        self.assertEqual(style.height, Length(64.0))

    def test_intrinsic_sizing_keyword_passes_through(self):
        self.assertEqual(layout_style(_styled("width: min-content")).width, Keyword("min-content"))


class LayoutStyleDisplayAndPosition(unittest.TestCase):
    def test_display_flex(self):
        self.assertEqual(layout_style(_styled("display: flex")).display, Keyword("flex"))

    def test_display_default_is_inline(self):
        self.assertEqual(layout_style(_styled("")).display, Keyword("inline"))

    def test_position_default_is_static(self):
        self.assertEqual(layout_style(_styled("")).position, Keyword("static"))

    def test_box_sizing(self):
        self.assertEqual(layout_style(_styled("box-sizing: border-box")).boxSizing, Keyword("border-box"))


class LayoutStyleEdges(unittest.TestCase):
    def test_margin_shorthand_expands_and_resolves(self):
        style = layout_style(_styled("margin: 10px 5% auto 0"))
        self.assertEqual(style.margin, Edges(Length(10.0), Percent(0.05), AUTO, Length(0.0)))

    def test_margin_default_is_zero_on_every_side(self):
        style = layout_style(_styled(""))
        self.assertEqual(style.margin, Edges(Length(0.0), Length(0.0), Length(0.0), Length(0.0)))

    def test_padding_never_reports_auto(self):
        # "auto" isn't valid CSS for padding; an author writing it anyway
        # should get a passthrough keyword, not a nonsensical AUTO.
        style = layout_style(_styled("padding-top: auto"))
        self.assertEqual(style.padding.top, Keyword("auto"))

    def test_border_width_keyword(self):
        # thin/medium/thick resolve to a real px length once a border-style
        # actually draws that side.
        style = layout_style(_styled("border-top-style: solid"))
        self.assertEqual(style.borderWidth.top, Length(3.0))

    def test_border_width_zero_when_style_none(self):
        # a side's used border-width is 0 whenever its border-style is
        # none/hidden, regardless of what border-width itself says -- an
        # unstyled element (border-style's initial value is "none") reports
        # 0, not the "medium" default width.
        style = layout_style(_styled(""))
        self.assertEqual(style.borderWidth.top, Length(0.0))

    def test_border_width_rejects_percent(self):
        style = layout_style(_styled("border-top-style: solid; border-top-width: 10%"))
        self.assertEqual(style.borderWidth.top, Keyword("10%"))

    def test_inset(self):
        style = layout_style(_styled("top: 1px; right: 2px; bottom: 3px; left: 4px"))
        self.assertEqual(style.inset, Edges(Length(1.0), Length(2.0), Length(3.0), Length(4.0)))


class LayoutStyleGap(unittest.TestCase):
    def test_gap_shorthand_splits_into_row_and_column(self):
        style = layout_style(_styled("gap: 8px 1em; font-size: 10px"))
        self.assertEqual(style.gap, Gap(Length(8.0), Length(10.0)))

    def test_gap_default_is_normal_keyword(self):
        style = layout_style(_styled(""))
        self.assertEqual(style.gap, Gap(Keyword("normal"), Keyword("normal")))


class LayoutStyleFlex(unittest.TestCase):
    def test_flex_shorthand_expands(self):
        style = layout_style(_styled("flex: 2 1 100px"))
        self.assertEqual(style.flexGrow, 2.0)
        self.assertEqual(style.flexShrink, 1.0)
        self.assertEqual(style.flexBasis, Length(100.0))

    def test_flex_grow_shrink_defaults(self):
        style = layout_style(_styled(""))
        self.assertEqual(style.flexGrow, 0.0)
        self.assertEqual(style.flexShrink, 1.0)

    def test_flex_direction_and_align(self):
        style = layout_style(_styled("flex-direction: row-reverse; align-items: center"))
        self.assertEqual(style.flexDirection, Keyword("row-reverse"))
        self.assertEqual(style.alignItems, Keyword("center"))


class LayoutStyleAspectRatio(unittest.TestCase):
    def test_ratio_syntax(self):
        self.assertEqual(layout_style(_styled("aspect-ratio: 16 / 9")).aspectRatio, Ratio(16.0, 9.0))

    def test_bare_number_is_ratio_to_one(self):
        self.assertEqual(layout_style(_styled("aspect-ratio: 1.5")).aspectRatio, Ratio(1.5, 1.0))

    def test_auto_and_unset_are_auto(self):
        self.assertIs(layout_style(_styled("aspect-ratio: auto")).aspectRatio, AUTO)
        self.assertIs(layout_style(_styled("")).aspectRatio, AUTO)


class LayoutStyleGrid(unittest.TestCase):
    def test_track_list_of_lengths_and_fr(self):
        style = layout_style(_styled("grid-template-columns: 1fr 2fr 100px"))
        self.assertEqual(style.gridTemplateColumns, [Fr(1.0), Fr(2.0), Length(100.0)])

    def test_none_is_an_empty_track_list(self):
        self.assertEqual(layout_style(_styled("")).gridTemplateColumns, [])

    def test_repeat_and_minmax_pass_through_unexpanded(self):
        style = layout_style(_styled("grid-template-columns: repeat(2, 1fr) minmax(10px, 1fr)"))
        self.assertEqual(style.gridTemplateColumns, [Keyword("repeat(2, 1fr)"), Keyword("minmax(10px, 1fr)")])

    def test_grid_column_shorthand_start_end(self):
        style = layout_style(_styled("grid-column: 2 / span 3"))
        self.assertEqual(style.gridColumnStart, GridLine(2))
        self.assertEqual(style.gridColumnEnd, GridSpan(3))

    def test_grid_line_auto_default(self):
        style = layout_style(_styled(""))
        self.assertIs(style.gridColumnStart, AUTO)

    def test_named_line_passes_through(self):
        style = layout_style(_styled("grid-column-start: sidebar-start"))
        self.assertEqual(style.gridColumnStart, Keyword("sidebar-start"))


class LayoutStyleWorksOnADetachedElement(unittest.TestCase):
    def test_no_parent_or_window_required(self):
        el = document.createElement("div")
        el.setAttribute("style", "width: 10px")
        self.assertIsNone(el.parentNode)
        self.assertEqual(layout_style(el).width, Length(10.0))


class GeometryHookFallsBackUnchanged(unittest.TestCase):
    """No layout engine attached -> the existing heuristics must be untouched."""

    def test_client_width_matches_pre_existing_heuristic(self):
        el = _styled("width: 100px; padding-left: 5px; padding-right: 5px")
        self.assertIsNone(get_layout_box(el))
        self.assertEqual(el.clientWidth, 110)

    def test_offset_width_matches_pre_existing_heuristic(self):
        el = _styled("width: 100px; border-left-width: 2px; border-right-width: 3px")
        self.assertEqual(el.offsetWidth(), 105)

    def test_bounding_rect_matches_pre_existing_heuristic(self):
        el = _styled("left: 10px; top: 20px; width: 100px")
        rect = el.getBoundingClientRect()
        self.assertEqual((rect.x, rect.y, rect.width), (10, 20, 100))


class GeometryHookUsesAnAttachedBox(unittest.TestCase):
    def setUp(self):
        self.el = document.createElement("div")
        self.box = LayoutBox(
            x=1, y=2, width=100, height=50, client_width=90, client_height=40, border_top=3, border_left=5
        )

    def tearDown(self):
        clear_layout_box(self.el)

    def test_set_and_get_layout_box(self):
        self.assertIsNone(get_layout_box(self.el))
        set_layout_box(self.el, self.box)
        self.assertIs(get_layout_box(self.el), self.box)

    def test_element_convenience_methods(self):
        self.el.set_layout_box(self.box)
        self.assertIs(self.el.get_layout_box(), self.box)

    def test_client_dimensions_come_from_the_box(self):
        set_layout_box(self.el, self.box)
        self.assertEqual(self.el.clientWidth, 90)
        self.assertEqual(self.el.clientHeight, 40)
        self.assertEqual(self.el.clientTop, 3)
        self.assertEqual(self.el.clientLeft, 5)

    def test_offset_dimensions_come_from_the_box(self):
        set_layout_box(self.el, self.box)
        self.assertEqual(self.el.offsetWidth(), 100)
        self.assertEqual(self.el.offsetHeight(), 50)
        self.assertEqual(self.el.offsetLeft(), 1)
        self.assertEqual(self.el.offsetTop(), 2)

    def test_bounding_rect_comes_from_the_box(self):
        set_layout_box(self.el, self.box)
        rect = self.el.getBoundingClientRect()
        self.assertEqual((rect.x, rect.y, rect.width, rect.height), (1, 2, 100, 50))

    def test_clear_layout_box_restores_the_fallback(self):
        self.el.setAttribute("style", "left: 7px; top: 8px")
        set_layout_box(self.el, self.box)
        clear_layout_box(self.el)
        self.assertIsNone(get_layout_box(self.el))
        rect = self.el.getBoundingClientRect()
        self.assertEqual((rect.x, rect.y), (7, 8))


if __name__ == "__main__":
    unittest.main()
