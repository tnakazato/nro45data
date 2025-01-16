import os

import numpy as np
import pytest

from nro45data.psw.ms2._casa import open_table

from ._utils import get_checker


@pytest.fixture(scope="module")
def tb(msfile):
    antenna_table = os.path.join(msfile, "FEED")
    assert os.path.exists(antenna_table)

    with open_table(antenna_table, read_only=True) as _tb:
        yield _tb


def test_feed_schema_antenna_id(tb):
    col = get_checker(tb, "ANTENNA_ID")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_feed_schema_feed_id(tb):
    col = get_checker(tb, "FEED_ID")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_feed_schema_spectral_window_id(tb):
    col = get_checker(tb, "SPECTRAL_WINDOW_ID")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_feed_schema_time(tb):
    col = get_checker(tb, "TIME")
    assert col.is_scalar()
    assert col.is_epoch_meas()
    assert col.get_meas_ref() == "UTC"
    assert len(col.get_meas_unit()) == 1
    assert np.all(col.get_meas_unit() == "s")
    assert col.get_type() == "double"


def test_feed_schema_interval(tb):
    col = get_checker(tb, "INTERVAL")
    assert col.is_scalar()
    assert col.get_type() == "double"


def test_feed_schema_num_receptors(tb):
    col = get_checker(tb, "NUM_RECEPTORS")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_feed_schema_beam_id(tb):
    col = get_checker(tb, "BEAM_ID")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_feed_schema_beam_offset(tb):
    col = get_checker(tb, "BEAM_OFFSET")
    assert col.is_array()
    assert col.is_direction_meas()
    assert col.get_ndim() == 2
    assert col.get_meas_ref() == "J2000"
    assert len(col.get_meas_unit()) == 2
    assert np.all(col.get_meas_unit() == "rad")
    assert col.get_type() == "double"


def test_feed_schema_polarization_type(tb):
    col = get_checker(tb, "POLARIZATION_TYPE")
    assert col.is_array()
    assert col.get_ndim() == 1
    assert col.get_type() == "string"


def test_feed_schema_pol_response(tb):
    col = get_checker(tb, "POL_RESPONSE")
    assert col.is_array()
    assert col.get_ndim() == 2
    assert col.get_type() == "complex"


def test_feed_schema_position(tb):
    col = get_checker(tb, "POSITION")
    assert col.is_array()
    assert col.is_position_meas()
    assert col.get_ndim() == 1
    assert col.get_meas_ref() == "ITRF"
    assert len(col.get_meas_unit()) == 3
    assert np.all(col.get_meas_unit() == "m")
    assert len(col.get_shape()) == 1
    assert col.get_shape()[0] == 3
    assert col.get_type() == "double"


def test_feed_schema_receptor_angle(tb):
    col = get_checker(tb, "RECEPTOR_ANGLE")
    assert col.is_array()
    assert col.get_ndim() == 1
    assert col.get_type() == "double"
