import unittest

from shadow_eval.stats import wilson_interval


class WilsonIntervalTest(unittest.TestCase):
    def test_half_of_ten_matches_known_value(self):
        low, high = wilson_interval(5, 10)
        self.assertAlmostEqual(low, 0.2366, places=4)
        self.assertAlmostEqual(high, 0.7634, places=4)

    def test_half_of_one_hundred_matches_known_value(self):
        low, high = wilson_interval(50, 100)
        self.assertAlmostEqual(low, 0.4038, places=4)
        self.assertAlmostEqual(high, 0.5962, places=4)

    def test_eight_of_ten_matches_known_value(self):
        low, high = wilson_interval(8, 10)
        self.assertAlmostEqual(low, 0.4902, places=4)
        self.assertAlmostEqual(high, 0.9433, places=4)

    def test_zero_successes_gives_lower_bound_zero(self):
        low, high = wilson_interval(0, 10)
        self.assertAlmostEqual(low, 0.0, places=6)
        self.assertAlmostEqual(high, 0.2775, places=4)

    def test_all_successes_gives_upper_bound_one(self):
        low, high = wilson_interval(10, 10)
        self.assertAlmostEqual(low, 0.7225, places=4)
        self.assertAlmostEqual(high, 1.0, places=6)

    def test_zero_trials_raises(self):
        with self.assertRaises(ValueError):
            wilson_interval(0, 0)

    def test_successes_outside_range_raise(self):
        with self.assertRaises(ValueError):
            wilson_interval(-1, 10)
        with self.assertRaises(ValueError):
            wilson_interval(11, 10)
