"""
ValidityState example
=====================

Use domonic's constraint-validation helpers to inspect why controls fail.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from domonic.dom import ValidityState
from domonic.html import form, input


def build_form():
    return form(
        input(
            _type="email",
            _name="email",
            _required=True,
            _value="not-an-email",
        ),
        input(
            _type="number",
            _name="tickets",
            _min="1",
            _max="10",
            _step="2",
            _value="12",
        ),
    )


if __name__ == "__main__":
    signup = build_form()
    email = signup.elements.namedItem("email")
    tickets = signup.elements.namedItem("tickets")

    print(isinstance(email.validity, ValidityState))
    print(email.validity.typeMismatch)
    print(tickets.validity.rangeOverflow)
    print(tickets.validationMessage)

    email.setCustomValidity("Use a work email address.")
    print(email.validity.customError)
    print(email.validationMessage)
    print(signup.checkValidity())
