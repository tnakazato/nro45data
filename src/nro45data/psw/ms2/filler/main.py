from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Generator

import numpy as np

from .._casa import open_table
from .utils import get_array_configuration, get_data_description_map, get_intent_map, get_processor_map

if TYPE_CHECKING:
    import astropy.io.fits as fits
    BinTableHDU = fits.BinTableHDU

LOG = logging.getLogger(__name__)


def _get_main_row(hdu: BinTableHDU) -> Generator[dict, None, None]:
    array_conf = get_array_configuration(hdu)
    dd_dict, array_dd_map, spw_map, pol_map = get_data_description_map(array_conf)

    mjdst = hdu.data["MJDST"]
    mjdet = hdu.data["MJDET"]
    arryt = np.array([a.strip() for a in hdu.data["ARRYT"]])
    multn = hdu.data["MULTN"]
    # integ = hdu.data['INTEG']
    iscn = hdu.data["ISCN"]
    scntp = hdu.data["SCNTP"]
    bebw = hdu.data["BEBW"]
    sfctr = hdu.data["SFCTR"]
    adoff = hdu.data["ADOFF"]
    ldata = hdu.data["LDATA"]

    intent_map = get_intent_map(iscn, scntp)

    arry1 = str(hdu.header["ARRY1"]).strip()
    arry2 = str(hdu.header["ARRY2"]).strip()
    arry3 = str(hdu.header["ARRY3"]).strip()
    arry4 = str(hdu.header["ARRY4"]).strip()
    _, processor_id_map = get_processor_map(arry1, arry2, arry3, arry4)

    beam_list = sorted(set(multn))
    unique_time = np.unique(mjdst)

    for t in unique_time:
        rows = np.where(mjdst == t)[0]

        main_start_time = mjdst[rows[0]]
        main_end_time = mjdet[rows[0]]
        main_mid_time = (main_end_time + main_start_time) / 2
        main_nominal_interval = main_end_time - main_start_time

        array_sub_list = arryt[rows].tolist()

        for _, conf in array_conf.items():
            _, _, nchan = conf[0]
            array_list = conf[3]
            dd_id_list = set([array_dd_map[_a] for _a in array_list])
            if not len(dd_id_list) == 1:
                raise RuntimeError(f"Mismatch of DATA_DESC_ID in dual-pol data: array {array_list}")

            dd_id = dd_id_list.pop()
            dd_rows = [rows[array_sub_list.index(a)] if a in array_sub_list else -1 for a in array_list]
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
            _pid = set(processor_id_map.find(a[0]) for a in array_list)
            assert len(_pid) == 1
            processor_id = _pid.pop()

            # FIELD_ID: always 0
            field_id = 0

            # INTERVAL
            interval = main_nominal_interval

            # EXPOSURE
            if all([x == -1 for x in dd_rows]):
                exposure = 0
            else:
                idx = [x for x in dd_rows if x != -1]
                exposure = interval

            # TIME_CENTROID
            time_centroid = time_midpoint

            # SCAN_NUMBER
            if all([x == -1 for x in dd_rows]):
                scan_number = 0
            else:
                idx = [x for x in dd_rows if x != -1]
                _scan_number = set(iscn[idx])
                assert len(_scan_number) == 1
                scan_number = _scan_number.pop()

            # ARRAY_ID: always 0
            array_id = 0

            # OBSERVATION_ID: always 0
            observation_id = 0

            # STATE_ID
            if all([x == -1 for x in dd_rows]):
                state_id = -1
            else:
                idx = [x for x in dd_rows if x != -1]
                scan_intent = set(scntp[idx])
                assert len(scan_intent) == 1
                state_id = intent_map[scan_intent.pop()]

            # UVW: always [0, 0, 0]
            uvw = np.zeros(3, dtype=float)

            # FLOAT_DATA
            float_data = np.zeros((npol, nchan), dtype=float)

            # FLAG
            flag = np.zeros((npol, nchan), dtype=bool)

            for ipol, _row in enumerate(dd_rows):
                if _row == -1:
                    # invalid data
                    flag[ipol, :] = True
                else:
                    # valid data
                    scaling_factor = sfctr[_row]
                    offset_value = adoff[_row]
                    quantized = ldata[_row, :]
                    assert len(quantized) == nchan
                    float_data[ipol] = scaling_factor * quantized + offset_value

            # SIGMA
            sigma = np.zeros(npol, dtype=float)
            for ipol, _row in enumerate(dd_rows):
                if _row != -1:
                    bw = bebw[_row]
                    sigma[ipol] = 1 / np.sqrt(2 * bw * interval)

            # WEIGHT
            weight = np.array([1 / (s * s) if s else 0 for s in sigma])

            # FLAG_ROW
            flag_row = False

            row = {
                "TIME": time_midpoint,
                "ANTENNA1": antenna1,
                "ANTENNA2": antenna2,
                "FEED1": feed1,
                "FEED2": feed2,
                "DATA_DESC_ID": data_desc_id,
                "PROCESSOR_ID": processor_id,
                "FIELD_ID": field_id,
                "INTERVAL": interval,
                "EXPOSURE": exposure,
                "TIME_CENTROID": time_centroid,
                "SCAN_NUMBER": scan_number,
                "ARRAY_ID": array_id,
                "OBSERVATION_ID": observation_id,
                "STATE_ID": state_id,
                "UVW": uvw,
                "FLOAT_DATA": float_data,
                "FLAG": flag,
                "SIGMA": sigma,
                "WEIGHT": weight,
                "FLAG_ROW": flag_row,
            }

            yield row


def fill_main(msfile: str, hdu: BinTableHDU):
    row_iterator = _get_main_row(hdu)
    with open_table(msfile, read_only=False) as tb:
        for row_id, row in enumerate(row_iterator):
            if tb.nrows() <= row_id:
                tb.addrows(tb.nrows() - row_id + 1)

            for key, value in row.items():
                LOG.debug("row %d key %s", row_id, key)
                tb.putcell(key, row_id, value)
            LOG.debug("main table %d row %s", row_id, row)
