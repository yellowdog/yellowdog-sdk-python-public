from datetime import timedelta

import pytest

from .test_utils import should_serde


class TestEncode(object):
    @pytest.mark.parametrize(
        "time_in_delta,str_format",
        [
            (timedelta(), "P0D"),
            (timedelta(microseconds=1), 'PT0.000001S'),
            (timedelta(microseconds=596), 'PT0.000596S'),
            (timedelta(milliseconds=1), 'PT0.001S'),
            (timedelta(milliseconds=123), 'PT0.123S'),
            (timedelta(milliseconds=123, microseconds=456), 'PT0.123456S'),
            (timedelta(seconds=5), 'PT5S'),
            (timedelta(seconds=59), 'PT59S'),
            (timedelta(minutes=1), 'PT1M'),
            (timedelta(minutes=1, seconds=30), 'PT1M30S'),
            (timedelta(minutes=10), 'PT10M'),
            (timedelta(minutes=59), 'PT59M'),
            (timedelta(hours=1), 'PT1H'),
            (timedelta(hours=12), 'PT12H'),
            (timedelta(hours=23, minutes=59, seconds=59), 'PT23H59M59S'),
            (timedelta(days=1), 'P1D'),
            (timedelta(days=5), 'P5D'),
            (timedelta(days=17, hours=23, minutes=59, seconds=59), 'P17DT23H59M59S'),
        ]
    )
    def test_serialize(self, time_in_delta, str_format):
        should_serde(time_in_delta, str_format)
