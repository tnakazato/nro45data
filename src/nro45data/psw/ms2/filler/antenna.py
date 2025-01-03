import logging
from typing import TYPE_CHECKING

import numpy as np

from .._casa import open_table
from .utils import fix_nrow_to, get_array_configuration

if TYPE_CHECKING:
    from astropy.io.fits.hdu.BinTableHDU import BinTableHDU

LOG = logging.getLogger(__name__)


def _get_antenna_columns(hdu: 'BinTableHDU') -> dict:
    array_conf = get_array_configuration(hdu)
    beam_list = np.unique(sorted([x[1] for x in array_conf.values()]))
    num_beam = len(beam_list)

    # NAME
    antenna_name_base = hdu.header['TELESCOP'].strip()
    antenna_name = np.array([f'{antenna_name_base}-BEAM{i}' for i in range(num_beam)])
    LOG.debug('antenna_name: %s', antenna_name)

    # POSITION
    # in ITRF, from casadata/geodetic/Observatories table
    antenna_position = np.array([-3871023.46, 3428106.87, 3724039.47])
    position = np.zeros((3, num_beam), dtype=float)
    position[0] = antenna_position[0]
    position[1] = antenna_position[1]
    position[2] = antenna_position[2]
    LOG.debug('position: %s', position)

    # OFFSET
    offset = np.zeros(position.shape, dtype=float)
    LOG.debug('offset: %s', offset)

    # DIAMETER
    diameter = np.array([45.0] * num_beam)

    # TYPE
    antenna_type = np.array(['GROUND-BASED'] * num_beam)
    LOG.debug('antenna_type: %s', antenna_type)

    # MOUNT
    mount = np.array(['ALT-AZ'] * num_beam)
    LOG.debug('mount: %s', mount)

    # STATION
    station = np.array([antenna_name_base] * num_beam)
    LOG.debug('station: %s', station)

    # FLAG_ROW
    flag_row = np.zeros(num_beam, dtype=bool)

    columns = {
        'NAME': antenna_name,
        'POSITION': position,
        'OFFSET': offset,
        'DISH_DIAMETER': diameter,
        'TYPE': antenna_type,
        'MOUNT': mount,
        'STATION': station,
        'FLAG_ROW': flag_row,
    }

    return columns


def _fill_antenna_columns(msfile: str, columns: dict):
    with open_table(msfile + '/ANTENNA', read_only=False) as tb:
        nrow = len(columns['NAME'])
        fix_nrow_to(nrow, tb)

        tb.putcol('NAME', columns['NAME'])
        tb.putcol('DISH_DIAMETER', columns['DISH_DIAMETER'])
        tb.putcol('TYPE', columns['TYPE'])
        tb.putcol('MOUNT', columns['MOUNT'])
        tb.putcol('STATION', columns['STATION'])
        tb.putcol('FLAG_ROW', columns['FLAG_ROW'])
        for i in range(nrow):
            tb.putcell('POSITION', i, columns['POSITION'][:, i])
            tb.putcell('OFFSET', i, columns['OFFSET'][:, i])
