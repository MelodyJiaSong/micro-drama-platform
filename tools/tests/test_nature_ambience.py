import unittest

import numpy as np

from tools.post.nature_ambience import synthesize


class NatureAmbienceTests(unittest.TestCase):
    def test_reproducible_source_and_no_clipping(self):
        a, events = synthesize(3, 106, 16000)
        b, _ = synthesize(3, 106, 16000)
        self.assertTrue(np.array_equal(a, b))
        self.assertGreater(len(events), 0)
        self.assertLess(np.max(np.abs(a.astype(float))), 1000)

    def test_tail_drops_before_the_cut(self):
        signal, _ = synthesize(4, 106, 16000)
        body = signal[-36000:-4000].astype(float)
        tail = signal[-4000:].astype(float)
        drop = 20 * np.log10(np.sqrt(np.mean(body**2)) / np.sqrt(np.mean(tail**2)))
        self.assertGreater(drop, 12)
        self.assertLessEqual(np.max(np.abs(signal[-100:].astype(float))), 1)

    def test_no_bird_chirps_during_final_fade(self):
        _, events = synthesize(2, 106, 16000)
        self.assertEqual(events, [])


if __name__ == "__main__":
    unittest.main()
