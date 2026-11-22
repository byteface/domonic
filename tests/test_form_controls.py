"""
test_form_controls
~~~~~~~~~~~~~~~~~~

Form-control APIs: valueAsNumber / valueAsDate / stepUp / stepDown, the text
selection API, labels / label.control, fieldset.elements, <output>,
<progress> and <meter> (https://html.spec.whatwg.org/#forms).
"""

import datetime
import math
import unittest

from domonic.dom import DOMException
from domonic.html import (
    button,
    datalist,
    div,
    fieldset,
    form,
    input,
    label,
    meter,
    output,
    progress,
    select,
    textarea,
)


class TestValueAsNumber(unittest.TestCase):
    def test_number(self):
        self.assertEqual(input(_type="number", _value="2.5").valueAsNumber, 2.5)
        self.assertTrue(math.isnan(input(_type="number", _value="abc").valueAsNumber))
        self.assertTrue(math.isnan(input(_type="number").valueAsNumber))
        field = input(_type="number")
        field.valueAsNumber = 3
        self.assertEqual(field.value, "3")
        field.valueAsNumber = float("nan")
        self.assertEqual(field.value, "")

    def test_not_applicable(self):
        self.assertTrue(math.isnan(input().valueAsNumber))
        with self.assertRaises(DOMException) as caught:
            input().valueAsNumber = 1
        self.assertEqual(caught.exception.name, "InvalidStateError")
        with self.assertRaises(TypeError):
            input(_type="number").valueAsNumber = float("inf")

    def test_range_always_has_a_value(self):
        self.assertEqual(input(_type="range").valueAsNumber, 50)
        self.assertEqual(input(_type="range", _min="0", _max="5").valueAsNumber, 3)  # 2.5 snaps up to the step
        self.assertEqual(input(_type="range", _value="500").valueAsNumber, 100)
        self.assertEqual(input(_type="range", _min="10", _max="5").valueAsNumber, 10)

    def test_dates_and_times(self):
        self.assertEqual(input(_type="date", _value="1970-01-02").valueAsNumber, 86_400_000)
        self.assertEqual(input(_type="month", _value="1971-02").valueAsNumber, 13)
        self.assertEqual(input(_type="week", _value="1970-W01").valueAsNumber, -259_200_000)
        self.assertEqual(input(_type="time", _value="01:00:30.5").valueAsNumber, 3_630_500)
        self.assertEqual(input(_type="datetime-local", _value="1970-01-01T00:01").valueAsNumber, 60_000)
        self.assertTrue(math.isnan(input(_type="date", _value="2026-02-30").valueAsNumber))
        self.assertTrue(math.isnan(input(_type="week", _value="2025-W53").valueAsNumber))  # 2025 has 52 weeks

    def test_setting_dates_and_times(self):
        field = input(_type="time")
        field.valueAsNumber = 3_723_456
        self.assertEqual(field.value, "01:02:03.456")
        field.valueAsNumber = 60_000
        self.assertEqual(field.value, "00:01")
        field = input(_type="datetime-local")
        field.valueAsNumber = 0
        self.assertEqual(field.value, "1970-01-01T00:00")
        field = input(_type="week")
        field.valueAsNumber = 1_767_225_600_000  # 2026-01-01
        self.assertEqual(field.value, "2026-W01")


class TestValueAsDate(unittest.TestCase):
    def test_reads_a_date(self):
        found = input(_type="date", _value="2026-11-22").valueAsDate
        self.assertEqual(found.toISOString(), "2026-11-22T00:00:00.000Z")
        self.assertEqual(input(_type="month", _value="2026-11").valueAsDate.toISOString(), "2026-11-01T00:00:00.000Z")
        self.assertIsNone(input(_type="date").valueAsDate)
        self.assertIsNone(input(_type="number", _value="1").valueAsDate)
        self.assertIsNone(input(_type="datetime-local", _value="2026-01-01T00:00").valueAsDate)

    def test_accepts_python_dates(self):
        field = input(_type="date")
        field.valueAsDate = datetime.date(2024, 2, 29)
        self.assertEqual(field.value, "2024-02-29")
        field.valueAsDate = datetime.datetime(2024, 3, 1, 23, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=-2)))
        self.assertEqual(field.value, "2024-03-02")  # 01:00 UTC the next day
        field.valueAsDate = None
        self.assertEqual(field.value, "")
        month = input(_type="month")
        month.valueAsDate = datetime.date(2026, 11, 22)
        self.assertEqual(month.value, "2026-11")

    def test_accepts_a_js_date(self):
        from domonic.javascript import Date

        field = input(_type="date")
        field.valueAsDate = Date(0)
        self.assertEqual(field.value, "1970-01-01")

    def test_not_applicable(self):
        with self.assertRaises(DOMException):
            input(_type="number").valueAsDate = datetime.date.today()
        with self.assertRaises(TypeError):
            input(_type="date").valueAsDate = "2026-01-01"


