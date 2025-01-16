import os

import numpy as np
import pytest

from nro45data.psw.ms2._casa import open_table

from ._utils import get_checker


@pytest.fixture(scope="module")
def tb(msfile):
    antenna_table = os.path.join(msfile, "POINTING")
    assert os.path.exists(antenna_table)

    with open_table(antenna_table, read_only=True) as _tb:
        yield _tb


def test_pointing_schema_time(tb):
    col = get_checker(tb, "TIME")
    assert col.is_scalar()
    assert col.is_epoch_meas()
    assert col.get_meas_ref() == "UTC"
    assert len(col.get_meas_unit()) == 1
    assert np.all(col.get_meas_unit() == "s")
    assert col.get_type() == "double"


def test_pointing_schema_interval(tb):
    col = get_checker(tb, "INTERVAL")
    assert col.is_scalar()
    assert col.get_type() == "double"


def test_pointing_schema_name(tb):
    col = get_checker(tb, "NAME")
    assert col.is_scalar()
    assert col.get_type() == "string"


def test_pointing_schema_num_poly(tb):
    col = get_checker(tb, "NUM_POLY")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_pointing_schema_time_origin(tb):
    col = get_checker(tb, "TIME_ORIGIN")
    assert col.is_scalar()
    assert col.is_epoch_meas()
    assert col.get_meas_ref() == "UTC"
    assert len(col.get_meas_unit()) == 1
    assert np.all(col.get_meas_unit() == "s")
    assert col.get_type() == "double"


def test_pointing_schema_direction(tb):
    col = get_checker(tb, "DIRECTION")
    assert col.is_array()
    assert col.is_direction_meas()
    assert col.get_ndim() == 2
    assert col.get_meas_ref() == "AZELGEO"
    assert len(col.get_meas_unit()) == 2
    assert np.all(col.get_meas_unit() == "rad")
    assert col.get_type() == "double"


def test_pointing_schema_target(tb):
    col = get_checker(tb, "TARGET")
    assert col.is_array()
    assert col.is_direction_meas()
    assert col.get_ndim() == 2
    assert col.get_meas_ref() == "AZELGEO"
    assert len(col.get_meas_unit()) == 2
    assert np.all(col.get_meas_unit() == "rad")
    assert col.get_type() == "double"


def test_pointing_schema_source_offset(tb):
    col = get_checker(tb, "SOURCE_OFFSET")
    assert col.is_array()
    assert col.is_direction_meas()
    assert col.get_ndim() == 2
    assert col.get_meas_ref() == "J2000"
    assert len(col.get_meas_unit()) == 2
    assert np.all(col.get_meas_unit() == "rad")
    assert col.get_type() == "double"


def test_pointing_schema_encoder(tb):
    col = get_checker(tb, "ENCODER")
    assert col.is_array()
    assert col.is_direction_meas()
    assert col.get_ndim() == 1
    assert col.get_meas_ref() == "AZELGEO"
    assert len(col.get_meas_unit()) == 2
    assert np.all(col.get_meas_unit() == "rad")
    assert col.get_type() == "double"


def test_pointing_schema_tracking(tb):
    col = get_checker(tb, "TRACKING")
    assert col.is_scalar()
    assert col.get_type() == "boolean"
