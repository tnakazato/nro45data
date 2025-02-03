from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING

import nro45data.psw.ms2._casa as _casa
from .antenna import fill_antenna
from .data_description import fill_data_description
from .feed import fill_feed
from .field import fill_field
from .observation import fill_observation
from .polarization import fill_polarization
from .main import fill_main
from .pointing import fill_pointing
from .processor import fill_processor
from .source import fill_source
from .spectral_window import fill_spectral_window
from .state import fill_state
from .syscal import fill_syscal
from .weather import fill_weather

if TYPE_CHECKING:
    from astropy.io.fits.hdu.BinTableHDU import BinTableHDU

LOG = logging.getLogger(__name__)


def fill_ms2(msfile: str, hdu: BinTableHDU):
    """Fill MS tables with data from FITS HDU.

    Note that the MS file must be generated before calling this function.

    Args:
        msfile: Name of MS file.
        hdu: NRO45m psw data in the form of BinTableHDU object.

    Raises:
        FileNotFoundError: If MS file does not exist.
    """
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
        'FLAG_CMD': None,
        'HISTORY': None,
    }
    for subtable_name, filler_method in subtable_filler_methods.items():
        if filler_method:
            filler_method(msfile, hdu)
        subtable_path = os.path.join(msfile, subtable_name)
        _casa.put_table_keyword(msfile, subtable_name, f"Table: {subtable_path}")
