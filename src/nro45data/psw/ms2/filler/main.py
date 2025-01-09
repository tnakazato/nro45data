import logging
from typing import TYPE_CHECKING, Generator

import numpy as np

from .._casa import convert_str_angle_to_rad, open_table
from .utils import get_array_configuration, get_data_description_map

if TYPE_CHECKING:
    from astropy.io.fits.hdu.BinTableHDU import BinTableHDU

LOG = logging.getLogger(__name__)


def _get_main_row(hdu: 'BinTableHDU') -> Generator[dict, None, None]:
    array_conf = get_array_configuration(hdu)
    dd_dict, array_dd_map, spw_map, pol_map = get_data_description_map(array_conf)

    mjdst = hdu.data['MJDST']
    mjdet = hdu.data['MJDET']
    arryt = np.array([a.strip() for a in hdu.data['ARRYT']])
    multn = hdu.data['MULTN']
    integ = hdu.data['INTEG']
    iscn = hdu.data['ISCN']


    beam_list = sorted(set(multn))
    unique_time = np.unique(mjdst)

    for t in unique_time:
        rows = np.where(mjdst == t)[0]

        main_start_time = mjdst[rows[0]]
        main_end_time = mjdet[rows[0]]
        main_mid_time = (main_end_time + main_start_time) / 2
        main_nominal_interval = main_end_time - main_start_time

        array_sub_list = arryt[rows].tolist()
        integ_sug_list = integ[rows]

        for dd_id, (_, conf) in enumerate(array_conf.items()):
            _, _, nchan = conf[0]
            array_list = conf[3]
            dd_rows = [
                rows[array_sub_list.index(a)] if a in array_sub_list else -1
                for a in array_list
            ]
            npol = len(dd_rows)

            # TIME
            time_midpoint = main_mid_time

            # ANTENNA1
            beam_number = conf[1]
            antenna1 = beam_list.index(beam_number)

            # ANTENNA2
            antenna2 = antenna1

            # FEED1: always 0
            feed1 = 0

            # FEED2: always 0
            feed2 = 0

            # DATA_DESC_ID
            data_desc_id = dd_id

            # PROCESSOR_ID
            processor_id = 'TODO'

            # FIELD_ID: always 0
            field_id = 0

            # INTERVAL
            interval = main_nominal_interval

            # EXPOSURE
            if all([x == -1 for x in dd_rows]):
                exposure = time_midpoint
            else:
                idx = [x for x in dd_rows if x != -1]
                exposure = iscn[idx]

            # TIME_CENTROID
            time_centroid = time_midpoint

            # SCAN_NUMBER
            if all([x == -1 for x in dd_rows]):
                scan_number = 0
            else:
                idx = [x for x in dd_rows if x != -1]
                scan_number = iscn[idx]

            # ARRAY_ID: always 0
            array_id = 0

            # OBSERVATION_ID: always 0
            observation_id = 0

            # STATE_ID

            # UVW: always [0, 0, 0]
            uvw = np.zeros(3, dtype=float)

            # FLOAT_DATA
            float_data = np.zeros((npol, nchan), dtype=float)

            # SIGMA
            sigma = np.zeros(npol, dtype=float)

            # WEIGHT
            weight = 1 / np.square(sigma)

            # FLAG
            flag = np.zeros((npol, nchan), dtype=bool)

            # FLAG_ROW
            flag_row = False

            row = {

            }

            yield row


def fill_main(msfile: str, hdu: 'BinTableHDU'):
    row_iterator = _get_main_row(hdu)
    with open_table(msfile, read_only=False) as tb:
        for row_id, row in enumerate(row_iterator):
            if tb.nrows() <= row_id:
                tb.addrows(tb.nrows() - row_id + 1)

            for key, value in row.items():
                tb.putcell(key, row_id, value)
            LOG.debug('main table %d row %s', row_id, row)