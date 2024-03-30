import datetime
import unittest
from typing import List, Tuple

from timerangeparser.parser import TimeRangeParser
from timerangeparser.types import TimeRange, WeekdaysRange, SingleTimeRange

from datetime import time


class ParserTest(unittest.TestCase):
    def assertParse_hourEnd(self, x: str, expected: List[TimeRange]) -> None:
        cfg = TimeRangeParser()
        cfg.hour_only_use_end = True
        t = cfg.parse(x)
        self.assertListEqual(expected, t.time_ranges)

    def assertParse_hourNotEnd(self, x: str, expected: List[TimeRange]) -> None:
        cfg = TimeRangeParser()
        cfg.hour_only_use_end = False
        t = cfg.parse(x)
        self.assertListEqual(expected, t.time_ranges)

    def assertParse_both(self, x: str, expected: List[TimeRange]) -> None:
        self.assertParse_hourEnd(x, expected)
        self.assertParse_hourNotEnd(x, expected)

    def test_empty(self) -> None:
        self.assertParse_both("", [])

    def test_whole_day(self) -> None:
        self.assertParse_hourEnd("0-0", [
            TimeRange(weekdays=WeekdaysRange(weekdays={0, 1, 2, 3, 4, 5, 6}),
                      ranges=[SingleTimeRange(start_time=time(0, 0), end_time=time(23, 59, 59))])
        ])

    def test_hour_only(self) -> None:
        self.assertParse_both("3", [
            TimeRange(weekdays=WeekdaysRange(weekdays={0, 1, 2, 3, 4, 5, 6}),
                      ranges=[SingleTimeRange(start_time=time(3, 0), end_time=time(3, 59, 59))])
        ])

    def test_minute_only(self) -> None:
        self.assertParse_both("3:15", [
            TimeRange(weekdays=WeekdaysRange(weekdays={0, 1, 2, 3, 4, 5, 6}),
                      ranges=[SingleTimeRange(start_time=time(3, 15), end_time=time(3, 15, 59))])
        ])

    def test_second_only(self) -> None:
        self.assertParse_both("3:15:45", [
            TimeRange(weekdays=WeekdaysRange(weekdays={0, 1, 2, 3, 4, 5, 6}),
                      ranges=[SingleTimeRange(start_time=time(3, 15, 45), end_time=time(3, 15, 45))])
        ])

    def test_hour_range_same(self) -> None:
        self.assertParse_hourEnd("3-3", [
            TimeRange(weekdays=WeekdaysRange(weekdays={0, 1, 2, 3, 4, 5, 6}),
                      ranges=[SingleTimeRange(start_time=time(3, 0), end_time=time(3, 59, 59))])
        ])

        self.assertParse_hourNotEnd("3-3", [
            TimeRange(weekdays=WeekdaysRange(weekdays={0, 1, 2, 3, 4, 5, 6}),
                      ranges=[
                          SingleTimeRange(start_time=time(3, 0), end_time=time(23, 59, 59)),
                          SingleTimeRange(start_time=time(0, 0), end_time=time(3, 0)),
                      ])
        ])

    def test_hour_range(self) -> None:
        self.assertParse_hourEnd("3-4", [
            TimeRange(weekdays=WeekdaysRange(weekdays={0, 1, 2, 3, 4, 5, 6}),
                      ranges=[SingleTimeRange(start_time=time(3, 0), end_time=time(4, 59, 59))])
        ])

        self.assertParse_hourNotEnd("3-4", [
            TimeRange(weekdays=WeekdaysRange(weekdays={0, 1, 2, 3, 4, 5, 6}),
                      ranges=[SingleTimeRange(start_time=time(3, 0), end_time=time(4, 0, 0))])
        ])

    def test_hour_range_cross_day(self) -> None:
        self.assertParse_hourEnd("3-1", [
            TimeRange(weekdays=WeekdaysRange(weekdays={0, 1, 2, 3, 4, 5, 6}),
                      ranges=[
                          SingleTimeRange(start_time=time(3, 0), end_time=time(23, 59, 59)),
                          SingleTimeRange(start_time=time(0, 0), end_time=time(1, 59, 59)),
                      ])
        ])

        self.assertParse_hourNotEnd("3-1", [
            TimeRange(weekdays=WeekdaysRange(weekdays={0, 1, 2, 3, 4, 5, 6}),
                      ranges=[
                          SingleTimeRange(start_time=time(3, 0), end_time=time(23, 59, 59)),
                          SingleTimeRange(start_time=time(0, 0), end_time=time(1, 0, 0)),
                      ])
        ])

    def test_hour_end_of_day(self) -> None:
        self.assertParse_hourEnd("3-0", [
            TimeRange(weekdays=WeekdaysRange(weekdays={0, 1, 2, 3, 4, 5, 6}),
                      ranges=[
                          SingleTimeRange(start_time=time(3, 0), end_time=time(23, 59, 59)),
                          SingleTimeRange(start_time=time(0, 0), end_time=time(0, 59, 59)),
                      ])
        ])

        self.assertParse_hourNotEnd("3-0", [
            TimeRange(weekdays=WeekdaysRange(weekdays={0, 1, 2, 3, 4, 5, 6}),
                      ranges=[
                          SingleTimeRange(start_time=time(3, 0), end_time=time(23, 59, 59)),
                      ])
        ])

        self.assertParse_both("3-24", [
            TimeRange(weekdays=WeekdaysRange(weekdays={0, 1, 2, 3, 4, 5, 6}),
                      ranges=[
                          SingleTimeRange(start_time=time(3, 0), end_time=time(23, 59, 59)),
                      ])
        ])

    def test_weekday_only(self) -> None:
        self.assertParse_both("tue@", [
            TimeRange(weekdays=WeekdaysRange(weekdays={1}),
                      ranges=[SingleTimeRange(start_time=time(0, 0), end_time=time(23, 59, 59))])
        ])

    def test_weekday_same(self) -> None:
        self.assertParse_both("tue-tue@", [
            TimeRange(weekdays=WeekdaysRange(weekdays={0, 1, 2, 3, 4, 5, 6}),
                      ranges=[SingleTimeRange(start_time=time(0, 0), end_time=time(23, 59, 59))])
        ])

    def test_weekday_range(self) -> None:
        self.assertParse_both("tue-wed@", [
            TimeRange(weekdays=WeekdaysRange(weekdays={1, 2}),
                      ranges=[SingleTimeRange(start_time=time(0, 0), end_time=time(23, 59, 59))])
        ])

    def test_weekday_range_cross_week(self) -> None:
        self.assertParse_both("fri-mon@", [
            TimeRange(weekdays=WeekdaysRange(weekdays={0, 4, 5, 6}),
                      ranges=[SingleTimeRange(start_time=time(0, 0), end_time=time(23, 59, 59))])
        ])

    def test_multiple_hours(self) -> None:
        self.assertParse_hourEnd("2-5,10-12,15", [
            TimeRange(weekdays=WeekdaysRange(weekdays={0, 1, 2, 3, 4, 5, 6}),
                      ranges=[
                          SingleTimeRange(start_time=time(2, 0), end_time=time(5, 59, 59)),
                          SingleTimeRange(start_time=time(10, 0), end_time=time(12, 59, 59)),
                          SingleTimeRange(start_time=time(15, 0), end_time=time(15, 59, 59)),
                      ])
        ])

        self.assertParse_hourNotEnd("2-5,10-12,15", [
            TimeRange(weekdays=WeekdaysRange(weekdays={0, 1, 2, 3, 4, 5, 6}),
                      ranges=[
                          SingleTimeRange(start_time=time(2, 0), end_time=time(5, 0, 0)),
                          SingleTimeRange(start_time=time(10, 0), end_time=time(12, 0, 0)),
                          SingleTimeRange(start_time=time(15, 0), end_time=time(15, 59, 59)),
                      ])
        ])

    def test_multiple_weekdays(self) -> None:
        self.assertParse_hourEnd("tue-wed@2-5,10-12,15", [
            TimeRange(weekdays=WeekdaysRange(weekdays={1, 2}),
                      ranges=[
                          SingleTimeRange(start_time=time(2, 0), end_time=time(5, 59, 59)),
                          SingleTimeRange(start_time=time(10, 0), end_time=time(12, 59, 59)),
                          SingleTimeRange(start_time=time(15, 0), end_time=time(15, 59, 59)),
                      ])
        ])

        self.assertParse_hourNotEnd("tue-wed@2-5,10-12,15", [
            TimeRange(weekdays=WeekdaysRange(weekdays={1, 2}),
                      ranges=[
                          SingleTimeRange(start_time=time(2, 0), end_time=time(5, 0, 0)),
                          SingleTimeRange(start_time=time(10, 0), end_time=time(12, 0, 0)),
                          SingleTimeRange(start_time=time(15, 0), end_time=time(15, 59, 59)),
                      ])
        ])

    def test_minutes(self) -> None:
        self.assertParse_hourEnd("1:05-2:00", [
            TimeRange(weekdays=WeekdaysRange(weekdays={0, 1, 2, 3, 4, 5, 6}),
                      ranges=[
                          SingleTimeRange(start_time=time(1, 5), end_time=time(2, 0, 59)),
                      ])
        ])

        self.assertParse_hourNotEnd("1:05-2:00", [
            TimeRange(weekdays=WeekdaysRange(weekdays={0, 1, 2, 3, 4, 5, 6}),
                      ranges=[
                          SingleTimeRange(start_time=time(1, 5), end_time=time(2, 0, 0)),
                      ])
        ])

    def test_seconds(self) -> None:
        self.assertParse_both("1:05-2:00:00", [
            TimeRange(weekdays=WeekdaysRange(weekdays={0, 1, 2, 3, 4, 5, 6}),
                      ranges=[
                          SingleTimeRange(start_time=time(1, 5), end_time=time(2, 0, 0)),
                      ])
        ])

    def test_multiple_entries(self) -> None:
        self.assertParse_hourEnd("2|3|4", [
            TimeRange(weekdays=WeekdaysRange(weekdays={0, 1, 2, 3, 4, 5, 6}),
                      ranges=[SingleTimeRange(start_time=time(2, 0), end_time=time(2, 59, 59))]),
            TimeRange(weekdays=WeekdaysRange(weekdays={0, 1, 2, 3, 4, 5, 6}),
                      ranges=[SingleTimeRange(start_time=time(3, 0), end_time=time(3, 59, 59))]),
            TimeRange(weekdays=WeekdaysRange(weekdays={0, 1, 2, 3, 4, 5, 6}),
                      ranges=[SingleTimeRange(start_time=time(4, 0), end_time=time(4, 59, 59))]),
        ])

    def test_check(self) -> None:
        cfg = TimeRangeParser()
        t = cfg.parse("2-3")
        self.assertFalse(t.check(datetime.datetime(2020, 1, 1, 1, 0, 0)))
        self.assertTrue(t.check(datetime.datetime(2020, 1, 1, 2, 0, 0)))
        self.assertTrue(t.check(datetime.datetime(2020, 1, 1, 3, 0, 0)))
        self.assertFalse(t.check(datetime.datetime(2020, 1, 1, 4, 0, 0)))

    def test_end_day(self) -> None:
        self.assertParse_both("2-24", [
            TimeRange(weekdays=WeekdaysRange(weekdays={0, 1, 2, 3, 4, 5, 6}),
                      ranges=[SingleTimeRange(start_time=time(2, 0), end_time=time(23, 59, 59))]),
        ])

    def test_notend(self) -> None:
        self.assertParse_hourNotEnd("2-3", [
            TimeRange(weekdays=WeekdaysRange(weekdays={0, 1, 2, 3, 4, 5, 6}),
                      ranges=[SingleTimeRange(start_time=time(2, 0), end_time=time(3, 0, 0))])
        ])

    def test_action(self) -> None:
        self.assertParse_hourEnd("mon@10-15|tue@2=ON", [
            TimeRange(weekdays=WeekdaysRange(weekdays={0}),
                      ranges=[
                          SingleTimeRange(start_time=time(10, 0), end_time=time(15, 59, 59)),
                      ],
                      action="ON"),
            TimeRange(weekdays=WeekdaysRange(weekdays={1}),
                      ranges=[
                          SingleTimeRange(start_time=time(2, 0), end_time=time(2, 59, 59)),
                      ],
                      action="ON")
        ])

    def test_get_action(self) -> None:
        cfg = TimeRangeParser()
        cfg.hour_only_use_end = False
        t = cfg.parse("1-2=VAL1\n5-6=VAL2")

        action = t.get_action(datetime.datetime(2024, 1, 1, 0, 30), "default")
        self.assertEqual("default", action)

        action = t.get_action(datetime.datetime(2024, 1, 1, 1, 30), "default")
        self.assertEqual("VAL1", action)

        action = t.get_action(datetime.datetime(2024, 1, 1, 5, 30), "default")
        self.assertEqual("VAL2", action)

    def test_multiline(self) -> None:
        cfg = TimeRangeParser()
        cfg.hour_only_use_end = False
        t = cfg.parse("1-2=VAL1\n5-6=VAL2")

        self.assertListEqual([
            TimeRange(weekdays=WeekdaysRange(weekdays={0, 1, 2, 3, 4, 5, 6}),
                      ranges=[
                          SingleTimeRange(start_time=time(1, 0), end_time=time(2, 0)),
                      ],
                      action="VAL1"),
            TimeRange(weekdays=WeekdaysRange(weekdays={0, 1, 2, 3, 4, 5, 6}),
                      ranges=[
                          SingleTimeRange(start_time=time(5, 0), end_time=time(6, 0)),
                      ],
                      action="VAL2"),
        ], t.time_ranges)

    def test_comment(self) -> None:
        cfg = TimeRangeParser()
        cfg.hour_only_use_end = False
        t = cfg.parse("""
# comment
# 1-2=VAL1
5
""")

        self.assertListEqual([
            TimeRange(weekdays=WeekdaysRange(weekdays={0, 1, 2, 3, 4, 5, 6}),
                      ranges=[SingleTimeRange(start_time=time(5, 0), end_time=time(5, 59, 59))])
        ], t.time_ranges)

    def test_pretty(self) -> None:
        cfg = TimeRangeParser()
        cfg.hour_only_use_end = False
        t = cfg.parse("1-2\nmon@1,2,3|8")

        self.assertEqual("""
TimeRangeCollection:
  mon,tue,wed,thu,fri,sat,sun - 01:00:00 - 02:00:00
  mon - 01:00:00 - 01:59:59 | 02:00:00 - 02:59:59 | 03:00:00 - 03:59:59
  mon,tue,wed,thu,fri,sat,sun - 08:00:00 - 08:59:59
""".strip(), t.pretty())
