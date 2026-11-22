"""
test_html_media
~~~~~~~~~~~~~~~

<audio> and <video> as HTMLMediaElements (https://html.spec.whatwg.org/#media-elements).
"""

import math
import unittest

from domonic.dom import DOMException, HTMLMediaElement
from domonic.html import audio, video


class TestMediaElements(unittest.TestCase):
    def test_audio_and_video_are_media_elements(self):
        self.assertIsInstance(audio(), HTMLMediaElement)
        self.assertIsInstance(video(), HTMLMediaElement)
        self.assertTrue(callable(video().play))

    def test_initial_state(self):
        clip = video()
        self.assertTrue(clip.paused)
        self.assertFalse(clip.ended)
        self.assertEqual(clip.currentTime, 0)
        self.assertTrue(math.isnan(clip.duration))
        self.assertEqual((clip.volume, clip.playbackRate, clip.defaultPlaybackRate), (1, 1, 1))
        self.assertEqual((clip.readyState, clip.networkState), (clip.HAVE_NOTHING, clip.NETWORK_EMPTY))
        self.assertEqual((clip.currentSrc, clip.videoWidth, clip.videoHeight), ("", 0, 0))
        self.assertEqual(len(clip.buffered), 0)
        self.assertIsNone(clip.error)

    def test_reflected_attributes(self):
        clip = video(_src="m.mp4", _poster="p.png", _width="640", _loop="", _playsinline="")
        self.assertEqual((clip.src, clip.poster, clip.width), ("m.mp4", "p.png", 640))
        self.assertTrue(clip.loop and clip.playsInline)
        self.assertFalse(clip.autoplay or clip.controls)
        self.assertEqual(clip.preload, "metadata")
        self.assertEqual(audio(_preload="").preload, "auto")
        clip.controls = True
        self.assertTrue(clip.hasAttribute("controls"))

    def test_play_and_pause(self):
        clip = audio()
        events = []
        for name in ("play", "playing", "pause", "timeupdate"):
            clip.addEventListener(name, lambda event, name=name: events.append(name))
        promise = clip.play()
        self.assertEqual(promise.state, "fulfilled")
        self.assertFalse(clip.paused)
        clip.play()  # already playing: no events
        clip.pause()
        clip.pause()  # already paused: no events
        self.assertTrue(clip.paused)
        self.assertEqual(events, ["play", "playing", "timeupdate", "pause"])

    def test_load_resets_playback(self):
        clip = audio(_src="song.mp3")
        clip.play()
        clip.currentTime = 12
        clip.load()
        self.assertTrue(clip.paused)
        self.assertEqual(clip.currentTime, 0)
        self.assertEqual(clip.currentSrc, "song.mp3")
        self.assertEqual(clip.readyState, clip.HAVE_CURRENT_DATA)

    def test_muted_starts_from_the_attribute(self):
        clip = video(_muted="")
        self.assertTrue(clip.muted and clip.defaultMuted)
        clip.muted = False
        self.assertFalse(clip.muted)
        self.assertTrue(clip.hasAttribute("muted"))  # the attribute is the default only

    def test_volume(self):
        clip = audio()
        changes = []
        clip.addEventListener("volumechange", lambda event: changes.append(clip.volume))
        clip.volume = 0.25
        clip.volume = 0.25
        self.assertEqual(changes, [0.25])
        with self.assertRaises(DOMException) as caught:
            clip.volume = 1.5
        self.assertEqual(caught.exception.name, "IndexSizeError")

    def test_seeking(self):
        clip = video()
        clip.currentTime = 3.5
        self.assertEqual(clip.currentTime, 3.5)
        clip.fastSeek(1)
        self.assertEqual(clip.currentTime, 1)

    def test_can_play_type(self):
        self.assertEqual(audio().canPlayType("audio/mpeg"), "maybe")
        self.assertEqual(video().canPlayType('video/mp4; codecs="avc1.42E01E"'), "probably")
        self.assertEqual(video().canPlayType("video/x-unknown"), "")
        self.assertEqual(video().canPlayType(""), "")


if __name__ == "__main__":
    unittest.main()
