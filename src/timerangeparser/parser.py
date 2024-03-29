import datetime
import re
from typing import List, Set

from timerangeparser.types import WeekdaysRange, SingleTimeRange, TimeRange, TimeRangeCollection

StartOfDay = datetime.time(0, 0, 0)
EndOfDay = datetime.time(23, 59, 59)

StartOfWeek = 0
EndOfWeek = 6


def parse_time(x: str, adjust_to_end: bool) -> datetime.time:
    m = re.match("^(?P<hour>\d\d?)(?::(?P<minute>\d\d?)(?::(?P<second>\d\d?))?)?$", x)
    assert m is not None

    hour_str = m.group("hour")
    minute_str = m.group("minute")
    second_str = m.group("second")

    if minute_str is not None and second_str is not None:
        return datetime.time(int(hour_str), int(minute_str), int(second_str))
    elif minute_str is not None:
        if adjust_to_end:
            return datetime.time(int(hour_str), int(minute_str), 59)
        else:
            return datetime.time(int(hour_str), int(minute_str), 0)
    else:
        if hour_str == "24":
            return EndOfDay
        else:
            if adjust_to_end:
                return datetime.time(int(hour_str), 59, 59)
            else:
                return datetime.time(int(hour_str), 0, 0)


def gen_set(s: int, e: int) -> Set[int]:
    return set(range(s, e + 1))


class TimeRangeParser:
    def __init__(self) -> None:
        self.weekdays = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
        self.hour_only_use_end = True
        self.separator_entries = "|"
        self.separator_weekdays = "@"
        self.separator_ranges = ","
        self.separator_range = "-"
        self.separator_action = "="

    def _parse_weekdays_range(self, weekdays_str: str) -> WeekdaysRange:
        if len(weekdays_str) == 0:
            return WeekdaysRange(gen_set(StartOfWeek, EndOfWeek))

        p = weekdays_str.split(self.separator_range)
        assert len(p) <= 2

        if len(p) == 2:
            idx_s = self.weekdays.index(p[0].lower())
            idx_e = self.weekdays.index(p[1].lower())

            if idx_s < idx_e:
                return WeekdaysRange(gen_set(idx_s, idx_e))
            else:
                return WeekdaysRange(gen_set(idx_s, EndOfWeek) | gen_set(StartOfWeek, idx_e))

        else:
            idx = self.weekdays.index(p[0].lower())
            return WeekdaysRange({idx})

    def _parse_weekdays_ranges(self, weekdays_str: str) -> WeekdaysRange:
        weekdays_str_arr = weekdays_str.split(self.separator_ranges)
        return WeekdaysRange(
                {weekday for weekdays_str in weekdays_str_arr for weekday in self._parse_weekdays_range(weekdays_str).weekdays})

    def _parse_range(self, range_str: str) -> List[SingleTimeRange]:
        p = range_str.split(self.separator_range)
        assert len(p) <= 2

        if len(p) == 2:
            start_range = parse_time(p[0], False)
            end_range = parse_time(p[1], self.hour_only_use_end)
        else:
            if len(p[0]) == 0:
                start_range = StartOfDay
                end_range = EndOfDay
            else:
                start_range = parse_time(p[0], False)
                end_range = parse_time(p[0], True)

                if start_range == end_range:
                    # special case - all parts specified, return early
                    return [SingleTimeRange(start_range, end_range)]

        if start_range < end_range:
            return [SingleTimeRange(start_range, end_range)]
        else:
            return [SingleTimeRange(start_range, EndOfDay), SingleTimeRange(StartOfDay, end_range)]

    def _parse_ranges(self, ranges_str: str) -> List[SingleTimeRange]:
        ranges_str_arr = ranges_str.split(self.separator_ranges)
        return [range_ for range_str in ranges_str_arr for range_ in self._parse_range(range_str)]

    def _parse_entry(self, entry_str: str) -> TimeRange:
        if self.separator_weekdays in entry_str:
            weekdays_str, ranges_str = entry_str.split(self.separator_weekdays, 1)
        else:
            weekdays_str, ranges_str = "", entry_str

        weekdays = self._parse_weekdays_ranges(weekdays_str)
        ranges = self._parse_ranges(ranges_str)

        return TimeRange(weekdays, ranges)

    def parse(self, x: str) -> TimeRangeCollection:
        if self.separator_action in x:
            ranges_str, action_str = x.rsplit(self.separator_action, 1)
        else:
            ranges_str, action_str = x, None

        entries_str_arr = ranges_str.split(self.separator_entries)

        return TimeRangeCollection([self._parse_entry(part) for part in entries_str_arr], action_str)
