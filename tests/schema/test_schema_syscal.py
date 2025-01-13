import os

import numpy as np
import pytest

from nro45data.psw.ms2._casa import open_table

from ._utils import get_checker


@pytest.fixture(scope="module")
def tb(msfile):
    antenna_table = os.path.join(msfile, "SYSCAL")
    assert os.path.exists(antenna_table)

    with open_table(antenna_table, read_only=True) as _tb:
        yield _tb


def test_syscal_schema_antenna_id(tb):
    col = get_checker(tb, "ANTENNA_ID")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_syscal_schema_feed_id(tb):
    col = get_checker(tb, "FEED_ID")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_syscal_schema_spectral_window_id(tb):
    col = get_checker(tb, "SPECTRAL_WINDOW_ID")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_syscal_schema_time(tb):
    col = get_checker(tb, "TIME")
    assert col.is_scalar()
    assert col.is_epoch_meas()
    assert col.get_meas_ref() == "UTC"
    assert len(col.get_meas_unit()) == 1
    assert np.all(col.get_meas_unit() == "s")
    assert col.get_type() == "double"


def test_syscal_schema_interval(tb):
    col = get_checker(tb, "INTERVAL")
    assert col.is_scalar()
    assert col.get_type() == "double"


def test_syscal_schema_tcal_spectrum(tb):
    col = get_checker(tb, "TCAL_SPECTRUM")
    assert col.is_array()
    assert len(col.get_meas_unit()) == 1
    assert col.get_meas_unit()[0] == 'K'
    assert col.get_ndim() == 2
    assert col.get_type() == "float"


def test_syscal_schema_tcal_flag(tb):
    col = get_checker(tb, "TCAL_FLAG")
    assert col.is_scalar()
    assert col.get_type() == "boolean"


def test_syscal_schema_trx_spectrum(tb):
    col = get_checker(tb, "TRX_SPECTRUM")
    assert col.is_array()
    assert len(col.get_meas_unit()) == 1
    assert col.get_meas_unit()[0] == 'K'
    assert col.get_ndim() == 2
    assert col.get_type() == "float"


def test_syscal_schema_trx_flag(tb):
    col = get_checker(tb, "TRX_FLAG")
    assert col.is_scalar()
    assert col.get_type() == "boolean"


def test_syscal_schema_tsky_spectrum(tb):
    col = get_checker(tb, "TSKY_SPECTRUM")
    assert col.is_array()
    assert len(col.get_meas_unit()) == 1
    assert col.get_meas_unit()[0] == 'K'
    assert col.get_ndim() == 2
    assert col.get_type() == "float"


def test_syscal_schema_tsky_flag(tb):
    col = get_checker(tb, "TSKY_FLAG")
    assert col.is_scalar()
    assert col.get_type() == "boolean"


def test_syscal_schema_tsys_spectrum(tb):
    col = get_checker(tb, "TSYS_SPECTRUM")
    assert col.is_array()
    assert len(col.get_meas_unit()) == 1
    assert col.get_meas_unit()[0] == 'K'
    assert col.get_ndim() == 2
    assert col.get_type() == "float"


def test_syscal_schema_tsys_flag(tb):
    col = get_checker(tb, "TSYS_FLAG")
    assert col.is_scalar()
    assert col.get_type() == "boolean"


def test_syscal_schema_tant_spectrum(tb):
    col = get_checker(tb, "TANT_SPECTRUM")
    assert col.is_array()
    assert len(col.get_meas_unit()) == 1
    assert col.get_meas_unit()[0] == 'K'
    assert col.get_ndim() == 2
    assert col.get_type() == "float"


def test_syscal_schema_tant_flag(tb):
    col = get_checker(tb, "TANT_FLAG")
    assert col.is_scalar()
    assert col.get_type() == "boolean"


def test_syscal_schema_tant_tsys_spectrum(tb):
    col = get_checker(tb, "TANT_TSYS_SPECTRUM")
    assert col.is_array()
    assert col.get_ndim() == 2
    assert col.get_type() == "float"


def test_syscal_schema_tant_tsys_flag(tb):
    col = get_checker(tb, "TANT_TSYS_FLAG")
    assert col.is_scalar()
    assert col.get_type() == "boolean"
