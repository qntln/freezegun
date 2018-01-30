import datetime
import time
import mock
import sys

from nose.plugins import skip

from freezegun import freeze_time
from tests import utils


@utils.cpython_only
def test_ticking_datetime():
    with freeze_time("Jan 14th, 2012", ticking_speed=1.0):
        time.sleep(0.001)  # Deal with potential clock resolution problems
        assert datetime.datetime.now() > datetime.datetime(2012, 1, 14)


@utils.cpython_only
def test_ticking_date():
    with freeze_time("Jan 14th, 2012, 23:59:59.9999999", ticking_speed=1.0):
        time.sleep(0.001)  # Deal with potential clock resolution problems
        assert datetime.date.today() == datetime.date(2012, 1, 15)


@utils.cpython_only
def test_ticking_time():
    with freeze_time("Jan 14th, 2012, 23:59:59", ticking_speed=1.0):
        time.sleep(0.001)  # Deal with potential clock resolution problems
        assert time.time() > 1326585599.0


@mock.patch('freezegun.api._is_cpython', False)
def test_pypy_compat():
    try:
        freeze_time("Jan 14th, 2012, 23:59:59", ticking_speed=1.0)
    except SystemError:
        pass
    else:
        raise AssertionError("tick=True should error on non-CPython")


@mock.patch('freezegun.api._is_cpython', True)
def test_non_pypy_compat():
    try:
        freeze_time("Jan 14th, 2012, 23:59:59", ticking_speed=1.0)
    except Exception:
        raise AssertionError("tick=True should not error on CPython")


@utils.cpython_only
def test_ticking_datetime_monotonic():
    if sys.version_info[0] != 3:
        raise skip.SkipTest("test target is Python3")

    with freeze_time("Jan 14th, 2012", ticking_speed=1.0):
        initial_monotonic = time.monotonic()
        time.sleep(0.001)  # Deal with potential clock resolution problems
        assert time.monotonic() > initial_monotonic


@utils.cpython_only
def test_ticking_time_speed():
    with freeze_time("Jan 14th, 2012, 23:59:59", ticking_speed=1000.0):
        time.sleep(0.001)  # Deal with potential clock resolution problems
        assert 1326585600.0 < time.time() < 1326585700.0
