import os

import numpy as np
import pytest

from nro45data.psw.ms2._casa import open_table

from ._utils import get_checker


@pytest.fixture(scope="module")
def tb(msfile):
    antenna_table = os.path.join(msfile, "STATE")
    assert os.path.exists(antenna_table)

    with open_table(antenna_table, read_only=True) as _tb:
        yield _tb


def test_state_schema_sig(tb):
    col = get_checker(tb, "SIG")
    assert col.is_scalar()
    assert col.get_type() == "boolean"


def test_state_schema_ref(tb):
    col = get_checker(tb, "REF")
    assert col.is_scalar()
    assert col.get_type() == "boolean"


def test_state_schema_cal(tb):
    col = get_checker(tb, "CAL")
    assert col.is_scalar()
    assert col.get_type() == "double"


def test_state_schema_load(tb):
    col = get_checker(tb, "LOAD")
    assert col.is_scalar()
    assert col.get_type() == "double"


def test_state_schema_sub_scan(tb):
    col = get_checker(tb, "SUB_SCAN")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_state_schema_obs_mode(tb):
    col = get_checker(tb, "OBS_MODE")
    assert col.is_scalar()
    assert col.get_type() == "string"


def test_state_schema_flag_row(tb):
    col = get_checker(tb, "FLAG_ROW")
    assert col.is_scalar()
    assert col.get_type() == "boolean"
