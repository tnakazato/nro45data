import logging
from typing import TYPE_CHECKING

import numpy as np

from .._casa import open_table
from .._casa import convert_str_angle_to_rad
from .utils import fix_nrow_to

if TYPE_CHECKING:
    from astropy.io.fits.hdu.BinTableHDU import BinTableHDU

LOG = logging.getLogger(__name__)


def _get_field_columns(hdu: "BinTableHDU") -> dict:
    # NAME
    field_name = hdu.header["OBJECT"].strip()
    LOG.debug("field_name: %s", field_name)

    # CODE
    field_code = ""

    # TIME
    # use start time of the observation
    history_cards = hdu.header["HISTORY"]
    start_time_card = [x for x in history_cards if x.startswith("NEWSTAR START-TIME")]
    field_time = float(start_time_card[0].split("=")[-1].strip(" '"))
    LOG.debug("field_time: %s", field_time)

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

    columns = {
        "NAME": field_name,
        "CODE": field_code,
        "TIME": field_time,
        "NUM_POLY": num_poly,
        "FIELD_EPOCH": field_epoch,
        "DELAY_DIR": delay_dir,
        "PHASE_DIR": phase_dir,
        "REFERENCE_DIR": reference_dir,
        "SOURCE_ID": source_id,
        "FLAG_ROW": flag_row,
    }

    return columns


def _fill_field_columns(msfile: str, columns: dict):
    with open_table(msfile + "/FIELD", read_only=False) as tb:
        fix_nrow_to(1, tb)

        tb.putcell("NAME", 0, columns["NAME"])
        tb.putcell("CODE", 0, columns["CODE"])
        tb.putcell("TIME", 0, columns["TIME"])
        tb.putcell("NUM_POLY", 0, columns["NUM_POLY"])
        tb.putcell("DELAY_DIR", 0, columns["DELAY_DIR"])
        colkeywords = tb.getcolkeywords("DELAY_DIR")
        colkeywords["MEASINFO"]["Ref"] = columns["FIELD_EPOCH"]
        tb.putcolkeywords("DELAY_DIR", colkeywords)
        tb.putcell("PHASE_DIR", 0, columns["PHASE_DIR"])
        tb.putcolkeywords("PHASE_DIR", colkeywords)
        tb.putcell("REFERENCE_DIR", 0, columns["REFERENCE_DIR"])
        tb.putcolkeywords("REFERENCE_DIR", colkeywords)
        tb.putcell("SOURCE_ID", 0, columns["SOURCE_ID"])
        tb.putcell("FLAG_ROW", 0, columns["FLAG_ROW"])
