import os

import numpy as np
import pytest

from nro45data.psw.ms2._casa import open_table

from ._utils import get_checker


@pytest.fixture(scope="module")
def tb(msfile):
    antenna_table = os.path.join(msfile, "POLARIZATION")
    assert os.path.exists(antenna_table)

    with open_table(antenna_table, read_only=True) as _tb:
        yield _tb


def test_polarization_schema_num_corr(tb):
    col = get_checker(tb, "NUM_CORR")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_polarization_schema_corr_type(tb):
    col = get_checker(tb, "CORR_TYPE")
    assert col.is_array()
    assert col.get_ndim() == 1
    assert col.get_type() == "int"


def test_polarization_schema_corr_product(tb):
    col = get_checker(tb, "CORR_PRODUCT")
    assert col.is_array()
    assert col.get_ndim() == 2
    assert col.get_type() == "int"


def test_polarization_schema_flag_row(tb):
    col = get_checker(tb, "FLAG_ROW")
    assert col.is_scalar()
    assert col.get_type() == "boolean"
