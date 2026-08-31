import unittest

from domonic.animation import (
    Animation,
    AnimationPlaybackEvent,
    ComputedEffectTiming,
    EffectTiming,
    KeyframeEffect,
)
from domonic.dom import DocumentTimeline
from domonic.html import div


class TestCase(unittest.TestCase):
    def test_effect_timing_and_computed_effect_timing(self):
        timing = EffectTiming(
            duration=200, delay=50, iterations=2, fill="forwards", easing="ease-in"
        )
        effect = KeyframeEffect(
            div(), [{"opacity": 0, "offset": 0}, {"opacity": 1, "offset": 1}], timing
        )

        raw = effect.getTiming()
        computed = effect.getComputedTiming(150)

        self.assertEqual(raw.duration, 200)
        self.assertEqual(raw.delay, 50)
        self.assertEqual(raw.iterations, 2)
        self.assertIsInstance(computed, ComputedEffectTiming)
        self.assertEqual(computed.activeDuration, 400)
        self.assertEqual(computed.endTime, 450)
        self.assertIsNotNone(computed.progress)

    def test_keyframe_effect_applies_interpolated_style_values(self):
        target = div()
        effect = KeyframeEffect(
            target,
            [
                {"offset": 0, "opacity": 0, "width": "100px"},
                {"offset": 1, "opacity": 1, "width": "200px"},
            ],
            {"duration": 1000, "fill": "forwards"},
        )

        effect.apply(500)

        self.assertEqual(target.style.width, "150px")
        self.assertAlmostEqual(float(target.style.opacity), 0.5)

    def test_animation_and_element_animate_surface(self):
        target = div()
        animation = target.animate(
            [{"offset": 0, "opacity": 0}, {"offset": 1, "opacity": 1}],
            {"duration": 1000, "fill": "forwards"},
        )

        self.assertIsInstance(animation, Animation)
        self.assertIsInstance(animation.timeline, DocumentTimeline)
        self.assertEqual(animation.playState, "running")

        animation.currentTime = 250
        self.assertAlmostEqual(float(target.style.opacity), 0.25)

        animation.updatePlaybackRate(2)
        self.assertEqual(animation.playbackRate, 2.0)

    def test_animation_finish_cancel_and_playback_events(self):
        target = div()
        effect = KeyframeEffect(
            target,
            [{"offset": 0, "opacity": 0}, {"offset": 1, "opacity": 1}],
            {"duration": 100},
        )
        animation = Animation(effect, DocumentTimeline())
        events = []

        animation.addEventListener(
            "finish", lambda event: events.append(("finish", event.currentTime))
        )
        animation.addEventListener(
            "cancel", lambda event: events.append(("cancel", event.currentTime))
        )

        animation.play()
        animation.finish()
        self.assertEqual(animation.playState, "finished")
        self.assertEqual(target.style.opacity, 1)
        self.assertIsInstance(AnimationPlaybackEvent("finish"), AnimationPlaybackEvent)

        animation.cancel()
        self.assertEqual(animation.playState, "idle")
        self.assertEqual(events[0][0], "finish")
        self.assertEqual(events[1], ("cancel", None))


if __name__ == "__main__":
    unittest.main()
