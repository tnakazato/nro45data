from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING

import nro45data.psw.ms2._casa as _casa
from .antenna import fill_antenna
from .data_description import fill_data_description
from .feed import fill_feed
from .field import _fill_field_columns, _get_field_columns
from .observation import _fill_observation_columns, _get_observation_columns
from .polarization import _fill_polarization_columns, _get_polarization_columns
from .main import fill_main
from .pointing import fill_pointing
from .processor import _fill_processor_columns, _get_processor_columns
from .source import fill_source
from .spectral_window import fill_spectral_window
from .state import fill_state
from .syscal import fill_syscal
from .weather import fill_weather

if TYPE_CHECKING:
    from astropy.io.fits.hdu.BinTableHDU import BinTableHDU

LOG = logging.getLogger(__name__)


def fill_field(msfile: str, hdu: BinTableHDU):
    columns = _get_field_columns(hdu)
    _fill_field_columns(msfile, columns)


def fill_observation(msfile: str, hdu: BinTableHDU):
    columns = _get_observation_columns(hdu)
    _fill_observation_columns(msfile, columns)


def fill_polarization(msfile: str, hdu: BinTableHDU):
    columns = _get_polarization_columns(hdu)
    _fill_polarization_columns(msfile, columns)


def fill_processor(msfile: str, hdu: BinTableHDU):
    columns = _get_processor_columns(hdu)
    _fill_processor_columns(msfile, columns)


def fill_nothing(msfile: str, hdu: BinTableHDU):
    pass


def fill_ms2(msfile: str, hdu: BinTableHDU):
    if not os.path.exists(msfile):
        FileNotFoundError("MS must be built before calling fill_ms2")

    fill_main(msfile, hdu)
    subtable_filler_methods = {
        'ANTENNA': fill_antenna,
        'DATA_DESCRIPTION': fill_data_description,
        'FEED': fill_feed,
        'FIELD': fill_field,
        'OBSERVATION': fill_observation,
        'POINTING': fill_pointing,
        'POLARIZATION': fill_polarization,
        'PROCESSOR': fill_processor,
        'SOURCE': fill_source,
        'SPECTRAL_WINDOW': fill_spectral_window,
        'STATE': fill_state,
        'SYSCAL': fill_syscal,
        'WEATHER': fill_weather,
        'FLAG_CMD': fill_nothing,
        'HISTORY': fill_nothing,
    }
    for subtable_name, filler_method in subtable_filler_methods.items():
        filler_method(msfile, hdu)
        subtable_path = os.path.join(msfile, subtable_name)
        _casa.put_table_keyword(msfile, subtable_name, f"Table: {subtable_path}")
