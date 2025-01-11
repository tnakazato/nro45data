import logging
from typing import TYPE_CHECKING

import numpy as np

from .antenna import _fill_antenna_columns, _get_antenna_columns
from .data_description import _fill_data_description_columns, _get_data_description_columns
from .feed import _fill_feed_columns, _get_feed_columns
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
from .utils import get_array_configuration
from .weather import fill_weather

if TYPE_CHECKING:
    from astropy.io.fits.hdu.BinTableHDU import BinTableHDU

LOG = logging.getLogger(__name__)


def fill_antenna(msfile: str, hdu: 'BinTableHDU'):
    columns = _get_antenna_columns(hdu)
    _fill_antenna_columns(msfile, columns)


def fill_data_description(msfile: str, hdu: 'BinTableHDU'):
    columns = _get_data_description_columns(hdu)
    _fill_data_description_columns(msfile, columns)


def fill_feed(msfile: str, hdu: 'BinTableHDU'):
    columns = _get_feed_columns(hdu)
    _fill_feed_columns(msfile, columns)


def fill_field(msfile: str, hdu: 'BinTableHDU'):
    columns = _get_field_columns(hdu)
    _fill_field_columns(msfile, columns)


def fill_observation(msfile: str, hdu: 'BinTableHDU'):
    columns = _get_observation_columns(hdu)
    _fill_observation_columns(msfile, columns)


def fill_polarization(msfile: str, hdu: 'BinTableHDU'):
    columns = _get_polarization_columns(hdu)
    _fill_polarization_columns(msfile, columns)


def fill_processor(msfile: str, hdu: 'BinTableHDU'):
    columns = _get_processor_columns(hdu)
    _fill_processor_columns(msfile, columns)
