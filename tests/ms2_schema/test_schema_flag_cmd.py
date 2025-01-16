import os

import numpy as np
import pytest

from nro45data.psw.ms2._casa import open_table

from ._utils import get_checker


@pytest.fixture(scope="module")
def tb(msfile):
    antenna_table = os.path.join(msfile, "FLAG_CMD")
    assert os.path.exists(antenna_table)

    with open_table(antenna_table, read_only=True) as _tb:
        yield _tb


def test_flag_cmd_schema_time(tb):
    col = get_checker(tb, "TIME")
    assert col.is_scalar()
    assert col.is_epoch_meas()
    assert col.get_meas_ref() == "UTC"
    assert len(col.get_unit()) == 1
    assert np.all(col.get_unit() == "s")
    assert col.get_type() == "double"


def test_flag_cmd_schema_interval(tb):
    col = get_checker(tb, "INTERVAL")
    assert col.is_scalar()
    assert col.get_type() == "double"


def test_flag_cmd_schema_type(tb):
    col = get_checker(tb, "TYPE")
    assert col.is_scalar()
    assert col.get_type() == "string"


def test_flag_cmd_schema_reason(tb):
    col = get_checker(tb, "REASON")
    assert col.is_scalar()
    assert col.get_type() == "string"


def test_flag_cmd_schema_level(tb):
    col = get_checker(tb, "LEVEL")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_flag_cmd_schema_severity(tb):
    col = get_checker(tb, "SEVERITY")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_flag_cmd_schema_applied(tb):
    col = get_checker(tb, "APPLIED")
    assert col.is_scalar()
    assert col.get_type() == "boolean"


def test_flag_cmd_schema_command(tb):
    col = get_checker(tb, "COMMAND")
    assert col.is_scalar()
    assert col.get_type() == "string"
