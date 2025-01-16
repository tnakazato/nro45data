import os

import numpy as np
import pytest

from nro45data.psw.ms2._casa import open_table

from ._utils import get_checker


@pytest.fixture(scope="module")
def tb(msfile):
    antenna_table = os.path.join(msfile, "HISTORY")
    assert os.path.exists(antenna_table)

    with open_table(antenna_table, read_only=True) as _tb:
        yield _tb


def test_history_schema_time(tb):
    col = get_checker(tb, "TIME")
    assert col.is_scalar()
    assert col.is_epoch_meas()
    assert col.get_meas_ref() == "UTC"
    assert len(col.get_unit()) == 1
    assert np.all(col.get_unit() == "s")
    assert col.get_type() == "double"


def test_history_schema_observation_id(tb):
    col = get_checker(tb, "OBSERVATION_ID")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_history_schema_message(tb):
    col = get_checker(tb, "MESSAGE")
    assert col.is_scalar()
    assert col.get_type() == "string"


def test_history_schema_priority(tb):
    col = get_checker(tb, "PRIORITY")
    assert col.is_scalar()
    assert col.get_type() == "string"


def test_history_schema_origin(tb):
    col = get_checker(tb, "ORIGIN")
    assert col.is_scalar()
    assert col.get_type() == "string"


def test_history_schema_object_id(tb):
    col = get_checker(tb, "OBJECT_ID")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_history_schema_application(tb):
    col = get_checker(tb, "APPLICATION")
    assert col.is_scalar()
    assert col.get_type() == "string"


def test_history_schema_cli_command(tb):
    col = get_checker(tb, "CLI_COMMAND")
    assert col.is_var_array()
    assert col.get_type() == "string"


def test_history_schema_app_params(tb):
    col = get_checker(tb, "APP_PARAMS")
    assert col.is_var_array()
    assert col.get_type() == "string"