class TestStepping(unittest.TestCase):
    def test_step_up_and_down(self):
        field = input(_type="number", _value="5")
        field.stepUp()
        self.assertEqual(field.value, "6")
        field.stepDown(3)
        self.assertEqual(field.value, "3")

    def test_decimal_steps_are_exact(self):
        field = input(_type="number", _value="0.1", _step="0.1")
        field.stepUp(2)
        self.assertEqual(field.value, "0.3")

    def test_snaps_to_the_step_and_clamps(self):
        field = input(_type="number", _min="1", _max="10", _step="2", _value="4")
        field.stepUp()  # 4 is off-step from base 1: snap to 5
        self.assertEqual(field.value, "5")
        field.stepUp(100)
        self.assertEqual(field.value, "9")  # largest on-step value <= max
        field.stepDown(100)
        self.assertEqual(field.value, "1")

    def test_empty_value_counts_as_zero(self):
        field = input(_type="number")
        field.stepDown()
        self.assertEqual(field.value, "-1")

    def test_does_not_step_the_wrong_way(self):
        field = input(_type="number", _max="3", _value="10")
        field.stepUp()  # clamping to max would go down: no change
        self.assertEqual(field.value, "10")

    def test_dates(self):
        day = input(_type="date", _value="2026-12-30")
        day.stepUp(3)
        self.assertEqual(day.value, "2027-01-02")
        month = input(_type="month", _value="2026-11")
        month.stepUp(3)
        self.assertEqual(month.value, "2027-02")
        week = input(_type="week", _value="2026-W01")
        week.stepDown()
        self.assertEqual(week.value, "2025-W52")
        clock = input(_type="time", _value="13:45")
        clock.stepUp()  # the default step is 60 seconds
        self.assertEqual(clock.value, "13:46")

    def test_errors(self):
        with self.assertRaises(DOMException) as caught:
            input().stepUp()
        self.assertEqual(caught.exception.name, "InvalidStateError")
        with self.assertRaises(DOMException):
            input(_type="number", _step="any").stepUp()

    def test_range_steps_from_its_default(self):
        field = input(_type="range")
        field.stepUp()
        self.assertEqual(field.value, "51")


class TestTextSelection(unittest.TestCase):
    def test_cursor_starts_at_the_end(self):
        field = input(_value="hello")
        self.assertEqual((field.selectionStart, field.selectionEnd, field.selectionDirection), (5, 5, "none"))

    def test_set_selection_range_clamps(self):
        field = input(_value="hello")
        field.setSelectionRange(3, 99, "backward")
        self.assertEqual((field.selectionStart, field.selectionEnd, field.selectionDirection), (3, 5, "backward"))
        field.setSelectionRange(4, 2)
        self.assertEqual((field.selectionStart, field.selectionEnd), (2, 2))

    def test_select_and_the_select_event(self):
        field = input(_value="hello")
        fired = []
        field.addEventListener("select", lambda event: fired.append(event.type))
        field.select()
        self.assertEqual((field.selectionStart, field.selectionEnd), (0, 5))
        self.assertEqual(fired, ["select"])

    def test_setting_value_moves_the_cursor_to_the_end(self):
        field = input(_value="hello")
        field.setSelectionRange(0, 2)
        field.value = "hi there"
        self.assertEqual((field.selectionStart, field.selectionEnd), (8, 8))

    def test_selection_start_and_end_setters(self):
        field = input(_value="hello")
        field.selectionStart = 1
        self.assertEqual((field.selectionStart, field.selectionEnd), (1, 5))
        field.selectionEnd = 3
        self.assertEqual((field.selectionStart, field.selectionEnd), (1, 3))

    def test_set_range_text(self):
        field = input(_value="hello world")
        field.setSelectionRange(0, 5)
        field.setRangeText("HELLO")
        self.assertEqual(field.value, "HELLO world")
        self.assertEqual((field.selectionStart, field.selectionEnd), (0, 5))
        field.setRangeText("there", 6, 11, "select")
        self.assertEqual(field.value, "HELLO there")
        self.assertEqual((field.selectionStart, field.selectionEnd), (6, 11))
        field.setRangeText("!", 11, 11, "end")
        self.assertEqual((field.value, field.selectionStart), ("HELLO there!", 12))
        with self.assertRaises(DOMException) as caught:
            field.setRangeText("x", 5, 2)
        self.assertEqual(caught.exception.name, "IndexSizeError")

    def test_types_without_a_selection(self):
        number = input(_type="number", _value="5")
        self.assertIsNone(number.selectionStart)
        number.select()  # allowed, does nothing
        with self.assertRaises(DOMException):
            number.setSelectionRange(0, 1)
        with self.assertRaises(DOMException):
            number.selectionStart = 0

    def test_textarea(self):
        area = textarea("abc")
        self.assertEqual((area.textLength, area.type, area.selectionEnd), (3, "textarea", 3))
        area.setSelectionRange(1, 2)
        area.setRangeText("XYZ", selectionMode="end")
        self.assertEqual((area.value, area.selectionStart), ("aXYZc", 4))


