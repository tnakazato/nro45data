from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Generator

import numpy as np

from .._casa import convert_str_angle_to_rad, datestr2mjd
from .utils import fill_ms_table

if TYPE_CHECKING:
    from astropy.io.fits.hdu.BinTableHDU import BinTableHDU

LOG = logging.getLogger(__name__)


def _get_source_row(hdu: BinTableHDU) -> Generator[dict, None, dict]:
    """Provide source row information.

    Args:
        hdu: NRO45m psw data in the form of BinTableHDU object.

    Yields:
        Dictionary containing source row information.

    Returns:
        Dictionary containing data-dependent column keywords.
    """
    # TIME and INTERVAL
    # use start and end time of the observation
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
    source_time = (end_time + start_time) / 2
    source_interval = end_time - start_time
    LOG.debug("source_time: %s", source_time)
    LOG.debug("source_interval: %s", source_interval)

    # SPECTRAL_WINDOW_ID: single row applies to all spws
    spw_id = -1

    # NUM_LINES: no spectral line information
    num_lines = 0

    # NAME
    source_name = hdu.header["OBJECT"].strip()

    # CALIBRATION_GROUP
    calibration_group = 0

    # CODE
    code = ""

    # DIRECTION
    ra_str = hdu.header["RA"]
    dec_str = hdu.header["DEC"]
    ra = convert_str_angle_to_rad(ra_str)
    dec = convert_str_angle_to_rad(dec_str)
    source_direction = np.array([ra, dec])

    # DIRECTION_REF
    epoch_value = hdu.header["EPOCH"]
    if epoch_value == 1950:
        source_direction_ref = "B1950"
    elif epoch_value == 2000:
        source_direction_ref = "J2000"
    else:
        LOG.warning('Unknown epoch value: %s. Fallback to "ICRS"', epoch_value)
        source_direction_ref = "ICRS"
    LOG.debug("direction_ref: %s", source_direction_ref)

    # POSITION
    source_position = np.zeros(3, dtype=float)

    # PROPER_MOTION
    source_proper_motion = np.zeros(2, dtype=float)

    # SYSVEL
    sysvel = hdu.header["VEL"]
    vref = hdu.header["VREF"].strip()
    if vref == "LSR":
        velocity_ref = "LSRK"
    elif vref == "HEL":
        LOG.warning("HEL is not suppoted. Use BARY.")
        velocity_ref = "BARY"
    elif vref == "GAL":
        velocity_ref = "GALACTO"
    else:
        LOG.warning('Unknown velocity reference value: %s. Fallback to "LSRK"', epoch_value)
        velocity_ref = "LSRK"

    row = {
        "TIME": source_time,
        "INTERVAL": source_interval,
        "SPECTRAL_WINDOW_ID": spw_id,
        "NUM_LINES": num_lines,
        "NAME": source_name,
        "CALIBRATION_GROUP": calibration_group,
        "CODE": code,
        "DIRECTION": source_direction,
        "POSITION": source_position,
        "PROPER_MOTION": source_proper_motion,
        "SYSVEL": sysvel,
    }

    yield row

    column_keywords = {
        "DIRECTION": {"MEASINFO": {"Ref": source_direction_ref}},
        "SYSVEL": {"MEASINFO": {"Ref": velocity_ref}},
    }

    return column_keywords


def fill_source(msfile: str, hdu: BinTableHDU):
    """Fill MS SOURCE table.

    Args:
        msfile: Name of MS file.
        hdu: NRO45m psw data in the form of BinTableHDU object.
    """
    fill_ms_table(msfile, hdu, "SOURCE", _get_source_row)
