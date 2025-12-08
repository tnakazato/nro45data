from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Generator

import numpy as np

from .._casa import open_table
from .utils import get_array_configuration, get_data_description_map

if TYPE_CHECKING:
    import astropy.io.fits as fits
    BinTableHDU = fits.BinTableHDU

LOG = logging.getLogger(__name__)


def _get_syscal_row(hdu: BinTableHDU) -> Generator[dict, None, None]:
    array_conf = get_array_configuration(hdu)
    dd_dict, array_dd_map, spw_map, pol_map = get_data_description_map(array_conf)

    mjdst = hdu.data["MJDST"]
    mjdet = hdu.data["MJDET"]
    arryt = np.array([a.strip() for a in hdu.data["ARRYT"]])
    tsys = hdu.data["TSYS"]
    multn = hdu.data["MULTN"]

    beam_list = sorted(set(multn))
    unique_time = np.unique(mjdst)

    for t in unique_time:
        rows = np.where(mjdst == t)[0]

        syscal_start_time = mjdst[rows[0]]
        syscal_end_time = mjdet[rows[0]]
        syscal_mid_time = (syscal_end_time + syscal_start_time) / 2
        syscal_nominal_interval = syscal_end_time - syscal_start_time

        array_sub_list = arryt[rows].tolist()
        LOG.info("array_sub_list %s", array_sub_list)
        tsys_sub_list = tsys[rows]

        for _, conf in array_conf.items():
            spw_conf, beam, pol_list, array_list = conf

            # ANTENNA_ID: beam_id
            beam_number = conf[1]
            antenna_id = beam_list.index(beam_number)

            # FEED_ID: always 0
            feed_id = 0

            # DATA_DESC_ID
            dd_id_set = set(array_dd_map[a] for a in array_list)
            assert len(dd_id_set) == 1
            dd_id = dd_id_set.pop()

            # SPECTRAL_WINDOW_ID
            spw_id = dd_dict[dd_id][0]

            # TIME
            syscal_time = syscal_mid_time

            # INTERVAL
            syscal_interval = syscal_nominal_interval

            # TSYS_SPECTRUM
            # spw_conf = conf[0]
            nchan = spw_conf[2]
            # array_list = conf[3]
            npol = len(array_list)
            tsys_spectrum = np.zeros((npol, nchan), dtype=float)
            tsys_flag_per_pol = np.zeros(npol, dtype=bool)
            for ipol, a in enumerate(array_list):
                LOG.info("examining %s", a)
                if a in array_sub_list:
                    idx = array_sub_list.index(a)
                    tsys_spectrum[ipol] = tsys_sub_list[idx]
                else:
                    tsys_flag_per_pol[ipol] = True

            # TSYS_FLAG
            tsys_flag = bool(np.any(tsys_flag_per_pol))

            row = {
                "ANTENNA_ID": antenna_id,
                "FEED_ID": feed_id,
                "SPECTRAL_WINDOW_ID": spw_id,
                "TIME": syscal_time,
                "INTERVAL": syscal_interval,
                "TSYS_SPECTRUM": tsys_spectrum,
                "TSYS_FLAG": tsys_flag,
            }

            yield row


def fill_syscal(msfile: str, hdu: BinTableHDU):
    row_iterator = _get_syscal_row(hdu)
    with open_table(msfile + "/SYSCAL", read_only=False) as tb:
        for row_id, row in enumerate(row_iterator):
            if tb.nrows() <= row_id:
                tb.addrows(tb.nrows() - row_id + 1)

            for key, value in row.items():
                LOG.debug("row_id %d key %s value %s (type %s)", row_id, key, value, type(value))
                tb.putcell(key, row_id, value)
            LOG.debug("syscal table %d row %s", row_id, row)
