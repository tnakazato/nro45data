import logging
from typing import TYPE_CHECKING

import numpy as np

from .._casa import open_table
from .utils import fix_nrow_to

if TYPE_CHECKING:
    from astropy.io.fits.hdu.BinTableHDU import BinTableHDU

LOG = logging.getLogger(__name__)


def _get_processor_columns(hdu: 'BinTableHDU') -> dict:
    # TYPE
    processor_type = 'SPECTROMETER'

    # SUB_TYPE
    processor_sub_type_list = []
    # AOS-High
    arry1 = hdu.header['ARRY1'].strip()
    if arry1.find('1') >= 0:
        processor_sub_type_list.append('AOS-High')

    # AOS-Wide 1-10 (0-9)
    # AOS-Ultrawide 1-5 (10-15)
    # FX 1-5? (16-20)
    arry2 = hdu.header['ARRY2'].strip()
    if arry2[:10].find('1') >= 0:
        processor_sub_type_list.append('AOS-Wide')

    if arry2[10:15].find('1') >= 0:
        processor_sub_type_list.append('AOS-Ultrawide')

    if arry2[15:20].find('1') >= 0:
        processor_sub_type_list.append('FX')

    # AC45
    arry3 = hdu.header['ARRY3'].strip()
    arry4 = hdu.header['ARRY4'].strip()
    if (arry3 + arry4).find('1') >= 0:
        processor_sub_type_list.append('AC45')

    LOG.debug('processor_sub_type_list: %s', processor_sub_type_list)
    LOG.debug('arr1: %s', arry1)
    LOG.debug('arry2: %s', arry2)
    LOG.debug('arry3: %s', arry3)
    LOG.debug('arry4: %s', arry4)

    # TYPE_ID
    processor_type_id = 0

    # MODE_ID
    processor_mode_id = 0

    # FLAG_ROW
    flag_row = False

    columns = {
        'TYPE': processor_type,
        'SUB_TYPE': processor_sub_type_list,
        'TYPE_ID': processor_type_id,
        'MODE_ID': processor_mode_id,
        'FLAG_ROW': flag_row
    }

    return columns


def _fill_processor_columns(msfile: str, columns: dict):
    with open_table(msfile + '/PROCESSOR', read_only=False) as tb:
        nrow = len(columns['SUB_TYPE'])
        fix_nrow_to(tb, nrow)
        type_column = np.array([columns['TYPE']] * nrow)
        tb.putcol('TYPE', type_column)
        tb.putcol('SUB_TYPE', columns['SUB_TYPE'])
        type_id_column = np.array([columns['TYPE_ID']] * nrow)
        tb.putcol('TYPE_ID', type_id_column)
        mode_id_column = np.array([columns['MODE_ID']] * nrow)
        tb.putcol('MODE_ID', mode_id_column)
        flag_row_column = np.array([columns['FLAG_ROW']] * nrow)
        tb.putcol('FLAG_ROW', flag_row_column)
