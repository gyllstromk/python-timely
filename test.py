from stopwatch import now, seconds_since, seconds, Blocker, Stopwatch

import datetime
import time
import unittest


class TestCase(unittest.TestCase):
    def assert_duration(self, minimum, duration, maximum, stretch=0):
        minimum -= stretch * minimum
        maximum += stretch * maximum

        self.assertTrue(duration >= minimum)
        self.assertTrue(duration <= maximum)

    def test_seconds(self):
        self.assertEqual(seconds(datetime.timedelta(3)), 259200)
        self.assertEqual(seconds(datetime.timedelta(hours=3)), 10800)

    def test_stopwatch(self):
        wait_time = 0.5

        start = now()
        with Stopwatch() as s:
            s.tick()
            time.sleep(wait_time)
            s.tick()

        self.assertTrue(s >= wait_time)
        self.assert_duration(0, seconds(s.ticks()[0] - start), 0.1)
        self.assert_duration(.4, seconds(s.ticks()[1] - s.ticks()[0]), 0.6)

    def test_blocker(self):
        for wait_for in (.1, .5, 1):
            portion = .2 * wait_for

            with Blocker(wait_for):
                time.sleep(portion)
                this_time = now()

            self.assert_duration(wait_for - portion,
                    seconds(now() - this_time), wait_for, .5)

        this_time = now()
        with Blocker(this_time + datetime.timedelta(seconds=1)):
            pass

        s = seconds_since(this_time)
        self.assertTrue(.95 <= s)
        self.assertTrue(s <= 1.05)

if __name__ == '__main__':
    unittest.main()
