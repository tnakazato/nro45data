import os

import numpy as np
import pytest

from nro45data.psw.ms2._casa import open_table

from ._utils import get_checker


@pytest.fixture(scope="module")
def tb(msfile):
    antenna_table = os.path.join(msfile, "SOURCE")
    assert os.path.exists(antenna_table)

    with open_table(antenna_table, read_only=True) as _tb:
        yield _tb


def test_source_schema_source_id(tb):
    col = get_checker(tb, "SOURCE_ID")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_source_schema_time(tb):
    col = get_checker(tb, "TIME")
    assert col.is_scalar()
    assert col.is_epoch_meas()
    assert col.get_meas_ref() == "UTC"
    assert len(col.get_unit()) == 1
    assert np.all(col.get_unit() == "s")
    assert col.get_type() == "double"


def test_source_schema_interval(tb):
    col = get_checker(tb, "INTERVAL")
    assert col.is_scalar()
    assert col.get_type() == "double"


def test_source_schema_spectral_window_id(tb):
    col = get_checker(tb, "SPECTRAL_WINDOW_ID")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_source_schema_num_lines(tb):
    col = get_checker(tb, "NUM_LINES")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_source_schema_name(tb):
    col = get_checker(tb, "NAME")
    assert col.is_scalar()
    assert col.get_type() == "string"


def test_source_schema_calibration_group(tb):
    col = get_checker(tb, "CALIBRATION_GROUP")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_source_schema_code(tb):
    col = get_checker(tb, "CODE")
    assert col.is_scalar()
    assert col.get_type() == "string"


def test_source_schema_direction(tb):
    col = get_checker(tb, "DIRECTION")
    assert col.is_array()
    assert col.is_direction_meas()
    assert col.get_ndim() == 1
    assert col.get_meas_ref() == "J2000"
    assert len(col.get_unit()) == 2
    assert np.all(col.get_unit() == "rad")
    assert col.get_type() == "double"


def test_source_schema_position(tb):
    col = get_checker(tb, "POSITION")
    assert col.is_array()
    assert col.is_position_meas()
    assert col.get_ndim() == 1
    assert col.get_meas_ref() == "ITRF"
    assert len(col.get_unit()) == 3
    assert np.all(col.get_unit() == "m")
    assert len(col.get_shape()) == 1
    assert col.get_shape()[0] == 3
    assert col.get_type() == "double"


def test_source_schema_proper_motion(tb):
    col = get_checker(tb, "PROPER_MOTION")
    assert col.is_array()
    assert col.get_ndim() == 1
    assert len(col.get_unit()) == 1
    assert np.all(col.get_unit() == "rad/s")
    assert len(col.get_shape()) == 1
    assert col.get_shape()[0] == 2
    assert col.get_type() == "double"


def test_source_schema_transition(tb):
    col = get_checker(tb, "TRANSITION")
    assert col.is_array()
    assert col.get_ndim() == 1
    assert col.get_type() == "string"


def test_source_schema_rest_frequency(tb):
    col = get_checker(tb, "REST_FREQUENCY")
    assert col.is_array()
    assert col.is_frequency_meas()
    assert col.get_meas_ref() == "LSRK"
    assert len(col.get_unit()) == 1
    assert np.all(col.get_unit() == "Hz")
    assert col.get_ndim() == 1
    assert col.get_type() == "double"


def test_source_schema_sysvel(tb):
    col = get_checker(tb, "SYSVEL")
    assert col.is_array()
    assert col.is_velocity_meas()
    assert col.get_meas_ref() == "LSRK"
    assert len(col.get_unit()) == 1
    assert np.all(col.get_unit() == "m/s")
    assert col.get_ndim() == 1
    assert col.get_type() == "double"
