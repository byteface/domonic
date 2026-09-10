"""Ported from wpt/dom/abort/abort-signal-any.any.js, AbortSignal.any.js and
the AbortSignal.abort() / .timeout() checks in wpt/dom/abort/event.any.js.
https://dom.spec.whatwg.org/#interface-AbortSignal

``AbortSignal.timeout()`` runs its timer on a daemon thread; the test waits
for it rather than driving an event loop.
"""

import time
import unittest

from domonic.events import AbortController, AbortSignal


class AbortSignalAbort(unittest.TestCase):
    def test_returns_an_already_aborted_signal(self):
        signal = AbortSignal.abort()
        self.assertTrue(signal.aborted)

    def test_default_reason_is_an_abort_error(self):
        signal = AbortSignal.abort()
        self.assertEqual(getattr(signal.reason, "name", None), "AbortError")

    def test_explicit_reason_is_kept(self):
        signal = AbortSignal.abort("custom")
        self.assertEqual(signal.reason, "custom")

    def test_throwIfAborted_raises_the_reason(self):
        signal = AbortSignal.abort()
        with self.assertRaises(Exception) as ctx:
            signal.throwIfAborted()
        self.assertEqual(getattr(ctx.exception, "name", None), "AbortError")

    def test_throwIfAborted_is_a_noop_when_not_aborted(self):
        AbortController().signal.throwIfAborted()  # must not raise


class AbortSignalAny(unittest.TestCase):
    def test_aborts_when_a_source_aborts_and_adopts_its_reason(self):
        c1 = AbortController()
        c2 = AbortController()
        combined = AbortSignal.any([c1.signal, c2.signal])
        self.assertFalse(combined.aborted)

        c2.abort("second")
        self.assertTrue(combined.aborted)
        self.assertEqual(combined.reason, "second")

    def test_is_already_aborted_when_a_source_is_already_aborted(self):
        pre = AbortSignal.abort("pre")
        combined = AbortSignal.any([pre, AbortController().signal])
        self.assertTrue(combined.aborted)
        self.assertEqual(combined.reason, "pre")

    def test_fires_an_abort_event(self):
        c = AbortController()
        combined = AbortSignal.any([c.signal])
        seen = []
        combined.addEventListener("abort", lambda e: seen.append(e.type))
        c.abort()
        self.assertEqual(seen, ["abort"])

    def test_only_the_first_source_to_abort_wins(self):
        c1 = AbortController()
        c2 = AbortController()
        combined = AbortSignal.any([c1.signal, c2.signal])
        c1.abort("first")
        c2.abort("second")
        self.assertEqual(combined.reason, "first")


class AbortSignalTimeout(unittest.TestCase):
    def test_aborts_with_a_timeout_error_after_the_delay(self):
        signal = AbortSignal.timeout(30)
        self.assertFalse(signal.aborted)
        time.sleep(0.1)
        self.assertTrue(signal.aborted)
        self.assertEqual(getattr(signal.reason, "name", None), "TimeoutError")


if __name__ == "__main__":
    unittest.main()
