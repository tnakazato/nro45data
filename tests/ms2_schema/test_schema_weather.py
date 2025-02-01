import os

import numpy as np
import pytest

from nro45data.psw.ms2._casa import open_table

from ._utils import get_checker


@pytest.fixture(scope="module")
def tb(msfile):
    antenna_table = os.path.join(msfile, "WEATHER")
    assert os.path.exists(antenna_table)

    with open_table(antenna_table, read_only=True) as _tb:
        yield _tb


def test_weather_schema_antenna_id(tb):
    col = get_checker(tb, "ANTENNA_ID")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_weather_schema_time(tb):
    col = get_checker(tb, "TIME")
    assert col.is_scalar()
    assert col.is_epoch_meas()
    assert col.get_meas_ref() == "UTC"
    assert len(col.get_unit()) == 1
    assert np.all(col.get_unit() == "s")
    assert col.get_type() == "double"


def test_weather_schema_interval(tb):
    col = get_checker(tb, "INTERVAL")
    assert col.is_scalar()
    assert col.get_type() == "double"


def test_weather_schema_pressure(tb):
    col = get_checker(tb, "PRESSURE")
    assert col.is_scalar()
    assert len(col.get_unit()) == 1
    assert col.get_unit()[0] == 'hPa'
    assert col.get_type() == "float"


def test_weather_schema_pressure_flag(tb):
    col = get_checker(tb, "PRESSURE_FLAG")
    assert col.is_scalar()
    assert col.get_type() == "boolean"


def test_weather_schema_rel_humidity(tb):
    col = get_checker(tb, "REL_HUMIDITY")
    assert col.is_scalar()
    assert len(col.get_unit()) == 1
    assert col.get_unit()[0] == '%'
    assert col.get_type() == "float"


def test_weather_schema_rel_humidity_flag(tb):
    col = get_checker(tb, "REL_HUMIDITY_FLAG")
    assert col.is_scalar()
    assert col.get_type() == "boolean"


def test_weather_schema_temperature(tb):
    col = get_checker(tb, "TEMPERATURE")
    assert col.is_scalar()
    assert len(col.get_unit()) == 1
    assert col.get_unit()[0] == 'K'
    assert col.get_type() == "float"


def test_weather_schema_temperature_flag(tb):
    col = get_checker(tb, "TEMPERATURE_FLAG")
    assert col.is_scalar()
    assert col.get_type() == "boolean"


def test_weather_schema_dew_point(tb):
    col = get_checker(tb, "DEW_POINT")
    assert col.is_scalar()
    assert len(col.get_unit()) == 1
    assert col.get_unit()[0] == 'K'
    assert col.get_type() == "float"


def test_weather_schema_dew_point_flag(tb):
    col = get_checker(tb, "DEW_POINT_FLAG")
    assert col.is_scalar()
    assert col.get_type() == "boolean"


def test_weather_schema_wind_direction(tb):
    col = get_checker(tb, "WIND_DIRECTION")
    assert col.is_scalar()
    assert len(col.get_unit()) == 1
    assert col.get_unit()[0] == 'rad'
    assert col.get_type() == "float"


def test_weather_schema_wind_direction_flag(tb):
    col = get_checker(tb, "WIND_DIRECTION_FLAG")
    assert col.is_scalar()
    assert col.get_type() == "boolean"


def test_weather_schema_wind_speed(tb):
    col = get_checker(tb, "WIND_SPEED")
    assert col.is_scalar()
    assert len(col.get_unit()) == 1
    assert col.get_unit()[0] == 'm/s'
    assert col.get_type() == "float"


def test_weather_schema_wind_speed_flag(tb):
    col = get_checker(tb, "WIND_SPEED_FLAG")
    assert col.is_scalar()
    assert col.get_type() == "boolean"


def test_weather_schema_ns_wx_station_id(tb):
    col = get_checker(tb, "NS_WX_STATION_ID")
    assert col.is_scalar()
    assert col.get_type() == "int"


def test_weather_schema_ns_ws_station_position(tb):
    col = get_checker(tb, "NS_WX_STATION_POSITION")
    assert col.is_array()
    assert col.get_ndim() == 1
    assert len(col.get_shape()) == 1
    assert col.get_shape()[0] == 3
    assert col.get_type() == "double"
