from __future__ import annotations

import logging
from typing import Generator, TYPE_CHECKING

from .utils import fill_ms_table

if TYPE_CHECKING:
    from astropy.io.fits.hdu.BinTableHDU import BinTableHDU

LOG = logging.getLogger(__name__)


def _get_processor_row(hdu: BinTableHDU) -> Generator[dict, None, None]:
    """Provide processor row information.

    Args:
        hdu: NRO45m psw data in the form of BinTableHDU object.

    Yields:
        Dictionary containing processor row information.
    """
    # TYPE
    processor_type = "SPECTROMETER"

    # SUB_TYPE
    processor_sub_type_list = []
    # AOS-High
    arry1 = hdu.header["ARRY1"].strip()
    if arry1.find("1") >= 0:
        processor_sub_type_list.append("AOS-High")

    # AOS-Wide 1-10 (0-9)
    # AOS-Ultrawide 1-5 (10-15)
    # FX 1-5? (16-20)
    arry2 = hdu.header["ARRY2"].strip()
    if arry2[:10].find("1") >= 0:
        processor_sub_type_list.append("AOS-Wide")

    if arry2[10:15].find("1") >= 0:
        processor_sub_type_list.append("AOS-Ultrawide")

    if arry2[15:20].find("1") >= 0:
        processor_sub_type_list.append("FX")

    # AC45
    arry3 = hdu.header["ARRY3"].strip()
    arry4 = hdu.header["ARRY4"].strip()
    if (arry3 + arry4).find("1") >= 0:
        processor_sub_type_list.append("AC45")

    processor_sub_type = ",".join(processor_sub_type_list)

    LOG.debug("processor_sub_type_list: %s", processor_sub_type_list)
    LOG.debug("arr1: %s", arry1)
    LOG.debug("arry2: %s", arry2)
    LOG.debug("arry3: %s", arry3)
    LOG.debug("arry4: %s", arry4)

    # TYPE_ID
    processor_type_id = 0

    # MODE_ID
    processor_mode_id = 0

    # FLAG_ROW
    flag_row = False

    row = {
        "TYPE": processor_type,
        "SUB_TYPE": processor_sub_type,
        "TYPE_ID": processor_type_id,
        "MODE_ID": processor_mode_id,
        "FLAG_ROW": flag_row,
    }

    yield row


def fill_processor(msfile: str, hdu: BinTableHDU):
    """Fill MS PROCESSOR table.

    Args:
        msfile: Name of MS file.
        hdu: NRO45m psw data in the form of BinTableHDU object.
    """
    fill_ms_table(msfile, hdu, "PROCESSOR", _get_processor_row)
