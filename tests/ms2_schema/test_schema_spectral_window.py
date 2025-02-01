import os

import numpy as np
import pytest

from nro45data.psw.ms2._casa import open_table

from ._utils import get_checker


@pytest.fixture(scope="module")
def tb(msfile):
    antenna_table = os.path.join(msfile, "SPECTRAL_WINDOW")
    assert os.path.exists(antenna_table)

    with open_table(antenna_table, read_only=True) as _tb:
        yield _tb


def test_spectral_window_schema_num_chan(tb):
    col = get_checker(tb, "NUM_CHAN")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_spectral_window_schema_name(tb):
    col = get_checker(tb, "NAME")
    assert col.is_scalar()
    assert col.get_type() == "string"


def test_spectral_window_schema_ref_frequency(tb):
    col = get_checker(tb, "REF_FREQUENCY")
    assert col.is_scalar()
    assert col.is_frequency_meas()
    assert len(col.get_unit()) == 1
    assert col.get_unit()[0] == 'Hz'
    assert col.get_type() == "double"


def test_spectral_window_schema_chan_freq(tb):
    col = get_checker(tb, "CHAN_FREQ")
    assert col.is_array()
    assert col.is_frequency_meas()
    assert len(col.get_unit()) == 1
    assert col.get_unit()[0] == 'Hz'
    assert col.get_ndim() == 1
    assert col.get_type() == "double"


def test_spectral_window_schema_chan_width(tb):
    col = get_checker(tb, "CHAN_WIDTH")
    assert col.is_array()
    assert len(col.get_unit()) == 1
    assert col.get_unit()[0] == 'Hz'
    assert col.get_ndim() == 1
    assert col.get_type() == "double"


def test_spectral_window_schema_meas_freq_ref(tb):
    col = get_checker(tb, "MEAS_FREQ_REF")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_spectral_window_schema_effective_bw(tb):
    col = get_checker(tb, "EFFECTIVE_BW")
    assert col.is_array()
    assert len(col.get_unit()) == 1
    assert col.get_unit()[0] == 'Hz'
    assert col.get_ndim() == 1
    assert col.get_type() == "double"


def test_spectral_window_schema_resolution(tb):
    col = get_checker(tb, "RESOLUTION")
    assert col.is_array()
    assert len(col.get_unit()) == 1
    assert col.get_unit()[0] == 'Hz'
    assert col.get_ndim() == 1
    assert col.get_type() == "double"


def test_spectral_window_schema_total_bandwidth(tb):
    col = get_checker(tb, "TOTAL_BANDWIDTH")
    assert col.is_scalar()
    assert len(col.get_unit()) == 1
    assert col.get_unit()[0] == 'Hz'
    assert col.get_type() == "double"


def test_spectral_window_schema_net_sideband(tb):
    col = get_checker(tb, "NET_SIDEBAND")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_spectral_window_schema_if_conv_chain(tb):
    col = get_checker(tb, "IF_CONV_CHAIN")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_spectral_window_schema_freq_group(tb):
    col = get_checker(tb, "FREQ_GROUP")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_spectral_window_schema_freq_group_name(tb):
    col = get_checker(tb, "FREQ_GROUP_NAME")
    assert col.is_scalar()
    assert col.get_type() == "string"


def test_spectral_window_schema_bbc_no(tb):
    col = get_checker(tb, "BBC_NO")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_spectral_window_schema_assoc_spw_id(tb):
    col = get_checker(tb, "ASSOC_SPW_ID")
    assert col.is_var_array()
    assert col.get_type() == "int"


def test_spectral_window_schema_assoc_nature(tb):
    col = get_checker(tb, "ASSOC_NATURE")
    assert col.is_var_array()
    assert col.get_type() == "string"


def test_spectral_window_schema_flag_row(tb):
    col = get_checker(tb, "FLAG_ROW")
    assert col.is_scalar()
    assert col.get_type() == "boolean"
