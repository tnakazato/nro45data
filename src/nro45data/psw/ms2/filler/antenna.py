from __future__ import annotations

import logging
from typing import Generator, TYPE_CHECKING

import numpy as np

from .utils import get_array_configuration, fill_ms_table

if TYPE_CHECKING:
    import astropy.io.fits as fits
    BinTableHDU = fits.BinTableHDU

LOG = logging.getLogger(__name__)


def _get_antenna_row(hdu: BinTableHDU) -> Generator[dict, None, None]:
    """Provide antenna row information.

    Args:
        hdu: NRO45m psw data in the form of BinTableHDU object.

    Yields:
        Dictionary containing antenna row information.
    """
    array_conf = get_array_configuration(hdu)
    beam_list = np.unique(sorted([x[1] for x in array_conf.values()]))
    num_beam = len(beam_list)

    antenna_name_base = hdu.header["TELESCOP"].strip()

    for i in range(num_beam):
        # NAME
        antenna_name = f"{antenna_name_base}-BEAM{i}"
        LOG.debug("antenna_name: %s", antenna_name)

        # POSITION
        # in ITRF, from casadata/geodetic/Observatories table
        position = np.array([-3871023.46, 3428106.87, 3724039.47])
        LOG.debug("position: %s", position)

        # OFFSET
        offset = np.zeros(position.shape, dtype=float)
        LOG.debug("offset: %s", offset)

        # DIAMETER
        diameter = 45.0

        # TYPE
        antenna_type = "GROUND-BASED"
        LOG.debug("antenna_type: %s", antenna_type)

        # MOUNT
        mount = "ALT-AZ"
        LOG.debug("mount: %s", mount)

        # STATION
        station = antenna_name_base
        LOG.debug("station: %s", station)

        # FLAG_ROW
        flag_row = False

        row = {
            "NAME": antenna_name,
            "POSITION": position,
            "OFFSET": offset,
            "DISH_DIAMETER": diameter,
            "TYPE": antenna_type,
            "MOUNT": mount,
            "STATION": station,
            "FLAG_ROW": flag_row,
        }

        yield row


def fill_antenna(msfile: str, hdu: BinTableHDU):
    """Fill MS ANTENNA table.

    Args:
        msfile: Name of MS file.
        hdu: NRO45m psw data in the form of BinTableHDU object.
    """
    fill_ms_table(msfile, hdu, "ANTENNA", _get_antenna_row)
