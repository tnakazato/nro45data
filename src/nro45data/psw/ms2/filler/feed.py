from __future__ import annotations

import logging
from typing import Generator, TYPE_CHECKING

import numpy as np

from .._casa import datestr2mjd
from .utils import get_array_configuration, fill_ms_table

if TYPE_CHECKING:
    from astropy.io.fits.hdu.BinTableHDU import BinTableHDU

LOG = logging.getLogger(__name__)


def _get_feed_row(hdu: BinTableHDU) -> Generator[dict, None, None]:
    """Provide feed row information.

    Args:
        hdu: NRO45m psw data in the form of BinTableHDU object.

    Yields:
        Dictionary containing feed row information.
    """
    array_conf = get_array_configuration(hdu)
    num_beam = len(np.unique([v[1] for v in array_conf.values()]))

    rx_str = np.unique(hdu.data["RX"])
    poltp_str = np.unique(hdu.data["POLTP"])
    if np.all(poltp_str == ""):
        pol_spec = rx_str[0].strip()[-1]
    else:
        pol_spec = poltp_str[0].strip()[-1]
    if pol_spec in ("H", "V"):
        _pol_type = ["X", "Y"]
    elif pol_spec in ("R", "L"):
        _pol_type = ["R", "L"]
    else:
        # fall back to ["X", "Y"]
        _pol_type = ["X", "Y"]

    for i in range(num_beam):
        # ANTENNA_ID
        antenna_id = i

        # FEED_ID
        feed_id = 0

        # SPECTRAL_WINDOW_ID
        spw_id = -1

        # NUM_RECEPTORS
        num_receptors = 2

        # BEAM_ID
        beam_id = 0

        # TIME and INTERVAL
        history_cards = hdu.header["HISTORY"]
        start_time_card = [x for x in history_cards if x.startswith("NEWSTAR START-TIME")]
        sstr = start_time_card[0].split("=")[-1].strip(" '")
        LOG.debug("sstr: %s", sstr)
        datestr = sstr[0:4] + "/" + sstr[4:6] + "/" + sstr[6:8] + " " + \
            sstr[8:10] + ":" + sstr[10:12] + ":" + sstr[12:14]
        LOG.debug("formatted sstr: %s", datestr)
        start_time = datestr2mjd(datestr) - 9 * 3600
        end_time_card = [x for x in history_cards if x.startswith("NEWSTAR END-TIME")]
        estr = end_time_card[0].split("=")[-1].strip(" '")
        LOG.debug("estr: %s", estr)
        datestr = estr[0:4] + "/" + estr[4:6] + "/" + estr[6:8] + " " + \
            estr[8:10] + ":" + estr[10:12] + ":" + estr[12:14]
        LOG.debug("formatted estr: %s", datestr)
        end_time = datestr2mjd(datestr) - 9 * 3600

        feed_time = (end_time + start_time) / 2
        feed_interval = end_time - start_time

        # BEAM_OFFSET
        beam_offset = np.zeros((2, 2), dtype=float)

        # POLARIZATION_TYPE
        pol_type = np.array(_pol_type)

        # POL_RESPONSE
        pol_response = np.zeros((2, 2), dtype=complex)

        # POSITION
        feed_position = np.zeros(3, dtype=float)

        # RECEPTOR_ANGLE
        receptor_angle = np.zeros(2, dtype=float)

        row = {
            "ANTENNA_ID": antenna_id,
            "FEED_ID": feed_id,
            "SPECTRAL_WINDOW_ID": spw_id,
            "TIME": feed_time,
            "INTERVAL": feed_interval,
            "NUM_RECEPTORS": num_receptors,
            "BEAM_ID": beam_id,
            "BEAM_OFFSET": beam_offset,
            "POLARIZATION_TYPE": pol_type,
            "POL_RESPONSE": pol_response,
            "POSITION": feed_position,
            "RECEPTOR_ANGLE": receptor_angle,
        }

        yield row


def fill_feed(msfile: str, hdu: BinTableHDU):
    """Fill MS FEED table.

    Args:
        msfile: Name of MS file.
        hdu: NRO45m psw data in the form of BinTableHDU object.
    """
    fill_ms_table(msfile, hdu, "FEED", _get_feed_row)
