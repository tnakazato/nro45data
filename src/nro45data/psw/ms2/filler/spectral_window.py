from __future__ import annotations

import collections
import logging
from typing import TYPE_CHECKING, Generator

import numpy as np

from .._casa import open_table
from .utils import get_array_configuration, get_data_description_map

if TYPE_CHECKING:
    import astropy.io.fits as fits
    BinTableHDU = fits.BinTableHDU

LOG = logging.getLogger(__name__)


def _get_frequency_spec(hdu: BinTableHDU, row_id: int) -> tuple[np.ndarray, np.ndarray, int]:
    data = hdu.data
    center_freq = data["F0CAL"][row_id]
    chwid = data["CHWID"][row_id]
    nch = data["NCH"][row_id]
    sidbd = data["SIDBD"][row_id]

    if sidbd == "USB":
        net_sideband = 1
    elif sidbd == "LSB":
        net_sideband = -1
    else:  # DSB
        net_sideband = 0

    if net_sideband < 0:  # LSB
        chan_freq = np.array([chwid * ((nch - 1) / 2 - i) + center_freq for i in range(nch)], dtype=float)
        chan_width = np.ones(nch, dtype=float) * (-chwid)
    else:  # USB or DSB
        chan_freq = np.array([chwid * (i - (nch - 1) / 2) + center_freq for i in range(nch)], dtype=float)
        chan_width = np.ones(nch, dtype=float) * chwid

    return chan_freq, chan_width, net_sideband


def _get_spectral_window_row(hdu: BinTableHDU, array_conf: dict) -> Generator[dict, None, None]:
    ddd, adm, spw_map, _ = get_data_description_map(array_conf)

    data = hdu.data
    arry = data["ARRYT"]
    nch = data["NCH"]

    num_spw = len(spw_map)

    spw_dd_map = collections.defaultdict(list)
    for dd_id, (spw_id, _) in ddd.items():
        spw_dd_map[spw_id].append(dd_id)

    dd_array_map = collections.defaultdict(list)
    for array, dd_id in adm.items():
        dd_array_map[dd_id].append(array)

    for spw_id in range(num_spw):
        dd_id = spw_dd_map[spw_id][0]
        array = dd_array_map[dd_id][0]
        i = np.where(arry == array)[0][0]
        meas_freq_ref = 1  # LSRK

        array_list = []
        for _dd_id in spw_dd_map[spw_id]:
            for _array in dd_array_map[_dd_id]:
                array_list.append(_array)

        spw_name = "_".join(array_list)

        chan_freq, chan_width, net_sideband = _get_frequency_spec(hdu, i)
        nchan = len(chan_freq)
        assert nchan == nch[i]

        ref_freq = chan_freq[0]  # frequency of the first channel
        spectral_window_row = {
            "NUM_CHAN": nchan,
            "NAME": spw_name,
            "REF_FREQUENCY": ref_freq,
            "CHAN_FREQ": chan_freq,
            "CHAN_WIDTH": chan_width,
            "MEAS_FREQ_REF": meas_freq_ref,
            "EFFECTIVE_BW": chan_width,
            "RESOLUTION": chan_width,
            "TOTAL_BANDWIDTH": sum(chan_width),
            "NET_SIDEBAND": net_sideband,
            "IF_CONV_CHAIN": 0,
            "FLAG_ROW": False,
        }

        yield spectral_window_row


def fill_spectral_window(msfile: str, hdu: BinTableHDU):
    array_conf = get_array_configuration(hdu)
    row_iterator = _get_spectral_window_row(hdu, array_conf)
    with open_table(msfile + "/SPECTRAL_WINDOW", read_only=False) as tb:
        for spw_id, row in enumerate(row_iterator):
            if tb.nrows() <= spw_id:
                tb.addrows()
            for key, value in row.items():
                tb.putcell(key, spw_id, value)
            LOG.debug("spw %d row %s", spw_id, row)
