import logging
from typing import TYPE_CHECKING, Generator

import numpy as np

from .._casa import open_table
from .utils import get_intent_map

if TYPE_CHECKING:
    from astropy.io.fits.hdu.BinTableHDU import BinTableHDU

LOG = logging.getLogger(__name__)


def _get_state_row(hdu: 'BinTableHDU') -> Generator[dict, None, None]:
    iscn = hdu.data['ISCN']
    scntp = hdu.data['SCNTP']
    intent_map = get_intent_map(iscn, scntp)
    inverted_map = dict((v, k) for k, v in intent_map.items())

    cal = 0
    load = 0

    for state_id in range(len(inverted_map)):
        sub_scan = state_id
        intent = inverted_map[state_id]
        if intent == 'ZERO':
            obs_mode = 'ZERO'
            sig = False
            ref = True
            flag_row = False
        elif intent == 'ON':
            obs_mode = 'OBSERVE_TARGET#ON_SOURCE'
            sig = True
            ref = False
            flag_row = False
        elif intent == 'OFF':
            obs_mode = 'OBSERVE_TARGET#OFF_SOURCE'
            sig = False
            ref = True
            flag_row = False
        else:
            obs_mode = 'UNKNOWN'
            sig = False
            ref = False
            flag_row = True

        row = {
            'SIG': sig,
            'REF': ref,
            'CAL': cal,
            'LOAD': load,
            'SUB_SCAN': sub_scan,
            'OBS_MODE': obs_mode,
            'FLAG_ROW': flag_row
        }

        yield row


def fill_state(msfile: str, hdu: 'BinTableHDU'):
    row_iterator = _get_state_row(hdu)
    with open_table(msfile + '/STATE', read_only=False) as tb:
        for row_id, row in enumerate(row_iterator):
            if tb.nrows() <= row_id:
                tb.addrows(tb.nrows() - row_id + 1)

            for k, v in row.items():
                tb.putcell(k, row_id, v)
            LOG.debug('state table %d row %s', row_id, row)