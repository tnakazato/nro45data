import logging
from typing import TYPE_CHECKING, Generator

import numpy as np

from .._casa import convert_str_angle_to_rad, open_table

if TYPE_CHECKING:
    from astropy.io.fits.hdu.BinTableHDU import BinTableHDU

LOG = logging.getLogger(__name__)


def _get_source_row(hdu: 'BinTableHDU') -> Generator[dict, None, None]:
    # TIME and INTERVAL
    # use start and end time of the observation
    history_cards = hdu.header['HISTORY']
    start_time_card = [x for x in history_cards if x.startswith('NEWSTAR START-TIME')]
    source_start_time = float(start_time_card[0].split('=')[-1].strip(" '"))
    end_time_card = [x for x in history_cards if x.startswith('NEWSTAR END-TIME')]
    source_end_time = float(end_time_card[0].split('=')[-1].strip(" '"))
    source_time = (source_end_time + source_start_time) / 2
    source_interval = source_end_time - source_start_time
    LOG.debug('source_time: %s', source_time)
    LOG.debug('source_interval: %s', source_interval)

    # SPECTRAL_WINDOW_ID: single row applies to all spws
    spw_id = -1

    # NUM_LINES: no spectral line information
    num_lines = 0

    # NAME
    source_name = hdu.header['OBJECT'].strip()

    # CALIBRATION_GROUP
    calibration_group = 0

    # CODE
    code = ''

    # DIRECTION
    ra_str = hdu.header['RA']
    dec_str = hdu.header['DEC']
    ra = convert_str_angle_to_rad(ra_str)
    dec = convert_str_angle_to_rad(dec_str)
    source_direction = np.array([ra, dec])

    # DIRECTION_REF
    epoch_value = hdu.header['EPOCH']
    if epoch_value == 1950:
        source_direction_ref = 'B1950'
    elif epoch_value == 2000:
        source_direction_ref = 'J2000'
    else:
        LOG.warning('Unknown epoch value: %s. Fallback to "ICRS"', epoch_value)
        source_direction_ref = 'ICRS'
    LOG.debug('direction_ref: %s', source_direction_ref)

    # POSITION
    source_position = np.zeros(3, dtype=float)

    # PROPER_MOTION
    source_proper_motion = np.zeros(2, dtype=float)

    # SYSVEL
    sysvel = hdu.header['VEL']
    vref = hdu.header['VREF'].strip()
    if vref == 'LSR':
        velocity_ref = 'LSRK'
    elif vref == 'HEL':
        LOG.warning('HEL is not suppoted. Use BARY.')
        velocity_ref = 'BARY'
    elif vref == 'GAL':
        velocity_ref = 'GALACTO'
    else:
        LOG.warning('Unknown velocity reference value: %s. Fallback to "LSRK"', epoch_value)
        velocity_ref = 'LSRK'

    row = {
        'TIME': source_time,
        'INTERVAL': source_interval,
        'SPECTRAL_WINDOW_ID': spw_id,
        'NUM_LINES': num_lines,
        'NAME': source_name,
        'CALIBRATION_GROUP': calibration_group,
        'CODE': code,
        'DIRECTION': source_direction,
        'DIRECTION_REF': source_direction_ref,
        'POSITION': source_position,
        'PROPER_MOTION': source_proper_motion,
        'SYSVEL': sysvel,
        'VELOCITY_REF': velocity_ref,
        # 'VELOCITY_DEF': velocity_def
    }

    yield row


def fill_source(msfile: str, hdu: 'BinTableHDU'):
    row_iterator = _get_source_row(hdu)
    with open_table(msfile + '/SOURCE', read_only=False) as tb:
        for row_id, row in enumerate(row_iterator):
            if tb.nrows() <= row_id:
                tb.addrows(tb.nrows() - row_id + 1)

            for key, value in row.items():
                if key == 'DIRECTION_REF':
                    colkeywords = tb.getcolkeywords('DIRECTION')
                    if colkeywords['MEASINFO']['Ref'] != value:
                        colkeywords['MEASINFO']['Ref'] = value
                        tb.putcolkeywords('DIRECTION', colkeywords)
                elif key == 'VELOCITY_REF':
                    colkeywords = tb.getcolkeywords('SYSVEL')
                    if colkeywords['MEASINFO']['Ref'] != value:
                        colkeywords['MEASINFO']['Ref'] = value
                        tb.putcolkeywords('SYSVEL', colkeywords)
                else:
                    tb.putcell(key, row_id, value)
            LOG.debug('source table %d row %s', row_id, row)
