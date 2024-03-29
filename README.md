timerangeparser
======

Python library for time-ranges parsing with optional action string support.

## Installation

```shell
pip install git+https://github.com/KrystianD/timerangeparser.git
```

## Example usage

```python
import datetime
import timerangeparser.parser

cfg = timerangeparser.parser.TimeRangeParser()

# if True, adjust the end of the range to the end of the specific hour
# for example, 2-5 would actually mean 2:00:00-5:59:59
cfg.hour_only_use_end = False

working_hours = cfg.parse("mon-fri@9-17|sat@9-15")

if working_hours.check(datetime.datetime.now()):
    print("OPEN")
else:
    print("CLOSED")
```

### Examples

with `hour_only_use_end = False`

| Range string          | Meaning                                                                               |
|-----------------------|---------------------------------------------------------------------------------------|
| `2`                   | all weekdays between 2:00:00 and 2:59:59                                              |
| `2-2`                 | all weekdays, the whole day                                                           |
| `2-5`                 | all weekdays between 2:00:00 and 5:00:00                                              |
| `2-5:30`              | all weekdays between 2:00:00 and 5:30:00                                              |
| `2-5:30:10`           | all weekdays between 2:00:00 and 5:30:10                                              |
| `2-24`                | all weekdays between 2:00:00 and 23:59:59                                             |
| `20-8`                | all weekdays between 20:00:00 and 8:00:00                                             |
| `mon@`                | on Monday, the whole day                                                              |
| `mon@9-15`            | on Monday between 9:00:00 and 15:00:00                                                |
| `mon-fri@9-15`        | between Monday and Friday (inclusive), between 9:00:00 and 15:00:00                   |
| `wed@9-10,13-15`      | on Wednesday between 9:00:00 and 10:00:00, and between 13:00:00 and 15:00:00          |
| `wed@9\|fri@15:30-20` | on Wednesday between 9:00:00 and 9:00:00, and on Friday between 15:30:00 and 20:00:00 |

with `hour_only_use_end = True`

| Range string          | Meaning                                                                               |
|-----------------------|---------------------------------------------------------------------------------------|
| `2`                   | all weekdays between 2:00:00 and 2:59:59                                              |
| `2-2`                 | all weekdays between 2:00:00 and 2:59:59                                              |
| `2-5`                 | all weekdays between 2:00:00 and 5:59:59                                              |
| `2-5:30`              | all weekdays between 2:00:00 and 5:30:59                                              |
| `2-5:30:10`           | all weekdays between 2:00:00 and 5:30:10                                              |
| `2-24`                | all weekdays between 2:00:00 and 23:59:59                                             |
| `20-8`                | all weekdays between 20:00:00 and 8:59:59                                             |
| `mon@`                | on Monday, the whole day                                                              |
| `mon@9-15`            | on Monday between 9:00:00 and 15:59:59                                                |
| `mon-fri@9-15`        | between Monday and Friday (inclusive), between 9:00:00 and 15:59:59                   |
| `wed@9-10,13-15`      | on Wednesday between 9:00:00 and 10:59:59, and between 13:00:00 and 15:59:59          |
| `wed@9\|fri@15:30-20` | on Wednesday between 9:00:00 and 9:59:59, and on Friday between 15:30:00 and 20:59:59 |
