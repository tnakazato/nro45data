from __future__ import annotations

import logging
from typing import Generator, TYPE_CHECKING

import numpy as np

from .utils import get_array_configuration, get_data_description_map, fill_ms_table

if TYPE_CHECKING:
    from astropy.io.fits.hdu.BinTableHDU import BinTableHDU

LOG = logging.getLogger(__name__)


def _get_data_description_row(hdu: BinTableHDU) -> Generator[dict, None, None]:
    """Provide data description row information.

    Args:
        hdu: NRO45m psw data in the form of BinTableHDU object.

    Yields:
        Dictionary containing data description row information.
    """
    array_conf = get_array_configuration(hdu)
    ddd, _, _, _ = get_data_description_map(array_conf)

    for _, (spw, pol) in ddd.items():
        spw_id = spw
        pol_id = pol

        flag_row = False

        row = {
            "SPECTRAL_WINDOW_ID": spw_id,
            "POLARIZATION_ID": pol_id,
            "FLAG_ROW": flag_row
        }
        LOG.debug("row: %s", row)

        yield row


def fill_data_description(msfile: str, hdu: BinTableHDU):
    """Fill MS DATA_DESCRIPTION table.

    Args:
        msfile: Name of MS file.
        hdu: NRO45m psw data in the form of BinTableHDU object.
    """
    fill_ms_table(msfile, hdu, "DATA_DESCRIPTION", _get_data_description_row)
