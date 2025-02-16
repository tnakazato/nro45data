import collections
import logging
from typing import TYPE_CHECKING, Generator

import numpy as np

from .utils import fill_ms_table, get_array_configuration, get_data_description_map

if TYPE_CHECKING:
    from astropy.io.fits.hdu.BinTableHDU import BinTableHDU

LOG = logging.getLogger(__name__)


def _get_spectral_window_row(hdu: "BinTableHDU") -> Generator[dict, None, None]:
    array_conf = get_array_configuration(hdu)
    ddd, adm, spw_map, _ = get_data_description_map(array_conf)

    data = hdu.data
    arry = data["ARRYT"]
    f0cal = data["F0CAL"]
    nfcal = data["NFCAL"]
    fqcal = data["FQCAL"]
    chcal = data["CHCAL"]
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
        nchan = nch[i]
        meas_freq_ref = 1  # LSRK

        array_list = []
        for _dd_id in spw_dd_map[spw_id]:
            for _array in dd_array_map[_dd_id]:
                array_list.append(_array)

        spw_name = "_".join(array_list)
        _fqcal = fqcal[i][:nfcal[i]]
        _chcal = chcal[i][:nfcal[i]] - 1  # 1-based index -> 0-based index
        _sort_index = np.argsort(_chcal)
        chan_freq = np.interp(np.arange(nchan), _chcal[_sort_index], _fqcal[_sort_index])
        chan_width = np.ones(nchan, dtype=float) * (chan_freq[1] - chan_freq[0])
        LOG.info("channel width: %s", chan_width[0])
        net_sideband = 1 if chan_freq[0] < chan_freq[-1] else -1
        ref_freq = f0cal[i]  # F0CAL
        spectral_window_row = {
            "NUM_CHAN": nchan,
            "NAME": spw_name,
            "REF_FREQUENCY": ref_freq,
            "CHAN_FREQ": chan_freq,
            "CHAN_WIDTH": chan_width,
            "MEAS_FREQ_REF": meas_freq_ref,
            "EFFECTIVE_BW": chan_width,
            "RESOLUTION": chan_width,
            "TOTAL_BANDWIDTH": sum(np.abs(chan_width)),
            "NET_SIDEBAND": net_sideband,
            "IF_CONV_CHAIN": 0,
            "FLAG_ROW": False,
        }

        yield spectral_window_row


def fill_spectral_window(msfile: str, hdu: "BinTableHDU"):
    fill_ms_table(msfile, hdu, "SPECTRAL_WINDOW", _get_spectral_window_row)
