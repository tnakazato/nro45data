from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Generator

from .utils import get_intent_map, fill_ms_table

if TYPE_CHECKING:
    from astropy.io.fits.hdu.BinTableHDU import BinTableHDU

LOG = logging.getLogger(__name__)


def _get_state_row(hdu: BinTableHDU) -> Generator[dict, None, None]:
    """Provide state row information.

    Args:
        hdu: NRO45m psw data in the form of BinTableHDU object.

    Yields:
        Dictionary containing state row information.
    """
    iscn = hdu.data["ISCN"]
    scntp = hdu.data["SCNTP"]
    intent_map = get_intent_map(iscn, scntp)
    inverted_map = dict((v, k) for k, v in intent_map.items())

    cal = 0
    load = 0

    for state_id in range(len(inverted_map)):
        sub_scan = state_id
        intent = inverted_map[state_id]
        if intent == "ZERO":
            obs_mode = "ZERO"
            sig = False
            ref = True
            flag_row = False
        elif intent == "ON":
            obs_mode = "OBSERVE_TARGET#ON_SOURCE"
            sig = True
            ref = False
            flag_row = False
        elif intent == "OFF":
            obs_mode = "OBSERVE_TARGET#OFF_SOURCE"
            sig = False
            ref = True
            flag_row = False
        else:
            obs_mode = "UNKNOWN"
            sig = False
            ref = False
            flag_row = True

        row = {
            "SIG": sig,
            "REF": ref,
            "CAL": cal,
            "LOAD": load,
            "SUB_SCAN": sub_scan,
            "OBS_MODE": obs_mode,
            "FLAG_ROW": flag_row,
        }

        yield row


def fill_state(msfile: str, hdu: BinTableHDU):
    """Fill MS STATE table.

    Args:
        msfile: Name of MS file.
        hdu: NRO45m psw data in the form of BinTableHDU object.
    """
    fill_ms_table(msfile, hdu, "STATE", _get_state_row)
