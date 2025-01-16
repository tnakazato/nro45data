import os

import numpy as np
import pytest

from nro45data.psw.ms2._casa import open_table

from ._utils import get_checker


@pytest.fixture(scope="module")
def tb(msfile):
    antenna_table = os.path.join(msfile, "PROCESSOR")
    assert os.path.exists(antenna_table)

    with open_table(antenna_table, read_only=True) as _tb:
        yield _tb


def test_processor_schema_type(tb):
    col = get_checker(tb, "TYPE")
    assert col.is_scalar()
    assert col.get_type() == "string"


def test_processor_schema_sub_type(tb):
    col = get_checker(tb, "SUB_TYPE")
    assert col.is_scalar()
    assert col.get_type() == "string"


def test_processor_schema_type_id(tb):
    col = get_checker(tb, "TYPE_ID")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_processor_schema_mode_id(tb):
    col = get_checker(tb, "MODE_ID")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_processor_schema_flag_row(tb):
    col = get_checker(tb, "FLAG_ROW")
    assert col.is_scalar()
    assert col.get_type() == "boolean"
