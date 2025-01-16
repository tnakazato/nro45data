import os

import numpy as np
import pytest

from nro45data.psw.ms2._casa import open_table

from ._utils import get_checker


@pytest.fixture(scope="module")
def tb(msfile):
    antenna_table = os.path.join(msfile, "OBSERVATION")
    assert os.path.exists(antenna_table)

    with open_table(antenna_table, read_only=True) as _tb:
        yield _tb


def test_observation_schema_telescope_name(tb):
    col = get_checker(tb, "TELESCOPE_NAME")
    assert col.is_scalar()
    assert col.get_type() == "string"


def test_observation_schema_time_range(tb):
    col = get_checker(tb, "TIME_RANGE")
    assert col.is_array()
    assert col.is_epoch_meas()
    assert col.get_ndim() == 1
    assert len(col.get_shape()) == 1
    assert col.get_shape()[0] == 2
    assert col.get_meas_ref() == "UTC"
    assert len(col.get_unit()) == 1
    assert np.all(col.get_unit() == "s")
    assert col.get_type() == "double"


def test_observation_schema_observer(tb):
    col = get_checker(tb, "OBSERVER")
    assert col.is_scalar()
    assert col.get_type() == "string"


def test_observation_schema_log(tb):
    col = get_checker(tb, "LOG")
    assert col.is_var_array()
    assert col.get_type() == "string"


def test_observation_schema_schedule_type(tb):
    col = get_checker(tb, "SCHEDULE_TYPE")
    assert col.is_scalar()
    assert col.get_type() == "string"


def test_observation_schema_schedule(tb):
    col = get_checker(tb, "SCHEDULE")
    assert col.is_var_array()
    assert col.get_type() == "string"


def test_observation_schema_project(tb):
    col = get_checker(tb, "PROJECT")
    assert col.is_scalar()
    assert col.get_type() == "string"


def test_observation_schema_release_date(tb):
    col = get_checker(tb, "RELEASE_DATE")
    assert col.is_scalar()
    assert col.is_epoch_meas()
    assert col.get_meas_ref() == "UTC"
    assert len(col.get_unit()) == 1
    assert np.all(col.get_unit() == "s")
    assert col.get_type() == "double"


def test_observation_schema_flag_row(tb):
    col = get_checker(tb, "FLAG_ROW")
    assert col.is_scalar()
    assert col.get_type() == "boolean"
