import os

import numpy as np
import pytest

from nro45data.psw.ms2._casa import open_table

from ._utils import get_checker


@pytest.fixture(scope="module")
def tb(msfile):
    antenna_table = os.path.join(msfile, "FIELD")
    assert os.path.exists(antenna_table)

    with open_table(antenna_table, read_only=True) as _tb:
        yield _tb


def test_field_schema_code(tb):
    col = get_checker(tb, "CODE")
    assert col.is_scalar()
    assert col.get_type() == "string"


def test_field_schema_time(tb):
    col = get_checker(tb, "TIME")
    assert col.is_scalar()
    assert col.is_epoch_meas()
    assert col.get_meas_ref() == "UTC"
    assert len(col.get_unit()) == 1
    assert np.all(col.get_unit() == "s")
    assert col.get_type() == "double"


def test_field_schema_num_poly(tb):
    col = get_checker(tb, "NUM_POLY")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_field_schema_delay_dir(tb):
    col = get_checker(tb, "DELAY_DIR")
    assert col.is_array()
    assert col.is_direction_meas()
    assert col.get_ndim() == 2
    assert col.get_meas_ref() == "J2000"
    assert len(col.get_unit()) == 2
    assert np.all(col.get_unit() == "rad")
    assert col.get_type() == "double"


def test_field_schema_phase_dir(tb):
    col = get_checker(tb, "PHASE_DIR")
    assert col.is_array()
    assert col.is_direction_meas()
    assert col.get_ndim() == 2
    assert col.get_meas_ref() == "J2000"
    assert len(col.get_unit()) == 2
    assert np.all(col.get_unit() == "rad")
    assert col.get_type() == "double"


def test_field_schema_reference_dir(tb):
    col = get_checker(tb, "REFERENCE_DIR")
    assert col.is_array()
    assert col.is_direction_meas()
    assert col.get_ndim() == 2
    assert col.get_meas_ref() == "J2000"
    assert len(col.get_unit()) == 2
    assert np.all(col.get_unit() == "rad")
    assert col.get_type() == "double"


def test_field_schema_source_id(tb):
    col = get_checker(tb, "SOURCE_ID")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_field_schema_flag_row(tb):
    col = get_checker(tb, "FLAG_ROW")
    assert col.is_scalar()
    assert col.get_type() == "boolean"
