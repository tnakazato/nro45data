from __future__ import annotations

import logging
import pprint
from typing import Any, Callable, Optional, TYPE_CHECKING

import numpy as np

from .._casa import open_table

if TYPE_CHECKING:
    import astropy.io.fits.hdu.BinTableHDU as BinTableHDU

    from .._casa import _table

LOG = logging.getLogger(__name__)


def fix_nrow_to(nrow: int, tb: "_table") -> "_table":
    nrow_current = tb.nrows()
    if nrow_current < nrow:
        tb.addrows(nrow - nrow_current)
    elif nrow_current > nrow:
        tb.removerows(np.arange(nrow, nrow_current))

    return tb


def get_array_configuration(hdu: "BinTableHDU"):
    # return value
    # {(spw_id, pol_id): [(array, pol, beam), ...], ...}
    num_array = hdu.header["ARYNM"]
    arryt = hdu.data["ARRYT"]
    unique_array, array_index = np.unique(arryt, return_index=True)
    assert len(unique_array) == num_array
    unique_array_id = np.array([int(x.lstrip("A")) for x in unique_array])
    LOG.debug("unique_array: %s", unique_array)
    LOG.debug("unique_array_id: %s", unique_array_id)
    LOG.debug("array_index: %s", array_index)
    sort_index = np.argsort(unique_array_id)

    multn = hdu.data["MULTN"][array_index]
    poltp = hdu.data["POLTP"][array_index]
    rx = hdu.data["RX"][array_index]
    fqcal = hdu.data["FQCAL"]
    # cwcal = hdu.data['CWCAL']
    chcal = hdu.data["CHCAL"]
    nfcal = hdu.data["NFCAL"]
    nch = hdu.data["NCH"]

    array_freq_spec = {}
    for isort in sort_index:
        a = unique_array_id[isort]
        i = array_index[isort]
        ncal = nfcal[i]
        nchan = nch[i]
        chan = chcal[i, :ncal]
        freq = fqcal[i, :ncal]
        freq_start, freq_end = np.interp([0, nchan - 1], chan, freq)
        freq_spec = (freq_start, freq_end, nchan)
        array_freq_spec[a] = freq_spec
    LOG.debug("array_freq_spec: %s", pprint.pformat(array_freq_spec))

    if np.all(poltp == ""):
        pol_spec = rx
    else:
        pol_spec = poltp
    array_pol_spec = dict((unique_array_id[isort], pol_spec[isort]) for isort in sort_index)
    LOG.debug("array_pol_spec: %s", pprint.pformat(array_pol_spec))

    array_beam_spec = dict((unique_array_id[isort], multn[isort]) for isort in sort_index)
    LOG.debug("array_beam_spec: %s", pprint.pformat(array_beam_spec))

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
    LOG.debug("freq_beam_spec: %s", pprint.pformat(freq_beam_spec))

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

    LOG.debug("freq_beam_pol_spec: %s", pprint.pformat(freq_beam_pol_spec))

    array_config = {}
    for fspec, beam_id, palist in freq_beam_pol_spec:
        assert len(palist) in (1, 2)
        min_array_id = min([x[1] for x in palist])
        array_list = [f"A{x[1]}" for x in palist]
        pol_list = [x[0] for x in palist]
        beam_id = int(beam_id)
        array_config[min_array_id] = (fspec, beam_id, pol_list, array_list)

    return array_config


