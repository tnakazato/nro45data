import logging
from typing import TYPE_CHECKING

import numpy as np

from .._casa import open_table
from .utils import fix_nrow_to, get_array_configuration, get_data_description_map

if TYPE_CHECKING:
    from astropy.io.fits.hdu.BinTableHDU import BinTableHDU

LOG = logging.getLogger(__name__)


def _get_data_description_columns(hdu: 'BinTableHDU') -> dict:
    array_conf = get_array_configuration(hdu)
    ddd, _, _, _ = get_data_description_map(array_conf)
    num_dd = len(ddd)
    spw_id = np.zeros(num_dd, dtype=int)
    pol_id = np.zeros(num_dd, dtype=int)
    for dd_id, (spw, pol) in ddd.items():
        spw_id[dd_id] = spw
        pol_id[dd_id] = pol

    flag_row = np.zeros(num_dd, dtype=bool)

    columns = {
        'SPECTRAL_WINDOW_ID': spw_id,
        'POLARIZATION_ID': pol_id,
        'FLAG_ROW': flag_row
    }
    LOG.debug('columns: %s', columns)

    return columns



def _fill_data_description_columns(msfile: str, columns: dict):
    with open_table(msfile + '/DATA_DESCRIPTION', read_only=False) as tb:
        num_dd = len(columns['SPECTRAL_WINDOW_ID'])
        fix_nrow_to(num_dd, tb)

        tb.putcol('SPECTRAL_WINDOW_ID', columns['SPECTRAL_WINDOW_ID'])
        tb.putcol('POLARIZATION_ID', columns['POLARIZATION_ID'])