import collections
import logging
from typing import TYPE_CHECKING, Generator

import numpy as np
import numpy.typing as npt

from .._casa import open_table
from .utils import fix_nrow_to, get_array_configuration, get_data_description_map

if TYPE_CHECKING:
    from astropy.io.fits.hdu.BinTableHDU import BinTableHDU

LOG = logging.getLogger(__name__)


def _get_spectral_window_row(hdu: 'BinTableHDU', array_conf: list) -> Generator[dict, None, None]:
    ddd, adm, spw_map, _ = get_data_description_map(array_conf)

    data = hdu.data
    arry = data['ARRYT']
    nfcal = data['NFCAL']
    fqcal = data['FQCAL']
    chcal = data['CHCAL']
    nch = data['NCH']

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

        spw_name = '_'.join(array_list)
        _fqcal = fqcal[i][:nfcal[i]]
        _chcal = chcal[i][:nfcal[i]]
        chan_edge_freq = np.interp(np.arange(-0.5, nchan), _chcal, _fqcal)
        chan_freq = (chan_edge_freq[1:] + chan_edge_freq[:-1]) / 2
        chan_width = np.diff(chan_edge_freq)
        net_sideband = 1 if chan_freq[0] < chan_freq[-1] else -1
        ref_freq = chan_freq[0]  # frequency of the first channel
        spectral_window_row = {
            'NUM_CHAN': nchan,
            'NAME': spw_name,
            'REF_FREQUENCY': ref_freq,
            'CHAN_FREQ': chan_freq,
            'CHAN_WIDTH': chan_width,
            'MEAS_FREQ_REF': meas_freq_ref,
            'EFFECTIVE_BW': chan_width,
            'RESOLUTION': chan_width,
            'TOTAL_BANDWIDTH': sum(chan_width),
            'NET_SIDEBAND': net_sideband,
            'IF_CONV_CHAIN': 0,
            'FLAG_ROW': False,
        }

        yield spectral_window_row


def _fill_spectral_window_row(msfile: str, spw_id: int, row: dict):
    with open_table(msfile + '/SPECTRAL_WINDOW', read_only=False) as tb:
        if tb.nrows() <= spw_id:
            tb.addrows()
        for key, value in row.items():
            tb.putcell(key, spw_id, value)
