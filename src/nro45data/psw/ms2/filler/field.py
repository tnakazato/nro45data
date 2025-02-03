from __future__ import annotations

import logging
from typing import Generator, TYPE_CHECKING

import numpy as np

from .._casa import datestr2mjd
from .._casa import convert_str_angle_to_rad
from .utils import fill_ms_table

if TYPE_CHECKING:
    from astropy.io.fits.hdu.BinTableHDU import BinTableHDU

LOG = logging.getLogger(__name__)


def _get_field_row(hdu: BinTableHDU) -> Generator[dict, None, dict]:
    """Provide field row information.

    Args:
        hdu: NRO45m psw data in the form of BinTableHDU object.

    Yields:
        Dictionary containing field row information.

    Returns:
        Dictionary containing data-dependent column keywords.
    """
    # NAME
    field_name = hdu.header["OBJECT"].strip()
    LOG.debug("field_name: %s", field_name)

    # CODE
    field_code = ""

    # TIME
    # use start time of the observation
    history_cards = hdu.header["HISTORY"]
    start_time_card = [x for x in history_cards if x.startswith("NEWSTAR START-TIME")]
    sstr = start_time_card[0].split("=")[-1].strip(" '")
    LOG.debug("sstr: %s", sstr)
    datestr = sstr[0:4] + "/" + sstr[4:6] + "/" + sstr[6:8] + " " + sstr[8:10] + ":" + sstr[10:12] + ":" + sstr[12:14]
    LOG.debug("formatted sstr: %s", datestr)
    field_time = datestr2mjd(datestr) - 9 * 3600

    # NUM_POLY
    num_poly = 0

    # FIELD EPOCH
    epoch_value = hdu.header["EPOCH"]
    if epoch_value == 1950:
        field_epoch = "B1950"
    elif epoch_value == 2000:
        field_epoch = "J2000"
    else:
        LOG.warning('Unknown epoch value: %s. Fallback to "ICRS"', epoch_value)
        field_epoch = "ICRS"
    LOG.debug("field_epoch: %s", field_epoch)

    # DELAY_DIR
    ra_str = hdu.header["RA"]
    dec_str = hdu.header["DEC"]
    ra = convert_str_angle_to_rad(ra_str)
    dec = convert_str_angle_to_rad(dec_str)
    delay_dir = np.array([[ra, dec]])
    LOG.debug("field direction: %s", delay_dir)

    # PHASE_DIR
    phase_dir = delay_dir

    # REFERENCE_DIR
    reference_dir = delay_dir

    # SOURCE_ID
    source_id = 0

    # FLAG_ROW
    flag_row = False

    row = {
        "NAME": field_name,
        "CODE": field_code,
        "TIME": field_time,
        "NUM_POLY": num_poly,
        "DELAY_DIR": delay_dir,
        "PHASE_DIR": phase_dir,
        "REFERENCE_DIR": reference_dir,
        "SOURCE_ID": source_id,
        "FLAG_ROW": flag_row,
    }

    yield row

    column_keywords = {
        "DELAY_DIR": {"MEASINFO": {"Ref": field_epoch}},
        "PHASE_DIR": {"MEASINFO": {"Ref": field_epoch}},
        "REFERENCE_DIR": {"MEASINFO": {"Ref": field_epoch}}
    }

    return column_keywords  # noqa


def fill_field(msfile: str, hdu: BinTableHDU):
    """Fill MS FIELD table.

    Args:
        msfile: Name of MS file.
        hdu: NRO45m psw data in the form of BinTableHDU object.
    """
    fill_ms_table(msfile, hdu, "FIELD", _get_field_row)
