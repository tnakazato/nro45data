import logging
from typing import TYPE_CHECKING

import numpy as np

from .._casa import open_table
from .utils import fix_nrow_to, get_array_configuration

if TYPE_CHECKING:
    from astropy.io.fits.hdu.BinTableHDU import BinTableHDU

LOG = logging.getLogger(__name__)


def _get_feed_columns(hdu: "BinTableHDU") -> dict:
    array_conf = get_array_configuration(hdu)
    num_beam = len(np.unique([v[1] for v in array_conf.values()]))

    antenna_id = np.arange(num_beam, dtype=int)

    feed_id = np.zeros(num_beam, dtype=int)

    spw_id = np.ones(num_beam, dtype=int) * -1

    num_receptors = np.ones(num_beam, dtype=int) * 2

    beam_id = np.zeros(num_beam, dtype=int)

    history_cards = hdu.header["HISTORY"]
    start_time_card = [x for x in history_cards if x.startswith("NEWSTAR START-TIME")]
    start_time = float(start_time_card[0].split("=")[-1].strip(" '"))
    end_time_card = [x for x in history_cards if x.startswith("NEWSTAR END-TIME")]
    end_time = float(end_time_card[0].split("=")[-1].strip(" '"))
    feed_time = np.ones(num_beam, dtype=int) * (end_time + start_time) / 2
    feed_interval = np.ones(num_beam, dtype=int) * (end_time - start_time)

    beam_offset = [np.zeros((2, 2), dtype=float) for _ in range(num_beam)]

    rx_str = np.unique(hdu.data["RX"])
    if rx_str[0][-1] in ("H", "V"):
        _pol_type = ["X", "Y"]
    elif rx_str[0][-1] in ("R", "L"):
        _pol_type = ["R", "L"]
    else:
        # fall back to ["X", "Y"]
        _pol_type = ["X", "Y"]
    pol_type = [np.array(_pol_type) for _ in range(num_beam)]

    pol_response = [np.zeros((2, 2), dtype=complex) for _ in range(num_beam)]

    feed_position = [np.zeros(3, dtype=float) for _ in range(num_beam)]

    receptor_angle = [np.zeros(2, dtype=float) for _ in range(num_beam)]

    columns = {
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

    return columns


def _fill_feed_columns(msfile: str, columns: dict):
    with open_table(msfile + "/FEED", read_only=False) as tb:
        num_feed = len(columns["ANTENNA_ID"])
        fix_nrow_to(num_feed, tb)

        tb.putcol("ANTENNA_ID", columns["ANTENNA_ID"])
        tb.putcol("FEED_ID", columns["FEED_ID"])
        tb.putcol("SPECTRAL_WINDOW_ID", columns["SPECTRAL_WINDOW_ID"])
        tb.putcol("TIME", columns["TIME"])
        tb.putcol("INTERVAL", columns["INTERVAL"])
        tb.putcol("NUM_RECEPTORS", columns["NUM_RECEPTORS"])
        tb.putcol("BEAM_ID", columns["BEAM_ID"])

        for i in range(num_feed):
            tb.putcell("BEAM_OFFSET", i, columns["BEAM_OFFSET"][i])
            tb.putcell("POLARIZATION_TYPE", i, columns["POLARIZATION_TYPE"][i])
            tb.putcell("POL_RESPONSE", i, columns["POL_RESPONSE"][i])
            tb.putcell("POSITION", i, columns["POSITION"][i])
            tb.putcell("RECEPTOR_ANGLE", i, columns["RECEPTOR_ANGLE"][i])
