import calendar
import datetime
from dataclasses import dataclass
from typing import List, Set, Optional


@dataclass
class SingleTimeRange:
    start_time: datetime.time
    end_time: datetime.time

    def check(self, x: datetime.time) -> bool:
        return self.start_time <= datetime.time(x.hour, x.minute, x.second) <= self.end_time

    def pretty(self):
        s = f"{self.start_time.hour:02}:{str(self.start_time.minute):02}:{str(self.start_time.second):02}"
        e = f"{self.end_time.hour:02}:{str(self.end_time.minute):02}:{str(self.end_time.second):02}"
        return f"{s} - {e}"


@dataclass
class WeekdaysRange:
    weekdays: Set[int]

    def check(self, x: datetime.datetime) -> bool:
        return x.weekday() in self.weekdays

    def pretty(self):
        return ",".join(calendar.day_abbr[x].lower() for x in self.weekdays)


@dataclass
class TimeRange:
    weekdays: WeekdaysRange
    ranges: List[SingleTimeRange]
    action: Optional[str] = None

    def check(self, x: datetime.datetime) -> bool:
        return self.weekdays.check(x) and any(rng.check(x.time()) for rng in self.ranges)

    def pretty(self):
        s = self.weekdays.pretty()
        s += " - "
        s += " | ".join(x.pretty() for x in self.ranges)
        return s


@dataclass
class TimeRangeCollection:
    time_ranges: List[TimeRange]

    def check(self, x: datetime.datetime) -> bool:
        return any(rng.check(x) for rng in self.time_ranges)

    def get_action(self, x: datetime.datetime, default_action: Optional[str]) -> Optional[str]:
        for r in self.time_ranges:
            if r.check(x):
                return r.action
        return default_action

    def pretty(self):
        s = "TimeRangeCollection:\n"
        for r in self.time_ranges:
            s += "  " + r.pretty() + "\n"
        return s.strip()
