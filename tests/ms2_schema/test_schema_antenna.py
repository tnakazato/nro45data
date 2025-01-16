import os

import numpy as np
import pytest

from nro45data.psw.ms2._casa import open_table

from ._utils import get_checker


@pytest.fixture(scope="module")
def tb(msfile):
    antenna_table = os.path.join(msfile, "ANTENNA")
    assert os.path.exists(antenna_table)

    with open_table(antenna_table, read_only=True) as _tb:
        yield _tb


def test_antenna_schema_name(tb):
    col = get_checker(tb, "NAME")
    assert col.is_scalar()
    assert col.get_type() == "string"


def test_antenna_schema_station(tb):
    col = get_checker(tb, "STATION")
    assert col.is_scalar()
    assert col.get_type() == "string"


def test_antenna_schema_type(tb):
    col = get_checker(tb, "TYPE")
    assert col.is_scalar()
    assert col.get_type() == "string"


def test_antenna_schema_mount(tb):
    col = get_checker(tb, "MOUNT")
    assert col.is_scalar()
    assert col.get_type() == "string"


def test_antenna_schema_position(tb):
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


def test_antenna_schema_offset(tb):
    col = get_checker(tb, "OFFSET")
    assert col.is_array()
    assert col.is_position_meas()
    assert col.get_ndim() == 1
    assert col.get_meas_ref() == "ITRF"
    assert len(col.get_unit()) == 3
    assert np.all(col.get_unit() == "m")
    assert len(col.get_shape()) == 1
    assert col.get_shape()[0] == 3
    assert col.get_type() == "double"


def test_antenna_schema_dish_diameter(tb):
    col = get_checker(tb, "DISH_DIAMETER")
    assert col.is_scalar()
    assert col.get_type() == "double"
    assert len(col.get_unit()) == 1
    assert np.all(col.get_unit() == "m")


def test_antenna_schema_flag_row(tb):
    col = get_checker(tb, "FLAG_ROW")
    assert col.is_scalar()
    assert col.get_type() == "boolean"
