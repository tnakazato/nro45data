import os

import numpy as np
import pytest

from nro45data.psw.ms2._casa import open_table

from ._utils import get_checker


@pytest.fixture(scope="module")
def tb(msfile):
    assert os.path.exists(msfile)

    with open_table(msfile, read_only=True) as _tb:
        yield _tb


def test_main_version(tb):
    ms_version = tb.getkeyword("MS_VERSION")
    assert ms_version == 2.0


def test_main_schema_time(tb):
    col = get_checker(tb, "TIME")
    assert col.is_scalar()
    assert col.is_epoch_meas()
    assert col.get_meas_ref() == "UTC"
    assert len(col.get_meas_unit()) == 1
    assert np.all(col.get_meas_unit() == "s")
    assert col.get_type() == "double"


def test_main_schema_antenna1(tb):
    col = get_checker(tb, "ANTENNA1")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_main_schema_antenna2(tb):
    col = get_checker(tb, "ANTENNA2")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_main_schema_feed1(tb):
    col = get_checker(tb, "FEED1")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_main_schema_feed2(tb):
    col = get_checker(tb, "FEED2")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_main_schema_data_desc_id(tb):
    col = get_checker(tb, "DATA_DESC_ID")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_main_schema_processor_id(tb):
    col = get_checker(tb, "PROCESSOR_ID")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_main_schema_field_id(tb):
    col = get_checker(tb, "FIELD_ID")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_main_schema_interval(tb):
    col = get_checker(tb, "INTERVAL")
    assert col.is_scalar()
    assert col.get_type() == "double"


def test_main_schema_exposure(tb):
    col = get_checker(tb, "EXPOSURE")
    assert col.is_scalar()
    assert col.get_type() == "double"


def test_main_schema_time_centroid(tb):
    col = get_checker(tb, "TIME_CENTROID")
    assert col.is_scalar()
    assert col.is_epoch_meas()
    assert col.get_meas_ref() == "UTC"
    assert len(col.get_meas_unit()) == 1
    assert np.all(col.get_meas_unit() == "s")
    assert col.get_type() == "double"


def test_main_schema_scan_number(tb):
    col = get_checker(tb, "SCAN_NUMBER")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_main_schema_array_id(tb):
    col = get_checker(tb, "ARRAY_ID")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_main_schema_observation_id(tb):
    col = get_checker(tb, "OBSERVATION_ID")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_main_schema_state_id(tb):
    col = get_checker(tb, "STATE_ID")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_main_schema_uvw(tb):
    col = get_checker(tb, "UVW")
    assert col.is_array()
    assert col.get_ndim() == 1
    assert col.is_uvw_meas()
    assert col.get_meas_ref() == "ITRF"
    assert len(col.get_meas_unit()) == 3
    assert np.all(col.get_meas_unit() == "m")
    assert col.get_type() == "double"
    assert len(col.get_shape()) == 1
    assert col.get_shape()[0] == 3


def test_main_schema_float_data(tb):
    col = get_checker(tb, "FLOAT_DATA")
    assert col.is_array()
    assert col.get_ndim() == 2
    assert col.get_type() == "float"


def test_main_schema_sigma(tb):
    col = get_checker(tb, "SIGMA")
    assert col.is_array()
    assert col.get_ndim() == 1
    assert col.get_type() == "float"


def test_main_schema_weight(tb):
    col = get_checker(tb, "WEIGHT")
    assert col.is_array()
    assert col.get_ndim() == 1
    assert col.get_type() == "float"


def test_main_schema_flag(tb):
    col = get_checker(tb, "FLAG")
    assert col.is_array()
    assert col.get_ndim() == 2
    assert col.get_type() == "boolean"


def test_main_schema_flag_category(tb):
    col = get_checker(tb, "FLAG_CATEGORY")
    assert col.is_array()
    assert col.get_ndim() == 3
    assert col.get_type() == "boolean"


def test_main_schema_flag_row(tb):
    col = get_checker(tb, "FLAG_ROW")
    assert col.is_scalar()
    assert col.get_type() == "boolean"
