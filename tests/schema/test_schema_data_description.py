import os

import pytest

from nro45data.psw.ms2._casa import open_table

from ._utils import get_checker


@pytest.fixture(scope="module")
def tb(msfile):
    antenna_table = os.path.join(msfile, "DATA_DESCRIPTION")
    assert os.path.exists(antenna_table)

    with open_table(antenna_table, read_only=True) as _tb:
        yield _tb


def test_data_description_schema_spectral_window_id(tb):
    col = get_checker(tb, "SPECTRAL_WINDOW_ID")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_data_description_schema_polarization_id(tb):
    col = get_checker(tb, "POLARIZATION_ID")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_data_description_schema_flag_row(tb):
    col = get_checker(tb, "FLAG_ROW")
    assert col.is_scalar()
    assert col.get_type() == "boolean"