class TestLabels(unittest.TestCase):
    def setUp(self):
        self.page = form(
            label("Name ", input(_id="name", _name="name")),
            label("Again", _for="name"),
            label("Nothing", _for="missing"),
        )
        self.field = self.page.querySelector("#name")
        self.wrapping, self.pointing, self.dangling = self.page.querySelectorAll("label")

    def test_label_control(self):
        self.assertIs(self.wrapping.control, self.field)
        self.assertIs(self.pointing.control, self.field)
        self.assertIsNone(self.dangling.control)
        self.assertIs(self.pointing.form, self.page)
        self.assertIsNone(self.dangling.form)

    def test_control_labels_are_live(self):
        labels = self.field.labels
        self.assertEqual(list(labels), [self.wrapping, self.pointing])
        self.page.appendChild(label("Third", _for="name"))
        self.assertEqual(len(labels), 3)

    def test_labelable_elements(self):
        for control in (button(), select(), textarea(), output(), progress(), meter()):
            self.assertEqual(len(label(control).querySelector(control.localName).labels), 1, control.localName)
        self.assertIsNone(input(_type="hidden").labels)
        self.assertIsNone(label(input(_type="hidden")).control)


class TestOtherControls(unittest.TestCase):
    def test_input_list(self):
        page = div(datalist(_id="colours"), input(_list="colours"), input(_list="colours", _type="checkbox"))
        text, checkbox = page.querySelectorAll("input")
        self.assertIs(text.list, page.querySelector("datalist"))
        self.assertIsNone(checkbox.list)
        self.assertIsNone(input(_list="nowhere").list)

    def test_indeterminate(self):
        box = input(_type="checkbox")
        self.assertFalse(box.indeterminate)
        box.indeterminate = True
        self.assertFalse(box.hasAttribute("indeterminate"))
        box.click()
        self.assertFalse(box.indeterminate)

    def test_fieldset(self):
        group = fieldset(input(), div(textarea()), output())
        self.assertEqual([el.localName for el in group.elements], ["input", "textarea", "output"])
        self.assertEqual(group.type, "fieldset")

    def test_output(self):
        result = output("5", _name="sum")
        sheet = form(result)
        self.assertEqual((result.value, result.defaultValue, result.type), ("5", "5", "output"))
        result.value = "9"
        self.assertEqual((result.value, result.defaultValue), ("9", "5"))
        result.defaultValue = "6"
        sheet.reset()
        self.assertEqual(result.value, "6")

    def test_output_is_not_submitted(self):
        from domonic.dom import _construct_form_data

        sheet = form(input(_name="a", _value="1"), output("5", _name="sum"))
        self.assertEqual(_construct_form_data(sheet), {"a": "1"})

    def test_progress(self):
        bar = progress()
        self.assertEqual((bar.value, bar.max, bar.position), (0, 1, -1))
        bar = progress(_value="3", _max="2")
        self.assertEqual((bar.value, bar.position), (2, 1))
        bar.value = 0.5
        self.assertEqual(bar.getAttribute("value"), "0.5")
        self.assertEqual(progress(_max="0").max, 1)

    def test_meter(self):
        gauge = meter(_value="15", _min="0", _max="10")
        self.assertEqual((gauge.value, gauge.min, gauge.max), (10, 0, 10))
        self.assertEqual((gauge.low, gauge.high, gauge.optimum), (0, 10, 5))
        gauge = meter(_min="5", _max="1", _low="9", _high="2")
        self.assertEqual((gauge.max, gauge.low, gauge.high), (5, 5, 5))
        gauge.high = 4
        self.assertEqual(gauge.getAttribute("high"), "4")


if __name__ == "__main__":
    unittest.main()