def get_data_description_map(array_conf: dict):
    dd_dict = {}
    dd_list = []
    array_dd_map = {}
    array_spw_map = {}
    array_pol_map = {}
    # pol_map = {}
    pol_map = []
    spw_map = {}
    array_beam_map = {}

    beam_list = np.unique([v[1] for v in array_conf.values()])
    LOG.debug("beam_list: %s", beam_list)
    array_conf_per_beam = [
        dict((k, v) for k, v in array_conf.items() if v[1] == beam_number) for beam_number in beam_list
    ]
    LOG.debug("array_conf_per_beam: %s", pprint.pformat(array_conf_per_beam))
    # only check frequency/polarization setup for the first beam
    dd_id = 0
    pol_id = 0
    spw_id = 0
    # number of entries in array_conf_per_beam should be equal to
    # a number of data descriptions even if freq and pol configuration
    # are effectively the same
    for spw_id, conf in enumerate(array_conf_per_beam[0].values()):
        freq_spec, beam, pol_list, array_list = conf
        pol_tuple = tuple(pol_list)
        if pol_tuple in pol_map:
            pol_id = pol_map.index(pol_tuple)
        else:
            pol_id = len(pol_map)
            pol_map.append(pol_tuple)

        for array in array_list:
            # array_dd_map[array] = dd_id
            array_spw_map[array] = spw_id
            array_pol_map[array] = pol_id
            array_beam_map[array] = np.where(beam_list == beam)[0][0]

        spw_map[spw_id] = freq_spec
        # dd_dict[dd_id] = (dd_id, pol_id)
        dd_list.append((spw_id, pol_id))
        dd_id = spw_id
        for array in array_list:
            array_dd_map[array] =dd_id

    LOG.debug("dd_list: %s", dd_list)
    LOG.debug("spw_map: %s", spw_map)
    LOG.debug("pol_map: %s", pol_map)

    for _array_conf in array_conf_per_beam[1:]:
        spw_flag = dict((i, False) for i in spw_map.keys())
        LOG.debug("spw_flag (initial) = %s", spw_flag)

        for conf in _array_conf.values():
            freq_spec, beam, pol_list, array_list = conf
            pol_tuple = tuple(pol_list)
            if pol_tuple in pol_map:
                pol_id = pol_map.index(pol_tuple)
            else:
                pol_id = len(pol_map)
                pol_map.append(pol_tuple)

            for _spw_id, spec in spw_map.items():
                flag = spw_flag[_spw_id]
                LOG.debug("spw_flag (loop) = %s", spw_flag)
                if flag:
                    continue
                if freq_spec == spec:
                    LOG.debug("matched!")
                    spw_id = _spw_id
                    spw_flag[_spw_id] = True
                    break
                LOG.debug("spw_id = %d", spw_id)
            else:
                spw_id = len(spw_map)
                spw_map[spw_id] = freq_spec

            if (spw_id, pol_id) in dd_list:
                dd_id = dd_list.index((spw_id, pol_id))
            else:
                dd_id = len(dd_list)
                dd_list.append((spw_id, pol_id))

            for array in array_list:
                array_dd_map[array] = dd_id

            # if len(_array_conf) == dd_id - 1:
            #     continue
            # freq_spec, beam, pol_list, array_list = conf
            # for array in array_list:
            #     array_dd_map[array] = dd_id
            #     array_spw_map[array] = spw_id

            # pol_tuple = tuple(pol_list)
            # if pol_tuple in pol_map:
            #     pol_id = pol_map.index(pol_tuple)
            # else:
            #     pol_id = len(pol_map)
            #     pol_map.append(pol_tuple)

        # spw_map[spw_id] = freq_spec
        # dd_dict[dd_id] = (spw_id, pol_id)
        # spw_id += 1

    dd_dict = dict(enumerate(dd_list))


    return dd_dict, array_dd_map, spw_map, pol_map  # , array_beam_map


def get_intent_map(scan_column: list[int], intent_column: list[str]) -> dict[str, int]:
    scan_intents, _indices = np.unique(intent_column, return_index=True)
    LOG.info("scan_intents %s, _indices %s", scan_intents, _indices)
    intent_sort_index = np.argsort(_indices)
    LOG.info("sort index %s", intent_sort_index)
    return dict((scan_intents[j], i) for i, j in enumerate(intent_sort_index))


def get_processor_map(arry1: str, arry2: str, arry3: str, arry4: str):
    # SUB_TYPE
    processor_sub_type_list = []
    processor_prefix_list = ""
    # AOS-High
    if arry1.find("1") >= 0:
        processor_sub_type_list.append("AOS-High")
        processor_prefix_list += "H"

    # AOS-Wide 1-10 (0-9)
    # AOS-Ultrawide 1-5 (10-15)
    # FX 1-5? (16-20)
    if arry2[:10].find("1") >= 0:
        processor_sub_type_list.append("AOS-Wide")
        processor_prefix_list += "W"

    if arry2[10:15].find("1") >= 0:
        processor_sub_type_list.append("AOS-Ultrawide")
        processor_prefix_list += "U"

    if arry2[15:20].find("1") >= 0:
        processor_sub_type_list.append("FX")
        processor_prefix_list += "X"

    # AC45
    if (arry3 + arry4).find("1") >= 0:
        processor_sub_type_list.append("AC45")
        processor_prefix_list += "A"

    LOG.debug("processor_sub_type_list: %s", processor_sub_type_list)
    LOG.debug("arr1: %s", arry1)
    LOG.debug("arry2: %s", arry2)
    LOG.debug("arry3: %s", arry3)
    LOG.debug("arry4: %s", arry4)

    return processor_sub_type_list, processor_prefix_list


def fill_ms_table(
        msfile: str,
        hdu: BinTableHDU,
        table_name: str,
        row_generator: Callable,
        column_keywords: Optional[dict[str, dict[str, Any]]] = None
):
    if table_name.upper() == "MAIN":
        table_path = msfile
    else:
        table_path = f"{msfile}/{table_name.upper()}"

    with open_table(table_path, read_only=False) as tb:
        # update table column keywords
        if column_keywords is None:
            column_keywords = {}

        for colname, colkeywords_new in column_keywords.items():
            colkeywords = tb.getcolkeywords(colname)
            for key, value_new in colkeywords_new.items():
                if key in colkeywords and isinstance(value_new, dict):
                    colkeywords[key].update(value_new)
                else:
                    colkeywords[key] = value_new
            tb.putcolkeywords(colname, colkeywords)

        # fill table rows
        for row_id, row in enumerate(row_generator(hdu)):
            if tb.nrows() <= row_id:
                tb.addrows(tb.nrows() - row_id + 1)

            for key, value in row.items():
                LOG.debug("row %d key %s", row_id, key)
                tb.putcell(key, row_id, value)
            LOG.debug("%s table %d row %s", table_name, row_id, row)
