import collections
import logging
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    import astropy.io.fits.hdu.BinTableHDU as BinTableHDU

    from .._casa import _table

LOG = logging.getLogger(__name__)


def fix_nrow_to(nrow: int, tb: '_table') -> '_table':
    nrow_current = tb.nrows()
    if nrow_current < nrow:
        tb.addrows(nrow - nrow_current)
    elif nrow_current > nrow:
        tb.removerows(np.arange(nrow, nrow_current))

    return tb


def get_array_configuration(hdu: 'BinTableHDU'):
    # return value
    # {(spw_id, pol_id): [(array, pol, beam), ...], ...}
    num_array = hdu.header['ARYNM']
    arryt = hdu.data['ARRYT']
    unique_array, array_index = np.unique(arryt, return_inverse=True)
    assert len(unique_array) == num_array
    unique_array_id = np.array(sorted([int(x.lstrip('A')) for x in unique_array]))

    multn = hdu.data['MULTN']
    poltp = hdu.data['POLTP']
    rx = hdu.data['RX']
    fqcal = hdu.data['FQCAL']
    cwcal = hdu.data['CWCAL']
    chcal = hdu.data['CHCAL']
    nfcal = hdu.data['NFCAL']
    nch = hdu.data['NCH']

    spw_config = {}
    spw_id = 0

    array_freq_spec = {}
    for a, i in zip(unique_array_id, array_index):
        mask = array_index == i
        ncal = nfcal[i]
        nchan = nch[i]
        chan = chcal[i, :ncal]
        freq = fqcal[i, :ncal]
        freq_start, freq_end = np.interp([0, nchan - 1], chan, freq)
        freq_spec = (freq_start, freq_end, nchan)
        array_freq_spec[a] = freq_spec
    LOG.debug('array_freq_spec: %s', array_freq_spec)

    if np.all(poltp == ''):
        pol_spec = rx
    else:
        pol_spec = poltp
    array_pol_spec = dict((a, p) for a, p in zip(unique_array_id, pol_spec[array_index]))
    LOG.debug('array_pol_spec: %s', array_pol_spec)

    array_beam_spec = dict((a, b) for a, b in zip(unique_array_id, multn[array_index]))
    LOG.debug('array_beam_spec: %s', array_beam_spec)

    # freq_beam_spec = [[freq_spec, beam_spec, [array, ...]], ...]
    # where freq_spec is (freq_start, freq_end, nchan)
    # array list in each item can be more than one either when
    #
    #  - different polarization components exist, or,
    #  - duplicate array configuration exists for redundancy
    freq_beam_spec = []
    for a, f in array_freq_spec.items():
        b = array_beam_spec[a]
        for fb in freq_beam_spec:
            _f = fb[0]
            _b = fb[1]
            if f == _f and b == _b:
                fb[2].append(a)
                break
        else:
            freq_beam_spec.append([f, b, [a]])
    LOG.debug('freq_beam_spec: %s', freq_beam_spec)

    freq_beam_pol_spec = []
    for f, b, alist in freq_beam_spec:
        # _pol_spec = [[(pol0, array), (pol2, array), ...], ...]
        _pol_spec = []
        for a in alist:
            _p = array_pol_spec[a]
            for _ps in _pol_spec:
                _plist = np.array([x[0] for x in _ps])
                if np.all(_plist != _p):
                    _ps.append((_p, a))
                    break
            else:
                _pol_spec.append([(_p, a)])
        for _ps in _pol_spec:
            freq_beam_pol_spec.append([f, b, _ps])

    LOG.info('freq_beam_pol_spec: %s', freq_beam_pol_spec)

    array_config = {}
    for fspec, beam_id, palist in freq_beam_pol_spec:
        assert len(palist) in (1, 2)
        min_array_id = min([x[1] for x in palist])
        array_list = [f'A{x[1]}' for x in palist]
        pol_list = [x[0] for x in palist]
        beam_id = int(beam_id)
        array_config[min_array_id] = (fspec, beam_id, pol_list, array_list)

    return array_config


def get_data_description_map(array_conf: dict):
    dd_dict = {}
    array_dd_map = {}
    pol_map = {}
    spw_map = {}

    beam_list = np.unique([v[1] for v in array_conf.values()])
    array_conf_per_beam = [
        dict((k, v) for k, v in array_conf.items()
        for beam_number in beam_list
        if v[1] == beam_number)
    ]
    # only check frequency/polarization setup for the first beam
    dd_id = 0
    pol_id = 0
    spw_id = 0
    for dd_id, conf in enumerate(array_conf_per_beam[0].values()):
        freq_spec, beam, pol_list, array_list = conf
        for array in array_list:
            array_dd_map[array] = dd_id

        for _array_conf in array_conf_per_beam[1:]:
            if len(_array_conf) >= dd_id:
                continue
            for array in _array_conf[-1]:
                array_dd_map[array] = dd_id

        pol_tuple = tuple(pol_list)
        for k, v in pol_map.items():
            if v == pol_tuple:
                pol_id = k
                break
        else:
            pol_id = len(pol_map)
            pol_map[pol_id] = pol_tuple

        spw_map[spw_id] = freq_spec
        dd_dict[dd_id] = (spw_id, pol_id)
        spw_id += 1

    return dd_dict, array_dd_map, spw_map, pol_map


